# Copyright (C) 2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

"""Getting Started with Anomalib Inference using the Python API.

This example shows how to perform inference on a trained model
using the Anomalib Python API.
"""
import os
from pathlib import Path
import importlib
import shutil
import json

from anomalib.data import PredictDataset
from anomalib.engine import Engine

from utils.utils import RESULTS_FOLDER, UPLOAD_FOLDER, StdOutListener
from utils.callbacks import InferenceProgressCallback


def before_testing(project_name: str, file_token: str):
    project_dir = RESULTS_FOLDER / project_name

    # Create test directory
    test_dir = project_dir / "test" / file_token
    test_dir.mkdir(parents=True, exist_ok=True)

    # Create input directory
    input_dir = test_dir / "input"
    if input_dir.exists():
        shutil.rmtree(input_dir)
    input_dir.mkdir(parents=True, exist_ok=True)

    # Get the model weight path
    for path in project_dir.rglob("*"):
        interrupt = False
        if path.is_dir() and path.name == "latest":
            for file in path.rglob("*.ckpt"):
                model_weight_path = str(file)
                interrupt = True
                break
        if interrupt:
            break
    else:
        raise FileNotFoundError(f"Model weight not found in {project_dir}")
    
    # Get model config
    model_config_dir = project_dir / "config"
    for file in model_config_dir.rglob("*"):
        if file.is_file() and file.name.endswith(".json"):
            with open(file, "r") as f:
                model_config = json.load(f)
                if model_config.get("model"):
                    model_config = model_config.get("model")
                    break
    
    # Move the uploaded files to the input directory
    upload_dir = UPLOAD_FOLDER / file_token
    if not upload_dir.exists():
        raise FileNotFoundError(f"Upload directory not found: {upload_dir}")
    for file in upload_dir.rglob("*"):
        if file.is_file():
            shutil.copy(file, input_dir / file.name)
    # Remove the upload directory
    shutil.rmtree(upload_dir)

    return model_config, model_weight_path, input_dir, test_dir


def testing(model_config: dict, model_weight_path: str, input_dir: Path, test_dir: Path, socketio, std_listener: StdOutListener):
    if std_listener.is_alive():
        std_listener.mount_buffer()  # Mount the buffer to stdout and stderr
    
    # Load model class
    model_module = ".".join(model_config.get("class_path").split(".")[:-1])
    model_class = getattr(importlib.import_module(model_module), model_config.get("class_path").split(".")[-1])

    # Initialize model
    model = model_class(**model_config.get("init_args"))

    # Initialize dataset
    dataset = PredictDataset(
        path=input_dir,
        image_size=(256, 256),
    )
    
    # Initialize callbacks
    callbacks = [
        InferenceProgressCallback(socketio=socketio, test_path=test_dir),
    ]

    # Initialize engine
    engine = Engine(
        callbacks=callbacks,
        default_root_dir=test_dir,
        max_epochs=1,
    )

    # Predict
    predictions = engine.predict(
        model=model,
        dataset=dataset,
        ckpt_path=model_weight_path,
    )

    after_testing(predictions, test_dir)

    if std_listener.is_alive():
        std_listener.unmount_buffer()  # Unmount the buffer from stdout and stderr


def after_testing(predictions, test_dir: Path):
    # Save the predictions
    metrics = []
    if predictions is not None:
        for idx, prediction in enumerate(predictions):
            image_path = prediction.image_path
            # anomaly_map = prediction.anomaly_map  # Pixel-level anomaly heatmap
            pred_label = prediction.pred_label  # Image-level label (0: normal, 1: anomalous)
            pred_score = prediction.pred_score  # Image-level anomaly score
            metrics.append({
                "image_path": image_path,
                # "anomaly_map": anomaly_map,
                "pred_label": int(pred_label),
                "pred_score": float(pred_score),
            })
            # Save anomaly map
            # if anomaly_map is not None:
            #     anomaly_map_path = test_dir / "anomaly_map" / f"{idx}.png"
            #     anomaly_map_path.parent.mkdir(parents=True, exist_ok=True)
            #     anomaly_map.save(anomaly_map_path)

    with open(test_dir / "metrics.json", "wt") as f:
        json.dump(metrics, f, indent=4)
