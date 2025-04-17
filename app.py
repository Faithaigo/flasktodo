from flask import Flask
from db import db
from flask_migrate import Migrate
from todo.todo_blueprint import todo_blueprint
from auth.auth_blueprint import auth_blueprint
from config import DevelopmentConfig
from extensions import bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.register_blueprint(todo_blueprint)
app.register_blueprint(auth_blueprint)

# Load configurations from the config file
app.config.from_object(DevelopmentConfig())

#Initialize app with JWT
jwt = JWTManager(app)

# initialize the app with the extension
db.init_app(app)

# Initialize the app with bcrypt
bcrypt.init_app(app)

# Initialize Flask-Migrate 
migrate = Migrate(app, db)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)