import cv2
import numpy as np

# Задаем параметры отрезков
b = 1250
c = 1000
f = 1500
a = (10000 - b - 2 * c - 2 * f) // 7
d = a
print(3 * a + b)

# Создаем белое изображение
width = 2500
height = 3200
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Толщина линий
thickness = 5

# Начальная точка
x, y = 200, 3020

# Функция для рисования отрезков с серыми линиями
def draw_line_with_gray(img, start_point, end_point, color, thickness):
    offset = 50

    # Вычисляем направления серых линий
    if start_point[0] == end_point[0]:  # Вертикальная линия
        start_point_left = (start_point[0] - offset, start_point[1] - 50)
        end_point_left = (end_point[0] - offset, end_point[1]-50)
        start_point_right = (start_point[0] + offset, start_point[1]+50)
        end_point_right = (end_point[0] + offset, end_point[1]+50)
    else:  # Горизонтальная линия
        start_point_left = (start_point[0]-50, start_point[1] - offset)
        end_point_left = (end_point[0]-50, end_point[1] - offset)
        start_point_right = (start_point[0]+50, start_point[1] + offset)
        end_point_right = (end_point[0]+50, end_point[1] + offset)

    # Рисуем черную линию
    cv2.line(img, start_point, end_point, color, thickness)

    # Рисуем серые линии
    gray_color = (128, 128, 128)
    cv2.line(img, start_point_left, end_point_left, gray_color, 2)
    cv2.line(img, start_point_right, end_point_right, gray_color, 2)

color = (0, 0, 0)  # Черный цвет

# Отрезок длины a вправо
draw_line_with_gray(image, (x, y), (x + a, y), color, thickness)
x += a

# Отрезок длины b вверх
draw_line_with_gray(image, (x, y), (x, y - b), color, thickness)
y -= b

# Отрезок длины c вправо
draw_line_with_gray(image, (x, y), (x + c, y), color, thickness)
x += c

# Отрезок длины a вверх
draw_line_with_gray(image, (x, y), (x, y - a), color, thickness)
y -= a

# Отрезок длины c влево
draw_line_with_gray(image, (x, y), (x - c, y), color, thickness)
x -= c

# Отрезок длины d вверх
draw_line_with_gray(image, (x, y), (x, y - d), color, thickness)
y -= d

# Отрезок длины f вправо
draw_line_with_gray(image, (x, y), (x + f, y), color, thickness)
x += f

# Отрезок длины a вверх
draw_line_with_gray(image, (x, y), (x, y - a), color, thickness)
y -= a

# Отрезок длины f+a влево
draw_line_with_gray(image, (x, y), (x - (f + a), y), color, thickness)
x -= (f + a)

# Отрезок длины 2a+d+b вниз
draw_line_with_gray(image, (x, y), (x, y + (2 * a + d + b)), color, thickness)

# Сохраняем изображение
cv2.imwrite('output_with_gray_lines.png', image)
img_show = cv2.resize(image, (width // 5, height // 5))
# Отображаем изображение
cv2.imshow('Drawing', img_show)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('letter_F.png', image)