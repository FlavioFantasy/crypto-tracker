from datetime import date
from pathlib import Path
from typing import Optional, Union

import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore

from tracker import db
from tracker.config import CurrentConf
from tracker.telegram_handler import send_image
from tracker.utils import log_info


def _get_file_name() -> Path:
    imgs_folder = CurrentConf.get().get_imgs_folder()

    img_name = Path(imgs_folder, f"{date.today()}.png")
    i = 0
    while img_name.exists():
        i += 1
        img_name = Path(imgs_folder, f"{date.today()}-{i}.png")
    return img_name


def draw_and_send(
    start_date: Optional[Union[str, date]] = None,
    end_date: Optional[Union[str, date]] = None,
) -> None:
    """Draw graph of eur valuation of crypto tracker and send it via Telegram"""

    total_balances_df = pd.DataFrame(
        db.balance.get_tot_balances(None, start_date, end_date)
    )

    # https://plotly.com/python/line-and-scatter/
    eur_graph = px.line(
        total_balances_df, x="date", y="eur_amount", title="Crypto portfolio"
    )
    # fig.show()  # to open browser with graph

    img_name = _get_file_name()
    # create img
    eur_graph.write_image(img_name)

    # send img
    send_image(img_name)

    log_info("draw_and_send: sent image")


# if __name__ == "__main__":
#     draw_and_send("2022-01-01", "2022-01-15")
