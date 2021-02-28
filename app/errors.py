from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404
    # This deals with 404 (page not found) errors, making it so that they look the same as the rest of the site

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500
    # this deals with 500 (database) errors, making it so that they look the same as the rest of the site
