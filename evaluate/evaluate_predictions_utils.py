# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
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
"""Utils for evaluating predictions."""

from language.compir.dataset_parsers.dataset_parser import Example
from language.compir.utils import dataset_parser_utils
from language.compir.utils import io_utils
import re


def find_structure(s):
    """parse SPARQL queries into triple, prefix and filter sections"""

    triples = re.findall('\??\w\d wdt\S+ \S+', s)
    prefix = re.findall('(.+) {', s)
    filters = re.findall('FILTER \( \S+ \!\= \S+ \)', s)
    return set(triples), set(prefix), set(filters)


def write_output(predictions, prediction_path, output_path):
    filename = prediction_path.split('/')[-1]
    output_file = output_path + '/reversed_' + filename
    with open(output_file, 'w') as f:
        f.writelines([p + '\n' for p in predictions])


def calc_exact_match(test_examples,
                     predictions,
                     is_print_error=False):
    """Calculates exact match accuracy of triples, prefix and filters
    for a test set and its corresponding predictions."""

    correct = 0
    incorrect = 0

    for test_example, prediction in zip(test_examples, predictions):
        utterance = test_example.utterance
        gold_program = test_example.program

        if prediction is not None and find_structure(prediction.lower()) == find_structure(gold_program.lower()):
            """check if triples, prefix and filters match"""
            correct += 1
        else:
            incorrect += 1
            if is_print_error:
                print("Incorrect: %s.\nTarg: %s\nPred: %s" %
                      (utterance, gold_program, prediction))

    accuracy = float(correct) / float(correct + incorrect)
    print("correct: %s" % correct)
    print("incorrect: %s" % incorrect)
    print("accuracy: %s" % accuracy)
    return accuracy


def evaluate_predictions(dataset, transformation,
                         train_data_path, dev_data_path, test_data_path,
                         prediction_path, output_path):
    """Postprocesses predictions and calculates accuracy against gold programs."""
    train_examples, dev_examples, test_examples, predictions = io_utils.load_data(
        train_data_path, dev_data_path, test_data_path, prediction_path)
    parser = dataset_parser_utils.get_parser(dataset)(train_examples, dev_examples, test_examples)
    is_rir = True if transformation in ["rir", "lird_rir2", "lirind_rir2"
                                        ] else False
    predictions_postprocessed = parser.postprocess_full(predictions, is_rir)
    accuracy = calc_exact_match(test_examples, predictions_postprocessed)

    write_output(predictions_postprocessed, prediction_path, output_path)
    return predictions_postprocessed, accuracy
