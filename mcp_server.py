from mcp.server.mcpserver import MCPServer
import sys
import os

# Добавляем корень проекта в sys.path для импорта модулей app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

mcp = MCPServer("GGS-DB-Context-Server")

@mcp.tool()
def get_house(house_id: int) -> dict:
    """Получить данные Домовладения (Объект КС) по его ID из базы ggs_stud."""
    try:
        from app.db.query_house import query_house_by_id
        result = query_house_by_id(house_id)
        return result if result else {"error": "House not found"}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

@mcp.tool()
def get_person(person_id: int) -> dict:
    """Получить данные Физического лица по его ID из базы ggs_stud."""
    try:
        from app.db.query_person import query_person_by_id
        result = query_person_by_id(person_id)
        return result if result else {"error": "Person not found"}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

@mcp.tool()
def get_organization(org_id: int) -> dict:
    """Получить данные Юридического лица (Организации) по его ID из базы ggs_stud."""
    try:
        from app.db.query_organization import query_organization_by_id
        result = query_organization_by_id(org_id)
        return result if result else {"error": "Organization not found"}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

@mcp.tool()
def get_contract(contract_id: int) -> dict:
    """Получить данные Договора по его ID из базы ggs_stud."""
    try:
        from app.db.query_contract import query_contract_by_id
        result = query_contract_by_id(contract_id)
        return result if result else {"error": "Contract not found"}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

@mcp.tool()
def get_db_schema_context() -> str:
    """Получить текстовое описание предметной области (DOMAIN.md)."""
    domain_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DOMAIN.md")
    try:
        with open(domain_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading DOMAIN.md: {e}"

if __name__ == "__main__":
    # Запуск сервера по стандарту stdio (для интеграции с Claude Desktop, IDE и агентами)
    mcp.run()
