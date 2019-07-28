#!/usr/bin/env bash

folder_name=$1

mkdir -p ${folder_name}

for p in total_runtime best_integer_cost max_edge_load max_node_load;
do

    python -m evaluation_fog_model_2019.cli make_box_plot $2 "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed"\
     "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" $p --output_plot_file_name \
     "Substrate_size-to-$p" --output_path `pwd`/${folder_name} --show_feasibility;
    for file in ${ALIB_EXPERIMENT_HOME}/log/*; 	do mv $file ${folder_name} ; done

done