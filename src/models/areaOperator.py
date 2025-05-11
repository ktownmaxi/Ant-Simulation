class AreaOperator:
    def __init__(self, area, navigation_model):
        self.area = area
        self.navigation_model = navigation_model

    def find_all_filled_colony(self, ant) -> list[dict[tuple[int, int], list[int]]]:
        filled_indices = []
        for i, array in enumerate(self.area):
            for j, item in enumerate(array):
                if item['colony']:  # colony is filled
                    filled_indices.append({
                        (i, j): item['colony']
                    })

        return filled_indices

    def find_all_filled_food(self, ant) -> list[dict[tuple[int, int], list[int]]]:
        filled_indices = []
        for i, array in enumerate(self.area):
            for j, item in enumerate(array):
                if item['food']:  # food is filled
                    filled_indices.append({
                        (i, j): item['food']
                    })

        return filled_indices

    def find_all_filled_toFood(self, ant) -> list[dict[tuple[int, int], list[int]]]:
        filled_indices = []
        for i, array in enumerate(self.area):
            for j, item in enumerate(array):
                if item['toFood']:  # toFood is filled
                    filled_indices.append({
                        (i, j): item['toFood']
                    })

        return filled_indices

    def find_all_filled_toColony(self, ant) -> list[dict[tuple[int, int], list[int]]]:
        filled_indices = []
        for i, array in enumerate(self.area):
            for j, item in enumerate(array):
                if item['toColony']:  # toColony is filled
                    filled_indices.append({
                        (i, j): item['toColony']
                    })

        final_indices = self.filter_invalid_cells(ant, filled_indices)
        if len(filled_indices) <= 0 or len(final_indices) <= 0:
            return self.find_all_unfilled_toColony(ant)

        return final_indices

    # TODO: fix death loop :)
    def find_all_unfilled_toColony(self, ant) -> list[dict[tuple[int, int], list[int]]]:
        filled_indices = []
        for i, array in enumerate(self.area):
            for j, item in enumerate(array):
                if not item['toColony']:  # toColony is filled
                    filled_indices.append({
                        (i, j): None
                    })

        final_indices = self.filter_invalid_cells(ant, filled_indices)
        if len(filled_indices) <= 0 or len(final_indices) <= 0:
            return self.find_all_filled_toColony(ant)

        return final_indices

    def find_largest_value(self, area: list[dict[tuple[int, int], list[int]]]) -> tuple[tuple[int, int], float]:
        largest_value = float('-inf')
        largest_value_key = [0, 0]

        for item in area:
            for key, value in item.items():
                # find the biggest value
                if max(value) > largest_value:
                    largest_value = max(value)
                    largest_value_key = key

        return largest_value_key, largest_value

    def filter_invalid_cells(self, ant, cell_selection: dict[tuple[int, int], object]) -> list[dict[tuple[int, int], list[int]]]:
        final_list = []
        for cell in cell_selection:
            final_list.append(cell)

        return final_list

    def get_area(self):
        return self.area
