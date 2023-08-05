import numpy as np
import pygame
from math import *

WINDOW_SIZE = 800
running = True
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()

projection_matrix = np.array([[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 0]])


def prospective(vertex: list[int, int, int], length):
    x, y, z = vertex
    new_x = (length * x)/(length + z)
    new_y = (length * vertex[1])/(length + z)
    return[new_x, new_y]


def line(index1, index2, points):
    pygame.draw.line(screen, (255, 0, 255),(points[index1][0], points[index1][1]), (points[index2][0], points[index2][1]), 5)


angle_x = angle_y = angle_z = 0
focal_length = 5  # a length value of 1 breaks, only used for weak perspective
scale = 100
scale_perspective = 125
perspective = False
cubeOrTriangle = False
rotate = False
while running:
    if cubeOrTriangle:
        cube_points = [n for n in range(8)]
        cube_points[0] = np.array([[-1], [-1], [1]])
        cube_points[1] = np.array([[1], [-1], [1]])
        cube_points[2] = np.array([[1], [1], [1]])
        cube_points[3] = np.array([[-1], [1], [1]])
        cube_points[4] = np.array([[-1], [-1], [-1]])
        cube_points[5] = np.array([[1], [-1], [-1]])
        cube_points[6] = np.array([[1], [1], [-1]])
        cube_points[7] = np.array([[-1], [1], [-1]])
    else:
        cube_points = [n for n in range(5)]
        cube_points[0] = np.array([[1], [1], [1]])
        cube_points[1] = np.array([[-1], [1], [1]])
        cube_points[2] = np.array([[1], [1], [-1]])
        cube_points[3] = np.array([[-1], [1], [-1]])
        cube_points[4] = np.array([[0], [-1], [0]])

    clock.tick(60)
    screen.fill((0, 0, 0))

    # Rotation Matrices that are used to calculate the new spots of each point
    rotation_x = np.array([[1, 0, 0],
                           [0, cos(angle_x), -sin(angle_x)],
                           [0, sin(angle_x), cos(angle_x)]])

    rotation_y = np.array([[cos(angle_y), 0, sin(angle_y)],
                           [0, 1, 0],
                           [-sin(angle_y), 0, cos(angle_y)]])

    rotation_z = np.array([[cos(angle_z), -sin(angle_z), 0],
                           [sin(angle_z), cos(angle_z), 0],
                           [0, 0, 1]])

    points = [0 for _ in range(len(cube_points))]
    i = 0

    for point in cube_points:
        rotate_x = np.dot(rotation_x, point)
        rotate_y = np.dot(rotation_y, rotate_x)
        rotate_z = np.dot(rotation_z, rotate_y)
        point_2d = np.dot(projection_matrix, rotate_z)

        # Some math changes if the wire frame is in weak perspective or not
        if perspective:
            new_arr = prospective([point_2d[0], point_2d[1], rotate_z[2]], focal_length)

            x = (new_arr[0].item(0) * scale_perspective) + WINDOW_SIZE / 2
            y = (new_arr[1].item(0) * scale_perspective) + WINDOW_SIZE / 2
        else:
            x = (point_2d[0][0] * scale) + WINDOW_SIZE / 2
            y = (point_2d[1][0] * scale) + WINDOW_SIZE / 2

        # Adds the new calculated points to an array which will be iterated over and lines drawn between the points
        # to construct the wireframe
        points[i] = (x, y)

        i += 1

        # pygame.draw.circle(screen, (255, 0, 255), (x, y), 3)

    if cubeOrTriangle:
        line(0, 1, points)
        line(0, 3, points)
        line(0, 4, points)
        line(1, 2, points)
        line(1, 5, points)
        line(2, 6, points)
        line(2, 3, points)
        line(3, 7, points)
        line(4, 5, points)
        line(4, 7, points)
        line(6, 5, points)
        line(6, 7, points)
    else:
        line(0, 1, points)
        line(0, 2, points)
        line(2, 3, points)
        line(1, 3, points)
        line(0, 4, points)
        line(1, 4, points)
        line(2, 4, points)
        line(3, 4, points)

    if perspective:  # Draws a circle as an indicator that weak perspective is being done
        pygame.draw.circle(screen, (255, 0, 255), (WINDOW_SIZE / 2, 10), 10)

    pygame.display.update()

    events = pygame.event.get()

    if rotate:  # Only allows rotation once it is manually started
        angle_y += .01
        angle_x += .01
        angle_z += .01

    # Key events
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                perspective = not perspective
            if event.key == pygame.K_s:
                rotate = True
            if event.key == pygame.K_w:
                cubeOrTriangle = not cubeOrTriangle


pygame.quit()
