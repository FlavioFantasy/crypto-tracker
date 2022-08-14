from datetime import date
from pathlib import Path
from typing import Optional

import pandas as pd  # type: ignore
import plotly.express as px  # type: ignore

from tracker import db
from tracker.config import CurrentConf
from tracker.utils import log_info


def draw_save_graph(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> None:
    """Draw graph of eur valuation of crypto tracker and save it"""

    def _get_img_file_path() -> Path:
        f_start = (start_date if start_date else total_balances[0]["date"]).strftime(
            "%Y%m%d"
        )
        f_end = (end_date if end_date else total_balances[-1]["date"]).strftime(
            "%Y%m%d"
        )
        file_name = f"{f_start}-{f_end}.png"

        return Path(CurrentConf.get().get_imgs_folder(), file_name)

    total_balances = db.balance.get_tot_balances(None, start_date, end_date)
    total_balances_df = pd.DataFrame(total_balances)

    # create graph
    # https://plotly.com/python/line-and-scatter/
    eur_graph = px.line(
        total_balances_df, x="date", y="eur_amount", title="Crypto portfolio"
    )
    # fig.show()  # to open browser with graph

    # save it
    file_path = _get_img_file_path()
    eur_graph.write_image(file_path)

    log_info(f"draw_save_graph: eur graph saved as '{file_path}'")
