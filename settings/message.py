from settings.config import KEYBOARD, VERSION, AUTHOR

trade_store = """

<b>Welcome to the TradeStore app !!!</b>

This bot was specifically designed 
for sales representatives, storekeepers, 
as well as commercial organizations engaged in wholesale and retail trade.

By using the TradeStore application, you can easily 
accept an order from a client in a convenient, intuitive form.
The application will help to place an order and will itself 
redirect it to the storekeeper of the firm for further order picking.

"""

settings = """
<b>Brief bot usage guide:</b>

<i>Navigation:</i>

-<b>({}) - </b><i>go back</i>
-<b>({}) - </b><i>go forward</i>
-<b>({}) - </b><i>increase font size</i>
-<b>({}) - </b><i>decrease font size</i>
-<b>({}) - </b><i>next</i>
-<b>({}) - </b><i>previous</i>

<i>Special Options:</i>

-<b>({}) - </b><i>delete</i>
-<b>({}) - </b><i>my order</i>
-<b>({}) - </b><i>set order</i>


<i>General information:</i>

-<b>bot version: - </b> <i>{}</i>
-<b>bot author: - </b> <i>{}</i>


<b>{}, AleXLaeR</b>

""".format(
    KEYBOARD['<<'],
    KEYBOARD['>>'],
    KEYBOARD['UP'],
    KEYBOARD['DOWN'],
    KEYBOARD['NEXT_STEP'],
    KEYBOARD['BACK_STEP'],
    KEYBOARD['X'],
    KEYBOARD['ORDER'],
    KEYBOARD['APPLY'],
    VERSION,
    AUTHOR,
    KEYBOARD['COPY'],
)

product_order = """
Selected product:

{}
{}
Total cost: {} USD

Added to the order !!!

Left in stock: {}
"""

order = """

<i>Name:</i> <b>{}</b>

<i>Description:</i> <b>{}</b>

<i>Price:</i> <b>{} USD for 1 p.</b>

<i>Item quantity:</i> <b>{} p.</b>
"""

order_number = """
<b>Item position in order № </b> <i>{}</i>
"""

no_order = """
<b>No order is currently being handled !!!</b>
"""

apply = """
<b>Your order is set !!!</b>

<i>Total order cost is:</i> <b>{} USD</b>

<i>Total quantity of items is:</i> <b>{} p.</b>

<b>The order has been sent to the warehouse !!!</b>
"""


REPLY_MESSAGES =  {
    'trade_store': trade_store,
    'product_order': product_order,
    'order': order,
    'order_number': order_number,
    'no_order': no_order,
    'apply': apply,
    'settings': settings,
}
