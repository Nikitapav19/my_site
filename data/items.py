import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Items(SqlAlchemyBase):
    __tablename__ = 'items'

    article = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user = orm.relationship('User')
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    about = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    orders = orm.relationship("Orders", back_populates='item')

    def __repr__(self):
        return f'<Created> {self.creator} {self.name} {self.article}'

    def saveToDB(self):
        sqlalchemy.session.add(self)
        sqlalchemy.session.commit()

    def deleteFromDB(self):
        sqlalchemy.session.delete(self)
        sqlalchemy.session.commit()
