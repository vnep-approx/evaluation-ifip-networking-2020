# MIT License
#
# Copyright (c) 2019 Balazs Nemeth
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import numpy as np
from collections import namedtuple
try:
    import cPickle as pickle
except ImportError:
    import pickle
import matplotlib.pyplot as plt

from alib import util

AggregatedData = namedtuple(
    "AggregatedData",
    [
        "min",
        "mean",
        "max",
        "std_dev",
        "value_count"
    ]
)


# TODO: these could be input arguments too
boxplot_options = dict(
    title="Cost",
    x_axis_label="N"
)


def get_aggregated_data(list_of_values):
    _min = np.min(list_of_values)
    _mean = np.mean(list_of_values)
    _max = np.max(list_of_values)
    _std_dev = np.std(list_of_values)
    _value_count = len(list_of_values)
    return AggregatedData(min=_min,
                          max=_max,
                          mean=_mean,
                          std_dev=_std_dev,
                          value_count=_value_count)


def extract_value_from_embedded_dict(embedded_dict, key_seq_str, sep='/'):
    split_key_seq = key_seq_str.split(sep)
    dict_value = embedded_dict[split_key_seq[0]]
    for i in range(1, len(split_key_seq)):
        dict_value = dict_value[split_key_seq[i]]
    return dict_value


class BoxPlotter(object):

    def __init__(self, reduced_solutions_input_pickle_name,
                          output_plot_file_name=None,
                          output_path=None,
                          output_filetype="png"):
        self.logger = util.get_logger(self.__class__.__name__, make_file=False, propagate=True)
        reduced_solutions_input_pickle_path = os.path.join(
            util.ExperimentPathHandler.INPUT_DIR,
            reduced_solutions_input_pickle_name
        )

        if output_plot_file_name is None:
            self.full_output_filename = os.path.basename(reduced_solutions_input_pickle_path).split(".")[0] + \
                                   "_plotted." + output_filetype
        else:
            self.full_output_filename = output_plot_file_name + "." + output_filetype
        if output_path is None:
            self.output_path = util.ExperimentPathHandler.OUTPUT_DIR
        else:
            self.output_path = os.path.join(util.ExperimentPathHandler.OUTPUT_DIR,
                                       reduced_solutions_input_pickle_name)

        self.logger.info("\nWill read from ..\n\t{} \n\t\tand save plot with name {} into\n\t{}\n".
                    format(reduced_solutions_input_pickle_path, self.full_output_filename, self.output_path))

        self.logger.info("Reading pickle file at {}".format(reduced_solutions_input_pickle_path))
        with open(reduced_solutions_input_pickle_path, "rb") as input_file:
            self.reduced_scenario_solution_storage = pickle.load(input_file)

    # TODO: make config_param_path_for_x_axis input
    def plot_reduced_data(self, config_param_path_for_aggregate,
                          config_param_path_for_x_axis="substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/sensor_actuator_loop_count"):
        spc = self.reduced_scenario_solution_storage.scenario_parameter_container
        config_path_list = config_param_path_for_aggregate.split('/')
        if len(config_path_list) < 2:
            raise ValueError("Config param path {} must be at least 2 long, e.g. "
                             "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/pseudo_random_seed".
                format(config_param_path_for_aggregate))
        # make a copy of the dict so we can modify it
        scenario_id_dict_for_aggregation = dict(extract_value_from_embedded_dict(spc.scenario_parameter_dict,
                                                                            config_param_path_for_aggregate))
        self.logger.info("Aggregating over parameter to scenario ID dictionary {}".format(scenario_id_dict_for_aggregation))
        there_is_at_least_one_left = True
        x_axis_to_aggregate_data = {}
        while there_is_at_least_one_left:
            scenario_ids_to_aggregate = []
            for aggregation_value, scenario_id_set in scenario_id_dict_for_aggregation.iteritems():
                if len(scenario_id_set) > 0:
                    scenario_ids_to_aggregate.append(scenario_id_set.pop())
            if len(scenario_ids_to_aggregate) > 0:
                # TODO: make 2nd parameter input
                aggegate_data, feasibility_ratio = self.aggregate_data_for_scenario_ids(scenario_ids_to_aggregate, "best_integer_cost")
                self.logger.debug("Feasibility ratio for scenario ids {}: {}".format(scenario_ids_to_aggregate, feasibility_ratio))
                # NOTE: x_tick_label should be the same for all aggregated scenarios (might be checked...)
                config_dict_of_aggregated_scenario = self.reduced_scenario_solution_storage.scenario_parameter_container\
                                                            .scenario_parameter_combination_list[scenario_ids_to_aggregate[0]]
                x_tick_label = extract_value_from_embedded_dict(config_dict_of_aggregated_scenario,
                                                                config_param_path_for_x_axis)
                x_axis_to_aggregate_data[x_tick_label] = aggegate_data
            else:
                there_is_at_least_one_left = False
        self.plot_from_aggregated_data(x_axis_to_aggregate_data)

    def plot_from_aggregated_data(self, x_axis_to_aggregate_data):
        # lists of values for each box
        values_to_plot = x_axis_to_aggregate_data.values()
        fig, ax = plt.subplots()
        pos = np.array(range(len(values_to_plot))) + 1
        ax.boxplot(values_to_plot, positions=pos)
        # TODO: use keys as x axis label
        plt.show()
        pass

    def aggregate_data_for_scenario_ids(self, scenario_id_list, reduced_result_key):
        # we are not prepared for multiple algorithms...
        alg_result_dict = self.reduced_scenario_solution_storage.algorithm_scenario_solution_dictionary
        if len(alg_result_dict) > 1:
            raise NotImplementedError("Algorithm result dictionary for multiple elements is not implemented: {}".format(alg_result_dict))
        reduced_result_dict = alg_result_dict.values()[0]
        values_to_aggregate = []
        infeasible_count = 0
        for sc_id in scenario_id_list:
            # TODO: only one execution id is considered, we might shuold aggregate for all execution ID-s?
            if sc_id in reduced_result_dict:
                red_res = reduced_result_dict[sc_id][0]
                if red_res.feasible:
                    values_to_aggregate.append(getattr(red_res, reduced_result_key))
                else:
                    infeasible_count += 1
            else:
                # TODO: why this might happen?
                self.logger.warn("Reduced solution not found for scenario number {}, skipping from aggregating...".format(sc_id))
        # TODO: fix names, input output
        feasibility_ratio = float(len(scenario_id_list) - infeasible_count) / len(scenario_id_list)
        return values_to_aggregate, feasibility_ratio
