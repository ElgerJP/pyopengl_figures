from typing import Union
from globals import *


def find_figure_idx(find_id: int) -> int:
    """
    Function that gets a figure id and returns the index of the figure in the figure list.

    Args:
        find_id (int): The id of the figure to find.

    Returns:
        int: -1 if the figure is not found, otherwise the index of the figure in the figure list.
    """
    for idx, figure in enumerate(MAIN_FIGURE_LIST):
        id = int(figure.figName.split(" ")[3])
        if find_id == id:
            return idx

    return -1


def find_last_id() -> int:
    """
    Function that gets the last ID of the figures in the figure list.

    Returns:
        int: 0 if the figure list is empty, otherwise the last ID of the figures in the figure list.
    """
    if len(MAIN_FIGURE_LIST):
        return int(MAIN_FIGURE_LIST[-1].figName.split(" ")[3])
    else:
        return 0
