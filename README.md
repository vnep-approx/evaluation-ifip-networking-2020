Evaluation code and examples for the collaboration with Stefan Schmidt, Matthias Rost, Yvonne-Anne Pignolet, 
Balazs Vass, Balazs Nemeth on reusing the vnep-approx library for the fog model experiments.

# Automatic experiments

setup-run-experiment.sh -- sets up an experiment home, generates, executes the scenarios and reduces the results
plot_all_from_vm.sh -- plots all supported plots of the evaluations repo #TODO: tweak to the automatic structure
plot_all_abb.sh -- plots ABB scenario examples (NOT included in paper)

# Example commands and arguments

Commands to run for ABB use case:
- python -m vnep_approx.cli generate_scenarios abb_scenarios.pickle scenario_generation_abb.yml
- python -m vnep_approx.cli start_experiment execution_abb.yml 0 10000 --concurrent 1 --overwrite_existing_intermediate_solutions --remove_temporary_scenarios --remove_intermediate_solutions

Commands to run for Synthetic use case:
- python -m vnep_approx.cli generate_scenarios synthetic_scenarios.pickle scenario_generation_synthetic.yml
- python -m vnep_approx.cli start_experiment execution_synthetic.yml 0 10000 --concurrent 1 --overwrite_existing_intermediate_solutions --remove_temporary_scenarios --remove_intermediate_solutions

Commands reducing the results:
- python -m evaluation_fog_model_2019.cli reduce_to_plotdata_rr_seplp_optdynvmp_cost_variant abb_scenarios_results.pickle abb_scenarios_results_reduced.pickle

Commands to make_and_save_plot the results:
- python -m evaluation_fog_model_2019.cli make_box_plot abb_scenarios_results_reduced.pickle "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/pseudo_random_seed" "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/sensor_actuator_loop_count" "best_integer_cost"
- python -m evaluation_fog_model_2019.cli make_box_plot scenarios_synthetic_small_result_reduced.pickle "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" "best_integer_cost" --output_plot_file_name "node_count-to-cost" --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/fixed_demand_newcostrr --show_feasibility

Plot results for ERF and NRF sweeps:
- python -m evaluation_fog_model_2019.cli make_box_plot scenarios_synthetic_small_result_inorder_numericfocus_reduced.pickle "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/node_resource_factor" "best_integer_cost" --output_plot_file_name "NRF-to-cost" --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep --show_feasibility
- python -m evaluation_fog_model_2019.cli make_box_plot scenarios_synthetic_small_result_inorder_numericfocus_reduced.pickle "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/edge_resource_factor" "best_integer_cost" --output_plot_file_name "ERF-to-cost" --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep --show_feasibility

With scenario ID restriction:
- python -m make_box_plot scenarios_synthetic_small_result_reduced.pickle "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" "best_integer_cost" --output_plot_file_name "node_count-to-cost-erf10-nrf05" --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep --show_feasibility --scenario_range 112-127
- python -m make_box_plot scenarios_synthetic_small_result_inorder_numericfocus_reduced.pickle "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" "best_integer_cost" --output_plot_file_name "node_count-to-cost-erf10-nrf01" --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep --show_feasibility --scenario_range 480-495
- python -m make_box_plot scenarios_synthetic_small_result_inorder_numericfocus_reduced.pickle "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" "best_integer_cost" --output_plot_file_name "node_count-to-cost-erf10-nrf025" --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep --show_feasibility --scenario_range 496-511

make_box_plot scenarios_synthetic_small_result_reduced.pickle "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" "best_integer_cost" --output_plot_file_name "node_count-to-cost" --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/prevm_small_scale_test --show_feasibility

# TODO
- setup.py to make it installable python package



