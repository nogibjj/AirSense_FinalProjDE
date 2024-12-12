from flask import Blueprint, jsonify, request
from sqlalchemy import text

def create_api_routes(db):
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    @api_bp.route("/dynamic_query", methods=["GET"])
    def dynamic_query():
        """
        Execute a dynamic SQL query based on the query string parameters.
        e.g. /api/dynamic_query?table_name=airline_performance&limit=5
        """
        try:
            # Retrieve parameters from the query string
            table_name = request.args.get("table_name")
            order_by = request.args.get("order_by")
            limit = request.args.get("limit", type=int)

            if not table_name:
                return jsonify({"message": "Parameter 'table_name' is required!"}), 400

            # Build the dynamic SQL query
            query = f"SELECT * FROM {table_name}"

            if order_by:
                query += f" ORDER BY {order_by}"

            if limit:
                query += f" LIMIT {limit}"

            # Use SQLAlchemy's text function to execute the query
            result = db.session.execute(text(query))
            rows = result.fetchall()
            column_names = result.keys()

            # Format the results as a list of dictionaries
            data = [dict(zip(column_names, row)) for row in rows]
            return jsonify(data)
        except Exception as e:
            return jsonify({"message": "Failed to execute query!", "error": str(e)}), 500

    return api_bp
