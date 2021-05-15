model_prefix="/home/root/workspace/autocar/"

front_cam = 0
side_cam = 1

full_speed = 35
turn_speed = full_speed * 0.8
EMLARGE_RATIO = 1.2

# mession config
# one more for background
MISSION_NUM = 8
mission_low = 0.3
mission_high = 0.75
MISS_DURATION = 200
mission_label_list = {
	0: "background",
	1: "daijun",
	2: "dunhuang",
	3: "dingxiangjun",
	4: "target",
	5: "trophies"
}

# task model
task = {
	"model":model_prefix + "models/task",
	"threshold":0.6,
	"label_list":mission_label_list
}

# sign config
MAX_SIGN_PER_FRAME = 2
sign_list = {
	0: "background",
	1: "barracks",
	2: "fenglangjuxu",
	3: "fortress",
	4: "soldier",
	5: "target"
}
HAS_SIGN_THRESHOLD = 80
# sign models
sign = {
	"model": model_prefix + "models/sign",
	"threshold": 0.6,
	"label_list": sign_list,
	"class_num": 10
}

# cruise model
cruise = {
	"model":model_prefix + "models/cruise"
}

JOYSTICK_ADDR = '/dev/input/js0'
# sign_threshold = 0.3
# task_threshold = 0.4

COLLECTION_SPEED = 35
RUN_SPEED = 35
RUN_KX = 0.9