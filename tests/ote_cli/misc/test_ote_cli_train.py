"""Tests for input parameters with OTE CLI train tool"""
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

import os
import pytest

from ote_sdk.test_suite.e2e_test_system import e2e_pytest_component

from ote_cli.utils.tests import (
    create_venv,
    get_some_vars,
)

from ote_cli_test_common import (
    default_train_args_paths,
    default_classification_args_paths,
    wrong_paths,
    ote_common,
    logger,
    parser_templates,
    root,
    ote_dir,
    train_args,
    errors_dict
)

params_values, params_ids, params_values_for_be, params_ids_for_be = parser_templates()


class TestTrainCommon:
    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values)
    def create_venv_fx(self, template):
        work_dir, template_work_dir, algo_backend_dir = get_some_vars(template, root)
        create_venv(algo_backend_dir, work_dir)

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_no_template(self, back_end, template, create_venv_fx):
        error_string = (
            "ote train: error: the following arguments are required: template"
        )
        command_line = []
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_no_train_ann_file(self, back_end, template, create_venv_fx):
        error_string = (
            "ote train: error: the following arguments are required: --train-ann-files"
        )
        command_line = [
            template.model_template_id,
            "--train-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
            "--val-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
            "--val-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
            "--save-model-to",
            f"./trained_{template.model_template_id}",
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_no_train_data_roots(self, back_end, template, create_venv_fx):
        error_string = (
            "ote train: error: the following arguments are required: --train-data-roots"
        )
        command_line = [
            template.model_template_id,
            "--train-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
            "--val-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
            "--val-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
            "--save-model-to",
            f"./trained_{template.model_template_id}",
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_no_val_ann_file(self, back_end, template, create_venv_fx):
        error_string = (
            "ote train: error: the following arguments are required: --val-ann-files"
        )
        command_line = [
            template.model_template_id,
            "--train-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
            "--train-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
            "--val-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
            "--save-model-to",
            f"./trained_{template.model_template_id}",
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_no_val_data_roots(self, back_end, template, create_venv_fx):
        error_string = (
            "ote train: error: the following arguments are required: --val-data-roots"
        )
        command_line = [
            template.model_template_id,
            "--train-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
            "--train-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
            "--val-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
            "--save-model-to",
            f"./trained_{template.model_template_id}",
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_no_save_model_to(self, back_end, template, create_venv_fx):
        error_string = (
            "ote train: error: the following arguments are required: --save-model-to"
        )
        command_line = [
            template.model_template_id,
            "--train-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
            "--train-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
            "--val-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
            "--val-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_hpo_not_enabled(self, back_end, template, create_venv_fx):
        error_string = "Parameter --hpo-time-ratio must be used with --enable-hpo key"
        command_line = [
            template.model_template_id,
            "--train-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
            "--train-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
            "--val-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
            "--val-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
            "--save-model-to",
            f"./trained_{template.model_template_id}",
            "--hpo-time-ratio",
            "4",
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_string_hpo_value(self, back_end, template, create_venv_fx):
        error_string = "ote train: error: argument --hpo-time-ratio: invalid float value: 'STRING_VALUE'"
        command_line = [
            template.model_template_id,
            "--train-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
            "--train-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
            "--val-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
            "--val-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
            "--save-model-to",
            f"./trained_{template.model_template_id}",
            "--enable-hpo",
            "--hpo-time-ratio",
            "STRING_VALUE",
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_negative_hpo_value(self, back_end, template, create_venv_fx):
        error_string = "Parameter --hpo-time-ratio must not be negative"
        command_line = [
            template.model_template_id,
            "--train-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
            "--train-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
            "--val-ann-files",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
            "--val-data-roots",
            f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
            "--save-model-to",
            f"./trained_{template.model_template_id}",
            "--enable-hpo",
            "--hpo-time-ratio",
            "-1",
        ]
        ret = ote_common(template, root, "train", command_line)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_wrong_path_train_ann_file(
        self, back_end, template, create_venv_fx
    ):
        error_string = "Path is not valid"
        for case in wrong_paths.values():
            command_line = [
                template.model_template_id,
                "--train-ann-files",
                case,
                "--train-data-roots",
                f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
                "--val-ann-files",
                f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
                "--val-data-roots",
                f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
                "--save-model-to",
                f"./trained_{template.model_template_id}",
            ]
            ret = ote_common(template, root, "train", command_line)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_wrong_paths_train_data_roots(
        self, back_end, template, create_venv_fx
    ):
        error_string = "Path is not valid"
        for case in wrong_paths.values():
            command_line = [
                template.model_template_id,
                "--train-ann-files",
                f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
                "--train-data-roots",
                case,
                "--val-ann-files",
                f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
                "--val-data-roots",
                f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
                "--save-model-to",
                f"./trained_{template.model_template_id}",
            ]
            ret = ote_common(template, root, "train", command_line)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_wrong_paths_val_ann_file(
        self, back_end, template, create_venv_fx
    ):
        error_string = "Path is not valid"
        for case in wrong_paths.values():
            command_line = [
                template.model_template_id,
                "--train-ann-files",
                f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
                "--train-data-roots",
                f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
                "--val-ann-files",
                case,
                "--val-data-roots",
                f'{os.path.join(ote_dir, default_train_args_paths["--val-data-roots"])}',
                "--save-model-to",
                f"./trained_{template.model_template_id}",
            ]
            ret = ote_common(template, root, "train", command_line)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_wrong_paths_val_data_roots(
        self, back_end, template, create_venv_fx
    ):
        error_string = "Path is not valid"
        for case in wrong_paths.values():
            command_line = [
                template.model_template_id,
                "--train-ann-files",
                f'{os.path.join(ote_dir, default_train_args_paths["--train-ann-files"])}',
                "--train-data-roots",
                f'{os.path.join(ote_dir, default_train_args_paths["--train-data-roots"])}',
                "--val-ann-files",
                f'{os.path.join(ote_dir, default_train_args_paths["--val-ann-files"])}',
                "--val-data-roots",
                case,
                "--save-model-to",
                f"./trained_{template.model_template_id}",
            ]
            ret = ote_common(template, root, "train", command_line)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize("back_end, template", params_values, ids=params_ids)
    def test_ote_train_wrong_saved_model_to(self, back_end, template, create_venv_fx):
        error_string = "Path is not valid"
        for case in wrong_paths.values():
            command_line = train_args(
                template, default_train_args_paths, ote_dir, root, smt_path=case
            )

            ret = ote_common(template, root, "train", command_line)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"


class TestTrainDetectionTemplateArguments:
    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def create_venv_fx(self, template):
        work_dir, template_work_dir, algo_backend_dir = get_some_vars(template, root)
        create_venv(algo_backend_dir, work_dir)

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_batch_size_type(self, template, create_venv_fx):
        error_string = "invalid int value"
        cases = ["1.0", "Alpha"]
        for case in cases:
            test_params = [
                "params",
                "--learning_parameters.batch_size",
                case,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_batch_size(self, template, create_venv_fx):
        test_params = [
            "params",
            "--learning_parameters.num_iters",
            "1",
            "--learning_parameters.batch_size",
            "1",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        # TODO: (fkutsepx) To write a hack what only check arguments correctness and provide a hook
        # TODO: (fkutsepx) that can be caught so it is not be need to waite entire tool execution
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_batch_size_oob(self, template, create_venv_fx):
        error_string = "is out of bounds."
        cases = ["0", "513"]
        for case in cases:
            test_params = [
                "params",
                "--learning_parameters.batch_size",
                case,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_learning_rate_type(self, template, create_venv_fx):
        error_string = "invalid float value"
        test_params = [
            "params",
            "--learning_parameters.learning_rate",
            "NotFloat",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_learning_rate(self, template, create_venv_fx):
        test_params = [
            "params",
            "--learning_parameters.num_iters",
            "1",
            "--learning_parameters.batch_size",
            "1",
            "--learning_parameters.learning_rate",
            "0.01",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_learning_rate_oob(self, template, create_venv_fx):
        error_string = "is out of bounds."
        cases = ["0.0", "0.2"]
        for case in cases:
            test_params = [
                "params",
                "--learning_parameters.learning_rate",
                case,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_lr_warmup_iters_type(self, template, create_venv_fx):
        error_string = "invalid int value"
        cases = ["1.0", "Alpha"]
        for case in cases:
            test_params = [
                "params",
                "--learning_parameters.learning_rate_warmup_iters",
                case,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_learning_rate_warmup_iters(self, template, create_venv_fx):
        test_params = [
            "params",
            "--learning_parameters.num_iters",
            "1",
            "--learning_parameters.batch_size",
            "1",
            "--learning_parameters.learning_rate_warmup_iters",
            "1",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_lr_warmup_iters_oob(self, template, create_venv_fx):
        error_string = "is out of bounds."
        oob_values = ["-1", "10001"]
        for value in oob_values:
            test_params = [
                "params",
                "--learning_parameters.learning_rate_warmup_iters",
                value,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_num_iters_type(self, template, create_venv_fx):
        error_string = "invalid int value"
        cases = ["1.0", "Alpha"]
        for case in cases:
            test_params = [
                "params",
                "--learning_parameters.num_iters",
                case,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_num_iters(self, template, create_venv_fx):
        test_params = [
            "params",
            "--learning_parameters.num_iters",
            "1",
            "--learning_parameters.batch_size",
            "1",
            "--learning_parameters.num_iters",
            "1",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_num_iters_oob(self, template, create_venv_fx):
        error_string = "is out of bounds."
        oob_values = ["0", "1000001"]
        for value in oob_values:
            test_params = [
                "params",
                "--learning_parameters.num_iters",
                value,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_pp_confidence_threshold_type(self, template, create_venv_fx):
        error_string = "invalid float value"
        test_params = [
            "params",
            "--postprocessing.confidence_threshold",
            "Alpha",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_pp_confidence_threshold(self, template, create_venv_fx):
        test_params = [
            "params",
            "--learning_parameters.num_iters",
            "1",
            "--learning_parameters.batch_size",
            "1",
            "--postprocessing.confidence_threshold",
            "0.5",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_pp_confidence_threshold_oob(self, template, create_venv_fx):
        error_string = "is out of bounds."
        oob_values = ["-0.9", "1.1"]
        for value in oob_values:
            test_params = [
                "params",
                "--postprocessing.confidence_threshold",
                value,
            ]
            command_args = train_args(
                template,
                default_train_args_paths,
                ote_dir,
                root,
                additional=test_params,
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert (
                error_string in ret["stderr"]
            ), f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_pp_result_based_confidence_threshold_type(
        self, template, create_venv_fx
    ):
        error_string = "Boolean value expected"
        test_params = [
            "params",
            "--postprocessing.result_based_confidence_threshold",
            "NonBoolean",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert error_string in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["DETECTION"],
        ids=params_ids_for_be["DETECTION"],
    )
    def test_ote_train_lp_result_based_confidence_threshold(
        self, template, create_venv_fx
    ):
        test_params = [
            "params",
            "--learning_parameters.num_iters",
            "1",
            "--learning_parameters.batch_size",
            "1",
            "--postprocessing.result_based_confidence_threshold",
            "True",
        ]
        command_args = train_args(
            template, default_train_args_paths, ote_dir, root, additional=test_params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"


class TestTrainClassificationTemplateArguments:
    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def create_venv_fx(self, template):
        work_dir, template_work_dir, algo_backend_dir = get_some_vars(template, root)
        create_venv(algo_backend_dir, work_dir)

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_batch_size_type(self, template, create_venv_fx):
        values = ["1.0", "String"]
        for value in values:
            params = [
                "params",
                "--learning_parameters.batch_size",
                value
            ]
            command_args = train_args(
                template, default_classification_args_paths, ote_dir, root, additional=params
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert errors_dict["int_value"] in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_batch_size(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.batch_size",
            "2"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_batch_size_oob(self, template, create_venv_fx):
        values = ["1", "513"]
        for value in values:
            params = [
                "params",
                "--learning_parameters.batch_size",
                value
            ]
            command_args = train_args(
                template, default_classification_args_paths, ote_dir, root, additional=params
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert errors_dict["oob"] in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_lr(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.learning_rate",
            "0.01"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_lr_type(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.learning_rate",
            "NotFloat"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert errors_dict["float_value"] in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_lr_oob(self, template, create_venv_fx):
        values = ["0", "0.11"]
        for value in values:
            params = [
                "params",
                "--learning_parameters.learning_rate",
                value
            ]
            command_args = train_args(
                template, default_classification_args_paths, ote_dir, root, additional=params
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert errors_dict["oob"] in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_mne(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.max_num_epochs",
            "2"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_mne_type(self, template, create_venv_fx):
        values = ["1.0", "String"]
        for value in values:
            params = [
                "params",
                "--learning_parameters.max_num_epochs",
                value
            ]
            command_args = train_args(
                template, default_classification_args_paths, ote_dir, root, additional=params
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert errors_dict["int_value"] in ret["stderr"], f"Different error message {ret['stderr']}"

    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_train_clf_lp_mne_oob(self, template, create_venv_fx):
        values = ["0", "1001"]
        for value in values:
            params = [
                "params",
                "--learning_parameters.max_num_epochs",
                value
            ]
            command_args = train_args(
                template, default_classification_args_paths, ote_dir, root, additional=params
            )
            ret = ote_common(template, root, "train", command_args)
            assert ret["exit_code"] != 0, "Exit code must not be equal 0"
            assert errors_dict["oob"] in ret["stderr"], f"Different error message {ret['stderr']}"

    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_optimize_clf_lp_es(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.enable_early_stopping",
            "False"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "optimize", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_optimize_clf_lp_es_type(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.enable_early_stopping",
            "NotBoolean"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert errors_dict["boolean_value"] in ret["stderr"], f"Different error message {ret['stderr']}"

    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_optimize_clf_lp_elf(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.enable_lr_finder",
            "False"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "optimize", command_args)
        assert ret["exit_code"] == 0, "Exit code must be equal 0"

    @pytest.fixture()
    @e2e_pytest_component
    @pytest.mark.parametrize(
        "template",
        params_values_for_be["CLASSIFICATION"],
        ids=params_ids_for_be["CLASSIFICATION"],
    )
    def test_ote_optimize_clf_lp_elf_type(self, template, create_venv_fx):
        params = [
            "params",
            "--learning_parameters.enable_lr_finder",
            "NotBoolean"
        ]
        command_args = train_args(
            template, default_classification_args_paths, ote_dir, root, additional=params
        )
        ret = ote_common(template, root, "train", command_args)
        assert ret["exit_code"] != 0, "Exit code must not be equal 0"
        assert errors_dict["boolean_value"] in ret["stderr"], f"Different error message {ret['stderr']}"
