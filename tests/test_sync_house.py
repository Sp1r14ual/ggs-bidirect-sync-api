"""
E2E tests for POST /forward_sync/house/{id}.

Requires:
  - The FastAPI server running at TEST_API_BASE_URL
  - tests/.env.test with TEST_HOUSE_ID configured
  - .env with Bitrix webhook and DB connection configured

Run with:
  pytest tests/test_sync_house.py -v
"""
import app.db.query_house as query_house
import app.db.query_house_owner as query_house_owner
import app.db.query_contract as query_contract
from app.utils.object_ks_gs import build_payloads_object_ks_gs
from app.settings import settings
from tests.helpers import assert_payload_matches_bitrix


def _build_expected_payloads(house_id: int) -> tuple[dict, dict]:
    """
    Replicates the payload preparation logic from the route handler so the test
    has an independent expected value to compare against Bitrix.
    """
    house = query_house.query_house_by_id(house_id)
    house_owner = query_house_owner.query_house_owner_by_house(house_id)

    if house_owner:
        house["company_id"] = house_owner.get("company_crm_id")
        house["contact_id"] = house_owner.get("contact_crm_id")

    contract = None
    if house.get("contract_id"):
        contract = query_contract.query_contract_by_id(house["contract_id"])

    oks_payload, gs_payload = build_payloads_object_ks_gs(house)

    if contract and contract.get("contract_crm_id"):
        oks_payload[f"parentId{settings.CONTRACT_TYPE_ID}"] = contract["contract_crm_id"]

    if contract and contract.get("ground_crm_id"):
        oks_payload[f"parentId{settings.GROUND_TYPE_ID}"] = contract["ground_crm_id"]

    gs_payload[f"parentId{settings.OBJECT_KS_TYPE_ID}"] = house["object_ks_crm_id"]

    return oks_payload, gs_payload


class TestSyncHouse:

    def test_sync_returns_200_with_crm_ids(self, house_sync_result):
        assert "object_ks_crm_id" in house_sync_result
        assert "gasification_stage_crm_id" in house_sync_result
        assert house_sync_result["object_ks_crm_id"] is not None
        assert house_sync_result["gasification_stage_crm_id"] is not None

    def test_crm_ids_stored_in_db(self, house_sync_result, test_settings):
        house_id = test_settings.TEST_HOUSE_ID
        house = query_house.query_house_by_id(house_id)

        assert house["object_ks_crm_id"] == house_sync_result["object_ks_crm_id"], (
            "object_ks_crm_id in DB does not match the value returned by the endpoint"
        )
        assert house["gasification_stage_crm_id"] == house_sync_result["gasification_stage_crm_id"], (
            "gasification_stage_crm_id in DB does not match the value returned by the endpoint"
        )

    def test_object_ks_fields_in_bitrix(self, house_sync_result, test_settings, bitrix):
        oks_crm_id = house_sync_result["object_ks_crm_id"]
        oks_payload, _ = _build_expected_payloads(test_settings.TEST_HOUSE_ID)

        bitrix_item = bitrix.call(
            "crm.item.get",
            {"id": oks_crm_id, "entityTypeId": settings.OBJECT_KS_TYPE_ID},
        )["item"]

        assert_payload_matches_bitrix(oks_payload, bitrix_item, "Object KS")

    def test_gasification_stage_fields_in_bitrix(self, house_sync_result, test_settings, bitrix):
        gs_crm_id = house_sync_result["gasification_stage_crm_id"]
        _, gs_payload = _build_expected_payloads(test_settings.TEST_HOUSE_ID)

        bitrix_item = bitrix.call(
            "crm.item.get",
            {"id": gs_crm_id, "entityTypeId": settings.GASIFICATION_STAGE_TYPE_ID},
        )["item"]

        assert_payload_matches_bitrix(gs_payload, bitrix_item, "Gasification Stage")

    def test_second_sync_is_update_not_create(self, api_client, house_sync_result, test_settings):
        """
        Critical: a second sync of the same entity must not create a new Bitrix record.
        The crm_ids returned must be identical to the first sync.
        """
        house_id = test_settings.TEST_HOUSE_ID
        first_oks_id = house_sync_result["object_ks_crm_id"]
        first_gs_id = house_sync_result["gasification_stage_crm_id"]

        response = api_client.post(f"/forward_sync/house/{house_id}")
        assert response.status_code == 200, f"Second sync failed: {response.text}"
        data = response.json()

        assert data["object_ks_crm_id"] == first_oks_id, (
            f"Object KS crm_id changed from {first_oks_id} to {data['object_ks_crm_id']} -- "
            "second sync created a new record instead of updating"
        )
        assert data["gasification_stage_crm_id"] == first_gs_id, (
            f"Gasification Stage crm_id changed from {first_gs_id} to {data['gasification_stage_crm_id']} -- "
            "second sync created a new record instead of updating"
        )
