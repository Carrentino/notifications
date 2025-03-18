from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.mail import Mail


class MailRepository(ISqlAlchemyRepository[Mail]):
    _model = Mail
