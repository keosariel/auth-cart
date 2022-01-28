from app import app, create_db

with app.app_context():
    create_db()
