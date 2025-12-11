import re

WHITELIST_TABLES = {"loans", "borrowers", "payments", "branches", "legal_actions"}

def is_safe_sql(sql: str) -> bool:
    sql = sql.lower().strip()

    if ";" in sql:
        return False

    if not (sql.startswith("select") or sql.startswith("with")):
        return False

    tables = re.findall(r"from\s+([a-z_]+)|join\s+([a-z_]+)", sql)
    used = set(x for tup in tables for x in tup if x)

    return used.issubset(WHITELIST_TABLES)
