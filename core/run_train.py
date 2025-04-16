import os
from datetime import datetime
from pathlib import Path
import importlib

from anomalib.engine import Engine
from anomalib.data import PredictDataset
from flask_socketio import SocketIO, emit

from utils.utils import RESULTS_FOLDER, StdOutListener
from utils.callbacks import TrainingProgressCallback


def before_training(model_name: str, dataset_name: str, model_config: str = None, dataset_config: str = None) -> Path:
    # Create project directory
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = f"{model_name}_{dataset_name}_{current_time}"
    project_path = RESULTS_FOLDER / project_name
    project_config_path = project_path / "config"
    project_result_path = project_path / "result"
    os.makedirs(project_path, exist_ok=True)
    os.makedirs(project_config_path, exist_ok=True)
    os.makedirs(project_result_path, exist_ok=True)

    # Save model and dataset configs
    with open(project_config_path / f"{model_name}.json", 'wt') as file:
        file.write(model_config)
    with open(project_config_path / f"{dataset_name}.json", 'wt') as file:
        file.write(dataset_config)

    return project_path


def training(model_config: dict, dataset_config: dict, project_path: Path, socketio: SocketIO, std_listener: StdOutListener):
    if std_listener.is_alive():
        std_listener.mount_buffer()  # Mount the buffer to stdout and stderr
    project_result_path = project_path / "result"
    model_config, trainer_config = model_config.get("model"), model_config.get("trainer", dict())

    # Load model and dataset classes
    # model_class = importlib.import_module(model_config.get("class_path"))
    # dataset_class = importlib.import_module(dataset_config.get("class_path"))
    model_module = ".".join(model_config.get("class_path").split(".")[:-1])
    dataset_module = ".".join(dataset_config.get("class_path").split(".")[:-1])
    model_class = getattr(importlib.import_module(model_module), model_config.get("class_path").split(".")[-1])
    dataset_class = getattr(importlib.import_module(dataset_module), dataset_config.get("class_path").split(".")[-1])

    # Initialize model and dataset
    model = model_class(**model_config.get("init_args"))
    dataset = dataset_class(**dataset_config.get("init_args"))

    # Initialize callbacks
    callbacks = [
        TrainingProgressCallback(socketio=socketio, project_path=project_path),
    ]

    if trainer_config.get("callbacks"):
        config_callbacks = trainer_config.pop("callbacks")
        for callback in config_callbacks:
            callback_module = ".".join(callback.get("class_path").split(".")[:-1])
            callback_class = getattr(importlib.import_module(callback_module), callback.get("class_path").split(".")[-1])
            callback_args = callback.get("init_args", dict())
            callbacks.append(callback_class(**callback_args))

    # Initialize engine
    engine = Engine(
        callbacks=callbacks, 
        default_root_dir=project_result_path, 
        **trainer_config
    )

    # Train
    engine.fit(
        model=model,
        datamodule=dataset,
    )

    after_training(engine, model, dataset)

    if std_listener.is_alive():
        std_listener.unmount_buffer()  # Unmount the buffer from stdout and stderr


def after_training(engine: Engine, model, datamodule):
    # Run inference
    engine.predict(
        model=model,
        datamodule=datamodule,
    )
    