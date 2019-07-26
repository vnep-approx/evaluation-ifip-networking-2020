#!/usr/bin/env bash

for type in total_runtime preprocess_runtime optimization_runtime postprocess_runtime best_integer_cost best_fractional_cost;
do
    for i in "1.0 0.1 0-24" "1.0 0.5 25-49" "1.0 1.0 50-74" "8.0 0.1 75-99" "8.0 0.5 100-124" "8.0 1.0 125-149" "10.0 0.1 150-174" "10.0 0.5 175-199" "10.0 1.0 200-224" "12.0 0.1 225-249" "12.0 0.5 250-274" "12.0 1.0 275-299" "1000.0 0.1 300-324" "1000.0 0.5 325-349" "1000.0 1.0 350-374";
    do
    set $i;
    python -m evaluation_fog_model_2019.cli make_box_plot scenarios_synthetic_small_result_reduced.pickle  \
                                            "request_generation/fog_app/SyntheticSeriesParallelDecomposableRequestGenerator/pseudo_random_seed" \
                                            "substrate_generation/substrates/SyntheticCactusSubstrateGenerator/node_count" \
                                            "${type}" --output_plot_file_name "node_count-to-${type}-erf$1-nrf$2" \
                                            --output_path /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep_nodecost \
                                            --show_feasibility --scenario_range $3;
    mkdir /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep_nodecost/node_count-to-${type}-erf$1-nrf$2
    mv ${ALIB_EXPERIMENT_HOME}/log/plotter* /home/balazs/university/stefan-collaboration-code/evaluation-fog-model-2019/erf_nrf_sweep_nodecost/node_count-to-${type}-erf$1-nrf$2
    done;
done

