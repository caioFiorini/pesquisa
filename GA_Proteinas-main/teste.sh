# Arguments for running this script:
# Population Size, Nø of Generations, CrossOver Factor, Tournament Size, Mutation Size, Elitism Factor,Quantidade de Experimentos
# ex: ./teste.sh
out_folder="./outputs/"
experimentos_folder="Experimentos/"
experimentos_out_folder=$out_folder$experimentos_folder$auxbar
current_out_folder=$experimentos_out_folder
seed=(9529851295 45243)
teste=0
# min max iterador <- O experimento deve seguir essa ideia.
Population=(16 20 1) 
Generations=(16 20 ) 
CrossOverFactor=(0.6 0.9)
TournamentSize=2
MutationRate=(0.2 0.4)
ElitismFactor=1
QuantidadedeExperimentos=0
experimento_contador=1
quantidade_semente=${#seed[@]}
flag="true" 
contador_geracao_arquivo=0


if [ -d "$current_out_folder" ]; then
    echo "Experiment has already been done"
else
    # echo "Beginning run"
    # mkdir -p "$current_out_folder"  # This will create all necessary directories



    for i in "${seed[@]}";
    do 
        for j in $(seq ${Population[0]} ${Population[2]} $(("${Population[1]}"-1)))
        do
            for k in $(seq ${Generations[0]} ${Generations[2]} $(("${Generations[1]}"-1)) );
            do
                for l in  $(seq ${CrossOverFactor[0]} ${CrossOverFactor[2]} $(("${CrossOverFactor[1]}"-0.1 | bc)));
                do
                    for m in $(seq ${MutationRate[0]} ${MutationRate[2]} $(("${MutationRate[1]}"-0.1 | bc)));
                    do 
                        QuantidadedeExperimentos = QuantidadeExperimentos + 1;
                    done
                done
            done
        done
    done

    echo "A quantidade de experimetos é: ""${QuantidadeExperimentos}"
    read -p "digite s para sim e n para não (minusculo)" input
    if [ "$input" == "n" ];then
        exit 0
    fi

    for i in "${seed[@]}";
    do 
        for (( j = Population[0]; j < Population[1]; j = j + Population[2]));
        do
            for (( k = Generations[0]; k < Generations[1]; k = k + Generations[2]));
            do
                for (( l = CrossOverFactor[0]; l < CrossOverFactor[1]; l = l + CrossOverFactor[2]));
                do
                    for (( m = MutationRate[0]; m < MutationRate[1]; m = m + MutationRate[2]));
                    do 
                        contador_geracao_arquivo=$((contador_geracao_arquivo+1))
                        experiment_dir="${current_out_folder}experiment_${contador_geracao_arquivo}/"
                        echo "$i" "$j" "$k" "$l" "${TournamentSize}" "$m" "${ElitismFactor}" "${contador_geracao_arquivo}" "$experiment_dir" "${experiment_dir}${contador_geracao_arquivo}"
                        # python3 mainTeste.py "$i" "$j" "$k" "$l" "${TournamentSize}" "$m" "${ElitismFactor}" "${contador_geracao_arquivo}" "$experiment_dir" "${experiment_dir}${contador_geracao_arquivo}" 
                    done
                done
            done
        done
    done

    echo "Done all experiments"
    python3 avalia_Geracao.py $QuantidadedeExperimentos
fi


    # for ((i=0; i <= QuantidadedeExperimentos; i++ ));do
    #     
    #     for ((j=0; j < tamanho; j++));do
    #         mkdir -p "$experiment_dir"
    #         python3 mainTeste.py "${seed[$j]}" "${Population[$i-1]}" "${Generations[$i-1]}" "${CrossOverFactor[$i-1]}" "${TournamentSize[$i-1]}" "${MutationRate[$i-1]}" "${ElitismFactor[$i-1]}" "$i" "$experiment_dir" > "${experiment_dir}${seed[$j]}.txt" 
    #     done
    #     echo "Done experiment $i"
    # done