
import datetime
import os
import subprocess
from pathlib import Path
import json
from controller import Supervisor, AnsiCodes, Node
import time
import math
import cv2
import numpy as np


def uprint(*text):
    with open(str(current_working_directory) + "\Marathon_log.txt",'a') as f:
        print(*text, file = f)
    print(*text)


def is_out_of_distance(image, robot_coords, grey_range=(100, 200)):
    pixel_value = image[int(robot_coords[0]), int(robot_coords[1])]
    return grey_range[0] <= pixel_value <= grey_range[1]


def main():
    image = cv2.imread('map_marathon.png', cv2.IMREAD_GRAYSCALE)
    supervisor = Supervisor()
    time_step = int(supervisor.getBasicTimeStep())

    robot_translation = supervisor.getFromDef('BLUE_PLAYER_1').getField('translation')
    robot_rotation = supervisor.getFromDef('BLUE_PLAYER_1').getField('rotation')

    current_working_directory = Path.cwd()

    os.chdir(current_working_directory.parent/'Robofest_TEAM')

    role01 = 'marathon'
    second_pressed_button = '4'
    initial_coord = '[0.0, 0.0, 0.0]'
    robot_color = 'blue'
    robot_number = '1'
    team_id = '-1'          # value -1 means game will be playing without Game Controller
    port01 = '7001'
    params_name = "Marathon_params.json"
    filename01 = "output" + f"{port01}"+ ".txt"
    with open(filename01, "w") as f01:
        print(datetime.datetime.now(), file = f01)
        p01 = subprocess.Popen(['python', 'main_pb.py', port01, team_id, robot_color, robot_number, role01, second_pressed_button, initial_coord, params_name], stderr=f01)

    distance_count = 0
    robot_coords = robot_translation.getSFVec3f()
    robot_angle = robot_rotation.getSFRotation()
    robot_coords_old = np.array([robot_coords[0], robot_coords[1]])
    robot_coords_np = robot_coords_old
    delta = 0
    delta_result = 0
    respawn_points = [[delta, robot_coords, robot_angle]]
    respawn_result = robot_coords
    respawn_result_angle = robot_angle
    out_flag = 201
    while supervisor.step(time_step) != -1:
        if out_flag < 200:
            out_flag += 1
            continue
        elif out_flag == 200:
            out_flag += 1
            delta = delta_result
            robot_translation.setSFVec3f(respawn_result)
            robot_rotation.setSFRotation(respawn_result_angle)
            robot_coords_old = np.array([respawn_result[0], respawn_result[1]])

        distance_count += 1
        robot_coords = robot_translation.getSFVec3f()
        robot_angle = robot_rotation.getSFRotation()
        robot_coords_np = np.array([robot_coords[0], robot_coords[1]])
        if distance_count % 1000 == 0:
            delta += np.linalg.norm(robot_coords_np - robot_coords_old)
            robot_coords_old = robot_coords_np
            print(delta)
            respawn_points.append([delta, robot_coords, robot_angle])
            for respawn_point in respawn_points:
                if delta - respawn_point[0] >= 5:
                    respawn_result = respawn_point[1]
                    respawn_result_angle = respawn_point[2]
                    # respawn_points.remove(respawn_point)
                    delta_result = respawn_point[0]
                else:
                    break

        if is_out_of_distance(image, np.abs(np.round(100*(robot_coords_np)))):
            out_flag = 0


    p01.terminate()
    supervisor.simulationReset()
    supervisor.step(time_step)
    supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
    #supervisor.worldReload()

if __name__ == '__main__':
    main()