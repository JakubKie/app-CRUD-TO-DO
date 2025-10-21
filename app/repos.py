from .models import Task, User
from typing import Optional, List

class TaskRepository:
    def __init__(self, session_factory):
        self._Session = session_factory

    def create(self, task: Task) -> Task:
        with self._Session() as session:
            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def get_all(self) -> List[Task]:
        with self._Session() as session:
            return session.query(Task).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        with self._Session() as session:
            return session.get(Task, task_id)

    def update(self, task: Task) -> Task:
        with self._Session() as session:
            session.merge(task)
            session.commit()
            session.refresh(task)
            return task

    def delete(self, task: Task) -> None:
        with self._Session() as session:
            session.delete(task)
            session.commit()

class UserRepository:
    def __init__(self, session_factory):
        self._Session = session_factory

    def create(self, user: User) -> User:
        with self._Session() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self._Session() as session:
            return session.get(User, user_id)

    def get_all(self) -> List[User]:
        with self._Session() as session:
            return session.query(User).all()
