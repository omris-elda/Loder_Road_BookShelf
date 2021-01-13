from app import db
from app.models import Books, Users

db.drop_all()
db.create_all()
