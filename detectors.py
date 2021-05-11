import time

import cv2
import numpy as np

import predictor_wrapper
import config
from camera import Camera


ssd_args = {
    'shape': [1, 3, 480, 480],
    'ms': [127.5, 0.007843]
}


def name_to_index(name, label_list):
    for k, v in label_list.items():
        if v == name:
            return k
    return None


def light_index_to_global(light_index):
    return light_index


def blue_index_to_global(blue_index):
    return blue_index + 11


def yellow_index_to_global(yellow_index):
    if yellow_index == 0:
        return 4
    return 10


def ssd_preprocess(args, src):
    shape = args["shape"]
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


def is_sign_valid(o):
    # TODO Calculating area
    valid = False
    if o[1] > config.sign['threshold']:
        valid = True
    return valid


def is_task_valid(o):
    valid = False
    # for o in res:
    if o[1] > config.task["threshold"]:
        valid = True
    return valid


class DetectionResult:
    def __init__(self):
        self.index = 0
        self.score = 0
        self.name = ''
        self.relative_box = [0, 0, 0, 0]
        self.relative_center_y = -1
        self.relative_center_x = -1

    def __str__(self):
        return "name:{} scroe:{} relative_box: {}".format(self.name, self.score, self.relative_box)


def clip_box(box):
    xmin, ymin, xmax, ymax = box
    x_center = (xmin + xmax) / 2
    y_center = (ymin + ymax) / 2
    h = ymax - ymin
    w = xmax - xmin
    scale = config.EMLARGE_RATIO
    return max(x_center - scale * w / 2, 0), max(y_center - scale * h / 2, 0), min(x_center + scale*w / 2, 1), min(y_center + scale * h / 2, 1)


def in_centered_in_image(res):
    for item in res:
        # TODO
        # if config.mission_label_list[int(item.index)] == 'redball' or config.mission_label_list[
        #     int(item.index)] == 'blueball':
        #     continue
        relative_box = item.relative_box
        relative_box = clip_box(relative_box)
        relative_center_x = (relative_box[0] + relative_box[2]) / 2
        print(">>>>>>>>>>>>>>>>>>>>>relative_center_x=",relative_center_x)
        if config.mission_high > relative_center_x > config.mission_low:
            return True
    return False


def res_to_detection(item, label_list, frame):
    detection_object = DetectionResult()
    detection_object.index = item[0]
    detection_object.score = item[1]
    detection_object.name = label_list[item[0]]
    detection_object.relative_box = item[2:6]
    detection_object.relative_center_x = (detection_object.relative_box[0]+ detection_object.relative_box[2]) / 2
    detection_object.relative_center_y = (detection_object.relative_box[1] + detection_object.relative_box[3]) / 2
    return detection_object


class SignDetector:
    def __init__(self):
        self.predictor = predictor_wrapper.PaddleLitePredictor()
        self.predictor.load(config.sign['model'])
        self.label_list = config.sign['label_list']
        self.class_num = config.sign['class_num']

    def detect(self, frame):
        res = infer_ssd(self.predictor, frame)
        res = np.array(res)
        labels = res[:, 0]
        scores = res[:, 1]
        # only one box for one class
        maxscore_index_per_class = [-1 for i in range(self.class_num)]
        maxscore_per_class = [-1 for i in range(self.class_num)]
        count = 0
        for label, score in zip(labels, scores):
            if score > maxscore_per_class[int(label)]:
                maxscore_per_class[int(label)] = score
                maxscore_index_per_class[int(label)] = count
            count += 1

        maxscore_index_per_class = [i for i in maxscore_index_per_class if i != -1]
        res = res[maxscore_index_per_class, :]
        blow_center = 0
        blow_center_index = -1
        results = []
        for index, item in enumerate(res):
            if is_sign_valid(item):
                detect_res = res_to_detection(item, self.label_list, frame)
                results.append(detect_res)
                if detect_res.relative_center_y > blow_center:
                    blow_center_index = index
                    blow_center = detect_res.relative_center_y
        return results, blow_center_index


class TaskDetector:
    def __init__(self):
        self.predictor = predictor_wrapper.PaddleLitePredictor()
        self.predictor.load(config.task['model'])
        self.label_list = config.task['label_list']

    # only one gt for one label
    def detect(self, frame):
        nmsed_out = infer_ssd(self.predictor, frame)
        # print("nmsed_out=",nmsed_out)
        max_indexes = [-1 for i in range(config.MISSION_NUM)]
        max_scores = [-1 for i in range(config.MISSION_NUM)]
        # print("max_scores=",max_scores)
        predict_label = nmsed_out[:, 0].tolist()
        predict_score = nmsed_out[:, 1].tolist()
        count = 0
        for label, score in zip(predict_label, predict_score):
            if score > max_scores[int(label)] and score > config.task['threshold']:
                max_indexes[int(label)] = count
                max_scores[int(label)] = score
            count += 1

        selected_indexes = [i for i in max_indexes if i != -1]
        task_index = [i for i in selected_indexes if
                      config.mission_label_list[predict_label[i]] != 'redball' or config.mission_label_list[
                          predict_label[i]] != 'blueball']
        res = nmsed_out[task_index, :]
        results = []
        for item in res:
            if is_task_valid(item):
                # TODO
                results.append(res_to_detection(item, self.label_list, frame))
        return results