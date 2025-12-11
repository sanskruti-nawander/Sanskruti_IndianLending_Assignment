import os
import sqlite3
from flask import Flask, request, jsonify
from Day2.enhancement.feature import compute_ews
from sql_validator import is_safe_sql

app = Flask(__name__)

DB_PATH = os.environ.get("DB_PATH", "indian_lending.db")
USE_AZURE = os.environ.get("USE_AZURE", "false").lower() == "true"

# -------- SQLite Query Helper ----------
def query_db(sql):
    if not is_safe_sql(sql):
        raise ValueError("Unsafe SQL blocked.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

# -------- Mock NL → SQL (no Azure needed) ----------
def mock_nl_to_sql(nl):
    nl = nl.lower()

    if "npa" in nl or "90+" in nl:
        return "SELECT loan_id, borrower_id, outstanding, dpd FROM loans WHERE dpd > 90 ORDER BY outstanding DESC LIMIT 50;"

    if "sma" in nl:
        return """SELECT loan_id, borrower_id, dpd,
                  CASE 
                    WHEN dpd BETWEEN 1 AND 30 THEN 'SMA-0'
                    WHEN dpd BETWEEN 31 AND 60 THEN 'SMA-1'
                    WHEN dpd BETWEEN 61 AND 90 THEN 'SMA-2'
                    ELSE 'NPA'
                  END AS category
                  FROM loans;"""

    if "top agents" in nl:
        return """SELECT agent_id, SUM(amount) AS collected 
                  FROM payments 
                  GROUP BY agent_id 
                  ORDER BY collected DESC 
                  LIMIT 5;"""

    return "SELECT loan_id, borrower_id, loan_type, outstanding, dpd FROM loans LIMIT 50;"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/nlq", methods=["POST"])
def nlq():
    data = request.json
    q = data.get("q")
    sql = mock_nl_to_sql(q)
    try:
        rows = query_db(sql)
        return jsonify({"sql": sql, "rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/sql", methods=["POST"])
def sql_endpoint():
    sql = request.json.get("sql")
    try:
        rows = query_db(sql)
        return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/ews")
def ews():
    try:
        dpd = int(request.args.get("dpd", 0))
        cibil = int(request.args.get("cibil", 700))
        outstanding = float(request.args.get("outstanding", 0))
        bounces = int(request.args.get("bounces", 0))
        score = compute_ews(dpd, cibil, outstanding, bounces)
        return jsonify({"ews": score})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
