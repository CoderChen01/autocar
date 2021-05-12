import os
import numpy as np
from paddlelite import Place
from paddlelite import CxxConfig
from paddlelite import CreatePaddlePredictor
from paddlelite import TargetType
from paddlelite import PrecisionType
from paddlelite import DataLayoutType


class PaddleLitePredictor:
    """ PaddlePaddle interface wrapper """
    def __init__(self):
        self.predictor = None

    def load(self, model_dir):
        valid_places = (
            Place(TargetType.kFPGA, PrecisionType.kFP16, DataLayoutType.kNHWC),
            Place(TargetType.kHost, PrecisionType.kFloat),
            Place(TargetType.kARM, PrecisionType.kFloat),
        )
        config = CxxConfig()
        if os.path.exists(model_dir + "/params"):
            config.set_model_file(model_dir + "/model")
            config.set_param_file(model_dir + "/params")
        else:
            config.set_model_dir(model_dir)
        config.set_valid_places(valid_places)
        self.predictor = CreatePaddlePredictor(config)

    def set_input(self, data, index):
        _input = self.predictor.get_input(index)
        _input.resize(data.shape)
        _input.set_data(data)

    def run(self):
        self.predictor.run()

    def get_output(self, index):
        return self.predictor.get_output(index)
