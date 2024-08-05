import cv2
import numpy as np

# Создаем белое изображение размером 1000x1000
image = np.ones((1000, 1000, 3), dtype=np.uint8) * 255

# Рисуем черную окружность в центре с диаметром 850 и толщиной 5
center_coordinates = (500, 500)
radius = 425
color = (0, 0, 0)  # Черный цвет
thickness = 5

cv2.circle(image, center_coordinates, radius, color, thickness)

# Сохраняем изображение
cv2.imwrite('black_circle_on_white.png', image)

# Создаем изображение с альфа-каналом (прозрачный фон)
image_with_alpha = np.zeros((1000, 1000, 4), dtype=np.uint8)

# Рисуем белую окружность на прозрачном фоне
color_with_alpha = (255, 255, 255, 255)  # Белый цвет с непрозрачным альфа-каналом
cv2.circle(image_with_alpha, center_coordinates, radius, color_with_alpha, thickness)

# Сохраняем изображение с альфа-каналом
cv2.imwrite('white_circle_on_transparent.png', image_with_alpha)
