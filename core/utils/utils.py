import os
import io
import re
import sys
import yaml
import json
import importlib
import secrets
from datetime import datetime
import time
import threading
from pathlib import Path
from flask_socketio import SocketIO

import anomalib
import anomalib.models
import anomalib.data.datamodules


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

# 配置上传文件的目录
UPLOAD_FOLDER = Path('uploads')
RESULTS_FOLDER = Path('results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def remove_control_characters(input_string: str) -> str:
    # 正则表达式匹配控制字符范围
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', input_string)


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


def get_validation_results(project_path: str | Path) -> list:
    project_path = Path(project_path) if isinstance(project_path, str) else project_path
    results_path = project_path / "result"
    if not results_path.exists():
        raise FileNotFoundError(f"Results path not found: {results_path}")
    results = []
    for path in results_path.rglob("*"):
        # print(path)
        if path.is_dir() and path.name == "latest":
            for file in path.rglob("*.png"):
                results.append(str(file))
    return results


def get_test_results(test_path: str | Path) -> list:
    test_path = Path(test_path) if isinstance(test_path, str) else test_path
    results = []
    for path in test_path.rglob("*"):
        if path.is_dir() and path.name == "latest":
            for file in path.rglob("*.png"):
                results.append(str(file))
    return results

def gen_token():
    return secrets.token_urlsafe(16)


class StdOutListener(threading.Thread):
    def __init__(self, socketio: SocketIO, emit_event="stdout"):
        self.socketio = socketio
        self.running = False  # Check if the thread is running
        self.suspended = False  # Check if the thread is suspended
        self.stdout = sys.stdout  # Save the original stdout
        self.stderr = sys.stderr  # Save the original stderr
        self.buffer = io.StringIO()  # Create a buffer to capture stdout and stderr
        self.mounted = False  # Check if the buffer is mounted on stdout and stderr

        self.prev_output = ""  # Store the previous output
        self.emit_event = emit_event  # Event name for socket emission
        super().__init__(daemon=True)  # Set the thread as a daemon thread

    def __del__(self):
        self.kill()

    def run(self):
        self.running = True
        while self.running:
            time.sleep(0.1)
            if self.suspended:
                continue
            
            if self.mounted:
                current_output = self.buffer.getvalue()
                if current_output != self.prev_output:
                    new_output = current_output[len(self.prev_output):]
                    if new_output.strip():
                        # Emit the new output to the socket
                        self.socketio.emit(self.emit_event, {'data': remove_control_characters(new_output).strip()})
                    self.prev_output = current_output
    
    def suspend(self):
        self.suspended = True
    
    def resume(self):
        self.suspended = False
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.prev_output = ""

    def mount_buffer(self):
        self.mounted = True
        sys.stdout = self.buffer
        sys.stderr = self.buffer
    
    def unmount_buffer(self):
        self.mounted = False
        sys.stdout = self.stdout
        sys.stderr = self.stderr
    
    def kill(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.running = False

if __name__ == "__main__":
    import random
    project_path = "/data/sjy/anomaly_detection/TextileAD-UI/core/results/Patchcore_MVTecAD_20250416_133535"
    res = get_validation_results(project_path)
    res = random.choices(res, k=10)
    host = "http://localhost:5000/"
    res = list(map(lambda x: host + x.split("/core/")[1], res))
    print(res)
