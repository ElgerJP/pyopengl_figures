import numpy as np
from typing import Tuple, List

from ponto import Ponto
from utilities import find_last_id
from globals import *


class Figura:
    def __init__(
        self,
        figName: str,
        pointsList: List[Ponto],
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

        return super(Figura, cls).__new__(cls)

    def __repr__(self) -> str:
        return f"{self.figName} with {self.pointsList}"


class FigureConstructor:
    @staticmethod
    def createSquare(figSize: float, posX: float, posY: float) -> Figura:

        pointsList = [
            Ponto(posX + figSize / 2, posY + figSize / 2),
            Ponto(posX - figSize / 2, posY + figSize / 2),
            Ponto(posX - figSize / 2, posY - figSize / 2),
            Ponto(posX + figSize / 2, posY - figSize / 2),
        ]

        return Figura(
            figName=f"Quadrado - ID: {find_last_id() + 1}",
            rgba=(0, 1, 0, 0.8),
            pointsList=pointsList,
        )

    @staticmethod
    def createTriangle(figSize: float, posX: float, posY: float) -> Figura:
        import math

        height = math.sqrt(pow(figSize, 2) - pow(figSize / 2, 2))

        pointsList = [
            Ponto(posX, posY),
            Ponto(posX + (figSize / 2), posY - height),
            Ponto(posX - (figSize / 2), posY - height),
        ]

        return Figura(
            figName=f"Triangulo - ID: {find_last_id() + 1}",
            rgba=(0, 0, 1, 0.8),
            pointsList=pointsList,
        )

    @staticmethod
    def createHexagon(figSize: float, posX: float, posY: float) -> Figura:
        import math

        height = math.sqrt(pow(figSize, 2) - pow(figSize / 2, 2))

        pointsList = [
            Ponto(posX + figSize, posY),
            Ponto(posX + (figSize / 2), posY + height),
            Ponto(posX - (figSize / 2), posY + height),
            Ponto(posX - figSize, posY),
            Ponto(posX - (figSize / 2), posY - height),
            Ponto(posX + (figSize / 2), posY - height),
        ]

        return Figura(
            figName=f"Hexagono - ID: {find_last_id() + 1}",
            rgba=(1, 0, 0, 0.8),
            pointsList=pointsList,
        )

    @staticmethod
    def createIrregular(pointsList: list) -> Figura:
        return Figura(
            figName=f"Irregular - ID: {find_last_id() + 1}",
            rgba=(1, 0, 1, 0.8),
            pointsList=pointsList,
        )
