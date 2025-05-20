#Arguments for running this script: 
# Population Size, Nø of Generations, CrossOver Factor, Tournament Size, MutationSize, ElitismFactor, Elitism Nø of Individuals, Quantidade de Experimentos
# ex: ./30tsp.sh 200 400 0.6 2 0.001 0.1 3 20
out_folder= "./outputs/"
direc=pop_$1_gen_$2_cx_$3_ts_$4_mut_$5_el_$6_exp_$7
auxbar="/"
current_out_folder=$out_folder$direc$auxbar
seed=(9529851295 45243 31130400 654 4840 65409804 651357 940684 9877154601 5357016874)
echo $current_out_folder
if [ -d "$current_out_folder" ]; then
	echo "Experiment has already been done"
fi
if [ ! -d "$current_out_folder" ]; then
	echo "Beggining run"
	mkdir -p $current_out_folder
	for sd in "${seed[@]}"
	do
		python3 AlgoritmoGeneticoMultiobjetivo.py $sd $1 $2 $3 $4 $5 $6 $7 > "$current_out_folder$sd.lol" 
	done
	wait
	#./delete_blank_space.sh $current_out_folder
	# python3 agAnalisys.py $current_out_folder $direc
fi


