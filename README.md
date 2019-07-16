Evaluation code and examples for the collaboration with Stefan Schmidt, Yvonne-Anne Pignolet, 
Balazs Vass, Balazs Nemeth on reusing the vnep-approx library for the fog model experiments.

Commands to run for ABB use case:
- python -m vnep_approx.cli generate_scenarios abb_scenarios.pickle scenario_generation_abb.yml
- python -m vnep_approx.cli start_experiment execution_abb.yml 0 10000 --concurrent 1 --overwrite_existing_intermediate_solutions --remove_temporary_scenarios --remove_intermediate_solutions

Commands to run for Synthetic use case:
- python -m vnep_approx.cli generate_scenarios synthetic_scenarios.pickle scenario_generation_synthetic.yml
- python -m vnep_approx.cli start_experiment execution_synthetic.yml 0 10000 --concurrent 1 --overwrite_existing_intermediate_solutions --remove_temporary_scenarios --remove_intermediate_solutions

# TODO
- setup.py to make it installable python package



