#!/usr/bin/env bash

experiment_name=$1
export ALIB_EXPERIMENT_HOME=`pwd`/experiment_root/${experiment_name}
mkdir -p ${ALIB_EXPERIMENT_HOME}/plots
mkdir -p ${ALIB_EXPERIMENT_HOME}/plots/log

for exid in 0 1;
do
    for p in total_runtime best_fractional_cost best_integer_cost max_edge_load \
              max_node_load preprocess_runtime optimization_runtime postprocess_runtime relative_cost;
    do
        python -m evaluation_fog_model_2019.cli make_box_plot reduced_results.pickle "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/pseudo_random_seed"\
                "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/sensor_actuator_loop_count"\
                $p --output_plot_file_name "N-to-$p-execution-${exid}" --output_path ${ALIB_EXPERIMENT_HOME}/plots --show_feasibility --execution_id ${exid} ;
            for file in ${ALIB_EXPERIMENT_HOME}/log/*; 	do mv $file ${ALIB_EXPERIMENT_HOME}/plots/log; done
    done
done