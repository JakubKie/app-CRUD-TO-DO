from flask import Flask
from flask_cors import CORS
from .models import Base, get_engine

def create_app(container):
  app = Flask(__name__)
  CORS(app)

  app.config.from_object(container.config)
  
  from .controllers.tasks import tasks_bp
  from .controllers.users import users_bp
  
  app.register_blueprint(tasks_bp, url_prefix='/tasks')
  app.register_blueprint(users_bp, url_prefix='/users')

  engine = get_engine(container.config.DATABASE_URL)
  Base.metadata.create_all(engine)

  app.container = container

  return app