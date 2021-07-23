########################### camera configs #########################
FRONT_CAM = 0
SIDE_CAM = 1


####################### collect dataset config ###################
COLLECTION_SPEED = 25
SUM_CIRCLE = 30


########################### run config ###########################
LOW_RUN_SPEED = 65  # 35
LOW_RUN_CRUISER_WEIGHTS = (0.6, 0.4)
HIGH_RUN_SPEED = 75  # 55
HIGH_RUN_CRUISE_WEIGHTS = (0.6, 0.4)
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
	'spoil': ((0.4328, 0.6257), (0.3666, 0.8997), (20536.7741, 40816.4628)),
	'hay': ((0.4109, 0.7663), (0.5004, 0.8969), (8996.4269, 39298.1453)),
	'end': ((0, 1), (0.4574, 0.8973), (12673.1957, 50265.9024))
}

# task model
# shot target task
SHOT_TARGET_TASK_LIST = {
	0: 'background',
	1: 'target'
}
SHOT_TARGET_TASK_THRESHOLD = [
	# (x_min, x_max), (area_min, area_max),
	((0.4883, 0.5526), (0, 9603.7098)),
	((0.4889, 0.5419), (0, 9374.0838)),
	((0.4887, 0.5473), (0, 9992.9603))
]
# hay task list
HAY_TASK_LIST = {
	0: 'background',
	1: 'hay'
}
# Parking forward requires a high basket threshold
# Parking backward requires setting the rim threshold low
HAY_TASK_THRESHOLD = ((0.2333, 0.2688), (0.82, 0.8709), (9637.873, 152778.0546))
TASK_MODELS = [
	{
		'model': MODEL_DIR_PREFIX + 'models/task/0',
		'threshold': 0.15,
		'label_list': SHOT_TARGET_TASK_LIST,
		'class_num': 2
	},
	{
		'model': MODEL_DIR_PREFIX + 'models/task/1',
		'threshold': 0.66,
		'label_list': HAY_TASK_LIST,
		'class_num': 2
	},
]
