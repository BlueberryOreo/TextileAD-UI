import os
import yaml
import json
import importlib

import anomalib.models

def get_supported_models_name():
    modules = anomalib.models.__all__
    return modules

if __name__ == "__main__":
    res = get_supported_models_name()
    print(res)
    