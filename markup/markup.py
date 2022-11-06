from settings import config
from data_base.dbalchemy import DBManager

from telebot.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:
    def __init__(self):
        self._markup = None
        self.DB = DBManager()

    def start_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)

        self._markup.add(self.set_button('SELECT_PRODUCTS'))
        self._markup.row(self.set_button('INFO'), self.set_button('SETTINGS'))

        return self._markup

    def info_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)
        self._markup.add(self.set_button('<<'))
        return self._markup

    def settings_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)
        self._markup.add(self.set_button('<<'))
        return self._markup

    def category_menu(self) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True, row_width=1)

        self._markup.add(self.set_button('SEMI-FINISHED_PRODUCT'))
        self._markup.add(self.set_button('GROCERY'))
        self._markup.add(self.set_button('ICE_CREAM'))

        self._markup.row(self.set_button('<<'), self.set_button('ORDER'))

        return self._markup

    def order_status_menu(self, step, quantity) -> ReplyKeyboardMarkup:
        self._markup = ReplyKeyboardMarkup(True, one_time_keyboard=True)

        self._markup.row(
            self.set_button('UP', step, quantity),
            self.set_button('PRODUCT_AMOUNT', step, quantity),
            self.set_button('DOWN', step, quantity)
        )
        self._markup.row(
            self.set_button('BACK_STEP', step, quantity),
            self.set_button('ORDER_AMOUNT', step, quantity),
            self.set_button('NEXT_STEP', step, quantity)
        )
        self._markup.row(
            self.set_button('<<', step, quantity),
            self.set_button('APPLY', step, quantity),
            self.set_button('X', step, quantity)
        )

        return self._markup

    def set_button(self, name, step=0, quantity=0) -> KeyboardButton:

        if name == 'ORDER_AMOUNT':
            config.KEYBOARD[name] = f'{step + 1} out of ' \
                             f'{str(self.DB.get_order_count())}'

        if name == 'PRODUCT_AMOUNT':
            config.KEYBOARD[name] = f'{quantity}'

        return KeyboardButton(config.KEYBOARD[name])

    @staticmethod
    def remove_menu() -> ReplyKeyboardRemove:
        # pop button analogue
        return ReplyKeyboardRemove()

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
