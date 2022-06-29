from settings.config import KEYBOARD
from data_base.dbalchemy import DBManager

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:
    def __init__(self):
        self._markup = None
        self.DB = DBManager()

    def start_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)

        self._markup.add(Keyboards.set_button('SELECT_PRODUCTS'))
        self._markup.row(Keyboards.set_button('INFO'), Keyboards.set_button('SETTINGS'))

        return self._markup

    def info_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)
        self._markup.add(Keyboards.set_button('<<'))
        return self._markup

    def settings_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)
        self._markup.add(Keyboards.set_button('<<'))
        return self._markup

    def category_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True, row_width=1)

        self._markup.add(self.set_button('SEMI-FINISHED_PRODUCT'))
        self._markup.add(self.set_button('GROCERY'))
        self._markup.add(self.set_button('ICE_CREAM'))

        self._markup.row(self.set_button('<<'), self.set_button('ORDER'))

        return self._markup

    def order_menu(self, step, quantity) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)

        self._markup.row(
            self.set_button('DOWN'),
            self.set_button('PRODUCT_AMOUNT'),
            self.set_button('UP')
        )
        self._markup.row(
            self.set_button('BACK_STEP'),
            self.set_button('ORDER_AMOUNT'),
            self.set_button('NEXT_STEP')
        )
        self._markup.row(
            self.set_button('<<'),
            self.set_button('APPLY'),
            self.set_button('X')
        )

        return self._markup

    @staticmethod
    def remove_menu() -> ReplyKeyboardRemove:
        # pop button analogue
        return ReplyKeyboardRemove()

    @staticmethod
    def set_button(name) -> KeyboardButton:
        return KeyboardButton(KEYBOARD[name])

    @staticmethod
    def set_inline_button(name) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            name.__str__(),
            callback_data=name.id.__str__()
        )

    def set_buttons_for_product_category(self, category) \
            -> InlineKeyboardMarkup:
        self._markup = InlineKeyboardMarkup(row_width=1)

        for item in self.DB.all_products_for(category):
            self._markup.add(self.set_inline_button(item))

        return self._markup
