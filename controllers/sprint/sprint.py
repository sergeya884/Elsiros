import datetime
import os
import subprocess
from pathlib import Path
import json
from controller import Supervisor, AnsiCodes, Node

is_pen = False
center_of_rows = (0.0, 1.05, 2.1)

# C:\Elsiros\controllers\Robofest_TEAM\Soccer\Motion\class_Motion.py

# C:\Elsiros\controllers\sprint\sprint.py

# motion = Motion1()
supervisor = Supervisor()
time_step = int(supervisor.getBasicTimeStep())
if is_pen:
    pen1 = supervisor.getFromDef('PEN_1')

    pen1_pen = supervisor.getDevice('pen')
    pen1_translation = pen1.getField('translation')
    pen1_leadSize = pen1.getField('leadSize')
    pen1_pen.write(True)
    pen1_translation.setSFVec3f([1.0, 0.0, 0.001])

texture_points = []
texture_points.append(supervisor.getFromDef('CUST_TEXTURE_1').getField('POINTS'))
texture_points.append(supervisor.getFromDef('CUST_TEXTURE_2').getField('POINTS'))
texture_points.append(supervisor.getFromDef('CUST_TEXTURE_3').getField('POINTS'))


robot_translation = []
robot_translation.append(supervisor.getFromDef('BLUE_PLAYER_1').getField('translation'))
robot_translation.append(supervisor.getFromDef('RED_PLAYER_2').getField('translation'))
robot_translation.append(supervisor.getFromDef('GREAN_PLAYER_3').getField('translation'))

robot_rotation = []
robot_rotation.append(supervisor.getFromDef('BLUE_PLAYER_1').getField('rotation'))
robot_rotation.append(supervisor.getFromDef('RED_PLAYER_2').getField('rotation'))
robot_rotation.append(supervisor.getFromDef('GREAN_PLAYER_3').getField('rotation'))


def out_text_red(text):
    start = "\033[1;31m"
    end = "\033[0;0m"
    print(start + str(datetime.datetime.now()) + text + end)

def out_text_grean(text):
    start = "\033[1;32m"
    end = "\033[0;0m"
    print(start + str(datetime.datetime.now()) + text + end)

current_working_directory = Path.cwd()


def uprint(*text):
    with open(str(current_working_directory) + "\Sprint_log.txt",'a') as f:
        print(*text, file = f)
    print(*text)


os.chdir(current_working_directory.parent/'Robofest_TEAM')

role01 = 'sprint' 
second_pressed_button = '4'
initial_coord = ['[0.0, 0.0, 0.288354]', '[0.0, 1.05, 0.288354]', '[0.0, 2.1, 0.288354]']
robot_color = ['blue', 'red', 'grean']
robot_number = ['1', '2', '3']
team_id = '-1'          # value -1 means game will be playing without Game Controller
port01 = ['7001', '7002', '7003']
params_name = ["Sprint_params1.json", "Sprint_params2.json", "Sprint_params3.json"]

p01 = [_ for _ in range(len(robot_translation))]
p01_flag = [True for _ in range(len(robot_translation))]
for i in range((len(robot_translation))):
    filename01 = "output" + f"{port01[i]}"+ ".txt"
    with open(filename01, "w") as f01:
        print(datetime.datetime.now(), file = f01)
        # p01 = subprocess.Popen(['python', 'main_pb.py', port01[i], team_id, robot_color[i], robot_number[i], role01, second_pressed_button, initial_coord[i], params_name[i]], stderr=f01)
        p01[i] = subprocess.Popen(['python', 'main_pb.py', port01[i], team_id, robot_color[i], robot_number[i], role01, second_pressed_button, initial_coord[i], params_name[i]], stderr=f01)

distance_count = 0


def clear_row():
    print('clear')
    pen1_translation.setSFVec3f([1.5, 0.0, 0.002])

list_coord = []
for coord_str in initial_coord:
    coord_str = coord_str.strip('[]')
    coord_parts = coord_str.split(',')
    coord = [float(part.strip()) for part in coord_parts]
    list_coord.append(coord)

print("\033[1;34m" + 'start_time: ' + str(datetime.datetime.now()) + "\033[0;0m")
if is_pen:
    color = 0xe0ffff
    ink_intensity = 0.8
    _ = 0
while supervisor.step(time_step) != -1:
    if is_pen:
        _ += 1
        if _ == 1:
            pen1_pen.setInkColor(0x006411, 1.0)
            pen1_leadSize.setSFFloat(2.0)
        if _ < 7:
            pen1_translation.setSFVec3f([1.5, 0.0, 0.002])
            continue

        pen1_leadSize.setSFFloat(0.1)
        pen1_pen.setInkColor(color, ink_intensity)
        pen1_translation.setSFVec3f([-0.1 + robot_translation[0].getSFVec3f()[0], 0.0, 0.002])

    distance_count += 1
    y_coordinate = []

    for i in range(len(robot_translation)):
        # Отрисовка дорожки за роботом
        robot_coord_x = robot_translation[i].getSFVec3f()[0] - 0.1
        if robot_coord_x <= 3.0 and p01_flag[i]:
            texture_points[i].setMFVec3f(1, (robot_coord_x, center_of_rows[i]-0.5, 0.001))
            texture_points[i].setMFVec3f(2, (robot_coord_x, center_of_rows[i]+0.5, 0.001))

        y_coordinate.append(robot_translation[i].getSFVec3f()[1])
        edge_1 = -0.5 + 1.05 * i
        edge_2 = 0.5 + 1.05 * i
        if y_coordinate[i] > edge_2 or y_coordinate[i] < edge_1 or robot_translation[i].getSFVec3f()[0] < -0.05:
            text = ' robot ' + str(i+1) + ': distance was NOT finished due to failure'
            out_text_red(text)
            robot_translation[i].setSFVec3f(list_coord[i])   # в начало координат
            if i == 0:
                _ = 0
            robot_rotation[i].setSFRotation([1, 0, 0, 0])       # вектор напрпавления

        if robot_translation[i].getSFVec3f()[0] > 3.05 and p01_flag[i]:
            texture_points[i].setMFVec3f(1, (3.0, center_of_rows[i]-0.5, 0.001))
            texture_points[i].setMFVec3f(2, (3.0, center_of_rows[i]+0.5, 0.001))
            text = ' robot ' + str(i+1) + ' distance was finished within timesteps: ' + str(distance_count)
            out_text_grean(text)
            p01[i].terminate()
            p01_flag[i] = False  # чтобы не писать больше одного раза

for i in range(len(p01)):
    p01[i].terminate()

supervisor.simulationReset()
supervisor.step(time_step)
supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
#supervisor.worldReload()