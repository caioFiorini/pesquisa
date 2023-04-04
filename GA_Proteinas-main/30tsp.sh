#Arguments for running this script: 
# Population Size, Nø of Generations, CrossOver Factor, Tournament Size, MutationSize, ElitismFactor, Elitism Nø of Individuals
# ex: ./30tsp.sh 200 400 0.6 2 0.001 0.1 3


out_folder="./outputs/"
direc=pop_$1_gen_$2_cx_$3_ts_$4_mut_$5_el_$6
auxbar="/"
current_out_folder=$out_folder$direc$auxbar
seed=(9529851295 45243 31130400 654 4840 65409804 651357 940684 9877154601 5357016874)
#seed=(9529851295 45243 31130400 654 4840 65409804 651357 940684 9877154601 5357016874 605470168 231657 986795 56468 1 6547168 6876 354106 35787 98936 39836 478718 73540658 35333333333 3543470 14848 144 877879 966 666666)

echo $current_out_folder

if [ -d "$current_out_folder" ]; then
	echo "Experiment has already been done"
fi
if [ ! -d "$current_out_folder" ]; then
	echo "Beggining run"
	mkdir -p $current_out_folder
	for sd in "${seed[@]}"; do

		python AlgoritmoGeneticoMultiobjetivo.py $sd $1 $2 $3 $4 $5 $6 > "$current_out_folder$sd.lol" &

	done
	wait
	./delete_blank_space.sh $current_out_folder
	python agAnalisys.py $current_out_folder $direc
fi


