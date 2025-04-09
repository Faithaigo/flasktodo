from flask import Flask
from db import db
from flask_migrate import Migrate
from todo.todo_blueprint import todo_blueprint
from config import DevelopmentConfig

app = Flask(__name__)

app.register_blueprint(todo_blueprint)

# Load configurations from the config file
app.config.from_object(DevelopmentConfig())

# initialize the app with the extension
db.init_app(app)

# Initialize Flask-Migrate 
migrate = Migrate(app, db)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)