#!/usr/bin/env bash

mkdir -p /abb_plots

python -m evaluation_fog_model_2019.cli make_box_plot $1 "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/pseudo_random_seed" "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/sensor_actuator_loop_count" "best_integer_cost" --output_plot_file_name "N-to-cost" --output_path `pwd`/abb_plots
./move_exp_logs.sh

python -m evaluation_fog_model_2019.cli make_box_plot $1 "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/pseudo_random_seed" "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/sensor_actuator_loop_count" "total_runtime" --output_plot_file_name "N-to-time" --output_path `pwd`/abb_plots
./move_exp_logs.sh
