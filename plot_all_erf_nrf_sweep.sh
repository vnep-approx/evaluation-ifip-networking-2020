#!/usr/bin/env bash

for type in total_runtime preprocess_runtime optimization_runtime postprocess_runtime best_integer_cost best_fractional_cost;
do
    for i in "0.4 10.0 0-24" "0.4 12.5 25-49" "0.4 15.0 50-74" "0.4 17.5 75-99" "0.4 20.0 100-124" "0.5 10.0 125-149" "0.5 12.5 150-174" "0.5 15.0 175-199" "0.5 17.5 200-224" "0.5 20.0 225-249" "0.6 10.0 250-274" "0.6 12.5 275-299" "0.6 15.0 300-324" "0.6 17.5 325-349" "0.6 20.0 350-374";
    do
    set $i;
    python -m evaluation_fog_model_2019.cli make_box_plot scenarios_synthetic_small_result_reduced.pickle  \
                                            "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" \
                                            "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" \
                                            "${type}" --output_plot_file_name "node_count-to-${type}-erf$2-nrf$1" \
                                            --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep_newcostrr \
                                            --show_feasibility --scenario_range $3;
    mkdir /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep_newcostrr/node_count-to-${type}-erf$2-nrf$1
    mv ${ALIB_EXPERIMENT_HOME}/log/plotter* /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep_newcostrr/node_count-to-${type}-erf$2-nrf$1
    done;
done

