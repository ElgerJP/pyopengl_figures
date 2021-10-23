import os
import numpy as np

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from point import Point
from figure import FigureConstructor
from utilities import find_figure_idx
from globals import *


def display() -> None:
    """
    Function that handles the display of the coordinates and the figures
    """
    glClear(GL_COLOR_BUFFER_BIT)

    displayCoordinates()
    displayFigures()

    glFinish()


# R10
def displayCoordinates() -> None:
    """
    Function that handles the generation of the coordinates
    """
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


# R5
def displayFigures() -> None:
    """
    Function that handles the display of the figures and the geometric transformatioms.
    The figures are drawn in the order they were added to the list, with colors defined by the figure type.
    """
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
        for point in figure.pointsList:
            glVertex2f(*point())

        glEnd()
        glPopMatrix()


# R1, R4
def LockedFigureMenu(option: int) -> int:
    """
    Function that handles the menu for the creation of the regular geometric figures.

    Args:
        option (int): Option selected by the user.

    Returns:
        int: 0 when the function is called.
    """
    os.system("cls")
    print("Creating Locked Figure")
    if option == 0:
        figSize = float(input("Insert the size of the edge of the triangle: "))
        posX = float(input("Insert the top vertice of the figure in X: "))
        posY = float(input("Insert the top vertice of the figure in Y: "))

        triangle = FigureConstructor.createTriangle(figSize, posX, posY)
        MAIN_FIGURE_LIST.append(triangle)

    elif option == 1:
        figSize = float(input("Insert the size of the edge of the square: "))
        posX = float(input("Insert the center position of the figure in X: "))
        posY = float(input("Insert the center position of the figure in Y: "))

        square = FigureConstructor.createSquare(figSize, posX, posY)
        MAIN_FIGURE_LIST.append(square)

    elif option == 2:
        figSize = float(input("Insert the size of the edge of the hexagon: "))
        posX = float(input("Insert the center position of the figure in X: "))
        posY = float(input("Insert the center position of the figure in Y: "))

        hexagon = FigureConstructor.createHexagon(figSize, posX, posY)
        MAIN_FIGURE_LIST.append(hexagon)

    glutPostRedisplay()

    return 0


# R2, R3
def FreeDrawMenu(option: int) -> int:
    """

    Function that handles the menu for the creation of the irregular geometric figures.

    Args:
        option (int): Option selected by the user.

    Returns:
        int: 0 when the function is called.
    """
    global QTD_CLICKS
    os.system("cls")
    print("Free Draw Mode")
    if option == 0:
        MOUSE_POINTS.clear()
        print("Selecting Points")
        QTD_CLICKS = int(input("How many points would you like to add? "))
        MOUSE_POINTS.clear()
        print("Press the middle button to cancel the placement\n")

    elif option == 1:
        print("Inserting Points Manually")
        points = []
        while True:
            posX = float(input("Insert the X for the point: "))
            posY = float(input("Insert the Y for the point: "))

            points.append(Point(posX, posY))

            continuar = input("Deseja continuar? [S/N]")
            if continuar.lower() == "s":
                pass
            else:
                break

        irregular = FigureConstructor.createIrregular(points)
        MAIN_FIGURE_LIST.append(irregular)

    return 0


# R6
def EditorMenu(option: int) -> int:
    """
    Function that handles the menu for the edition or removal of the figures.

    Args:
        option (int): Option selected by the user.

    Raises:
        ValueError: Error when the figure is not found.

    Returns:
        int: 0 when the function is called.
    """
    os.system("cls")
    print("Edit/Delete Figures\n")
    for figure in MAIN_FIGURE_LIST:
        print(figure)

    id = int(input("Select the ID of the figure you want to Edit/Delete "))
    idx = find_figure_idx(id)
    if idx != -1:
        figure = MAIN_FIGURE_LIST[idx]
    else:
        raise ValueError("ID not found!")

    os.system("cls")
    print(f"Selected: {figure}")

    if option == 0:
        posX = float(input("X coordinate to translate: "))
        posY = float(input("Y coordinate to translate: "))
        figure.figPos = (posX, posY, 0)
    elif option == 1:
        scaleX = float(input("X proportion to scale: "))
        scaleY = float(input("Y proportion to scale: "))
        figure.figScale = (scaleX, scaleY, 1)
    elif option == 2:
        axis = input("Select the Reflection Axis [X|Y]: ")
        figReflex = np.identity(4)
        if axis.lower() == "x":
            figReflex[1][1] = -1
            figure.figReflex = figReflex
        elif axis.lower() == "y":
            figReflex[0][0] = -1
            figure.figReflex = figReflex
        else:
            print("Invalid Option")
    elif option == 3:
        angle = float(input("Rotation Angle: "))
        figure.figRot = angle
    elif option == 4:
        axis = input("Select the axis for shearing [X|Y]: ")
        shear_value = float(input("Value for shearing: "))
        figShear = np.identity(4)

        if axis.lower() == "x":
            figShear[1][0] = shear_value
            figure.figShear = figShear
        elif axis.lower() == "y":
            figShear[0][1] = shear_value
            figure.figShear = figShear
        else:
            print("Invalid Option!")
    elif option == 5:
        MAIN_FIGURE_LIST.pop(idx)
        print(f"Figure {id} removed!")

    glutPostRedisplay()

    return 0


def MainMenu(**kwargs) -> int:
    """
    Wrapper function for the main menu.

    Returns:
        int: 0 when the function is called.
    """
    return 0


# R11
def CreateMenu() -> None:
    """
    Function that handles the creation of the floating menu, that contains all other menus.

    """
    menu_free_draw = glutCreateMenu(FreeDrawMenu)
    glutAddMenuEntry("Select Points", 0)
    glutAddMenuEntry("Add Points Manually", 1)

    menu_locked_draw = glutCreateMenu(LockedFigureMenu)
    glutAddMenuEntry("Triangle", 0)
    glutAddMenuEntry("Square", 1)
    glutAddMenuEntry("Hexagon", 2)

    menu_editor = glutCreateMenu(EditorMenu)
    glutAddMenuEntry("Translate", 0)
    glutAddMenuEntry("Scale", 1)
    glutAddMenuEntry("Reflect", 2)
    glutAddMenuEntry("Rotate", 3)
    glutAddMenuEntry("Shear", 4)
    glutAddMenuEntry("Delete Figure", 5)

    menu = glutCreateMenu(MainMenu)
    glutAddSubMenu("Free Drawing", menu_free_draw)
    glutAddSubMenu("Locked Figures", menu_locked_draw)
    glutAddSubMenu("Edit/Delete Figures", menu_editor)

    glutAttachMenu(GLUT_RIGHT_BUTTON)


def MouseManager(button: int, state: int, x: int, y: int) -> None:
    """
    Function that handles the mouse events.

    Args:
        button (int): Button pressed.
        state (int): State of the button.
        x (int): X coordinate of the mouse.
        y (int): Y coordinate of the mouse.
    """
    global QTD_CLICKS

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            CreateMenu()

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            posX = (x - WINDOW_WIDTH / 2) / 250
            posY = -(y - WINDOW_HEIGHT / 2) / 250
            print(Point(posX, posY))
            if QTD_CLICKS:
                MOUSE_POINTS.append(Point(posX, posY))
            if (len(MOUSE_POINTS) == QTD_CLICKS) and bool(QTD_CLICKS):
                irregular = FigureConstructor.createIrregular(MOUSE_POINTS.copy())
                MAIN_FIGURE_LIST.append(irregular)
                print(f"Inserted: {MAIN_FIGURE_LIST[-1]}")
                MOUSE_POINTS.clear()
                QTD_CLICKS = 0

    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            QTD_CLICKS = 0
            if len(MOUSE_POINTS) and not QTD_CLICKS:
                print("Points selection canceled!")
                MOUSE_POINTS.clear()


def main(*args, **kwargs):
    """
    Main funtion of the program.
    """
    os.system("cls")
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_DEPTH | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("OpenGL - Figures")

    glutDisplayFunc(display)
    glutMouseFunc(MouseManager)

    glutMainLoop()


if __name__ == "__main__":
    main()
