import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Orders(SqlAlchemyBase):
    __tablename__ = 'orders'

    order_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    item = orm.relationship("Items")
    item_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("items.article"))
     #size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    # address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user = orm.relationship('User')
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
   # quantity = sqlalchemy.Column(sqlalchemy.Integer, default=1)


    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id



    def saveToDB(self):
        sqlalchemy.session.add(self)
        sqlalchemy.session.commit()

    def deleteFromDB(self):
        sqlalchemy.session.delete(self)
        sqlalchemy.session.commit()