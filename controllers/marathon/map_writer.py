import cv2
import numpy as np
import math
import json

start_coords = [2, 8, 3.14]
map_size = (1600, 1600)
thickness = 100
gradient_step = 25
map_road_thickness = 7
imshow_size = 5


def write_line(gradient_img, map_img, img_background, length, direction, points):
    # direction: 0: v ; 1: < ; 2: ^ ; 3: > ;
    start_color = len(points) - 1

    x_real, y_real = points[start_color][0], points[start_color][1]
    x_add, y_add = int(x_real * 100), int(y_real * 100)
    current_color = start_color + 1
    x = x_add
    y = y_add
    length_px = int(length*100)
    if direction == 0: y += length_px
    if direction == 1: x -= length_px
    if direction == 2: y -= length_px
    if direction == 3: x += length_px

    cv2.line(map_img, (x_add, y_add), (x, y), (0, 0, 0), map_road_thickness)

    # Рисуем текстуру для файла wbt
    cv2.line(img_background, (x_add, y_add), (x, y), (0, 0, 255, 255), map_road_thickness)
    if direction == 0 or direction == 2:
        cv2.line(img_background, (x_add+thickness//2, y_add), (x+thickness//2, y), (255, 255, 255, 255), map_road_thickness//2)
        cv2.line(img_background, (x_add-thickness//2, y_add), (x-thickness//2, y), (255, 255, 255, 255), map_road_thickness//2)
    if direction == 1 or direction == 3:
        cv2.line(img_background, (x_add, y_add+thickness//2), (x, y+thickness//2), (255, 255, 255, 255), map_road_thickness//2)
        cv2.line(img_background, (x_add, y_add-thickness//2), (x, y-thickness//2), (255, 255, 255, 255), map_road_thickness//2)

    for i in range(int(length * 100 / gradient_step)):
        if direction == 0:
            cv2.rectangle(gradient_img, (x_add-thickness//2, y_add + i*gradient_step), (x_add + thickness//2, y_add + (i+1)*gradient_step), color=(current_color, current_color, current_color), thickness=-1)
            points.append([x_real, y_real + (i+1)*gradient_step/100, 0])
        if direction == 1:
            cv2.rectangle(gradient_img, (x_add- i*gradient_step, y_add-thickness//2), (x_add - (i+1)*gradient_step, y_add + thickness//2), color=(current_color, current_color, current_color), thickness=-1)
            points.append([x_real - (i+1)*gradient_step/100, y_real, -np.pi/2])
        if direction == 2:
            cv2.rectangle(gradient_img, (x_add-thickness//2, y_add - i*gradient_step), (x_add + thickness//2, y_add - (i+1)*gradient_step), color=(current_color, current_color, current_color), thickness=-1)
            points.append([x_real, y_real - (i+1)*gradient_step/100, np.pi])
        if direction == 3:
            cv2.rectangle(gradient_img, (x_add + i * gradient_step, y_add - thickness // 2), (x_add + (i + 1) * gradient_step, y_add + thickness // 2), color=(current_color, current_color, current_color), thickness=-1)
            points.append([x_real + (i + 1) * gradient_step / 100, y_real, np.pi/2])
        current_color += 1
    print(current_color)
    return gradient_img, map_img, img_background, points


def write_circle(gradient_img, map_img, img_background, direction, points):
    # direction: 0: v <; 1: < ^; 2: ^ >; 3: > v;

    start_color = len(points) - 1
    image = np.ones((300, 300, 3), dtype=np.uint8)
    center = (150, 150)  # Центр круга
    radius = 100  # Радиус круга
    if direction == 0:  x_real, y_real = points[start_color][0]-1, points[start_color][1]
    if direction == 1:  x_real, y_real = points[start_color][0]-1.5, points[start_color][1]-1
    if direction == 2:  x_real, y_real = points[start_color][0]-0.5, points[start_color][1]-1.5
    if direction == 3:  x_real, y_real = points[start_color][0], points[start_color][1]-0.5

    if direction == 0:  x_map, y_map = int(points[start_color][0]*100)-radius, int(points[start_color][1]*100)
    if direction == 1:  x_map, y_map = int(points[start_color][0]*100), int(points[start_color][1]*100)-radius
    if direction == 2:  x_map, y_map = int(points[start_color][0]*100)+radius, int(points[start_color][1]*100)
    if direction == 3:  x_map, y_map = int(points[start_color][0]*100), int(points[start_color][1]*100)+radius

    x_add, y_add = int(x_real*100), int(y_real*100)

    external_r = radius+thickness//2
    angle_step = gradient_step / external_r
    current_color = start_color
    points.pop(start_color)
    # Рисуем градиентную линию вдоль окружности
    if direction < 4:
        cv2.ellipse(map_img, (x_map, y_map), (radius, radius), 0, 90*direction, 90*(direction+1), (0, 0, 0), map_road_thickness)

        cv2.ellipse(img_background, (x_map, y_map), (radius, radius), 0, 90*direction, 90*(direction+1), (0, 0, 255, 255), map_road_thickness)
        cv2.ellipse(img_background, (x_map, y_map), (radius-thickness//2, radius-thickness//2), 0, 90*direction, 90*(direction+1), (255, 255, 255, 255), map_road_thickness//2)
        cv2.ellipse(img_background, (x_map, y_map), (radius+thickness//2, radius+thickness//2), 0, 90*direction, 90*(direction+1), (255, 255, 255, 255), map_road_thickness//2)

        for angle in np.arange(math.pi/2*direction, math.pi/2*(direction+1), angle_step):
            for angle_color in np.arange(angle, min(math.pi/2*(direction+1), angle + angle_step), 0.0001):
                x = int(center[0] + (external_r+100) * math.cos(angle_color))
                y = int(center[1] + (external_r+100) * math.sin(angle_color))

                cv2.line(image, center, (x, y), (current_color, current_color, current_color), 3)
            # Обновляем текущий цвет
            current_color += 1

            # добавляем путевую точку
            if direction == 0: points.append([x_real + radius * math.cos(angle)/100, y_real + radius * math.sin(angle)/100, -angle])
            if direction == 1: points.append([x_real + 1.5 + radius * math.cos(angle)/100, y_real + radius * math.sin(angle)/100, -angle])
            if direction == 2: points.append([x_real + 1.5 + radius * math.cos(angle)/100, y_real + radius * math.sin(angle)/100+1.5, -angle])
            if direction == 3: points.append([x_real + radius * math.cos(angle)/100, y_real + radius * math.sin(angle)/100+1.5, -angle])

    cv2.circle(image, center, external_r + 150, (255, 0, 0), 300)
    cv2.circle(image, center, radius - thickness//2, (255, 0, 0), -1)
    if direction == 0: image = image[150:, 150:]
    if direction == 1: image = image[150:, :150]
    if direction == 2: image = image[:150, :150]
    if direction == 3: image = image[:150, 150:]
    w, h, _ = image.shape
    gradient_img[y_add:y_add + h, x_add:x_add + w] = image
    return gradient_img, map_img, img_background, points


gradient_img = np.ones((map_size[0], map_size[1], 3), dtype=np.uint8)
gradient_img[:, :] = (255, 0, 0)

map_img = np.ones((map_size[0], map_size[1], 3), dtype=np.uint8)
map_img[:, :] = (255, 255, 255)

img_background = np.ones((map_size[0], map_size[1], 4), dtype=np.uint8)
img_background[:, :, 0:3] = [255, 255, 255]  # RGB
img_background[:, :, 3] = 0

points = [start_coords]

gradient_img, map_img, img_background, points = write_line(gradient_img, map_img, img_background, 5, 2, points)
gradient_img, map_img, img_background, points = write_circle(gradient_img, map_img, img_background, 2, points)
gradient_img, map_img, img_background, points = write_line(gradient_img, map_img, img_background, 10, 3, points)
gradient_img, map_img, img_background, points = write_circle(gradient_img, map_img, img_background, 3, points)
gradient_img, map_img, img_background, points = write_line(gradient_img, map_img, img_background, 10, 0, points)
gradient_img, map_img, img_background, points = write_circle(gradient_img, map_img, img_background, 0, points)
gradient_img, map_img, img_background, points = write_line(gradient_img, map_img, img_background, 10, 1, points)
gradient_img, map_img, img_background, points = write_circle(gradient_img, map_img, img_background, 1, points)
gradient_img, map_img, img_background, points = write_line(gradient_img, map_img, img_background, 5, 2, points)



print(points)

with open('respawn_points.json', 'w') as file:
    json.dump(points, file)


gradient_img_resize = cv2.resize(gradient_img, (gradient_img.shape[1] // imshow_size, gradient_img.shape[0] // imshow_size))
map_img_resize = cv2.resize(map_img, (map_img.shape[1] // imshow_size, map_img.shape[0] // imshow_size))
img_background_resize = cv2.resize(img_background, (img_background.shape[1] // imshow_size, img_background.shape[0] // imshow_size))
img_background_2048 = cv2.resize(img_background, (2048, 2048))

# Выводим изображение на экран
cv2.imshow('Gradient', gradient_img_resize)
cv2.imwrite('gradient.png', gradient_img)
cv2.imshow('map', map_img_resize)
cv2.imwrite('map.png', map_img)
cv2.imshow('background', cv2.flip(img_background_resize, -1))
cv2.imwrite('marathon_background.png', cv2.flip(img_background_2048, -1))

# Ждем нажатия клавиши и закрываем окно
cv2.waitKey(0)
cv2.destroyAllWindows()
