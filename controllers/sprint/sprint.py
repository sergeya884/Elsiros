import datetime
import os
import subprocess
from pathlib import Path
import json
from controller import Supervisor, AnsiCodes, Node

# import sys
# sys.path.append('C:\Elsiros\controllers\Robofest_TEAM\Soccer\Motion')
# from class_Motion import Motion1
# Path1 = os.chdir('../Soccer/Motion')
# print(sys.path)
# print(Path.cwd())
# from class_Motion import Motion1 


# C:\Elsiros\controllers\Robofest_TEAM\Soccer\Motion\class_Motion.py

# C:\Elsiros\controllers\sprint\sprint.py

# motion = Motion1()
supervisor = Supervisor()
time_step = int(supervisor.getBasicTimeStep())

robot_translation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('translation'),
                     supervisor.getFromDef('RED_PLAYER_2').getField('translation'),
                     supervisor.getFromDef('GREEN_PLAYER_3').getField('translation'),
                     supervisor.getFromDef('BLACK_PLAYER_4').getField('translation'),
                     supervisor.getFromDef('PURPLE_PLAYER_5').getField('translation'),
                     supervisor.getFromDef('ORANGE_PLAYER_6').getField('translation'),
                     supervisor.getFromDef('BROWN_PLAYER_7').getField('translation'),
                     supervisor.getFromDef('GREY_PLAYER_8').getField('translation'),
                     supervisor.getFromDef('PINK_PLAYER_9').getField('translation'),
                     supervisor.getFromDef('TURQUOISE_PLAYER_10').getField('translation')]

robot_rotation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('rotation'),
                  supervisor.getFromDef('RED_PLAYER_2').getField('rotation'),
                  supervisor.getFromDef('GREEN_PLAYER_3').getField('rotation'),
                  supervisor.getFromDef('BLACK_PLAYER_4').getField('rotation'),
                  supervisor.getFromDef('PURPLE_PLAYER_5').getField('rotation'),
                  supervisor.getFromDef('ORANGE_PLAYER_6').getField('rotation'),
                  supervisor.getFromDef('BROWN_PLAYER_7').getField('rotation'),
                  supervisor.getFromDef('GREY_PLAYER_8').getField('rotation'),
                  supervisor.getFromDef('PINK_PLAYER_9').getField('rotation'),
                  supervisor.getFromDef('TURQUOISE_PLAYER_10').getField('rotation')]


def uprint(*text):
    with open(str(current_working_directory) + "\Sprint_log.txt", 'a') as f:
        print(*text, file=f)
    print(*text)


def out_text_red(text):
    start = "\033[1;31m"
    end = "\033[0;0m"
    uprint(start + str(datetime.datetime.now()) + text + end)


def out_text_green(text):
    start = "\033[1;32m"
    end = "\033[0;0m"
    uprint(start + str(datetime.datetime.now()) + text + end)


current_working_directory = Path.cwd()

os.chdir(current_working_directory.parent/'Robofest_TEAM')

quantity_robots = 3
role01 = 'sprint' 
second_pressed_button = '4'
robot_color = ['blue', 'red', 'green', 'black', 'purple', 'orange', 'brown', 'grey', 'pink', 'turquoise']
team_id = '-1'          # value -1 means game will be playing without Game Controller
robot_number, ports, parameter_names, initial_coords = [], [], [], []

for i in range(1, quantity_robots+1):
    robot_number.append(str(i))

    port = str(7000 + i)
    ports.append(port)

    coord = str([0.0, 1.05*(i-1), 0.288354])
    initial_coords.append(coord)

    params_name = "Sprint_params" + str(i) + ".json"
    parameter_names.append(params_name)

p01 = [_ for _ in range(quantity_robots)]
p01_flag = [True for _ in range(quantity_robots)]

for i in range(quantity_robots):
    filename01 = "output" + f"{ports[i]}" + ".txt"
    with open(filename01, "w") as f01:
        print(datetime.datetime.now(), file=f01)
        p01[i] = subprocess.Popen(['python', 'main_pb.py', ports[i], team_id, robot_color[i], robot_number[i],
                                   role01, second_pressed_button, initial_coords[i], parameter_names[i]], stderr=f01)

distance_count = 0

print("\033[1;34m" + 'start_time: ' + str(datetime.datetime.now()) + "\033[0;0m")

while supervisor.step(time_step) != -1:
    distance_count += 1
    y_coordinate = []
    for i in range(quantity_robots):
        y_coordinate.append(robot_translation[i].getSFVec3f()[1])
        edge_1 = -0.5 + 1.05 * i
        edge_2 = 0.5 + 1.05 * i
        if y_coordinate[i] > edge_2 or y_coordinate[i] < edge_1 or robot_translation[i].getSFVec3f()[0] < -0.05:
            text = ' robot ' + str(i+1) + ': distance was NOT finished due to failure'
            out_text_red(text)
            robot_translation[i].setSFVec3f([0.0, 1.05*i, 0.288354])   # в начало координат
            robot_rotation[i].setSFRotation([1, 0, 0, 0])       # вектор напрпавления

        if robot_translation[i].getSFVec3f()[0] > 3.05 and p01_flag[i]:
            text = ' robot ' + str(i+1) + ' distance was finished within timesteps: ' + str(distance_count)
            out_text_green(text)
            p01[i].terminate()
            p01_flag[i] = False  # чтобы не писать больше одного раза

for i in range(len(p01)):
    p01[i].terminate()

supervisor.simulationReset()
supervisor.step(time_step)
supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
#supervisor.worldReload()