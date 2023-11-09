output_folder="./outputs/"
directory_name=pop_$1_gen_$2_cx_$3_ts_$4_mut_$5_el_$6
path_separator="/"
current_output_folder=$output_folder$directory_name$path_separator
# seeds=(9529851295 45243 31130400 654 4840 65409804 651357 940684 9877154601 5357016874)
#seeds=(9529851295 45243 31130400 654 4840 65409804 651357 940684 9877154601 5357016874 605470168 231657 986795 56468 1 6547168 6876 354106 35787 98936 39836 478718 73540658 35333333333 3543470 14848 144 877879 966 666666)
seeds=(9529851295 45243 31130400)
echo $current_output_folder
if [ -d "$current_output_folder" ]; then
	echo "Experiment has already been done"
else
	echo "Beginning run"
	mkdir -p "$current_output_folder"
	for seed in "${seeds[@]}"; do
		echo "Running seed $seed"
		python3 main.py "$seed" "$1" "$2" "$3" "$4" "$5" "$6" > "$current_output_folder$seed.lol"
	done
	wait
	#./delete_blank_space.sh "$current_output_folder"
	echo "Plotting data..."
	# python3 agAnalysis.py "$current_output_folder" "$directory_name"
fi
