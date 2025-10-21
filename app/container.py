from . import config as cfg
from .repos import TaskRepository, UserRepository
from .services import TaskService, UserService

class Container:
  def __init__(self):
    self.config = cfg.config

def create_container():
  container = Container()
  return container