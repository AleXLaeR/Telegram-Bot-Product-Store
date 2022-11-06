def total_cost(price_list, quant_list) -> float:
    total = 0
    for item in zip(price_list, quant_list):
        total += item[0] * item[1]
    return total


def get_total_cost(DB) -> float:
    pd_ids = DB.select_product_ids(amount='all')
    all_prices = [DB.select_product_attr(pd, 'price') for pd in pd_ids]
    all_quantities = [DB.select_order_quantity(pd) for pd in pd_ids]

    return total_cost(all_prices, all_quantities)


def get_total_quantity(DB) -> int:
    pd_ids = DB.select_product_ids(amount='all')
    all_quantities = [DB.select_order_quantity(pd) for pd in pd_ids]

    return sum(all_quantities, 0)
