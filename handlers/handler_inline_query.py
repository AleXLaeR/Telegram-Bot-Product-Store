from handlers.handler import Handler
from settings.message import REPLY_MESSAGES


class InlineQueryHandler(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def _on_some_product_button_click(self, call, product_code_id) -> None:
        self.DB.add_order(product_code_id, user_id=1)

        self.bot.answer_callback_query(
            call.id,
            REPLY_MESSAGES['product_order'].format(
                self.DB.select_product_attr(product_code_id, by_name='name'),
                self.DB.select_product_attr(product_code_id, by_name='title'),
                self.DB.select_product_attr(product_code_id, by_name='price'),
                 self.DB.select_product_attr(product_code_id, by_name='quantity')
            ),
            show_alert=True
        )

    def handle(self) -> None:
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call) -> None:
            code = int(_code) if (_code := call.data).isdigit() else _code
            self._on_some_product_button_click(call, code)
