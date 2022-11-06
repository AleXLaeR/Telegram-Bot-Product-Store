from handlers.handler import Handler
from settings import utility
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
        # resetting the step
        # (current item at which cursor is pointing)
        self._step = 0
        self._send_order_message(msg)

    def _send_order_message(self, msg) -> None:
        def send_message(product_id, quantity) -> None:
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
                    self.DB.select_order_quantity(product_id)
                ),
                parse_mode='html',
                reply_markup=self.keyboards.order_status_menu(
                    self._step,
                    quantity
                )
            )

        # list of all product ids in an order
        pd_ids = self.DB.select_product_ids(amount='all')
        # quantity for single item in an order
        order_quantity = self.DB.select_order_quantity(
            pd_id := pd_ids[self._step]
        )
        send_message(pd_id, order_quantity)

    def _on_up_button_click(self, msg) -> None:
        # list of all product ids in an order
        pd_ids = self.DB.select_product_ids(amount='all')

        # quantity of an item in order
        order_quantity = self.DB.select_order_quantity(
            pd_id := pd_ids[self._step]
        )
        # quantity of an item in stock
        product_quantity = self.DB.select_product_attr(pd_id, 'quantity')

        if product_quantity > 0:
            order_quantity += 1
            product_quantity -= 1

            self.DB.update_order_attr(pd_id, order_quantity, by_name='quantity')
            self.DB.update_product_attr(pd_id, product_quantity, by_name='quantity')

        self._send_order_message(msg)

    def _on_down_button_click(self, msg) -> None:
        # list of all product ids in an order
        pd_ids = self.DB.select_product_ids(amount='all')

        # quantity of an item in order
        order_quantity = self.DB.select_order_quantity(
            pd_id := pd_ids[self._step]
        )
        # quantity of an item in stock
        product_quantity = self.DB.select_product_attr(pd_id, 'quantity')

        if product_quantity > 0:
            order_quantity -= 1
            product_quantity += 1

            self.DB.update_order_attr(pd_id, order_quantity, by_name='quantity')
            self.DB.update_product_attr(pd_id, product_quantity, by_name='quantity')

        self._send_order_message(msg)

    def _on_nextstep_button_click(self, msg) -> None:
        if self._step < self.DB.get_order_count() - 1:
            self._step += 1
        self._send_order_message(msg)

    def _on_backstep_button_click(self, msg) -> None:
        if self._step > 0:
            self._step -= 1
        self._send_order_message(msg)

    def _on_cancel_button_click(self, msg) -> None:
        if len(pd_ids := self.DB.select_product_ids(amount='all')) > 0:
            order_quantity = self.DB.select_order_quantity(
                pd_id := pd_ids[self._step]
            )

            self.DB.cancel_order(pd_id)
            self._step -= 1

            product_quantity = self.DB.select_product_attr(pd_id, 'quantity')
            self.DB.update_product_attr(
                pd_id,
                product_quantity + order_quantity,
                by_name='quantity'
            )

        if len(self.DB.select_product_ids(amount='all')) > 0:
            self._send_order_message(msg)
        else:
            self.bot.send_message(
                msg.chat.id,
                REPLY_MESSAGES['no_order'],
                parse_mode='html',
                reply_markup=self.keyboards.category_menu()
            )

    def _on_apply_button_click(self, msg) -> None:
        self.bot.send_message(
            msg.chat.id,
            REPLY_MESSAGES['apply'].format(
                utility.get_total_cost(self.DB),
                utility.get_total_quantity(self.DB)
            ),
            parse_mode='html',
            reply_markup=self.keyboards.category_menu()
        )
        self.DB.cancel_all_orders()

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
                self._on_down_button_click(msg)

            if msg.text == KEYBOARD['UP']:
                self._on_up_button_click(msg)

            if msg.text == KEYBOARD['X']:
                self._on_cancel_button_click(msg)

            if msg.text == KEYBOARD['BACK_STEP']:
                self._on_backstep_button_click(msg)

            if msg.text == KEYBOARD['NEXT_STEP']:
                self._on_nextstep_button_click(msg)

            if msg.text == KEYBOARD['APPLY']:
                self._on_apply_button_click(msg)
