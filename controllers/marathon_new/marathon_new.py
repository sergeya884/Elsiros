
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

current_working_directory = Path.cwd()

def out_text_green(text):
    start = "\033[1;32m"
    end = "\033[0;0m"
    print(start + str(datetime.datetime.now()) + text + end)

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

    robot_translation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('translation'),
                         supervisor.getFromDef('RED_PLAYER_2').getField('translation'),
                         supervisor.getFromDef('GREEN_PLAYER_3').getField('translation')]

    robot_rotation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('rotation'),
                      supervisor.getFromDef('RED_PLAYER_2').getField('rotation'),
                      supervisor.getFromDef('GREEN_PLAYER_3').getField('rotation')]


    # robot_translation = supervisor.getFromDef('BLUE_PLAYER_1').getField('translation')
    # robot_rotation = supervisor.getFromDef('BLUE_PLAYER_1').getField('rotation')

    current_working_directory = Path.cwd()

    os.chdir(current_working_directory.parent/'Robofest_TEAM')

    quantity_robots = 3
    role01 = 'marathon'
    second_pressed_button = '4'
    initial_coord = '[0.0, 0.0, 0.0]'
    robot_color = ['blue', 'red', 'green']
    ports, robot_number, parameter_names, filenames = [], [], [], []
    team_id = '-1'          # value -1 means game will be playing without Game Controller
    p01 = [_ for _ in range(quantity_robots)]
    for i in range(1, quantity_robots + 1):
        robot_number.append(str(i))

        port = str(7000 + i)
        ports.append(port)

        params_name = "Marathon_params" + str(i) + ".json"
        parameter_names.append(params_name)

        filename = "output_marathon" + f"{port}" + ".txt"
        filenames.append(filename)
    # robot_color = 'blue'
    # robot_number = '1'
    # port01 = '7001'
    # params_name = "Marathon_params.json"
    # filename01 = "output" + f"{port01}"+ ".txt"
    robots_start_time = []
    j = 0  # запускаем первого робота
    with open(filenames[0], "w") as f01:
        p01[j] = subprocess.Popen(['python', 'main_pb.py', ports[j], team_id, robot_color[j], robot_number[j], role01,
                                   second_pressed_button, initial_coord, parameter_names[j]], stderr=f01)
        t0 = time.time()
        robots_start_time.append(t0)

    distance_count = 0
    robot_sequence = [j + 1]

    start_coords = [5, 17.6, 0.3]
    start_rotation = [1, 0, 0, 0]
    finish_coords = [4, 17.6]
    robot_coords = [robot_translation[0].getSFVec3f()] * quantity_robots
    robot_angle = [robot_rotation[0].getSFRotation()] * quantity_robots
    robot_coords_old = [np.array([robot_coords[0][0], robot_coords[0][1]])] * quantity_robots
    robot_coords_np = [np.array([robot_coords[0][0], robot_coords[0][1]])] * quantity_robots
    delta = [0] * quantity_robots
    delta_result = delta
    respawn_points = [[[delta[0], robot_coords[0], robot_angle[0]]]] * quantity_robots
    respawn_result = robot_coords
    respawn_result_angle = robot_angle
    out_flag = [201] * quantity_robots
    end_flag = [False] * quantity_robots

    while supervisor.step(time_step) != -1:
        distance_count += 1
        if j < quantity_robots - 1:
            t1 = time.time()
            if abs(t1 - t0) >= 20:  # запускаем остальных роботов
                j += 1
                robot_sequence.append(j + 1)
                with open(filenames[j], "w") as f01:
                    p01[j] = subprocess.Popen(
                        ['python', 'main_pb.py', ports[j], team_id, robot_color[j], robot_number[j], role01,
                         second_pressed_button, initial_coord, parameter_names[j]], stderr=f01)
                    t0 = time.time()
                    robot_translation[j].setSFVec3f(start_coords)  # в начало координат
                    robot_rotation[j].setSFRotation(start_rotation)
                    robots_start_time.append(t0)

        for robot in range(j+1):
            if not end_flag[robot]:
                if out_flag[robot] < 200:
                    out_flag[robot] += 1
                    continue
                elif out_flag[robot] == 200:
                    out_flag[robot] += 1
                    print('delta0')
                    delta[robot] = delta_result[robot]
                    robot_translation[robot].setSFVec3f(respawn_result[robot])
                    robot_rotation[robot].setSFRotation(respawn_result_angle[robot])
                    robot_coords_old[robot] = np.array([respawn_result[robot][0], respawn_result[robot][1]])

                robot_coords[robot] = robot_translation[robot].getSFVec3f()
                #print(robot_coords)
                robot_angle[robot] = robot_rotation[robot].getSFRotation()
                robot_coords_np[robot] = np.array([robot_coords[robot][0], robot_coords[robot][1]])
                if distance_count % 500 == 0:
                    delta[robot] += np.linalg.norm(robot_coords_np[robot] - robot_coords_old[robot])
                    print(delta[robot])
                    robot_coords_old[robot] = robot_coords_np[robot]
                    respawn_points[robot].append([[delta[robot], robot_coords[robot], robot_angle[robot]]])
                    for respawn_point in respawn_points[robot]:
                        if delta[robot] - respawn_point[0] >= 5:
                            respawn_result[robot] = respawn_point[1]
                            respawn_result_angle[robot] = respawn_point[2]
                            # respawn_points.remove(respawn_point)
                            delta_result[robot] = respawn_point[0]
                        else:
                            break

                # if is_out_of_distance(image, np.abs(np.round(100*(robot_coords_np[robot])))):
                #     out_flag[robot] = 0

                # # Проверка на конец дистанции
                # if np.linalg.norm(robot_coords_np - finish_coords) < 0.5 and delta > 50:
                #     text = ' robot distance was finished within timesteps: ' + str(distance_count)
                #     out_text_green(text)
                #     p01.terminate()
                #     robot_translation.setSFVec3f([1, 1, 0.3])
                #     end_flag = True





    p01.terminate()
    supervisor.simulationReset()
    supervisor.step(time_step)
    supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
    #supervisor.worldReload()

if __name__ == '__main__':
    main()