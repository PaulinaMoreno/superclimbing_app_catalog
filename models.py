from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(300))
    cat_image_filename = Column(String, default=None, nullable=True)
    cat_image_url = Column(String, default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'cat_image_filename': self.cat_image_filename,
            'cat_image_url': self.cat_image_url,

        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(300))
    price = Column(String(8))
    item_image_filename = Column(String, default=None, nullable=True)
    item_image_url = Column(String, default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category_id = Column(Integer, ForeignKey('category.id'))
    # Cascade delete
    category = relationship(
        Category,
        backref=backref('items',
                        uselist=True,
                        cascade='delete,all', lazy='dynamic'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,

        }


engine = create_engine('sqlite:///superclimbing.db')


Base.metadata.create_all(engine)
