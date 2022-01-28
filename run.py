from app import app, create_db
import os

base_dir    = os.path.dirname(os.path.abspath(__file__))
db_dir      = os.path.join(base_dir, "db")

if not os.path.exists(db_dir):
    os.mkdir(db_dir)

if __name__ == '__main__':
    create_db()
    
    app.run(debug=True)
