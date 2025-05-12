import random


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

        if not filled_indices:
            return []

        return filled_indices

    def find_all_unfilled_toColony(self, ant) -> list[dict[tuple[int, int], list[int]]]:
        filled_indices = []
        for i, array in enumerate(self.area):
            for j, item in enumerate(array):
                if not item['toColony']:  # toColony is not filled
                    filled_indices.append({
                        (i, j): None
                    })

        if not filled_indices:
            return [{
                self.generate_random_cell(): None
            }]

        return filled_indices

    def find_largest_value(self, area: list[dict[tuple[int, int], list[int]]]) -> tuple[tuple[int, int], float]:
        """
        Get the largest value in the area and the corresponding cell. Orders by value in dict
        :param area:
        :return:
        """
        largest_value = float('-inf')
        largest_value_key = (0, 0)

        for item in area:
            for key, value in item.items():
                if max(value) > largest_value:
                    largest_value = max(value)
                    largest_value_key = key

        if largest_value_key == (1, 1):
            return self.generate_random_cell(), largest_value - 0.001

        return largest_value_key, largest_value

    def generate_random_cell(self) -> tuple[int, int]:
        matrix_elements = [(i, j) for i in range(3) for j in range(3) if (i, j) != (1, 1)]  # random cell except (1,1)
        return random.choice(matrix_elements)

    def get_area(self):
        return self.area
