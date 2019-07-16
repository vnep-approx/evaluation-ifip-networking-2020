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
try:
    import cPickle as pickle
except ImportError:
    import pickle

from alib import util, solutions

REQUIRED_FOR_PICKLE = solutions  # this prevents pycharm from removing this import, which is required for unpickling solutions


class RandRoundSepLPOptDynVMPCollectionCostVariantResultReducer(object):

    def __init__(self):
        self.logger = util.get_logger(self.__class__.__name__, make_file=False, propagate=True)

    def reduce_result_collection(self, randround_solutions_input_pickle_name, reduced_randround_solutions_output_pickle_name):
        randround_solutions_input_pickle_path = os.path.join(util.ExperimentPathHandler.INPUT_DIR,
                                                             randround_solutions_input_pickle_name)

        if reduced_randround_solutions_output_pickle_name is None:
            file_basename = os.path.basename(randround_solutions_input_pickle_path).split(".")[0]
            reduced_randround_solutions_output_pickle_path = os.path.join(util.ExperimentPathHandler.OUTPUT_DIR,
                                                                          file_basename + "_reduced.pickle")
        else:
            reduced_randround_solutions_output_pickle_path = os.path.join(util.ExperimentPathHandler.OUTPUT_DIR,
                                                                          randround_solutions_input_pickle_name)

        self.logger.info("\nWill read from ..\n\t{} \n\t\tand store reduced data into\n\t{}\n".format(
            randround_solutions_input_pickle_path, reduced_randround_solutions_output_pickle_path))

        self.logger.info("Reading pickle file at {}".format(randround_solutions_input_pickle_path))
        with open(randround_solutions_input_pickle_path, "rb") as f:
            sss = pickle.load(f)

        sss.scenario_parameter_container.scenario_list = None
        sss.scenario_parameter_container.scenario_triple = None

        for alg, scenario_solution_dict in sss.algorithm_scenario_solution_dictionary.iteritems():
            self.logger.info(".. Reducing results of algorithm {}".format(alg))
            for sc_id, ex_param_solution_dict in scenario_solution_dict.iteritems():
                self.logger.info("   .. handling scenario {}".format(sc_id))
                for ex_id, solution in ex_param_solution_dict.iteritems():
                    compressed = self.reduce_single_solution(solution)
                    ex_param_solution_dict[ex_id] = compressed

        self.logger.info("Writing result pickle to {}".format(reduced_randround_solutions_output_pickle_path))
        with open(reduced_randround_solutions_output_pickle_path, "w") as f:
            pickle.dump(sss, f)
        self.logger.info("All done.")
        return sss

    def reduce_single_solution(self, solution):
        return solution