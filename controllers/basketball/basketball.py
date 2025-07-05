import datetime
import os
import subprocess
from pathlib import Path
import json
from controller import Supervisor, AnsiCodes, Node
current_working_directory = Path.cwd()
def uprint(*text):
    with open(str(current_working_directory) + "\Basketball_log.txt", 'a') as f:
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


def is_point_in_cylinder(point, cylinder_center=(0, 1.93, 0.45), cylinder_height=0.08, cylinder_radius = 0.09):
    """
    Проверяет, находится ли точка внутри цилиндра.

    Параметры:
    - cylinder_center: tuple (x, y, z) - координаты центра цилиндра
    - cylinder_height: float - высота цилиндра (вдоль оси Z)
    - cylinder_radius: float - радиус цилиндра
    - point: tuple (x, y, z) - координаты проверяемой точки

    Возвращает:
    - bool: True, если точка внутри цилиндра, иначе False
    """
    # Разделяем координаты центра цилиндра и точки
    cx, cy, cz = cylinder_center
    px, py, pz = point

    # Проверяем, находится ли точка в пределах высоты цилиндра
    half_height = cylinder_height / 2
    z_min = cz - half_height
    z_max = cz + half_height

    if not (z_min <= pz <= z_max):
        return False

    # Проверяем, находится ли точка в пределах радиуса в плоскости XY
    distance_squared = (px - cx) ** 2 + (py - cy) ** 2

    return distance_squared <= cylinder_radius ** 2

def main():
    quantity_robots = 1

    supervisor = Supervisor()
    time_step = int(supervisor.getBasicTimeStep())

    robot_translation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('translation')]

    robot_rotation = [supervisor.getFromDef('BLUE_PLAYER_1').getField('rotation')]

    ball_translation = supervisor.getFromDef('BALL').getField('translation')

    os.chdir(current_working_directory.parent/'Robofest_TEAM')

    role01 = 'basketball'
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

        params_name = "basketball" + str(i) + ".json"
        parameter_names.append(params_name)

    p01 = [_ for _ in range(quantity_robots)]
    p01_flag = [True for _ in range(quantity_robots)]

    for i in range(quantity_robots):
        filename01 = "output_basketball" + f"{ports[i]}" + ".txt"
        with open(filename01, "w") as f01:
            print(datetime.datetime.now(), file=f01)
            p01[i] = subprocess.Popen(['python', 'main_pb.py', ports[i], team_id, robot_color[i], robot_number[i],
                                       role01, second_pressed_button, initial_coords[0], parameter_names[i], 'roki2'], stderr=f01)


    print("\033[1;34m" + 'start_time: ' + str(datetime.datetime.now()) + "\033[0;0m")

    time_count = 0
    max_time = 20 #sec
    while supervisor.step(time_step) != -1:
        # Подготовка к броску
        if time_count == 1100:
            time_count +=1
            ball_translation.setSFVec3f([0.01, 0.79, 0.4])

        elif time_count > 1200:
            # Проверяем попадание
            ball_coords = ball_translation.getSFVec3f()
            if is_point_in_cylinder(point=ball_coords):
                out_text_green('Five-point shot!')
                break
            #Если мяч упал на землю
            elif ball_coords[2] <= 0.05:
                out_text_red('Missed')
                break

        # Проверка на максимальное время
        if time_count >= (max_time//time_step*1000):
            break
        time_count += 1



    for i in range(quantity_robots):
        p01[i].terminate()

    supervisor.simulationReset()
    supervisor.step(time_step)
    supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
    #supervisor.worldReload()

if __name__ == '__main__':
    main()