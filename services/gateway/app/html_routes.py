from flask import Blueprint, render_template

def create_html_routes(db):
    html_bp = Blueprint('html', __name__)

    @html_bp.route("/")
    def home():
        return render_template("home.html")
    
    @html_bp.route("/explorer", methods=["GET"])
    def show_explorer():
        return render_template("explorer.html")

    @html_bp.route("/tables", methods=["GET"])
    def show_tables():
        return render_template("tables.html")

    return html_bp
