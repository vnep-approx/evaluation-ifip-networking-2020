#!/usr/bin/env bash

folder_name=$1

mkdir -p ${folder_name}

for p in total_runtime best_fractional_cost best_integer_cost max_edge_load \
          max_node_load preprocess_runtime optimization_runtime postprocess_runtime relative_cost;
do
    python -m evaluation_fog_model_2019.cli make_box_plot $2 "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed"\
     "substrate_generation/substrates/TopologyZooReader/topology" $p --output_plot_file_name \
     "Substrate_size-to-$p" --output_path `pwd`/${folder_name} --axis_tick_rarity 1 --output_filetype png ;
    for file in ${ALIB_EXPERIMENT_HOME}/log/*; 	do mv $file ${folder_name} ; done
done


