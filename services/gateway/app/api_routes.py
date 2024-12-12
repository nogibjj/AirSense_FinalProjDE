from flask import Blueprint, jsonify, request
from sqlalchemy import text

def create_api_routes(db):
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    @api_bp.route("/dynamic_query", methods=["GET"])
    def dynamic_query():
        """
        Execute a dynamic SQL query based on the query string parameters.
        e.g. /api/dynamic_query?table_name=airline_performance&columns=col1,col2&limit=5&where=column1:value1
        """
        try:
            # Retrieve parameters from the query string
            table_name = request.args.get("table_name")
            columns = request.args.get("columns", "*")
            where_clause = request.args.get("where")
            order_by = request.args.get("order_by")
            limit = request.args.get("limit", type=int)

            if not table_name:
                return jsonify({"message": "Parameter 'table_name' is required!"}), 400

            # Build the dynamic SQL query
            query = f"SELECT {columns} FROM {table_name}"

            if where_clause:
                # Process where_clause with proper quoting for column names
                conditions = where_clause.split(",")
                formatted_conditions = []
                for condition in conditions:
                    if ":" in condition:
                        column, value = condition.split(":", 1)
                        formatted_conditions.append(f"\"{column}\" = '{value}'")
                if formatted_conditions:
                    query += f" WHERE {' AND '.join(formatted_conditions)}"

            if order_by:
                query += f" ORDER BY \"{order_by}\""

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
