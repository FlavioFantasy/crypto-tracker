
# https://plotly.com/python/line-and-scatter/

import plotly.express as px
import pandas as pd
from datetime import datetime

from tracker.db_handler import db_get_tot_balances
from tracker.telegram_handler import send_image
from tracker.utils import log_info

def draw_and_send():
    all_balances = db_get_tot_balances()
    all_balances_df = pd.DataFrame(all_balances)
    # print(all_balances_df)

    fig = px.line(all_balances_df, x="date", y="eur_amount", title="Crypto portfolio")
    # fig.show()

    today = datetime.today().date().strftime("%Y-%m-%d")
    img_name = f"tracker/images/{today}.png"
    fig.write_image(img_name)

    send_image(img_name)
    print("graph_drawer: sent image")
    log_info("graph_drawer: sent image")


# if __name__ == '__main__':
#     draw_and_send()
