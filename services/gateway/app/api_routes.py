import os
from flask import Blueprint, jsonify, request
from sqlalchemy import text, inspect
from openai import OpenAI

def create_api_routes(db):
    api_bp = Blueprint('api', __name__, url_prefix='/api')

    @api_bp.route("/chat", methods=["POST"])
    def chat():
        """
        Handle chat requests and return responses from OpenAI.
        """
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return jsonify({"message": "OpenAI API key is missing!"}), 500
        print(openai_api_key)
        client = OpenAI(openai_api_key)
        user_message = request.json.get("message", "")

        if not user_message:
            return jsonify({"message": "Parameter 'message' is required!"}), 400

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message}]
            )
            chat_response = response.choices[0].message.content
            return jsonify({"reply": chat_response})
        except Exception as e:
            return jsonify({"message": "Failed to fetch response!", "error": str(e)}), 500

    @api_bp.route("/advanced_search", methods=["POST"])
    def advanced_search():
        """
        Perform an advanced search across all tables for records matching the given search string.
        Returns categorized results by table with rows and column names.
        """
        try:
            search_query = request.json.get("query")

            if not search_query:
                return jsonify({"message": "Parameter 'query' is required!"}), 400

            inspector = inspect(db.engine)
            tables = inspector.get_table_names()

            result_data = {}
            
            for table in tables:
                columns = inspector.get_columns(table)
                column_names = [col['name'] for col in columns]

                where_clauses = []
                for column in column_names:
                    where_clauses.append(f"\"{column}\"::text ILIKE :search_query")
                
                query = f"SELECT * FROM \"{table}\" WHERE {' OR '.join(where_clauses)}"

                result = db.session.execute(text(query), {"search_query": f"%{search_query}%"})
                rows = result.fetchall()

                if rows:
                    result_data[table] = {
                        "columns": column_names,
                        "rows": [dict(zip(result.keys(), row)) for row in rows]
                    }

            if not result_data:
                return jsonify({"message": "No matching records found."}), 404

            return jsonify(result_data)

        except Exception as e:
            return jsonify({"message": "Failed to execute advanced search!", "error": str(e)}), 500

    @api_bp.route("/dynamic_query", methods=["GET"])
    def dynamic_query():
        """
        Execute a dynamic SQL query based on the query string parameters.
        """
        try:
            table_name = request.args.get("table_name")
            columns = request.args.get("columns", "*")
            where_clause = request.args.get("where")
            order_by = request.args.get("order_by")
            order_direction = request.args.get("order_direction", "ASC").upper()
            limit = request.args.get("limit", type=int)

            if not table_name:
                return jsonify({"message": "Parameter 'table_name' is required!"}), 400

            if order_direction not in ["ASC", "DESC"]:
                return jsonify({"message": "Invalid value for 'order_direction'. Must be 'ASC' or 'DESC'."}), 400

            query = f"SELECT {columns} FROM {table_name}"

            if where_clause:
                conditions = where_clause.split(",")
                formatted_conditions = []
                for condition in conditions:
                    if ":" in condition:
                        column, value = condition.split(":", 1)
                        formatted_conditions.append(f"\"{column}\" = '{value}'")
                if formatted_conditions:
                    query += f" WHERE {' AND '.join(formatted_conditions)}"

            if order_by:
                query += f" ORDER BY \"{order_by}\" {order_direction}"

            if limit:
                query += f" LIMIT {limit}"

            result = db.session.execute(text(query))
            rows = result.fetchall()
            column_names = result.keys()

            data = [dict(zip(column_names, row)) for row in rows]
            return jsonify(data)

        except Exception as e:
            return jsonify({"message": "Failed to execute query!", "error": str(e)}), 500

    return api_bp
