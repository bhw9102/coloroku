import random


def shuffle_ordering(count: int):
    order_list = list(range(0, count))
    random.shuffle(order_list)
    return order_list

