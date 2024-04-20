import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'), nullable=False)
    mug_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('items.id'), nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    def __init__(self, user_id, mug_id, quantity=1):
        self.user_id = user_id
        self.mug_id = mug_id
        self.quantity = quantity

    def update_quantity(self, quantity):
        self.quantity += quantity
        sqlalchemy.session.commit()

    def saveToDB(self):
        sqlalchemy.session.add(self)
        sqlalchemy.session.commit()

    def deleteFromDB(self):
        sqlalchemy.session.delete(self)
        sqlalchemy.session.commit()