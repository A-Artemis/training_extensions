"""
Utils for demo
"""
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#

import json
from pathlib import Path
from typing import Optional

from ote_sdk.entities.label_schema import LabelSchemaEntity
from ote_sdk.entities.model_template import TaskType, task_type_to_label_domain
from ote_sdk.usecases.exportable_code.prediction_to_annotation_converter import (
    create_converter,
)
from ote_sdk.usecases.exportable_code.visualizers import Visualizer


def get_model_path(path: Optional[Path]) -> Path:
    """
    Get path to model
    """
    model_path = path
    if model_path is None:
        model_path = Path(__file__).parent / "model.xml"
    if not model_path.exists():
        raise IOError("The path to the model was not found.")

    return model_path


def get_parameters(path: Optional[Path]) -> dict:
    """
    Get hyper parameters to creating model
    """
    parameters_path = path
    if parameters_path is None:
        parameters_path = Path(__file__).parent / "config.json"
    if not parameters_path.exists():
        raise IOError("The path to the config was not found.")

    with open(parameters_path, "r", encoding="utf8") as file:
        parameters = json.load(file)

    return parameters


def create_output_converter(task_type: TaskType, labels: LabelSchemaEntity):
    """
    Create annotation converter according to kind of task
    """

    converter_type = task_type_to_label_domain(task_type)
    return create_converter(converter_type, labels)


def create_visualizer(_task_type: TaskType):
    """
    Create visualizer according to kind of task
    """

    # TODO: use anomaly-specific visualizer for anomaly tasks

    return Visualizer(window_name="Result")
