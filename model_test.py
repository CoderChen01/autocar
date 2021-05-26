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
    directory = 'image/test_side_image_20561102075542'
    detector = TaskDetector()
    x_result = []
    y_result = []
    for entry in os.scandir(directory):
        img = cv2.imread(entry.path)
        result = detector.detect(img)
        if not result:
            continue
        print(entry.name, result.relative_center_x, result.relative_center_y)
        x_result.append(result.relative_center_x)
        y_result.append(result.relative_center_y)
        cv2.imwrite(directory + '/' + entry.name.split('.')[0] + '.png', draw_res(img, [result]))
    print('x_min: {}, x_max: {}'.format(min(x_result), max(x_result)))
    print('y_min: {}, y_max: {}'.format(min(y_result), max(y_result)))

