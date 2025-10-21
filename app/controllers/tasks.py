from flask import Blueprint, request, jsonify, current_app
from ..schemas import TaskSchema
from ..models import Task as TaskModel, User as UserModel, get_sessionmaker

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.before_app_request
def _ensure_sessionmaker():
    container = current_app.container
    if getattr(container, 'sessionmaker', None) is None:
        container.sessionmaker = get_sessionmaker(container.config.DATABASE_URL)

@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    schema = TaskSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    container = current_app.container
    Session = container.sessionmaker
    session = Session()
    try:
        user = session.get(UserModel, data.get('user_id'))
        if not user:
            return jsonify({'error': 'User not found'}), 404

        task = TaskModel(
            task_name=data['task_name'],
            user_id=data['user_id'],
            due_date=data.get('due_date'),
            status=data.get('status') or None,
            priority=data.get('priority') or None
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return jsonify(schema.dump(task)), 201
    finally:
        session.close()

@tasks_bp.route('/', methods=['GET'])
def list_tasks():
    schema = TaskSchema(many=True)
    container = current_app.container
    Session = container.sessionmaker
    session = Session()
    try:
        tasks = session.query(TaskModel).all()
        return jsonify(schema.dump(tasks)), 200
    finally:
        session.close()

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    schema = TaskSchema()
    container = current_app.container
    Session = container.sessionmaker
    session = Session()
    try:
        task = session.get(TaskModel, task_id)
        if not task:
            return jsonify({'error': 'not found'}), 404
        return jsonify(schema.dump(task)), 200
    finally:
        session.close()

@tasks_bp.route('/<int:task_id>', methods=['PUT', 'PATCH'])
def update_task(task_id):
    data = request.get_json() or {}
    schema = TaskSchema(partial=True)
    errors = schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    container = current_app.container
    Session = container.sessionmaker
    session = Session()
    try:
        task = session.get(TaskModel, task_id)
        if not task:
            return jsonify({'error': 'not found'}), 404

        if 'task_name' in data:
            task.task_name = data['task_name']
        if 'status' in data:
            task.status = data['status']
        if 'due_date' in data:
            task.due_date = data['due_date']
        if 'priority' in data:
            task.priority = data['priority']

        session.add(task)
        session.commit()
        session.refresh(task)
        return jsonify(schema.dump(task)), 200
    finally:
        session.close()

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    container = current_app.container
    Session = container.sessionmaker
    session = Session()
    try:
        task = session.get(TaskModel, task_id)
        if not task:
            return jsonify({'error': 'not found'}), 404
        session.delete(task)
        session.commit()
        return '', 204
    finally:
        session.close()
