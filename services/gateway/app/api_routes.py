from flask import Blueprint, jsonify
from sqlalchemy import text

def create_api_routes(db):
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

    return api_bp
