########################### camera configs #########################
FRONT_CAM = 0
SIDE_CAM = 1


####################### collect dataset config ###################
COLLECTION_SPEED = 25
SUM_CIRCLE = 35


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
	'castle': ((0.4374, 0.7216), (0.6417, 0.8955)),
	'target': ((0.4416, 0.6316), (0.7645, 0.9114)),
	'stop': ((0.4289, 0.6379), (0.0589, 0.3961)),
	'spoil': ((0.4478, 0.6571), (0.6297, 0.8975)),
	'hay': ((0.4336, 0.5831), (0.6988, 0.8987)),
	'end': ((0.3805, 0.6452), (0.7082, 0.9041))
}

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
	'model': MODEL_DIR_PREFIX + 'models/task',
	'threshold': 0.6,
	'label_list': TASK_LIST,
	'class_num': 7
}