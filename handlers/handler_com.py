from handlers.handler import Handler


class CommandHandler(Handler):
    # class that handles commands like /start, /help ...
    def __init__(self, bot):
        super().__init__(bot)

    def _on_start_button_click(self, msg) -> None:
        self.bot.send_message(msg.chat.id,
                              'Hello! Waiting for other commands',
                              reply_markup=self.keyboards.start_menu()
                              )

    def handle(self) -> None:
        #  '/start' input event handler
        @self.bot.message_handler(commands=['start'])
        def handle(msg) -> None:
            if msg.text == '/start':
                self._on_start_button_click(msg)
