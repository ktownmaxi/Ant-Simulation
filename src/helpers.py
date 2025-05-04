def threeToThreeMatrixToRelativeVector(matrix: tuple[int, int]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(matrix, (-1, -1)))
