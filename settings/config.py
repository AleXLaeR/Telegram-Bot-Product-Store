from emoji import emojize
import os


TOKEN = '5531445496:AAFXEc-qeg4egjtBgDtUQxAvr_CbE__FYms'

DB_NAME = 'products.db'

VERSION = '0.0.1'

AUTHOR = 'AleXLaeR'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join('sqlite:///' + BASE_DIR, DB_NAME)

COUNT = 0

KEYBOARD = {
    'SELECT_PRODUCTS': emojize(':open_file_folder: Choose a product'),
    'INFO': emojize(':speech_balloon: About us'),
    'SETTINGS': emojize(':gear: Settings'),
    'SEMI-FINISHED_PRODUCT': emojize(':pizza: Prepacks'),
    'GROCERY': emojize(':bread: Groceries'),
    'ICE_CREAM': emojize(':shaved_ice: Ice cream'),
    '<<': emojize(':fast_reverse_button:'),
    '>>': emojize(':fast-forward_button:'),
    'BACK_STEP': emojize(':reverse_button:'),
    'NEXT_STEP': emojize(':play_button:'),
    'ORDER': emojize(':check_mark: ORDER'),
    'X': emojize(':cross_mark:'),
    'DOWN': emojize('⏷'),
    'PRODUCT_AMOUNT': COUNT,
    'ORDER_AMOUNT': COUNT,
    'UP': emojize('⏶'),
    'APPLY': emojize(':check_mark: CHECKOUT'),
    'COPY': emojize(':copyright: All Rights Reserved'),
}

PRODUCT_CATEGORY = {
    'SEMI-FINISHED_PRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
}

COMMANDS = {
    'START': 'start',
    'HELP': 'help',
}
