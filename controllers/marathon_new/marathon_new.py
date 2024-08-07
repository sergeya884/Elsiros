import datetime
import os
import subprocess
from pathlib import Path
import json
from controller import Supervisor, AnsiCodes, Node
import time
import math

supervisor = Supervisor()
time_step = int(supervisor.getBasicTimeStep())

robot_translation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('translation'),
                     supervisor.getFromDef('RED_PLAYER_2').getField('translation'),
                     supervisor.getFromDef('GREEN_PLAYER_3').getField('translation')]

robot_rotation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('rotation'),
                  supervisor.getFromDef('RED_PLAYER_2').getField('rotation'),
                  supervisor.getFromDef('GREEN_PLAYER_3').getField('rotation')]

current_working_directory = Path.cwd()


def compute_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def uprint(*text):
    with open(str(current_working_directory) + "\Marathon_log.txt",'a') as f:
        print(*text, file=f)
    print(*text)

os.chdir(current_working_directory.parent/'Robofest_TEAM')

quantity_robots = 3
role01 = 'marathon'
second_pressed_button = '4'
initial_coord = '[0.0, 0.0, 0.0]'
robot_color = ['blue', 'red', 'green']
team_id = '-1'          # value -1 means game will be playing without Game Controller

ports, robot_number, parameter_names, filenames = [], [], [], []
p01 = [_ for _ in range(quantity_robots)]
for i in range(1, quantity_robots+1):
    robot_number.append(str(i))

    port = str(7000 + i)
    ports.append(port)

    params_name = "Marathon_params" + str(i) + ".json"
    parameter_names.append(params_name)

    filename = "output_marathon" + f"{port}" + ".txt"
    filenames.append(filename)

j = 0   # запускаем первого робота
with open(filenames[0], "w") as f01:
    p01[j] = subprocess.Popen(['python', 'main_pb.py', ports[j], team_id, robot_color[j], robot_number[j], role01,
                               second_pressed_button, initial_coord, parameter_names[j]], stderr=f01)
    t0 = time.time()

distance_count = 0
robot_sequence = [j+1]
flag_one_step_time = True
while supervisor.step(time_step) != -1:
    distance_count += 1
    t1 = time.time()
    if j < quantity_robots-1 and abs(t1 - t0) >= 20:     # запускаем остальных роботов
        j += 1
        robot_sequence.append(j+1)
        with open(filenames[j], "w") as f01:
            p01[j] = subprocess.Popen(
                ['python', 'main_pb.py', ports[j], team_id, robot_color[j], robot_number[j], role01,
                 second_pressed_button, initial_coord, parameter_names[j]], stderr=f01)
            t0 = time.time()
            robot_translation[j].setSFVec3f([5.0, 0.75, 0.288354])     # в начало координат
            robot_rotation[j].setSFRotation([1, 0, 0, 0])              # вектор напрпавления

    if len(robot_sequence) > 1 and distance_count % 1000 == 0:
        for i in range(len(robot_sequence)):
            for j in range(i + 1, len(robot_sequence)):
                distance = compute_distance(robot_translation[i].getSFVec3f(), robot_translation[j].getSFVec3f())

                if distance < 0.55:
                    print(f'Расстояние между роботами {i+1} и {j+1}: {distance}')
                    print('before:', robot_sequence)
                    index1 = robot_sequence.index(i+1)
                    index2 = robot_sequence.index(j+1)
                    robot_sequence[index1], robot_sequence[index2] = robot_sequence[index2], robot_sequence[index1]
                    print('after:', robot_sequence)
                    distance_count = 0
for i in range(quantity_robots):
    p01[i].terminate()

supervisor.simulationReset()
supervisor.step(time_step)
supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
#supervisor.worldReload()