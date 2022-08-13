# https://plotly.com/python/line-and-scatter/

from datetime import date
from typing import Optional, Union

import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore

from tracker import db
from tracker.telegram_handler import send_image
from tracker.utils import log_info


def draw_and_send(
    start_date: Optional[Union[str, date]] = None,
    end_date: Optional[Union[str, date]] = None,
):
    all_balances = db.balance.db_get_tot_balances(None, start_date, end_date)
    all_balances_df = pd.DataFrame(all_balances)

    fig = px.line(all_balances_df, x="date", y="eur_amount", title="Crypto portfolio")
    # fig.show()

    img_name = f"tracker/images/{date.today()}.png"
    try:
        fig.write_image(img_name)
    except:
        img_name = f"tracker/images/{date.today()}-1.png"
        fig.write_image(img_name)

    send_image(img_name)
    print("graph_drawer: sent image")
    log_info("graph_drawer: sent image")


# if __name__ == '__main__':
#     draw_and_send('2022-01-01', '2022-01-15')
