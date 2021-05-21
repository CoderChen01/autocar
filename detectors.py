import time

import cv2
import numpy as np

import predictor_wrapper
import configs


ssd_args = {
    'shape': [1, 3, 480, 480],
    'ms': [127.5, 0.007843]
}


def calculate_area(relative_box, shape):
    left = relative_box[0] * shape[1]
    top = relative_box[1] * shape[0]
    right = relative_box[2] * shape[1]
    bottom = relative_box[3] * shape[0]
    return (right - left) * (bottom - top)


def is_sign_valid(res, shape):
    box = res[2:6]
    area = calculate_area(box, shape)
    relative_center_x = (box[0] + box[2]) / 2
    relative_center_y = (box[1] + box[3]) / 2
    valid = False
    if res[1] > configs.SIGN_MODEL['threshold'] \
       and (3000 < area < 15000) \
       and (0.4 <= relative_center_x <= 0.64) \
       and (0.67 <= relative_center_y <= 0.72):
    # if res[1] > configs.SIGN_MODEL['threshold']:
        valid = True
    return valid


def is_task_valid(o):
    valid = False
    # for o in res:
    if o[1] > configs.TASK_MODEL['threshold']:
        valid = True
    return valid


def res_to_detection(item, label_list, frame):
    detection_object = DetectionResult()
    detection_object.index = item[0]
    detection_object.score = item[1]
    detection_object.name = label_list[item[0]]
    detection_object.shape = frame.shape
    detection_object.relative_box = item[2:6]
    detection_object.relative_center_x = (detection_object.relative_box[0]+ detection_object.relative_box[2]) / 2
    detection_object.relative_center_y = (detection_object.relative_box[1] + detection_object.relative_box[3]) / 2
    return detection_object


def ssd_preprocess(args, src):
    shape = args['shape']
    img = cv2.resize(src, (shape[3], shape[2]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32)
    img -= 127.5
    img *= 0.007843

    z = np.zeros((1, shape[2], shape[3], 3)).astype(np.float32)
    z[0, 0:img.shape[0], 0:img.shape[1] + 0, 0:img.shape[2]] = img
    z = z.reshape((1, 3, shape[3], shape[2]))
    return z


def infer_ssd(predictor, image):
    data = ssd_preprocess(ssd_args, image)
    # print(data.shape)
    predictor.set_input(data, 0)
    predictor.run()
    out = predictor.get_output(0)
    # print(out.shape())
    return np.array(out)


class DetectionResult:
    def __init__(self):
        self.index = 0
        self.score = 0
        self.name = ''
        self.shape = (640, 480)
        self.relative_box = [0, 0, 0, 0]
        self.relative_center_y = -1
        self.relative_center_x = -1

    def __repr__(self):
        return 'name:{} scroe:{} relative_box: {}'.format(self.name, self.score, self.relative_box)


class SignDetector:
    def __init__(self):
        self.predictor = predictor_wrapper.PaddleLitePredictor()
        self.predictor.load(configs.SIGN_MODEL['model'])
        self.label_list = configs.SIGN_MODEL['label_list']
        self.class_num = configs.SIGN_MODEL['class_num']

    def detect(self, frame):
        nmsed_out = infer_ssd(self.predictor, frame)
        try:
            predict_score = nmsed_out[:, 1].tolist()
        except IndexError:
            return
        res = nmsed_out[predict_score.index(max(predict_score))]
        if not is_sign_valid(res, frame.shape):
            return
        return res_to_detection(res, self.label_list, frame)


class TaskDetector:
    def __init__(self):
        self.predictor = predictor_wrapper.PaddleLitePredictor()
        self.predictor.load(configs.TASK_MODEL['model'])
        self.label_list = configs.TASK_MODEL['label_list']

    def detect(self, frame):
        nmsed_out = infer_ssd(self.predictor, frame)
        try:
            predict_score = nmsed_out[:, 1].tolist()
        except IndexError:
            return
        res = nmsed_out[predict_score.index(max(predict_score))]
        if not is_task_valid(res):
            return
        return res_to_detection(res, self.label_list, frame)
