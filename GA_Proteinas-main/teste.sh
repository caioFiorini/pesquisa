# Arguments for running this script:
# Population Size, Nø of Generations, CrossOver Factor, Tournament Size, Mutation Size, Elitism Factor,Quantidade de Experimentos
# ex: ./teste.sh
out_folder="./outputs/"
experimentos_folder="Experimentos/"
experimentos_out_folder=$out_folder$experimentos_folder$auxbar
current_out_folder=$experimentos_out_folder
seed=(9529851295 45243)
Population=(16 20) 
Generations=(16 20) 
CrossOverFactor=(0.6 0.9)
TournamentSize=(2 2)
MutationRate=(0.2 0.4)
ElitismFactor=(1 1)
QuantidadedeExperimentos=2
experimento_contador=1
tamanho=${#seed[@]}

if [ -d "$current_out_folder" ]; then
    echo "Experiment has already been done"
else
    echo "Beginning run"
    mkdir -p "$current_out_folder"  # This will create all necessary directories

    for ((i=1; i <= QuantidadedeExperimentos; i++ ));do
        experiment_dir="${current_out_folder}experiment_$i/"
        for ((j=0; j < tamanho; j++));do
            mkdir -p "$experiment_dir"
            python3 mainTeste.py "${seed[$j]}" "${Population[$i-1]}" "${Generations[$i-1]}" "${CrossOverFactor[$i-1]}" "${TournamentSize[$i-1]}" "${MutationRate[$i-1]}" "${ElitismFactor[$i-1]}" "$i" "$experiment_dir" > "${experiment_dir}${seed[$j]}.txt" 
        done
        echo "Done experiment $i"
    done
    echo "Done all experiments"
    python3 avalia_Geracao.py $QuantidadedeExperimentos
fi