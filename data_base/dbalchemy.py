from datetime import datetime

from models.order import Order
from settings.config import DATABASE
from models.product import Products

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from data_base.dbcore import Base

from os import path
from typing import Any, Literal


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    def __init__(self):
        self._engine = create_engine(DATABASE)
        self._session = sessionmaker(bind=self._engine).__call__()

        if not path.isfile(DATABASE):
            Base.metadata.create_all(self._engine)

    def add_order(self, product_id, *, user_id=1, quantity=1) -> None:
        if product_id in self.select_product_ids(amount='all'):
            order_quantity = self.select_order_quantity(product_id)
            self.update_order_attr(product_id, order_quantity + 1, by_name='quantity')
        else:
            order = Order(
                quantity=quantity,
                product_id=product_id,
                user_id=user_id,
                data=datetime.now()
            )
            self._session.add(order)
            self._session.commit()

        product_quantity = self.select_product_attr(product_id, by_name='quantity')
        self.update_product_attr(product_id, product_quantity - 1, by_name='quantity')

        self._session.close()

    def all_products_for(self, category) -> Any:
        result = self._session.query(Products).filter_by(
            category_id=category
        ).all()
        self._session.close()
        return result

    def select_product_ids(self, amount: Literal['one', 'all']) -> list[int]:
        result = self._session.query(Order.product_id)
        result = result.all() if amount == 'all' else result.one()

        self._session.close()
        return [item[0] for item in result]

    def select_all_order_ids(self) -> list[int]:
        result = self._session.query(Order.id).all()

        self._session.close()
        return [item[0] for item in result]

    def update_order_attr(self, row_id, new_value, *, by_name) -> None:
        self._session.query(Order) \
            .filter_by(product_id=row_id) \
            .update({by_name: new_value})

        self._session.commit()
        self._session.close()

    def update_product_attr(self, product_id, new_value, *, by_name) -> None:
        self._session.query(Products) \
            .filter_by(id=product_id) \
            .update({by_name: new_value})

        self._session.commit()
        self._session.close()

    def select_order_quantity(self, product_id) -> int:
        result = self._session.query(Order.quantity) \
            .filter_by(product_id=product_id) \
            .one()

        self._session.close()
        return result.quantity

    def select_product_attr(self, row_id,
                            by_name: Literal['quantity', 'name', 'title', 'price']) -> Any:
        attr_dict = {
            'quantity': Products.quantity,
            'name': Products.name,
            'title': Products.title,
            'price': Products.price
        }

        result = self._session.query(attr_dict[by_name]) \
            .filter_by(id=row_id) \
            .one()
        self._session.close()

        if by_name == 'quantity':
            return result.quantity
        if by_name == 'name':
            return result.name
        if by_name == 'title':
            return result.title
        return result.price

    def get_order_count(self) -> int:
        result = self._session.query(Order).count()
        self._session.close()
        return result

    def cancel_order(self, product_id) -> None:
        self._session.query(Order) \
            .filter_by(product_id=product_id) \
            .delete()

        self._session.commit()
        self._session.close()

    def cancel_all_orders(self) -> None:
        for ord_id in self.select_all_order_ids():
            self._session.query(Order) \
                .filter_by(id=ord_id) \
                .delete()

            self._session.close()
