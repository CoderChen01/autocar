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
    print(results)
    for item in results:
        print(item)
        print(type(item))
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
    #视频文件
    cap=cv2.VideoCapture('run.avi')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(1)
    cruiser = Cruiser()
    sd = SignDetector()
    time.sleep(1)
    time_name = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./' + time_name + '.avi', fourcc, 6, (640, 480))
    while True:
        ret,front_image = cap.read()
        cruise_result = cruiser.cruise(front_image )
        frame = draw_cruise_result(front_image , cruise_result)
        signs, index = sd.detect(frame)
        draw_res(frame, signs)
        # frame = cv2.flip(frame, 2)
        out.write(frame)
        cv2.imshow("Output", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    directory = 'image/test_front_image_20561025015415'
    sign_detector = SignDetector()
    for entry in os.scandir(directory):
        img = cv2.imread(entry.path)
        results = sign_detector.detect(img)
        if not results:
            continue
        print(entry.name, results[0].relative_center_x, results[0].relative_center_y)
        cv2.imwrite(directory + '/' + entry.name.split('.')[0] + '.png', draw_res(img, results))
        # print(results[blow_index].relative_center_y, results[blow_index].index)
    # directory = 'image/side_image_test'
    # task_detector = TaskDetector()
    # for entry in os.scandir(directory):
    #     img = cv2.imread(entry.path)
    #     results = task_detector.detect(img)
    #     print(results)
        # print(results[0].relative_center_x, results[0].index)
