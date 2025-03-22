from typing import Type

from src.models.gridModel import GridModel


def sync_model_data(copy_model: Type[GridModel], paste_model: Type[GridModel]):
    """
    Copys all cells, which don't have the default value from the copy_model and pasts them into the past_model.
    Only the affected cells are overwritten!
    """
    # creates a mask of all changed cells
    mask = copy_model.data != copy_model.default_value
    # overwrite all cells in which the mask is true
    paste_model.data[mask] = copy_model.data[mask]
