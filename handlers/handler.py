from markup.markup import Keyboards
from data_base.dbalchemy import DBManager
from abc import ABCMeta, abstractmethod


class Handler(metaclass=ABCMeta):
    def __init__(self, bot):
        self.bot = bot
        self.keyboards = Keyboards()  # initialising keyboard markup
        self.DB = DBManager()  # initialising manager for db control

    @abstractmethod
    def handle(self) -> None:
        pass
