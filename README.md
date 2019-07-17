Evaluation code and examples for the collaboration with Stefan Schmidt, Yvonne-Anne Pignolet, 
Balazs Vass, Balazs Nemeth on reusing the vnep-approx library for the fog model experiments.

Commands to run for ABB use case:
- python -m vnep_approx.cli generate_scenarios abb_scenarios.pickle scenario_generation_abb.yml
- python -m vnep_approx.cli start_experiment execution_abb.yml 0 10000 --concurrent 1 --overwrite_existing_intermediate_solutions --remove_temporary_scenarios --remove_intermediate_solutions

Commands to run for Synthetic use case:
- python -m vnep_approx.cli generate_scenarios synthetic_scenarios.pickle scenario_generation_synthetic.yml
- python -m vnep_approx.cli start_experiment execution_synthetic.yml 0 10000 --concurrent 1 --overwrite_existing_intermediate_solutions --remove_temporary_scenarios --remove_intermediate_solutions

Commands reducing the results:
- python -m evaluation_fog_model_2019.cli reduce_to_plotdata_rr_seplp_optdynvmp_cost_variant abb_scenarios_results.pickle abb_scenarios_results_reduced.pickle

Commands to plot the results:
- python -m evaluation_fog_model_2019.cli make_box_plot abb_scenarios_results_reduced.pickle "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/pseudo_random_seed" "substrate_generation/substrates/ABBUseCaseFogNetworkGenerator/sensor_actuator_loop_count" "best_integer_cost" 

# TODO
- setup.py to make it installable python package



