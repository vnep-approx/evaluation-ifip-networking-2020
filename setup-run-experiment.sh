#!/usr/bin/env bash

help=$' Script to automate the environment setup, also generates the experiment scenarios, executes them, and reduces the results.
 Sets the ALIB_EXPERIMENT_HOME environment variable needed for the framework experiments.
 Must be run from a (virtual) python environment, where the alib, gurobipy and vnep-approx packages are installed.

 Usage: ./setup-run-evaluate.sh <<experiment name>> <<scenario yaml file>> <<execution yaml file>>
 Example: ./setup-run-experiment.sh cleanup_exp results/topology-zoo/scenarios_zoo_trial.yml results/topology-zoo/fixed-routing/execution_zoo_trial_FAAP.yml'

experiment_name=$1
scenario_yaml=$2
execution_yaml=$3

if [[ "$@" == *'-h'* ]] || [[ "$@" == *'--help' ]]; then
    echo "${help}";
    exit 0;
fi;

function move_logs_and_output() {
    cd ${ALIB_EXPERIMENT_HOME}
    printf "Errors and warnings: \n"
    grep ERR log/* | head -n 50
    grep WARN log/* | head -n 50
    grep ERR log/* >> ${ALIB_EXPERIMENT_HOME}/warnings-errors.log
    grep WARN log/* >> ${ALIB_EXPERIMENT_HOME}/warnings-errors.log
	for file in output/*; 	do mv $file input/; done
	for file in log/*; 	do mv $file old_log/; done
	cd -
}

mkdir -p experiment_root/${experiment_name}
mkdir -p experiment_root/${experiment_name}/input
mkdir -p experiment_root/${experiment_name}/output
mkdir -p experiment_root/${experiment_name}/log
mkdir -p experiment_root/${experiment_name}/old_log
rm experiment_root/${experiment_name}/log/*
rm experiment_root/${experiment_name}/output/*
rm experiment_root/${experiment_name}/input/*
rm experiment_root/${experiment_name}/warnings-errors.log
touch experiment_root/${experiment_name}/warnings-errors.log
rm experiment_root/${experiment_name}/git_statuses.txt

export ALIB_EXPERIMENT_HOME=`pwd`/experiment_root/${experiment_name}
printf "ALIB_EXPERIMENT_HOME: ${ALIB_EXPERIMENT_HOME} \n"
prev_path=`pwd`
for repo in alib vnep-approx PACE2017-TrackA;
do
    cd ../${repo}
    pwd >> ${ALIB_EXPERIMENT_HOME}/git_statuses.txt
    printf "\n" >> ${ALIB_EXPERIMENT_HOME}/git_statuses.txt
    git log | head -n 50 >> ${ALIB_EXPERIMENT_HOME}/git_statuses.txt
    git status >> ${ALIB_EXPERIMENT_HOME}/git_statuses.txt
    git diff >> ${ALIB_EXPERIMENT_HOME}/git_statuses.txt
done
cd ${prev_path}

cp ${scenario_yaml} ${ALIB_EXPERIMENT_HOME}/scenario_generation.yml
cp ${execution_yaml} ${ALIB_EXPERIMENT_HOME}/execution.yml

printf "Setup of experiment ${experiment_name}: \n"
ls -hl experiment_root/${experiment_name}

printf "Generating scenarios with config: \n"
cat ${ALIB_EXPERIMENT_HOME}/scenario_generation.yml
python -m vnep_approx.cli generate_scenarios scenarios.pickle ${ALIB_EXPERIMENT_HOME}/scenario_generation.yml
move_logs_and_output

printf "Executing experiment with config: \n"
cat ${ALIB_EXPERIMENT_HOME}/execution.yml
python -m vnep_approx.cli start_experiment ${ALIB_EXPERIMENT_HOME}/execution.yml 0 10000 --concurrent 1 --overwrite_existing_intermediate_solutions --remove_temporary_scenarios --remove_intermediate_solutions --original_order
move_logs_and_output

printf "Reducing results into reduced_results.pickle \n"
python -m evaluation_ifip_networking_2020.cli reduce_to_plotdata_rr_seplp_optdynvmp_cost_variant results.pickle --output_pickle_file reduced_results.pickle
move_logs_and_output

