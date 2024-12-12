from flask import Blueprint, render_template, jsonify
from sqlalchemy import text

def create_html_routes(db):
    html_bp = Blueprint('html', __name__)

    @html_bp.route("/tables", methods=["GET"])
    def list_tables():
        try:
            tables = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
            return render_template("tables.html", tables=tables)
        except Exception as e:
            return jsonify({"message": "Failed to retrieve data!", "error": str(e)}), 500

    return html_bp
