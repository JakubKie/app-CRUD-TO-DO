from flask import Blueprint, request, jsonify, current_app
from ..schemas import UserSchema
from ..models import User as UserModel, get_sessionmaker

users_bp = Blueprint('users', __name__)

@users_bp.before_app_request
def _ensure_sessionmaker():
    container = current_app.container
    if getattr(container, 'sessionmaker', None) is None:
        container.sessionmaker = get_sessionmaker(container.config.DATABASE_URL)

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    schema = UserSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({'errors': errors}), 400

    container = current_app.container
    Session = container.sessionmaker

    session = Session()
    try:
        user = UserModel(username=data['username'], role=data.get('role'))
        session.add(user)
        session.commit()
        session.refresh(user)
        return jsonify(schema.dump(user)), 201
    finally:
        session.close()

@users_bp.route('/', methods=['GET'])
def list_users():
    schema = UserSchema(many=True)
    container = current_app.container
    Session = container.sessionmaker
    session = Session()
    try:
        users = session.query(UserModel).all()
        return jsonify(schema.dump(users)), 200
    finally:
        session.close()

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    schema = UserSchema()
    container = current_app.container
    Session = container.sessionmaker
    session = Session()
    try:
        user = session.get(UserModel, user_id)
        if not user:
            return jsonify({'error': 'not found'}), 404
        return jsonify(schema.dump(user)), 200
    finally:
        session.close()
