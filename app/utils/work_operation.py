import app.enums.db_bitrix_fields_mapping as field_mapper
import app.db.query_crm_fields as crm_fields_db
import app.settings as settings
from datetime import date
import logging

logger = logging.getLogger(__name__)


def build_payload_work(work_operation):
    work_payload = dict()
    logger.error('We are here! ')
    for key, value in work_operation.items():
        logger.error(f'*** {key}:{value} ***')
        if key not in field_mapper.WorkToWork.__members__:
            continue

        field_ru_label = field_mapper.WorkToWork[key].value
        field = crm_fields_db.query_crm_field_by_ru_label(field_ru_label, settings.settings.WORK_ENTITY_ID)
        logger.error(f'!!{key}:{value}:{field_ru_label} !!')
        work_payload[field["field_name_unified"]] = value

    # Добавляем отдельно заголовки
    work_payload["title"] = f"{work_operation['contract_number']} от {date.strftime(work_operation['date_appoint'],'%d.%m.%Y')}" if work_operation['date_appoint'] else f"{work_operation['contract_number']} н/д"
    
    return work_payload
