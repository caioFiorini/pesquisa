out_folder="./outputs/"
direc=/pop_$1_gen_$2_cx_$3_ts_$4_mut_$5_el_$6
auxbar="/"
current_out_folder=$out_folder$direc$auxbar

python3	 agAnalisys.py $current_out_folder $direc