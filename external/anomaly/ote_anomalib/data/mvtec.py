"""OTE MVTec Dataset facilitate OTE Anomaly Training."""

# Copyright (C) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

from pathlib import Path
from typing import List, Union

import cv2
import numpy as np
from anomalib.data.mvtec import make_mvtec_dataset
from pandas.core.frame import DataFrame

from ote_anomalib.data import LabelNames
from ote_sdk.entities.annotation import (
    Annotation,
    AnnotationSceneEntity,
    AnnotationSceneKind,
)
from ote_sdk.entities.dataset_item import DatasetItemEntity
from ote_sdk.entities.datasets import DatasetEntity
from ote_sdk.entities.id import ID
from ote_sdk.entities.image import Image
from ote_sdk.entities.label import Domain, LabelEntity
from ote_sdk.entities.scored_label import ScoredLabel
from ote_sdk.entities.shapes.polygon import Point, Polygon
from ote_sdk.entities.shapes.rectangle import Rectangle
from ote_sdk.entities.subset import Subset
from ote_sdk.entities.model_template import TaskType


class OteMvtecDataset:
    """Generate OTE MVTec Dataset from the anomaly detection datasets that follows the MVTec format.
    Args:
        path (Union[str, Path], optional): Path to the MVTec dataset category.
            Defaults to "./datasets/MVTec/bottle".
        split_ratio (float, optional): Ratio to split normal training images and add to the
            test set in case test set doesn't contain any normal images.
            Defaults to 0.5.
        seed (int, optional): Random seed to ensure reproducibility when splitting. Defaults to 0.
        create_validation_set (bool, optional): Create validation set from the test set by splitting
            it to half. Default to True.
    Examples:
        >>> dataset_generator = OteMvtecDataset()
        >>> dataset = dataset_generator.generate()
        >>> dataset[0].media.numpy.shape
        (900, 900, 3)
    """

    def __init__(
        self,
        path: Union[str, Path],
        split_ratio: float = 0.5,
        seed: int = 0,
        create_validation_set: bool = True,
        task_type: TaskType = TaskType.ANOMALY_CLASSIFICATION,
    ):
        self.path = path if isinstance(path, Path) else Path(path)
        self.split_ratio = split_ratio
        self.seed = seed
        self.create_validation_set = create_validation_set
        self.task_type = task_type

        self.normal_label = LabelEntity(
            name=LabelNames.normal, domain=Domain.ANOMALY_CLASSIFICATION, id=ID(LabelNames.normal)
        )
        self.abnormal_label = LabelEntity(
            name=LabelNames.anomalous, domain=Domain.ANOMALY_CLASSIFICATION, id=ID(LabelNames.anomalous)
        )

    def get_samples(self) -> DataFrame:
        """Get MVTec samples.
        Get MVTec samples in a pandas DataFrame. Update the certain columns
        to match the OTE naming terminology. For example, column `split` is
        renamed to `subset`. Labels are also renamed by creating their
        corresponding OTE LabelEntities
        Returns:
            DataFrame: Final list of samples comprising all the required
                information to create the OTE Dataset.
        """
        samples = make_mvtec_dataset(
            path=self.path,
            split_ratio=self.split_ratio,
            seed=self.seed,
            create_validation_set=self.create_validation_set,
        )

        # Set the OTE SDK Splits
        samples = samples.rename(columns={"split": "subset"})
        samples.loc[samples.subset == "train", "subset"] = Subset.TRAINING
        samples.loc[samples.subset == "val", "subset"] = Subset.VALIDATION
        samples.loc[samples.subset == "test", "subset"] = Subset.TESTING

        # Create and Set the OTE Labels
        samples.loc[samples.label != "good", "label"] = self.abnormal_label
        samples.loc[samples.label == "good", "label"] = self.normal_label

        samples = samples.reset_index(drop=True)

        return samples

    def generate(self) -> DatasetEntity:
        """Generate OTE Anomaly Dataset.
        Returns:
            DatasetEntity: Output OTE Anomaly Dataset from an MVTec
        """
        samples = self.get_samples()
        dataset_items: List[DatasetItemEntity] = []
        for _, sample in samples.iterrows():
            # Create image
            image = Image(file_path=sample.image_path)

            # Create annotation
            if self.task_type == TaskType.ANOMALY_CLASSIFICATION or sample.label == self.normal_label:
                shape = Rectangle(x1=0, y1=0, x2=1, y2=1)
                labels = [ScoredLabel(sample.label)]
                annotations = [Annotation(shape=shape, labels=labels)]
                annotation_scene = AnnotationSceneEntity(annotations=annotations, kind=AnnotationSceneKind.ANNOTATION)
            elif self.task_type == TaskType.ANOMALY_SEGMENTATION and sample.label == self.abnormal_label:
                mask = cv2.imread(sample.mask_path, cv2.IMREAD_GRAYSCALE)
                annotations = self.annotations_from_mask(mask)
                annotation_scene = AnnotationSceneEntity(annotations=annotations, kind=AnnotationSceneKind.ANNOTATION)
            else:
                raise ValueError(f"Unknown task type: {self.task_type}")

            # Create dataset item
            dataset_item = DatasetItemEntity(media=image, annotation_scene=annotation_scene, subset=sample.subset)

            # Add to dataset items
            dataset_items.append(dataset_item)

        dataset = DatasetEntity(items=dataset_items)
        return dataset

    def annotations_from_mask(self, mask: np.ndarray):
        height, width = mask.shape[:2]
        contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        annotations = []

        for contour in contours:
            points = list((point[0][0] / width, point[0][1] / height) for point in contour)
            points = [Point(x=x, y=y) for x, y in points]

            polygon = Polygon(points=points)
            annotations.append(
                Annotation(
                    shape=polygon,
                    labels=[ScoredLabel(self.abnormal_label, 1.0)],
                    # id=ID(ObjectId()),
                )
            )

        return annotations
