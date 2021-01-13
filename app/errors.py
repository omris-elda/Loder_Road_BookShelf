from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404
    # this will handle 404 errors so that it looks like the rest of the website

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500
    # this handles 500 database errors
    # such as duplicated info that's slipped through any other error checking