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
import logging
from collections import namedtuple

from vnep_approx import treewidth_based_fog_model, greedy_border_allocation
from . import solution_reducer

try:
    import cPickle as pickle
except ImportError:
    import pickle
import matplotlib.pyplot as plt

from alib import util

# NOTE: not used currently
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

# maps from reduced key data or config file data to text which should be shown.
boxplot_shown_text = dict(
    best_integer_cost="Cost",
    total_runtime="Total running time [s]",
    preprocess_runtime="Model creation time [s]",
    optimization_runtime="Optimization time [s]",
    postprocess_runtime="Randomized Rounding time [s]",
    sensor_actuator_loop_count="N",
    node_count="Substrate network node count",
    node_resource_factor="NRF",
    edge_resource_factor="ERF",
    best_fractional_cost="Fractional cost",
    max_node_load="Max node load ratio",
    max_edge_load="Max edge load ratio",
    cost="Cost",
    relative_cost="Relative cost"
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


# Calculate feasibility ratio
calc_feas = lambda infc, totc: (totc - infc) / float(totc) if totc > 0 else 0.0


class BoxPlotter(object):

    def __init__(self, reduced_solutions_input_pickle_name,
                          output_plot_file_name=None,
                          output_path=None,
                          output_filetype="png", show_feasibility=True,
                          axis_tick_rarity=1, execution_id_to_plot=0):
        self.logger = util.get_logger(self.__class__.__name__, make_file=False, propagate=True,
                                      print_level=logging.DEBUG)

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
            self.output_path = output_path

        self.logger.info("\nWill read from ..\n\t{} \n\t\tand save plot with name {} into\n\t{}\n".
                    format(reduced_solutions_input_pickle_path, self.full_output_filename, self.output_path))

        self.logger.info("Reading pickle file at {}".format(reduced_solutions_input_pickle_path))
        with open(reduced_solutions_input_pickle_path, "rb") as input_file:
            self.reduced_scenario_solution_storage = pickle.load(input_file)
        self.show_feasibility = show_feasibility
        self.scenario_range = None
        self.axis_tick_rarity = axis_tick_rarity
        self.execution_id_to_plot = execution_id_to_plot

    def get_scenario_x_tick_label(self, scenario_id, config_param_path_for_x_axis):
        config_dict_of_aggregated_scenario = self.reduced_scenario_solution_storage.scenario_parameter_container \
            .scenario_parameter_combination_list[scenario_id]
        x_tick_label = extract_value_from_embedded_dict(config_dict_of_aggregated_scenario,
                                                        config_param_path_for_x_axis)
        return x_tick_label

    def plot_reduced_data(self, config_param_path_for_aggregate, config_param_path_for_x_axis, reduced_result_key_to_plot,
                          scenario_range):

        spc = self.reduced_scenario_solution_storage.scenario_parameter_container
        config_path_list = config_param_path_for_aggregate.split('/')
        if len(config_path_list) < 2:
            raise ValueError("Config param path {} must be at least 2 long, e.g. "
                             "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/pseudo_random_seed".
                format(config_param_path_for_aggregate))
        # make a copy of the dict so we can modify it
        scenario_id_dict_for_aggregation = dict(extract_value_from_embedded_dict(spc.scenario_parameter_dict,
                                                                            config_param_path_for_aggregate))
        if scenario_range != '':
            self.scenario_range = []
            for single_range in scenario_range.split(','):
                start = int(single_range.split('-')[0])
                stop = int(single_range.split('-')[1])
                self.scenario_range.extend([s for s in range(start, stop+1)])
            self.logger.info("Using scenarios only: {}".format(self.scenario_range))
        self.logger.info("Aggregating over parameter to scenario ID dictionary {}".format(scenario_id_dict_for_aggregation))
        there_is_at_least_one_left = {k: len(v)>0 for k, v in scenario_id_dict_for_aggregation.items()}
        x_axis_to_aggregate_data = {}
        while any(there_is_at_least_one_left.values()):
            scenario_ids_to_aggregate = []
            x_tick_label = None
            for aggregation_value, scenario_id_set in scenario_id_dict_for_aggregation.iteritems():
                if len(scenario_id_set) > 0:
                    sc_id = scenario_id_set.pop()
                    # skip scenarios is a range is given an this is not in the range
                    if self.scenario_range is not None:
                        if sc_id not in self.scenario_range:
                            continue
                    if x_tick_label is None:
                        # bind which x tick label value we are looking for
                        x_tick_label = self.get_scenario_x_tick_label(sc_id, config_param_path_for_x_axis)
                        scenario_ids_to_aggregate.append(sc_id)
                    elif x_tick_label == self.get_scenario_x_tick_label(sc_id, config_param_path_for_x_axis):
                        # only proceed if this is the same value
                        scenario_ids_to_aggregate.append(sc_id)
                    else:
                        # add back, another iteration will take care of it.
                        scenario_id_set.add(sc_id)
                else:
                    there_is_at_least_one_left[aggregation_value] = False
            if len(scenario_ids_to_aggregate) > 0:
                plot_data, infeasible_count, found_sol_count = self.collect_data_for_scenario_ids(scenario_ids_to_aggregate,
                                                                                      reduced_result_key=reduced_result_key_to_plot)
                self.logger.debug("Feasibility ratio for scenario ids {}: {}".format(scenario_ids_to_aggregate,
                                                                                     calc_feas(infeasible_count, found_sol_count)))
                if x_tick_label not in x_axis_to_aggregate_data:
                    self.logger.debug("Saving plot data {} for x tick label {}".format(plot_data, x_tick_label))
                    x_axis_to_aggregate_data[x_tick_label] = [plot_data, infeasible_count, found_sol_count]
                else:
                    self.logger.debug("Appending plot data {} for x tick label {} with existing values: {}".
                                      format(plot_data, x_tick_label, x_axis_to_aggregate_data[x_tick_label]))
                    x_axis_to_aggregate_data[x_tick_label][0].extend(plot_data)
                    x_axis_to_aggregate_data[x_tick_label][1] += infeasible_count
                    x_axis_to_aggregate_data[x_tick_label][2] += found_sol_count
        self.plot_from_aggregated_data(x_axis_to_aggregate_data, config_param_path_for_x_axis.split('/')[-1], reduced_result_key_to_plot)

    def plot_from_aggregated_data(self, x_axis_to_aggregate_data, internal_xaxis_name, internal_yaxis_name):
        self.logger.info("Plotting data: {}".format(x_axis_to_aggregate_data))
        all_fontsize = 20
        # sort the data to be plotted by their x tick values
        x_tick_with_values_sorted = sorted(x_axis_to_aggregate_data.iteritems(),
                                           key=lambda t: t[0])
        # lists of values for each box
        values_to_plot = map(lambda t: t[1][0], x_tick_with_values_sorted)
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=(all_fontsize-1)/100.0, left=(all_fontsize-2)/100.0)
        ax.tick_params(labelsize=all_fontsize)
        pos = np.array(range(len(values_to_plot))) + 1
        ax.boxplot(values_to_plot, positions=pos, whis=1.5,
                   boxprops={'linewidth': 2}, medianprops={'linewidth': 3}, whiskerprops={'linewidth': 1.8})
        x_tick_labels = map(lambda t: t[0], x_tick_with_values_sorted)
        tick_num = 0
        for idx, tick in enumerate(x_tick_labels):
            if tick_num % self.axis_tick_rarity != 0:
                x_tick_labels[idx] = ''
            tick_num += 1
        ax.set_xticklabels(x_tick_labels)
        ax.set_xlabel(boxplot_shown_text[internal_xaxis_name], fontsize=all_fontsize)
        ax.set_ylabel(boxplot_shown_text[internal_yaxis_name], fontsize=all_fontsize)


        if self.show_feasibility:
            ax.text(0.0, 1.05, 'Feasib.', horizontalalignment='center',
                    transform=ax.get_xaxis_transform(), fontsize=14)
            for x_tick, plot_data_tuple in zip(pos, x_tick_with_values_sorted):
                infeasible_count = plot_data_tuple[1][1]
                found_sol_count = plot_data_tuple[1][2]
                feasibility = calc_feas(infeasible_count, found_sol_count)
                ax.text(x_tick, 1.05, str(int(np.round(feasibility * 100)))+'%', horizontalalignment='center',
                        transform=ax.get_xaxis_transform(), fontsize=14)

        plt.savefig(os.path.join(self.output_path, self.full_output_filename))

    def collect_data_for_scenario_ids(self, scenario_id_list, reduced_result_key):
        # we are not prepared for multiple algorithms...
        alg_result_dict = self.reduced_scenario_solution_storage.algorithm_scenario_solution_dictionary
        # TODO: add checking of reduced_result_key and algorithm ID matching
        self.check_key_algo_conformity(alg_result_dict, reduced_result_key)
        if len(alg_result_dict) > 1:
            raise NotImplementedError("Algorithm result dictionary for multiple elements is not implemented: {}".format(alg_result_dict))
        reduced_result_dict = alg_result_dict.values()[0]
        values_to_aggregate = []
        infeasible_count = 0
        number_of_found_results = len(scenario_id_list)
        for sc_id in scenario_id_list:
            if sc_id in reduced_result_dict:
                if self.execution_id_to_plot in reduced_result_dict[sc_id]:
                    red_res = reduced_result_dict[sc_id][self.execution_id_to_plot]
                    if red_res.feasible:
                        values_to_aggregate.append(getattr(red_res, reduced_result_key))
                    else:
                        infeasible_count += 1
                else:
                    raise ValueError("Specified execution ID {} not found, possible values in current input: {}".
                                     format(self.execution_id_to_plot, reduced_result_dict.keys()))
            else:
                # it might happen when we executed to scenarios in two batches
                self.logger.warn("Reduced solution not found for scenario number {}, skipping "
                                 "from aggregating...".format(sc_id))
                # we do not want these to affect the feasibility ratio
                number_of_found_results -= 1
        return values_to_aggregate, infeasible_count, number_of_found_results

    def check_key_algo_conformity(self, alg_result_dict, reduced_result_key):
        alg_id = alg_result_dict.keys()[0]
        if alg_id == treewidth_based_fog_model.RandRoundSepLPOptDynVMPCollectionForFogModel.ALGORITHM_ID:
            assert reduced_result_key in solution_reducer.SepLPCostVariantSingleReducedResult._fields
        elif alg_id == greedy_border_allocation.GreedyBorderAllocationForFogModel.ALGORITHM_ID:
            assert reduced_result_key in solution_reducer.GreedyBorderAllocationReducedResult._fields
        else:
            raise ValueError("Unknown reduced result key")