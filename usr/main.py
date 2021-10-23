import os
import numpy as np

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from ponto import Ponto
from figura import FigureConstructor
from utilities import find_figure_idx
from globals import *


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    displayCoordinates()
    displayFigures()

    glFlush()


def displayCoordinates() -> None:
    MAX = 1

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.8, 0.8, 0.8, 0.3)

    glLineWidth(1.0)
    glBegin(GL_LINES)
    for x in np.arange(-MAX, MAX, 0.1):
        glVertex2f(x, -MAX)
        glVertex2f(x, MAX)
        glVertex2f(-MAX, x)
        glVertex2f(MAX, x)

    glEnd()
    glColor3f(1, 1, 1)
    glLineWidth(1.5)

    glBegin(GL_LINES)
    glVertex2f(-MAX, 0)
    glVertex2f(MAX, 0)
    glVertex2f(0, -MAX)
    glVertex2f(0, MAX)
    glEnd()


def displayFigures() -> None:
    for figure in MAIN_FIGURE_LIST:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(*(figure.rgba))

        glPushMatrix()
        glTranslatef(*figure.figPos)
        glScalef(*figure.figScale)
        glRotatef(figure.figRot, 0, 0, 1.0)
        glMultMatrixf(figure.figShear)
        glMultMatrixf(figure.figReflex)

        glBegin(GL_POLYGON)
        for ponto in figure.pointsList:
            glVertex2f(*ponto())

        glEnd()
        glPopMatrix()


def LockedFigureMenu(option: int) -> int:
    os.system("cls")
    print("Criando Figura Pré-Definida")
    if option == 0:
        figSize = float(input("Insira o tamanho da aresta: "))
        posX = float(input("Insira a posicao inicial em X: "))
        posY = float(input("Insira a posicao inicial em Y: "))

        triangle = FigureConstructor.createTriangle(figSize, posX, posY)
        MAIN_FIGURE_LIST.append(triangle)

    elif option == 1:
        figSize = float(input("Insira o tamanho da aresta: "))
        posX = float(input("Insira a posicao inicial em X: "))
        posY = float(input("Insira a posicao inicial em Y: "))

        square = FigureConstructor.createSquare(figSize, posX, posY)
        MAIN_FIGURE_LIST.append(square)

    elif option == 2:
        figSize = float(input("Insira o tamanho da aresta: "))
        posX = float(input("Insira a posicao inicial em X: "))
        posY = float(input("Insira a posicao inicial em Y: "))

        hexagon = FigureConstructor.createHexagon(figSize, posX, posY)
        MAIN_FIGURE_LIST.append(hexagon)

    glutPostRedisplay()

    return 0


def FreeDrawMenu(option: int) -> int:
    global QTD_CLICKS
    os.system("cls")
    print("Desenho Livre")
    if option == 0:
        MOUSE_POINTS.clear()
        print("Selecionando Pontos")
        QTD_CLICKS = int(input("Quantos pontos você deseja utilizar? "))
        MOUSE_POINTS.clear()
        print("Pressione o botão do meio para cancelar")

    elif option == 1:
        print("Digitar Pontos")
        points = []
        while True:
            posX = float(input("Insira a posicao inicial em X: "))
            posY = float(input("Insira a posicao inicial em Y: "))

            points.append(Ponto(posX, posY))

            continuar = input("Deseja continuar? [S/N]")
            if continuar.lower() == "s":
                pass
            else:
                break

        irregular = FigureConstructor.createIrregular(points)
        MAIN_FIGURE_LIST.append(irregular)

    return 0


def EditorMenu(option: int) -> int:
    os.system("cls")
    print("Editar/Remover Figuras\n")
    for figure in MAIN_FIGURE_LIST:
        print(figure)

    id = int(input("Escolha a figura que deseja editar/remover: "))
    idx = find_figure_idx(id)
    if idx != -1:
        figure = MAIN_FIGURE_LIST[idx]
    else:
        raise ValueError("ID não existente")

    os.system("cls")
    print(f"Alterando: {figure}")

    if option == 0:
        posX = float(input("Escolha a coordenada X para transladar: "))
        posY = float(input("Escolha a coordenada Y para transladar: "))
        figure.figPos = (posX, posY, 0)
    elif option == 1:
        scaleX = float(input("Escolha a escala X para editar: "))
        scaleY = float(input("Escolha a escala Y para editar: "))
        figure.figScale = (scaleX, scaleY, 1)
    elif option == 2:
        axis = input("Eixo de Reflexão [X|Y]: ")
        figReflex = np.identity(4)
        if axis.lower() == "x":
            figReflex[1][1] = -1
            figure.figReflex = figReflex
        elif axis.lower() == "y":
            figReflex[0][0] = -1
            figure.figReflex = figReflex
        else:
            print("Opção inválida!")
    elif option == 3:
        angle = float(input("Angulo de Rotação: "))
        figure.figRot = angle
    elif option == 4:
        axis = input("Eixo de Cisalhamento [X|Y]: ")
        shear_value = float(input("Valor de Cisalhamento: "))
        figShear = np.identity(4)

        if axis.lower() == "x":
            figShear[1][0] = shear_value
            figure.figShear = figShear
        elif axis.lower() == "y":
            figShear[0][1] = shear_value
            figure.figShear = figShear
        else:
            print("Opção inválida!")
    elif option == 5:
        MAIN_FIGURE_LIST.pop(idx)
        print(f"Figura {id} removida!")

    glutPostRedisplay()

    return 0


def MenuMain(**kwargs) -> int:
    return 0


def CriaMenuFlutuante() -> None:
    menu_free_draw = glutCreateMenu(FreeDrawMenu)
    glutAddMenuEntry("Selecionar Pontos", 0)
    glutAddMenuEntry("Fixar Pontos", 1)

    menu_locked_draw = glutCreateMenu(LockedFigureMenu)
    glutAddMenuEntry("Triangulo", 0)
    glutAddMenuEntry("Quadrado", 1)
    glutAddMenuEntry("Hexagono", 2)

    menu_editor = glutCreateMenu(EditorMenu)
    glutAddMenuEntry("Translacao", 0)
    glutAddMenuEntry("Escala", 1)
    glutAddMenuEntry("Reflexao", 2)
    glutAddMenuEntry("Rotacao", 3)
    glutAddMenuEntry("Cisalhamento", 4)
    glutAddMenuEntry("Apagar Figura", 5)

    menu = glutCreateMenu(MenuMain)
    glutAddSubMenu("Desenho Livre", menu_free_draw)
    glutAddSubMenu("Figuras Pre-Definidas", menu_locked_draw)
    glutAddSubMenu("Editar Figuras", menu_editor)

    glutAttachMenu(GLUT_RIGHT_BUTTON)


def MouseManager(button: int, state: int, x: int, y: int) -> None:
    global QTD_CLICKS

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            CriaMenuFlutuante()

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            posX = (x - WINDOW_WIDTH / 2) / 250
            posY = -(y - WINDOW_HEIGHT / 2) / 250
            print(Ponto(posX, posY))
            if QTD_CLICKS:
                MOUSE_POINTS.append(Ponto(posX, posY))
            if (len(MOUSE_POINTS) == QTD_CLICKS) and bool(QTD_CLICKS):
                irregular = FigureConstructor.createIrregular(MOUSE_POINTS.copy())
                MAIN_FIGURE_LIST.append(irregular)
                print(f"Inserido: {MAIN_FIGURE_LIST[-1]}")
                MOUSE_POINTS.clear()
                QTD_CLICKS = 0

    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            QTD_CLICKS = 0
            if len(MOUSE_POINTS) and not QTD_CLICKS:
                print("Seleção de pontos cancelada!")
                MOUSE_POINTS.clear()


def main(*args, **kwargs):
    os.system("cls")
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_DEPTH | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("Atividade 1 - Computacao Grafica")

    glutDisplayFunc(display)
    glutMouseFunc(MouseManager)

    glutMainLoop()


if __name__ == "__main__":
    main()
