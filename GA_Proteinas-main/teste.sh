# Arguments for running this script:
# Population Size, Nø of Generations, CrossOver Factor, Tournament Size, Mutation Size, Elitism Factor,Quantidade de Experimentos
# ex: ./teste.sh 16 16 0.6 2 0.2 1 2
out_folder="./outputs/"
experimentos_folder="Experimentos/"
direc="pop_$1_gen_$2_cx_$3_ts_$4_mut_$5_el_$6_exp_$7"
auxbar="/"
experimentos_out_folder=$out_folder$experimentos_folder$auxbar
current_out_folder=$experimentos_out_folder$direc$auxbar
seed=(9529851295 45243)

echo $current_out_folder

if [ -d "$current_out_folder" ]; then
    echo "Experiment has already been done"
fi

if [ ! -d "$current_out_folder" ]; then
    echo "Beginning run"
    mkdir -p "$current_out_folder"  # This will create all necessary directories

    for i in $(seq 1 $7)
    do
        experiment_dir="${current_out_folder}experiment_$i/"
        mkdir -p "$experiment_dir"

        for sd in "${seed[@]}"
        do
            python3 mainTeste.py $sd $1 $2 $3 $4 $5 $6 $i $experiment_dir > "${experiment_dir}${sd}.txt" 
        done
    done

    wait
    echo "Done"
fi