from tracker.coin_balances import coinbal_update
from tracker.prices import prices_update
from tracker.tot_balances import tot_balances_update
from tracker.graph_drawer import draw_and_send


def recurrent_update():
    """
    Do all updates necessary (coin_balances, prices and total_balances) and the updated graph.
    """
    coinbal_update()
    prices_update()
    tot_balances_update()

    draw_and_send()


if __name__ == "__main__":
    recurrent_update()
