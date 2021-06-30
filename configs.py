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
	'castle': ((0.4023, 0.7137), (0.6193, 0.8841)),
	'target': ((0.3758, 0.6481), (0.6283, 0.8791)),
	'stop': ((0.4085, 0.6117), (0.1288, 0.3579)),
	'spoil': ((0.4327, 0.6256), (0.6131, 0.8697)),
	'hay': ((0.4109, 0.5663), (0.6603, 0.8468)),
	'end': ((0.3757, 0.6312), (0.6573, 0.8573))
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