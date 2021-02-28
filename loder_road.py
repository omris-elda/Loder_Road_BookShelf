from app import app, db
from app.models import User, Book

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Book": Book}
    # this adds the various imports to the flask shell so that you don't have to import them
    # every time, making it easier to quickly test things in the terminal
    