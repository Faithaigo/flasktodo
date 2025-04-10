from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from todo.models import Todo, db
from error_handler import InvalidAPIUsage
from datetime import datetime

todo_blueprint = Blueprint('todo', __name__, url_prefix='/todo')
api = Api(todo_blueprint)


@todo_blueprint.errorhandler(InvalidAPIUsage)
def handle_api_error(e):
    return jsonify(e.to_dict()), e.status_code


class TodosApi(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        todos = Todo.query.filter_by(user_id=user_id).all()
        return jsonify([todo.to_dict() for todo in todos])

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")

        if not title:
            raise InvalidAPIUsage("Title is required", 400)

        todo = Todo(
            title=title,
            description=description,
            due_date=datetime.fromisoformat(due_date) if due_date else None,
            user_id=user_id
        )
        db.session.add(todo)
        db.session.commit()
        return todo.to_dict(), 201


class TodoApi(Resource):
    @jwt_required()
    def get(self, todo_id):
        user_id = get_jwt_identity()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user_id:
            raise InvalidAPIUsage("Unauthorized access", 401)
        return todo.to_dict()

    @jwt_required()
    def put(self, todo_id):
        user_id = get_jwt_identity()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user_id:
            raise InvalidAPIUsage("Unauthorized access", 401)

        data = request.get_json()
        todo.title = data.get("title", todo.title)
        todo.description = data.get("description", todo.description)
        if data.get("due_date"):
            todo.due_date = datetime.fromisoformat(data["due_date"])

        # Validate and update status
        valid_states = ["pending", "in_progress", "completed"]
        if "status" in data:
            if data["status"] not in valid_states:
                raise InvalidAPIUsage(f"Invalid status. Valid statuses are: {', '.join(valid_states)}", 400)
            todo.status = data["status"]

        # Perform actions based on status
            status_actions = {
                "completed": lambda: datetime.now(),
                "pending": lambda: None,
                "in_progress": lambda: datetime.now(),
            }
            if todo.status in status_actions:
                todo.due_date = status_actions[todo.status]()

        db.session.commit()
        return todo.to_dict()

    @jwt_required()
    def delete(self, todo_id):
        user_id = get_jwt_identity()
        todo = Todo.query.get_or_404(todo_id)
        if todo.user_id != user_id:
            raise InvalidAPIUsage("Unauthorized access", 401)

        db.session.delete(todo)
        db.session.commit()
        return {"msg": "Deleted"}, 200


api.add_resource(TodosApi, '/')
api.add_resource(TodoApi, '/<int:todo_id>')
