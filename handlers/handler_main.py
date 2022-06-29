from handlers.handler_com import CommandHandler
from handlers.handler_misc_text import MiscTextHandler
from handlers.handler_inline_query import InlineQueryHandler


class HandlerMain:
    def __init__(self, bot):
        self._bot = bot
        self._com_handler = CommandHandler(self._bot)
        self._text_handler = MiscTextHandler(self._bot)
        self._inline_query_handler = InlineQueryHandler(self._bot)

    def handle(self) -> None:
        self._com_handler.handle()
        self._text_handler.handle()
        self._inline_query_handler.handle()
