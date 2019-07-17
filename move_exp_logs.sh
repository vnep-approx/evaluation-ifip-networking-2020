#!/usr/bin/env bash

echo "make sure to check the logs for errors and that the generated output is correct"
for file in ${ALIB_EXPERIMENT_HOME}/log/*; 	do mv $file ${ALIB_EXPERIMENT_HOME}/old_log/ ; done
