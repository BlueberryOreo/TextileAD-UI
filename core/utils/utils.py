import os
import yaml
import json
import importlib
from pathlib import Path

import anomalib.models

from custom_enum import ModelName, DatasetName


def get_supported_models_name():
    modules = anomalib.models.__all__
    return modules


def load_model_config(model_name: str) -> dict:
    config_path = Path("../configs") / "model" / f"{model_name}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Model config file not found: {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_dataset_config(dataset_name: str) -> dict:
    pass

if __name__ == "__main__":
    model_name = ModelName.PATCHCORE
    print(load_model_config(model_name.value))
    