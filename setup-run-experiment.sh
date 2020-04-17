#!/usr/bin/env bash

# Must be run from a (virtual) python environment, where the alib, and vnep-approx packages are installed.
# Sets the ALIB_EXPERIMENT_HOME environment variable needed for the framework experiments.
# Generates the experiment scenarios, executes them, and reduces the results.

# Usage: ./setup-run-evaluate.sh <<experiment name>> <<scenario yaml file>> <<execution yaml file>>

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

mkdir -p experiment_root/$1
mkdir -p experiment_root/$1/input
mkdir -p experiment_root/$1/output
mkdir -p experiment_root/$1/log
mkdir -p experiment_root/$1/old_log
rm experiment_root/$1/log/*
rm experiment_root/$1/output/*
rm experiment_root/$1/input/*
rm experiment_root/$1/warnings-errors.log
touch experiment_root/$1/warnings-errors.log
rm experiment_root/$1/git_statuses.txt

export ALIB_EXPERIMENT_HOME=`pwd`/experiment_root/$1
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

cp $2 ${ALIB_EXPERIMENT_HOME}/scenario_generation.yml
cp $3 ${ALIB_EXPERIMENT_HOME}/execution.yml

printf "Setup of experiment $1: \n"
ls -hl experiment_root/$1

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

