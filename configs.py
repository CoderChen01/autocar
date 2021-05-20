########################### camera configs #########################
FRONT_CAM = 0
SIDE_CAM = 1


####################### collect dataset config ###################
COLLECTION_SPEED = 25
SUM_CIRCLE = 15


########################### run config ###########################
RUN_SPEED = 23
RUN_KX = 0.95
full_speed = 35
turn_speed = full_speed * 0.8


########################### model configs ##########################
# base config
MODEL_DIR_PREFIX='/home/root/workspace/autocar/'

# cruise model
CRUISE_MODEL = {
	'model':MODEL_DIR_PREFIX + 'models/cruise'
}

# sign model
SIGN_LIST = {
	0: 'background',
	1: 'castle',
	2: 'target',
	3: 'stop',
	4: 'spoil',
	5: 'hay',
	6: 'end'
}
SIGN_MODEL = {
	'model': MODEL_DIR_PREFIX + 'models/sign',
	'threshold': 0.6,
	'label_list': SIGN_LIST,
	'class_num': 7
}
MAX_SIGN_PER_FRAME = 2
HAS_SIGN_THRESHOLD = 80

# task model
TASK_LIST = {
	0: 'background',
	1: 'dh',
	2: 'dj',
	3: 'dxj',
	4: 'target',
	5: 'spoil',
	6: 'hay'
}
TASK_MODEL = {
	'model':MODEL_DIR_PREFIX + 'models/task',
	'threshold':0.6,
	'label_list':TASK_LIST
}
MISSION_NUM = 8
mission_low = 0.3
mission_high = 0.75
MISS_DURATION = 200
EMLARGE_RATIO = 1.2
