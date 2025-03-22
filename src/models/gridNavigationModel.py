import numpy as np
from typing import Type

from src.models.gridModel import GridModel
from src.models.modelHelper import sync_model_data


class GridNavigationModel(GridModel):
    def __init__(self, viewModel: Type[GridModel]):
        super().__init__(*viewModel.getDimensions())
        sync_model_data(viewModel, self)
