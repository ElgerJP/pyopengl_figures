from typing import Union
from globals import *


def find_figure_idx(find_id: int) -> Union[int, None]:
    for idx, figure in enumerate(MAIN_FIGURE_LIST):
        id = int(figure.figName.split(" ")[3])
        if find_id == id:
            return idx

    return -1


def find_last_id() -> int:
    if len(MAIN_FIGURE_LIST):
        return int(MAIN_FIGURE_LIST[-1].figName.split(" ")[3])
    else:
        return 0
