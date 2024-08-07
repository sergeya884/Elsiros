import cv2
import numpy as np


class RectangleAnalyzer:
    def __init__(self, image_path, width, height, robot_coords, draw=False):
        self.width = width
        self.height = height
        self.robot_coords = robot_coords  # [B_x, B_y, angle_degrees]
        self.angle_radians = np.deg2rad(robot_coords[2])
        self.image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        self.draw = draw

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
        rotated_corners = [self.rotate_point(x, y, 0, 0, self.angle_radians) for x, y in corners]
        translated_corners = [(x + B[0], y + B[1]) for x, y in rotated_corners]
        return translated_corners

    def get_black_pixel_mean(self, corners):
        mask = np.zeros(self.image.shape, dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(corners, dtype=np.int32)], 255)
        black_pixels = np.where((self.image == 0) & (mask == 255))
        if len(black_pixels[0]) > 0:
            mean_y = np.mean(black_pixels[0])
            mean_x = np.mean(black_pixels[1])
            return mean_x, mean_y
        else:
            return None

    def get_next_B(self, prev_corners):
        return (int((prev_corners[2][0] + prev_corners[3][0]) / 2), int((prev_corners[2][1] + prev_corners[3][1]) / 2))

    def analyze(self):
        mean_coordinates_list = []
        if self.draw:
            image_color = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        B = (self.robot_coords[0], self.robot_coords[1])
        for i in range(3):
            rectangle_corners = self.get_rectangle_points(B)
            mean_coordinates = self.get_black_pixel_mean(rectangle_corners)
            mean_coordinates_list.append(mean_coordinates)

            if self.draw:
                rectangle_corners_int = [(int(x), int(y)) for x, y in rectangle_corners]
                cv2.polylines(image_color, [np.array(rectangle_corners_int)], isClosed=True, color=colors[i],
                              thickness=20)
                cv2.circle(image_color, B, 20, (0, 0, 255), thickness=-1)

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


image_path = 'images/map.png'
robot_coords = [1000, 1500, -45]  # Начальная позиция и угол
analyzer = RectangleAnalyzer(image_path=image_path, width=100, height=200, robot_coords=robot_coords, draw=True)
mean_coordinates_list = analyzer.analyze()
print("Res:", mean_coordinates_list)
