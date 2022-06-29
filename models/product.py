from models.category import Category
from data_base.dbcore import Base

from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

    # for cascade deletion from table
    category = relationship(
        Category,  # relation by foreign key with table 'Category'
        backref=backref('products',
                        uselist=True,  # applying mechanism to all found relations
                        cascade='delete, all')
    )

    def __str__(self):
        return f'{self.name}-{self.title}-{self.price}'
