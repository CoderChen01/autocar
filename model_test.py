import os
import time

import cv2

from cruiser import Cruiser
from detectors import SignDetector, TaskDetector, calculate_area
import configs


def draw_cruise_result(frame, res):
    color = (0, 244, 10)
    thickness = 2

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = 450, 50

    fontScale = 1
    txt = "{:.4f}".format(round(res, 5))
    frame = cv2.putText(frame, txt, org, font,
                       fontScale, color, thickness, cv2.LINE_AA)
    print("angle=",txt)
    return frame


def draw_res(frame, results):
    res = list(frame.shape)
    for item in results:
        left = item.relative_box[0] * res[1]
        top = item.relative_box[1] * res[0]
        right = item.relative_box[2] * res[1]
        bottom = item.relative_box[3] * res[0]
        start_point = (int(left), int(top))
        end_point = (int(right), int(bottom))
        color = (0, 244, 10)
        thickness = 2
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = start_point[0], start_point[1] - 10
        fontScale = 1
        frame = cv2.putText(frame, item.name, org, font,
                           fontScale, color, thickness, cv2.LINE_AA)
        frame = cv2.putText(frame, str(round(item.relative_center_x, 2)) + ',' + str(round(item.relative_center_y, 2)),
                            (40, 40), font, fontScale, color, 1, cv2.LINE_AA)
        frame = cv2.circle(frame, ((int(left) + int(right)) // 2, (int(top) + int(bottom)) // 2), 1, (0, 0, 255), 4)
        return frame


def test_front_video():
    data_dir = 'data/20561025042130'
    name_range = range(6087)
    sd = SignDetector()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    time_name = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    out = cv2.VideoWriter('./' + time_name + '.avi', fourcc, 6, (640, 480))
    for name in name_range:
        front_image = cv2.imread(data_dir + '/' + str(name) + '.jpg')
        signs = sd.detect(front_image)
        if signs:
            front_image = draw_res(front_image, signs)
        out.write(front_image)
        print(name)
    out.release()


if __name__ == "__main__":
    # test_front_video()
    directory = 'image/test_front_image_20561113061404'
    detector = SignDetector()
    x_result = []
    y_result = []
    area_result = []
    for entry in os.scandir(directory):
        if entry.name.endswith('.png'):
            continue
        img = cv2.imread(entry.path)
        result = detector.detect(img)
        if not result:
            continue
        print(entry.name, result.relative_center_x, result.relative_center_y)
        x_result.append(result.relative_center_x)
        y_result.append(result.relative_center_y)
        area_result.append(calculate_area(result.relative_box, result.shape))
        cv2.imwrite(directory + '/' + entry.name.split('.')[0] + '.png', draw_res(img, [result]))
    x_min, x_max = min(x_result), max(x_result)
    y_min, y_max = min(y_result), max(y_result)
    area_min, area_max = min(area_result), max(area_result)
    print('x_min: {}, x_max: {}'.format(x_min, x_max))
    print('y_min: {}, y_max: {}'.format(y_min, y_max))
    print('area_min: {}, area_max: {}'.format(area_min, area_max))
    print(f'(({round(x_min, 4)}, {round(x_max, 4)}),'
          f' ({round(y_min, 4)}, {round(y_max, 4)}),'
          f' ({round(area_min, 4)}, {round(area_max, 4)}))')
