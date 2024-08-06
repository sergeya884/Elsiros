'''
Класс строит перед роботом три прямоугольника заданного размера и вычисляет среднюю координату всех пикселей линии
марафона в этих прямоугольниках
'''
import time

import cv2
import numpy as np


class RectangleAnalyzer:
    def __init__(self, image_path, width, height, draw=False):
        self.width = width
        self.height = height
        #self.angle_radians = np.deg2rad(robot_coords[2])
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.draw = draw
        self.robot_coords = [0.0, 0.0, 0.0]

    def rotate_point(self, px, py, ox, oy, angle):
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        qx = ox + cos_angle * (px - ox) - sin_angle * (py - oy)
        qy = oy + sin_angle * (px - ox) + cos_angle * (py - oy)
        return qx, qy

    def get_rectangle_points(self, B):
        half_width = self.width / 2
        corners = [
            (-half_width, 0),  # середина левой стороны
            (half_width, 0),  # середина правой стороны
            (half_width, self.height),
            (-half_width, self.height)
        ]
        rotated_corners = [self.rotate_point(x, y, 0, 0, self.robot_coords[2]) for x, y in corners]
        translated_corners = [(x + B[0], y + B[1]) for x, y in rotated_corners]
        return translated_corners

    import numpy as np
    import cv2

    def get_black_pixel_mean(self, corners, B):
        # Создаем ограничивающий прямоугольник
        x_min = int(min([p[0] for p in corners]))
        x_max = int(max([p[0] for p in corners]))
        y_min = int(min([p[1] for p in corners]))
        y_max = int(max([p[1] for p in corners]))

        # Проверяем, что координаты не выходят за границы изображения
        x_min = max(x_min, 0)
        x_max = min(x_max, self.image.shape[1] - 1)
        y_min = max(y_min, 0)
        y_max = min(y_max, self.image.shape[0] - 1)

        # Извлекаем подизображение, содержащее только область ограничивающего прямоугольника
        sub_image = self.image[y_min:y_max + 1, x_min:x_max + 1]

        # Создаем маску только для подизображения
        sub_corners = [(p[0] - x_min, p[1] - y_min) for p in corners]
        sub_mask = np.zeros(sub_image.shape, dtype=np.uint8)
        cv2.fillPoly(sub_mask, [np.array(sub_corners, dtype=np.int32)], 255)

        # Находим черные пиксели только в подизображении
        black_pixels = np.where((sub_image == 0) & (sub_mask == 255))

        if len(black_pixels[0]) > 0:
            mean_y = np.mean(black_pixels[0]) + y_min
            mean_x = np.mean(black_pixels[1]) + x_min

            # ВАЖНО. Тут координаты поменены местами, так как в cv и в webots зеркальные
            x = mean_x - B[0]
            y = mean_y - B[1]

            x, y = self.rotate_point(y, x, 0, 0, self.robot_coords[2])
            return x, y
        else:
            return None

    def is_out_of_distance(self, grey_range=(100, 200)):
        pixel_value = self.image[self.robot_coords[1], self.robot_coords[0]]
        return grey_range[0] <= pixel_value <= grey_range[1]

    def get_next_B(self, prev_corners):
        return (int((prev_corners[2][0] + prev_corners[3][0]) / 2), int((prev_corners[2][1] + prev_corners[3][1]) / 2))

    def found_black_centers(self):
        mean_coordinates_list = []
        B = (self.robot_coords[0], self.robot_coords[1])
        if self.draw:
            image_color = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Красный, зеленый, синий
            cv2.circle(image_color, B, 10, (0, 0, 255), thickness=-1)
        for i in range(3):
            rectangle_corners = self.get_rectangle_points(B)
            mean_coordinates = self.get_black_pixel_mean(rectangle_corners, B)
            mean_coordinates_list.append(mean_coordinates)

            if self.draw:
                rectangle_corners_int = [(int(x), int(y)) for x, y in rectangle_corners]
                cv2.polylines(image_color, [np.array(rectangle_corners_int)], isClosed=True, color=colors[i],
                              thickness=2)

            B = self.get_next_B(rectangle_corners)

        if self.draw:
            # Отображение координат в правом верхнем углу
            if mean_coordinates_list[0] is not None:
                text = f"Mean X: {mean_coordinates_list[0][0]:.2f}, Mean Y: {mean_coordinates_list[0][1]:.2f}"
                cv2.putText(image_color, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            resized_image = cv2.resize(image_color, (500, 500))
            cv2.imshow("Image with Rectangles and Point B", resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return mean_coordinates_list


# Пример использования
def main():
    image_path = 'map_marathon.png'
    analyzer = RectangleAnalyzer(image_path=image_path, width=30, height=20, draw=True)
    analyzer.robot_coords = [500, 1760, 3.14]  # Начальная позиция и угол
    time1 = time.time()
    mean_coordinates_list = analyzer.found_black_centers()
    print(f'Время выполнения:{time.time()-time1}')
    print("Средние координаты всех черных пикселей внутри прямоугольников:", mean_coordinates_list)
    print(analyzer.is_out_of_distance())


if __name__ == '__main__':
    main()
