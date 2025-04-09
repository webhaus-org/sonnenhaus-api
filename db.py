import json
import sqlalchemy.orm

from sqlalchemy import create_engine
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Integer, JSON, String


class Base(sqlalchemy.orm.DeclarativeBase):
    pass


class MeasurementEntry(Base):
    __tablename__ = "measurement_entry"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    type = mapped_column(String, nullable=False)
    _measurement = mapped_column(JSON, server_default='{}')
    _meta = mapped_column(JSON, server_default='{}')

    def measurement(self):
        return json.loads(self._measurement)

    def meta(self):
        return json.loads(self._meta)


def create_session(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    session_factory = sqlalchemy.orm.sessionmaker(bind=engine)
    session = sqlalchemy.orm.scoped_session(session_factory)

    return session


class DBMiddleware:

    def __init__(self, db_session):
        self.db_session = db_session

    def process_resource(self, req, resp, resource, params):
        req.context.db_session = self.db_session()

    def process_response(self, req, resp, resource, req_succeeded):
        if not resource or not hasattr(req.context, "db_session"):
            return

        req.context.db_session.commit()
        self.db_session.remove()
