########################### camera configs #########################
FRONT_CAM = 0
SIDE_CAM = 1


####################### collect dataset config ###################
COLLECTION_SPEED = 25
SUM_CIRCLE = 30


########################### run config ###########################
RUN_SPEED = 30

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
SIGN_THRESHOLD = {
	# ((x_min, x_max), (y_min, y_max), (area_min, area_max))
	'castle': ((0.4023, 0.7138), (0.6194, 0.8842), (18347.6277, 27915.8926)),
	'target': ((0.3759, 0.648), (0.6283, 0.8791), (18260.0665, 29918.9187)),
	'stop': ((0.4086, 0.6118), (0.1288, 0.358), (7680.4382, 13497.8017)),
	'spoil': ((0.4328, 0.6257), (0.6131, 0.8697), (20536.7741, 30816.4628)),
	'hay': ((0.4109, 0.5663), (0.5604, 0.8469), (10096.4269, 29298.1453)),
	'end': ((0.2757, 0.7312), (0.6574, 0.8573), (22673.1957, 30265.9024))
}

# task model
TASK_LIST = {
	0: 'background',
	1: 'target'
}
TASK_MODEL = {
	'model': MODEL_DIR_PREFIX + 'models/task',
	'threshold': 0.6,
	'label_list': TASK_LIST,
	'class_num': 7
}