# Overview

This repository contains the evaluation code as well as the raw results presented in our published in IFIP Networking 2020 [1].

The implementation of the respective algorithms can be found in our separate python packages: 
- **[alib](https://github.com/vnep-approx/alib)**, providing for example the data model and the Mixed-Integer Program for the classic multi-commodity formulation, as well as
- **[vnep_approx](https://github.com/vnep-approx/vnep_approx)**, providing novel Linear Programming formulations, specifically the one based on the Dyn-VMP algorithm, as well as our proposed Randomized Rounding algorithms.

## Contents

- evaluation_fog_model_2019: CLI for the solution pickle reduction and plotting functions.
- results: raw results and plots, plotting automation scripts.

## Papers

**[1]** Balázs Németh, Yvonne-Anne Pignolet, Matthias Rost, Stefan Schmid, Balázs Vass -- "Cost-Efficient Embedding of Virtual Networks With and Without Routing Flexibility" published in IFIP Networking 2020.

# Dependencies and Requirements

The **vnep_approx** library requires Python 2.7. Required python libraries: gurobipy, numpy, cPickle, networkx , matplotlib, **[alib](https://github.com/vnep-approx/alib)** and **[vnep-approx](https://github.com/vnep-approx/vnep-approx)**.  

Gurobi must be installed and the .../gurobi64/lib directory added to the environment variable LD_LIBRARY_PATH.

Furthermore, we use Tamaki's algorithm presented in his [paper at ESA 2017](http://drops.dagstuhl.de/opus/volltexte/2017/7880/pdf/LIPIcs-ESA-2017-68.pdf) to compute tree decompositions (efficiently). The corresponding GitHub repository [TCS-Meiji/PACE2017-TrackA](https://github.com/TCS-Meiji/PACE2017-TrackA) must be cloned locally and the environment variable **PACE_TD_ALGORITHM_PATH** must be set to point the location of the repository: PACE_TD_ALGORITHM_PATH="$PATH_TO_PACE/PACE2017-TrackA".

For generating and executing (etc.) experiments, the environment variable ALIB_EXPERIMENT_HOME must be set to a path, such that the subfolders input/ output/ and log/ exist.

**Note**: Our source was only tested on Linux (specifically Ubuntu 14/16).  

# Installation

To install the package, we provide a setup script. Simply execute from within evaluation_acm_ccr_2019's root directory: 

```
pip install .
```

Furthermore, if the code base will be edited by you, we propose to install it as editable:
```
pip install -e .
```
When choosing this option, sources are not copied during the installation but the local sources are used: changes to
the sources are directly reflected in the installed package.

We generally propose to install our libraries (i.e. **alib**, **vnep_approx**, **evaluation_ifip_networking_2018**) into a virtual environment.


## Additional setup steps

For guide on creating virtual environment and setting up Tamaki's algorithm 
required for the efficient tree decomposition calculation, please refer to [evaluation_acm_ccr_2019](https://github.com/vnep-approx/evaluation-acm-ccr-2019).

# Usage

You may either use our code via our API by importing the library or via our command line interface:
```
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  make_box_plot                   Creates a boxplot for costs and total
                                  running times. Config param paths should be
                                  leading to values in the scenario config
                                  files, e.g. 'substrate_generation/substrates
                                  /ABBUseCaseFogNetworkGenerator/sensor_actuat
                                  or_loop_count'.The
                                  reduced_result_key_to_plot should be a key
                                  of <class 'evaluation_ifip_networking_2020.s
                                  olution_reducer.SepLPCostVariantSingleReduce
                                  dResult'>
  reduce_to_plotdata_rr_seplp_optdynvmp_cost_variant
                                  Extracts data to be plotted for the
                                  randomized rounding algorithms (using the
                                  separation LP and DynVMP) for the cost
                                  variant
```

Both commands have their respective help messages for their arguments:

```
Usage: cli.py make_box_plot [OPTIONS] REDUCED_SOLUTIONS_INPUT_PICKLE_NAME
                            CONFIG_PARAM_PATH_FOR_AGGREGATE
                            CONFIG_PARAM_PATH_FOR_X_AXIS
                            REDUCED_RESULT_KEY_TO_PLOT

Options:
  --output_plot_file_name TEXT    Output file name
  --output_path PATH              Output folder
  --output_filetype TEXT          Output file type
  --log_level_print TEXT          log level for stdout
  --log_level_file TEXT           log level for log file
  --show_feasibility              Whether to show feasibility percentages on
                                  top of boxplots
  --scenario_range TEXT           Range of scenarios to use for plot e.g.
                                  0-14,30-44
  --axis_tick_rarity INTEGER      Controls how rare the tick marks should be
                                  shown
  --execution_id INTEGER          Execution ID to plot
  --reduced_solutions_input_pickle_name_relative_to PATH
                                  Divide all plotted values of the
                                  reduced_solutions_input_pickle_name by the
                                  values of this pickle file
  --help                          Show this message and exit.
  
Usage: cli.py reduce_to_plotdata_rr_seplp_optdynvmp_cost_variant 
           [OPTIONS] INPUT_PICKLE_FILE

  Given a scenario solution pickle (input_pickle_file) this function
  extracts data to be plotted and writes it to --output_pickle_file. If
  --output_pickle_file is not given, a default name (derived from the
  input's basename) is derived.

  The input_file must be contained in ALIB_EXPERIMENT_HOME/input and the
  output will be written to ALIB_EXPERIMENT_HOME/output while the log is
  saved in ALIB_EXPERIMENT_HOME/log.

Options:
  --output_pickle_file PATH  file to write to
  --log_level_print TEXT     log level for stdout
  --log_level_file TEXT      log level for log file
  --help                     Show this message and exit.
```

# Step-by-step guide to reproduce results

Run the "setup-run-experiment.sh" script with the given example arguments, plot the results using the "plot_all_from_vm.sh" script.
 