import os
import yaml
import json
import importlib
from pathlib import Path

import anomalib
import anomalib.models
import anomalib.data.datamodules

from utils.custom_enum import ModelName, DatasetName


MAPPER = {
    "Folder3D": "folder_3d",
    "MVTec3D": "mvtec_3d",
    "BTech": "btech",
    "Datumaro": "datumaro",
    "Folder": "folder",
    "Kolektor": "kolektor",
    "MVTecAD": "mvtec",
    "MVTecAD2": "mvtecad2",
    "MVTecLOCO": "mvtec_loco",
    "RealIAD": "realiad",
    "VAD": "vad",
    "Visa": "visa",
    "Avenue": "avenue", 
    "ShanghaiTech": "shanghaitech", 
    "UCSDped": "ucsdped",
    "Cfa": "cfa",
    "Cflow": "cflow",
    "Csflow": "csflow",
    "Dfkde": "dfkde",
    "Dfm": "dfm",
    "Draem": "draem",
    "Dsr": "dsr",
    "EfficientAd": "efficient_ad",
    "Fastflow": "fastflow",
    "Fre": "fre",
    "Ganomaly": "ganomaly",
    "Padim": "padim",
    "Patchcore": "patchcore",
    "ReverseDistillation": "reverse_distillation",
    "Stfpm": "stfpm",
    "Supersimplenet": "supersimplenet",
    "Uflow": "uflow",
    "VlmAd": "vlm_ad",
    "WinClip": "winclip",
    "AiVad": "ai_vad",
    "Fuvas": "fuvas",
}

DEPRECATED = {"MVTec"}


def get_supported_models_name():
    modules = anomalib.models.__all__
    return modules


def get_supported_datasets_name():
    modules = set(anomalib.data.datamodules.depth.__all__ + anomalib.data.datamodules.image.__all__ + anomalib.data.datamodules.video.__all__)
    modules = modules - DEPRECATED
    return sorted(list(modules))


def load_model_config(model_name: str) -> dict:
    config_path = Path("configs") / "model" / f"{model_name}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Model config file not found: {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_dataset_config(dataset_name: str) -> dict:
    config_path = Path("configs") / "data" / f"{dataset_name}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Dataset config file not found: {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


if __name__ == "__main__":
    model_name = ModelName.PATCHCORE
    print(load_model_config(model_name.value))
    