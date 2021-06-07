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
	'castle': ((0.4403, 0.7455), (0.6531, 0.9371)),
	'target': ((0.3933, 0.6614), (0.6707, 0.9395)),
	'stop': ((0.4448, 0.6515), (0.1344, 0.3961)),
	'spoil': ((0.4478, 0.6589), (0.6297, 0.9069)),
	'hay': ((0.4429, 0.5940), (0.6297, 0.8987)),
	'end': ((0.3911, 0.6589), (0.7117, 0.9096))
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