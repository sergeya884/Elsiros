import cv2
import numpy as np

def replace_colors(image_path, output_path):
    # Загрузка изображения с помощью OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Проверка, что изображение загружено
    if image is None:
        print("Не удалось загрузить изображение")
        return

    # Проверка, есть ли альфа-канал; если нет, добавляем его
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    # Определение маски для черных и серых пикселей
    lower_black = np.array([0, 0, 0, 0])
    upper_black = np.array([180, 180, 180, 255])
    black_mask = cv2.inRange(image, lower_black, upper_black)

    # Определение маски для белых пикселей
    lower_white = np.array([255, 255, 255, 255])
    upper_white = np.array([255, 255, 255, 255])
    white_mask = cv2.inRange(image, lower_white, upper_white)

    # Замена белых пикселей на прозрачные
    image[white_mask == 255, 3] = 0
    # Замена черных и серых пикселей на белые
    image[black_mask == 255] = [255, 255, 255, 255]
    # Поворот изображения на 90 градусов по часовой стрелке
    #image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Сохранение итогового изображения
    cv2.imwrite(output_path, image)

# Пример использования функции
for i in range (11):
    replace_colors(f'teams/teams_white/team{i}.png', f'teams/teams_empty/team{i}.png')
