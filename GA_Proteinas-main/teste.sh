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
Population=(16 20 4) 
Generations=(16 20 4) 
CrossOverFactor=(0.6 0.9 0.3)
TournamentSize=2
MutationRate=(0.2 0.4 0.2)
ElitismFactor=1
declare -g QuantidadedeExperimentos=0
experimento_contador=1
quantidade_semente=${#seed[@]}
flag="true" 
contador_geracao_arquivo=0
tempo_estimado=0


if [ -d "$current_out_folder" ]; then
    echo "Experiment has already been done"
else
    echo "Beginning run"
    mkdir -p "$current_out_folder"  # This will create all necessary directories



    for i in "${seed[@]}";
    do 
        for j in $(seq ${Population[0]} ${Population[2]} ${Population[1]})
        do
            for k in $(seq ${Generations[0]} ${Generations[2]} ${Generations[1]});
            do
                for l in  $(seq ${CrossOverFactor[0]} ${CrossOverFactor[2]} ${CrossOverFactor[1]});
                do
                    for m in $(seq ${MutationRate[0]} ${MutationRate[2]} ${MutationRate[1]});
                    do 
                        # echo "$i" "$j" "$k" "$l" "${TournamentSize}" "$m" "${ElitismFactor}" "${contador_geracao_arquivo}" "$experiment_dir" 
                        ((QuantidadedeExperimentos+=1));
                    done
                done
            done
        done
    done

    echo "A quantidade de experimetos é: "$QuantidadedeExperimentos
    read -p "digite s para continuar e n para sair (minusculo)" input
    if [ "$input" == "n" ];then
        exit 0
    fi
   
    for i in "${seed[@]}";
    do 
        for j in $(seq ${Population[0]} ${Population[2]} ${Population[1]})
        do
            for k in $(seq ${Generations[0]} ${Generations[2]} ${Generations[1]});
            do
                for l in  $(seq ${CrossOverFactor[0]} ${CrossOverFactor[2]} ${CrossOverFactor[1]});
                do
                    for m in $(seq ${MutationRate[0]} ${MutationRate[2]} ${MutationRate[1]});
                    do 
                        contador_geracao_arquivo=$((contador_geracao_arquivo+1))
                        experiment_dir="${current_out_folder}experiment_${contador_geracao_arquivo}/"
                        # echo "$i" "$j" "$k" "$l" "${TournamentSize}" "$m" "${ElitismFactor}" "${contador_geracao_arquivo}" "$experiment_dir" "${experiment_dir}${contador_geracao_arquivo}"
                        mkdir -p "$experiment_dir"
                        inicio=$(date +%s)
                        python3 mainTeste.py "$i" "$j" "$k" "$l" "${TournamentSize}" "$m" "${ElitismFactor}" "${contador_geracao_arquivo}" "$experiment_dir" > "${experiment_dir}$i.txt" 
                        fim=$(date +%s)
                        duracao=$((fim - inicio))
                        tempo_estimado=$(($tempo_estimado+$duracao))
                        experimentos_restantes=$(($QuantidadedeExperimentos-$contador_geracao_arquivo))
                        estimativa=$(($tempo_estimado/$contador_geracao_arquivo*$QuantidadedeExperimentos))
                        echo "O experimento $contador_geracao_arquivo levou $duracao segundos para execeutar"
                        
                        # modificar para minutos.
                        echo "Estimativa de tempo até o término $estimativa segundos"

                    done
                done
            done
        done
    done
    echo "Done all experiments"
    python3 avalia_Geracao.py $QuantidadedeExperimentos
fi
