import cv2
import numpy as np

# Задаем параметры отрезков

b = 1250
c = 1000
f = 1500
a = (10000 - b - 2*c - 2*f)//7
d = a
print(3*a+b)


# Создаем белое изображение
width = 2500
height = 3220
image = np.ones((height, width, 3), dtype=np.uint8) * 255

# Толщина линий
thickness = 5

# Начальная точка
x, y = 200, 3020

# Рисуем отрезки
def draw_line(img, start_point, end_point, color, thickness):
    cv2.line(img, start_point, end_point, color, thickness)

color = (0, 0, 0)  # Черный цвет

# Отрезок длины a вправо
draw_line(image, (x, y), (x + a, y), color, thickness)
x += a

# Отрезок длины b вверх
draw_line(image, (x, y), (x, y - b), color, thickness)
y -= b

# Отрезок длины c вправо
draw_line(image, (x, y), (x + c, y), color, thickness)
x += c

# Отрезок длины a вверх
draw_line(image, (x, y), (x, y - a), color, thickness)
y -= a

# Отрезок длины c влево
draw_line(image, (x, y), (x - c, y), color, thickness)
x -= c

# Отрезок длины d вверх
draw_line(image, (x, y), (x, y - d), color, thickness)
y -= d

# Отрезок длины f вправо
draw_line(image, (x, y), (x + f, y), color, thickness)
x += f

# Отрезок длины a вверх
draw_line(image, (x, y), (x, y - a), color, thickness)
y -= a

# Отрезок длины f+a влево
draw_line(image, (x, y), (x - (f + a), y), color, thickness)
x -= (f + a)

# Отрезок длины 2a+d+b вниз
draw_line(image, (x, y), (x, y + (2 * a + d + b)), color, thickness)

# Сохраняем изображение
cv2.imwrite('output.png', image)

# Отображаем изображение
cv2.imshow('Drawing', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('letter_F.png', image)
