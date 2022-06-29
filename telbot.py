from handlers.handler_main import HandlerMain
from settings.config import VERSION, AUTHOR, TOKEN
from telebot import TeleBot


class TelegramBot:
    __author__ = AUTHOR
    __version__ = VERSION

    def __init__(self):
        # Bot and event handler init
        self._token = TOKEN
        self._bot = TeleBot(self._token)
        self._handler = HandlerMain(self._bot)

    def _start(self) -> None:
        self._handler.handle()

    def run(self) -> None:
        self._start()
        self._bot.polling(non_stop=True)


if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()
