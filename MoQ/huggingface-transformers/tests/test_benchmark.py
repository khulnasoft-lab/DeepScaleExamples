# Copyright 2020 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import unittest
from pathlib import Path

from transformers import AutoConfig, is_torch_available
from transformers.testing_utils import require_torch, torch_device

if is_torch_available():
    from transformers import PyTorchBenchmark, PyTorchBenchmarkArguments


@require_torch
class BenchmarkTest(unittest.TestCase):
    def check_results_dict_not_empty(self, results):
        for model_result in results.values():
            for batch_size, sequence_length in zip(model_result["bs"],
                                                   model_result["ss"]):
                result = model_result["result"][batch_size][sequence_length]
                self.assertIsNotNone(result)

    def test_inference_no_configs(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=False,
            inference=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args)
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_inference_result)
        self.check_results_dict_not_empty(results.memory_inference_result)

    def test_inference_no_configs_only_pretrain(self):
        MODEL_ID = "sshleifer/tiny-distilbert-base-uncased-finetuned-sst-2-english"
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=False,
            inference=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
            only_pretrain_model=True,
        )
        benchmark = PyTorchBenchmark(benchmark_args)
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_inference_result)
        self.check_results_dict_not_empty(results.memory_inference_result)

    def test_inference_torchscript(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=False,
            inference=True,
            torchscript=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args)
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_inference_result)
        self.check_results_dict_not_empty(results.memory_inference_result)

    @unittest.skipIf(torch_device == "cpu", "Cant do half precision")
    def test_inference_fp16(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=False,
            inference=True,
            fp16=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args)
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_inference_result)
        self.check_results_dict_not_empty(results.memory_inference_result)

    def test_inference_no_model_no_architectures(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        config = AutoConfig.from_pretrained(MODEL_ID)
        # set architectures equal to `None`
        config.architectures = None
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=True,
            inference=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args, configs=[config])
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_inference_result)
        self.check_results_dict_not_empty(results.memory_inference_result)

    def test_train_no_configs(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=True,
            inference=False,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args)
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_train_result)
        self.check_results_dict_not_empty(results.memory_train_result)

    @unittest.skipIf(torch_device == "cpu", "Can't do half precision")
    def test_train_no_configs_fp16(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=True,
            inference=False,
            sequence_lengths=[8],
            batch_sizes=[1],
            fp16=True,
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args)
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_train_result)
        self.check_results_dict_not_empty(results.memory_train_result)

    def test_inference_with_configs(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        config = AutoConfig.from_pretrained(MODEL_ID)
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=False,
            inference=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args, configs=[config])
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_inference_result)
        self.check_results_dict_not_empty(results.memory_inference_result)

    def test_inference_encoder_decoder_with_configs(self):
        MODEL_ID = "sshleifer/tinier_bart"
        config = AutoConfig.from_pretrained(MODEL_ID)
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=False,
            inference=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args, configs=[config])
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_inference_result)
        self.check_results_dict_not_empty(results.memory_inference_result)

    def test_train_with_configs(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        config = AutoConfig.from_pretrained(MODEL_ID)
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=True,
            inference=False,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args, configs=[config])
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_train_result)
        self.check_results_dict_not_empty(results.memory_train_result)

    def test_train_encoder_decoder_with_configs(self):
        MODEL_ID = "sshleifer/tinier_bart"
        config = AutoConfig.from_pretrained(MODEL_ID)
        benchmark_args = PyTorchBenchmarkArguments(
            models=[MODEL_ID],
            training=True,
            inference=True,
            sequence_lengths=[8],
            batch_sizes=[1],
            multi_process=False,
        )
        benchmark = PyTorchBenchmark(benchmark_args, configs=[config])
        results = benchmark.run()
        self.check_results_dict_not_empty(results.time_train_result)
        self.check_results_dict_not_empty(results.memory_train_result)

    def test_save_csv_files(self):
        MODEL_ID = "sshleifer/tiny-gpt2"
        with tempfile.TemporaryDirectory() as tmp_dir:
            benchmark_args = PyTorchBenchmarkArguments(
                models=[MODEL_ID],
                training=True,
                inference=True,
                save_to_csv=True,
                sequence_lengths=[8],
                batch_sizes=[1],
                inference_time_csv_file=os.path.join(tmp_dir, "inf_time.csv"),
                train_memory_csv_file=os.path.join(tmp_dir, "train_mem.csv"),
                inference_memory_csv_file=os.path.join(tmp_dir, "inf_mem.csv"),
                train_time_csv_file=os.path.join(tmp_dir, "train_time.csv"),
                env_info_csv_file=os.path.join(tmp_dir, "env.csv"),
                multi_process=False,
            )
            benchmark = PyTorchBenchmark(benchmark_args)
            benchmark.run()
            self.assertTrue(
                Path(os.path.join(tmp_dir, "inf_time.csv")).exists())
            self.assertTrue(
                Path(os.path.join(tmp_dir, "train_time.csv")).exists())
            self.assertTrue(
                Path(os.path.join(tmp_dir, "inf_mem.csv")).exists())
            self.assertTrue(
                Path(os.path.join(tmp_dir, "train_mem.csv")).exists())
            self.assertTrue(Path(os.path.join(tmp_dir, "env.csv")).exists())

    def test_trace_memory(self):
        MODEL_ID = "sshleifer/tiny-gpt2"

        def _check_summary_is_not_empty(summary):
            self.assertTrue(hasattr(summary, "sequential"))
            self.assertTrue(hasattr(summary, "cumulative"))
            self.assertTrue(hasattr(summary, "current"))
            self.assertTrue(hasattr(summary, "total"))

        with tempfile.TemporaryDirectory() as tmp_dir:
            benchmark_args = PyTorchBenchmarkArguments(
                models=[MODEL_ID],
                training=True,
                inference=True,
                sequence_lengths=[8],
                batch_sizes=[1],
                log_filename=os.path.join(tmp_dir, "log.txt"),
                log_print=True,
                trace_memory_line_by_line=True,
                multi_process=False,
            )
            benchmark = PyTorchBenchmark(benchmark_args)
            result = benchmark.run()
            _check_summary_is_not_empty(result.inference_summary)
            _check_summary_is_not_empty(result.train_summary)
            self.assertTrue(Path(os.path.join(tmp_dir, "log.txt")).exists())
