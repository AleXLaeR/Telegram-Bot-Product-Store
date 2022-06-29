from handlers.handler import Handler
from settings.config import KEYBOARD, PRODUCT_CATEGORY
from settings.message import REPLY_MESSAGES


class MiscTextHandler(Handler):
    def __init__(self, bot):
        super().__init__(bot)
        self._step = 0

    def _on_category_button_click(self, msg) -> None:
        self.bot.send_message(msg.chat.id,
                              'Product category catalogue',
                              reply_markup=self.keyboards.remove_menu()
                              )
        self.bot.send_message(msg.chat.id,
                              'Make a choice',
                              reply_markup=self.keyboards.category_menu()
                              )

    def _on_info_button_click(self, msg) -> None:
        self.bot.send_message(msg.chat.id,
                              REPLY_MESSAGES['trade_store'],
                              parse_mode='html',
                              reply_markup=self.keyboards.info_menu()
                              )

    def _on_settings_button_click(self, msg) -> None:
        self.bot.send_message(msg.chat.id,
                              REPLY_MESSAGES['settings'],
                              parse_mode='html',
                              reply_markup=self.keyboards.settings_menu()
                              )

    def _on_return_back_button_click(self, msg) -> None:
        self.bot.send_message(msg.chat.id,
                              'You have returned back',
                              reply_markup=self.keyboards.start_menu()
                              )

    def _on_product_button_click(self, msg, product) -> None:
        self.bot.send_message(msg.chat.id,
                              f'Category {KEYBOARD[product]}',
                              reply_markup=self.keyboards
                              .set_buttons_for_product_category(PRODUCT_CATEGORY[product])
                              )
        self.bot.send_message(msg.chat.id,
                              'OK',
                              reply_markup=self.keyboards.category_menu()
                              )

    def _on_order_button_click(self, msg) -> None:
        # resetting the step (current item at which cursor is pointing)
        self._step = 0
        # list of all product ids in an order
        pd_ids = self.DB.select_product_ids(amount='all')

        # quantity for every item in an order
        order_quantity = self.DB.select_order_quantity(
            pd_id := pd_ids[self._step]
        )

        self._send_order_message(pd_id, order_quantity, msg)

    def _send_order_message(self, product_id, quantity, msg) -> None:
        self.bot.send_message(
            msg.chat.id,
            REPLY_MESSAGES['order_number'].format(self._step + 1),
            parse_mode='html'
        )

        self.bot.send_message(
            msg.chat.id,
            REPLY_MESSAGES['order'].format(
                self.DB.select_product_attr(product_id, 'name'),
                self.DB.select_product_attr(product_id, 'title'),
                self.DB.select_product_attr(product_id, 'price'),
                self.DB.select_product_attr(product_id, 'quantity')
            ),
            parse_mode='html',
            reply_markup=self.keyboards.order_menu(
                self._step, quantity
            )
        )

    def _on_up_button_click(self, msg) -> None:
        self.bot.send_message(
            msg.chat.id,
            'You have returned back',
            reply_markup=self.keyboards.start_menu()
        )

    def _on_down_button_click(self, msg) -> None:
        self.bot.send_message(
            msg.chat.id,
            'You have returned back',
            reply_markup=self.keyboards.start_menu()
        )

    def _on_nextstep_button_click(self, msg) -> None:
        self.bot.send_message(
            msg.chat.id,
            'You have returned back',
            reply_markup=self.keyboards.start_menu()
        )

    def _on_backstep_button_click(self, msg) -> None:
        self.bot.send_message(
            msg.chat.id,
            'You have returned back',
            reply_markup=self.keyboards.start_menu()
        )

    def _on_cancel_button_click(self, msg) -> None:
        self.bot.send_message(
            msg.chat.id,
            'You have returned back',
            reply_markup=self.keyboards.start_menu()
        )

    def handle(self) -> None:
        @self.bot.message_handler(func=lambda msg: True)
        def handle(msg) -> None:
            if msg.text == KEYBOARD['SELECT_PRODUCTS']:
                self._on_category_button_click(msg)

            if msg.text == KEYBOARD['INFO']:
                self._on_info_button_click(msg)

            if msg.text == KEYBOARD['SETTINGS']:
                self._on_settings_button_click(msg)

            if msg.text == KEYBOARD['<<']:
                self._on_return_back_button_click(msg)

            if msg.text == KEYBOARD['ORDER']:
                if self.DB.get_order_count() > 0:
                    self._on_order_button_click(msg)
                else:
                    self.bot.send_message(
                        msg.chat.id,
                        REPLY_MESSAGES['no_order'],
                        parse_mode='html',
                        reply_markup=self.keyboards.category_menu()
                    )

            categories = ('SEMI-FINISHED_PRODUCT', 'GROCERY', 'ICE_CREAM',)
            if msg.text in (binds := [KEYBOARD[category] for category in categories]):
                self._on_product_button_click(msg, categories[binds.index(msg.text)])

            # ------------- ORDER MENU -------------

            if msg.text == KEYBOARD['DOWN']:
                self._on_up_button_click(msg)

            if msg.text == KEYBOARD['UP']:
                self._on_down_button_click(msg)

            if msg.text == KEYBOARD['X']:
                self._on_up_button_click(msg)

            if msg.text == KEYBOARD['BACK_STEP']:
                self._on_down_button_click(msg)

            if msg.text == KEYBOARD['NEXT_STEP']:
                self._on_up_button_click(msg)
