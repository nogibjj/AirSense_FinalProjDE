from flask import Blueprint, jsonify, render_template
from sqlalchemy import text

def register_routes(app, db):
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    @api_bp.route("/airline_performance", methods=["GET"])
    def get_airline_performance():
        try:
            query = text("SELECT * FROM airline_performance;")
            result = db.session.execute(query)
            rows = result.fetchall()
            column_names = result.keys()
            performance_data = [dict(zip(column_names, row)) for row in rows]
            return jsonify(performance_data)
        except Exception as e:
            return jsonify({"message": "Failed to retrieve data!", "error": str(e)}), 500

    app.register_blueprint(api_bp)

    html_bp = Blueprint('html', __name__)

    @html_bp.route("/tables", methods=["GET"])
    def list_tables():
        try:
            tables = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
            return render_template("tables.html", tables=tables)
        except Exception as e:
            return jsonify({"message": "Failed to retrieve data!", "error": str(e)}), 500

    app.register_blueprint(html_bp)
