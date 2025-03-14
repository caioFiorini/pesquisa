out_folder="./outputs/"
experimentos_folder="Experimentos/"
experimentos_out_folder=$out_folder$experimentos_folder$auxbar
current_out_folder=$experimentos_out_folder

if [ -d "$current_out_folder" ]; then
    echo "Experiment has already been done"
else
    echo "Beginning run"
    mkdir -p "$current_out_folder"  # This will create all necessary directories
    contador_geracao_arquivo=$((contador_geracao_arquivo+1))
    experiment_dir="${current_out_folder}experiment_${contador_geracao_arquivo}/"
    mkdir -p "$experiment_dir"
    python3 mainTeste.py > "${experiment_dir}$i.txt" 
    wait 
    echo "Done all experiments"
    python3 avalia_Geracao.py $QuantidadedeExperimentos
fi
