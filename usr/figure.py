import numpy as np
from typing import Tuple, List

from point import Point
from utilities import find_last_id
from globals import *


class Figure:
    """
    Class that stores all the parameters of a figure
    """

    def __init__(
        self,
        figName: str,
        pointsList: List[Point],
        rgba: Tuple[float, float, float, float] = (1, 1, 1, 0.5),
        figRot: float = 0,
        figPos: Tuple[float, float, float] = (0, 0, 0),
        figScale: Tuple[float, float, float] = (1, 1, 1),
        figShear: np.array = np.identity(4),
        figReflex: np.array = np.identity(4),
    ):
        self.figName = figName
        self.pointsList = pointsList
        self.rgba = rgba

        self.figRot = figRot
        self.figPos = figPos
        self.figScale = figScale
        self.figShear = figShear
        self.figReflex = figReflex

    def __str__(self) -> str:
        return f"{self.figName} with {self.pointsList}"

    def __new__(cls, *args, **kwargs):
        new_points = kwargs.get("pointsList")
        max_range = 1
        for new_point in new_points:
            if new_point > max_range:
                raise ValueError(
                    f"Possui ponto ({new_point}) fora do máximo permitido ({max_range})"
                )
            for figure in MAIN_FIGURE_LIST:
                if new_point in figure.pointsList:
                    raise ValueError(f"Possui ponto duplicado {new_point}")

        return super(Figure, cls).__new__(cls)

    def __repr__(self) -> str:
        return f"{self.figName} with {self.pointsList}"


class FigureConstructor:

    """
    Class with helper methods to create figures
    """

    @staticmethod
    def createSquare(figSize: float, posX: float, posY: float) -> Figure:
        """
        Helper method that creates a square with the given size and the center position of it

        Args:
            figSize (float): Size of the edge of the square
            posX (float): X position of the center of the square
            posY (float): Y position of the center of the square

        Returns:
            Figure: A figure with the given parameters
        """

        pointsList = [
            Point(posX + figSize / 2, posY + figSize / 2),
            Point(posX - figSize / 2, posY + figSize / 2),
            Point(posX - figSize / 2, posY - figSize / 2),
            Point(posX + figSize / 2, posY - figSize / 2),
        ]

        return Figure(
            figName=f"Quadrado - ID: {find_last_id() + 1}",
            rgba=(0, 1, 0, 0.8),
            pointsList=pointsList,
        )

    @staticmethod
    def createTriangle(figSize: float, posX: float, posY: float) -> Figure:
        """
        Helper method that creates a triangle with the given size and the top vertice position of it

        Args:
            figSize (float): Size of the edge of the square
            posX (float): X position of the top vertice of the triangle
            posY (float): Y position of the top vertice of the triangle

        Returns:
            Figure: A figure with the given parameters
        """
        import math

        height = math.sqrt(pow(figSize, 2) - pow(figSize / 2, 2))

        pointsList = [
            Point(posX, posY),
            Point(posX + (figSize / 2), posY - height),
            Point(posX - (figSize / 2), posY - height),
        ]

        return Figure(
            figName=f"Triangulo - ID: {find_last_id() + 1}",
            rgba=(0, 0, 1, 0.8),
            pointsList=pointsList,
        )

    @staticmethod
    def createHexagon(figSize: float, posX: float, posY: float) -> Figure:
        """
        Helper method that creates a hexagon with the given size and the center position of it

        Args:
            figSize (float): Size of the edge of the hexagon
            posX (float): X position of the center of the hexagon
            posY (float): Y position of the center of the hexagon

        Returns:
            Figure: A figure with the given parameters
        """
        import math

        height = math.sqrt(pow(figSize, 2) - pow(figSize / 2, 2))

        pointsList = [
            Point(posX + figSize, posY),
            Point(posX + (figSize / 2), posY + height),
            Point(posX - (figSize / 2), posY + height),
            Point(posX - figSize, posY),
            Point(posX - (figSize / 2), posY - height),
            Point(posX + (figSize / 2), posY - height),
        ]

        return Figure(
            figName=f"Hexagono - ID: {find_last_id() + 1}",
            rgba=(1, 0, 0, 0.8),
            pointsList=pointsList,
        )

    @staticmethod
    def createIrregular(pointsList: list) -> Figure:
        """
        Helper method that creates an irregular figure with the given points

        Args:
            pointsList (list): List of points that will be used to create the figure

        Returns:
            Figure: A figure with the given parameters
        """
        return Figure(
            figName=f"Irregular - ID: {find_last_id() + 1}",
            rgba=(1, 0, 1, 0.8),
            pointsList=pointsList,
        )
