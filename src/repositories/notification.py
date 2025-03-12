from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.notification import Notification


class NotificationRepository(ISqlAlchemyRepository[Notification]):
    _model = Notification
