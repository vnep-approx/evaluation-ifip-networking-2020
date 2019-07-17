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

import click
import os
import logging
from alib import util
from . import solution_reducer, fog_model_plots


@click.group()
def cli():
    pass


def initialize_logger(filename, log_level_print, log_level_file, allow_override=False):
    log_level_print = logging._levelNames[log_level_print.upper()]
    log_level_file = logging._levelNames[log_level_file.upper()]
    util.initialize_root_logger(filename, log_level_print, log_level_file, allow_override=allow_override)


@cli.command(short_help="Extracts data to be plotted for the randomized rounding algorithms (using the separation LP and DynVMP) for the "
                        "cost variant")
@click.argument('input_pickle_file', type=click.Path())
@click.option('--output_pickle_file', type=click.Path(), default=None, help="file to write to")
@click.option('--log_level_print', type=click.STRING, default="info", help="log level for stdout")
@click.option('--log_level_file', type=click.STRING, default="debug", help="log level for log file")
def reduce_to_plotdata_rr_seplp_optdynvmp_cost_variant(input_pickle_file, output_pickle_file, log_level_print, log_level_file):
    """ Given a scenario solution pickle (input_pickle_file) this function extracts data
        to be plotted and writes it to --output_pickle_file. If --output_pickle_file is not
        given, a default name (derived from the input's basename) is derived.

        The input_file must be contained in ALIB_EXPERIMENT_HOME/input and the output
        will be written to ALIB_EXPERIMENT_HOME/output while the log is saved in
        ALIB_EXPERIMENT_HOME/log.
    """
    util.ExperimentPathHandler.initialize(check_emptiness_log=False, check_emptiness_output=False)
    log_file = os.path.join(util.ExperimentPathHandler.LOG_DIR,
                            "reduce_{}.log".format(os.path.basename(input_pickle_file)))
    initialize_logger(log_file, log_level_print, log_level_file)
    reducer = solution_reducer.RandRoundSepLPOptDynVMPCollectionCostVariantResultReducer()
    reducer.reduce_result_collection(input_pickle_file, output_pickle_file)


@cli.command(short_help="Creates a boxplot for costs and total running times. Config param paths should be leading to values in the "
                        "scenario config files, e.g. "
                        "'substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/sensor_actuator_loop_count'."
                        "The reduced_result_key_to_plot should be a key of {}".format(solution_reducer.SepLPCostVariantSingleReducedResult))
@click.argument('reduced_solutions_input_pickle_name', type=click.Path())
@click.argument('config_param_path_for_aggregate', type=click.STRING)
@click.argument('config_param_path_for_x_axis', type=click.STRING)
@click.argument('reduced_result_key_to_plot', type=click.STRING)
@click.option('--output_plot_file_name', type=click.STRING, default=None, help="Output file name")
@click.option('--output_path', type=click.Path(), default=None, help="Output folder")
@click.option('--output_filetype', type=click.STRING, default="png", help="Output file type")
@click.option('--log_level_print', type=click.STRING, default="info", help="log level for stdout")
@click.option('--log_level_file', type=click.STRING, default="debug", help="log level for log file")
def make_box_plot(reduced_solutions_input_pickle_name,
                  config_param_path_for_aggregate, config_param_path_for_x_axis, reduced_result_key_to_plot,
                  output_plot_file_name, output_path, output_filetype, log_level_print, log_level_file):
    util.ExperimentPathHandler.initialize(check_emptiness_log=False, check_emptiness_output=False)
    log_file = os.path.join(util.ExperimentPathHandler.LOG_DIR,
                            "plotter_{}_{}.log".format(os.getpid(),
                                                       os.path.basename(reduced_solutions_input_pickle_name)))
    initialize_logger(log_file, log_level_print, log_level_file)
    plotter = fog_model_plots.BoxPlotter(reduced_solutions_input_pickle_name,
                                         output_plot_file_name, output_path, output_filetype)
    plotter.plot_reduced_data(config_param_path_for_aggregate, config_param_path_for_x_axis, reduced_result_key_to_plot)


if __name__ == '__main__':
    cli()
