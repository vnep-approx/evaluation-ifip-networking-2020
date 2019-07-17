#!/usr/bin/env bash

mkdir -p synthetic_plots

python -m evaluation_fog_model_2019.cli make_box_plot $1 "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" "best_integer_cost" --output_plot_file_name "Substrate_size-to-cost" --output_path `pwd`/synthetic_plots
./move_exp_logs.sh

python -m evaluation_fog_model_2019.cli make_box_plot $1 "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" "total_runtime" --output_plot_file_name "Substrate_size-to-time" --output_path `pwd`/synthetic_plots
./move_exp_logs.sh
