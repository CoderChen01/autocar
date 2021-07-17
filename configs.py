########################### camera configs #########################
FRONT_CAM = 0
SIDE_CAM = 1


####################### collect dataset config ###################
COLLECTION_SPEED = 25
SUM_CIRCLE = 30


########################### run config ###########################
RUN_SPEED = 35
FINETUNE_THRESHOLD = 0.015

########################### models configs ##########################
# base config
MODEL_DIR_PREFIX='/home/root/workspace/autocar/'

# cruise model
CRUISE_MODEL = {
	'models':[
		MODEL_DIR_PREFIX + 'models/cruise/0',
		MODEL_DIR_PREFIX + 'models/cruise/1'
	]
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
	'threshold': 0.5,
	'label_list': SIGN_LIST,
	'class_num': 7
}
SIGN_THRESHOLD = {
	# ((x_min, x_max), (y_min, y_max), (area_min, area_max))
	'castle': ((0.4023, 0.7138), (0.5094, 0.8942), (18347.6277, 37915.8926)),
	'target': ((0.3759, 0.648), (0.5083, 0.8991), (18260.0665, 39918.9187)),
	'stop': ((0.4109, 0.7663), (0.5004, 0.8969), (7680.4382, 23497.8017)),
	'spoil': ((0.4328, 0.6257), (0.5031, 0.8997), (20536.7741, 40816.4628)),
	'hay': ((0.4109, 0.7663), (0.5004, 0.8969), (8996.4269, 39298.1453)),
	'end': ((0, 1), (0.6574, 0.8973), (22673.1957, 40265.9024))
}

# task model
TASK_LIST = {
	0: 'background',
	1: 'target'
}
TASK_MODEL = {
	'model': MODEL_DIR_PREFIX + 'models/task',
	'threshold': 0,
	'label_list': TASK_LIST,
	'class_num': 2
}
TASK_THRESHOLD = [
	# (x_min, x_max), (area_min, area_max),
	((0.5203, 0.5526), (2643.8867, 7603.7098)),
	((0.5229, 0.5419), (1835.9532, 7374.0838)),
	((0.5257, 0.5473), (2392.0574, 7092.9603))
]
