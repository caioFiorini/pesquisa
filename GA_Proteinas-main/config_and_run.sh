#Define range of variations
#Arguments for running this script: 
# Population Size, Nø of Generations, CrossOver Factor, Tournament Size, MutationSize, ElitismFactor, Elitism Nø of Individuals
# ex: ./30tsp.sh 200 400 0.6 2 0.001 0.1 3
# declare the array
popsize=(500)
nbgen=(100)
crossoverfactor=(0.70)
tournsize=(2)
mutationfactor=(0.01)
elitismo=(1)

# to get the elements out of the array, use this syntax:
#   "${ARRAY[@]}" -- with the quotes

for ps in "${popsize[@]}"; do
for gen in "${nbgen[@]}"; do
for cx in "${crossoverfactor[@]}"; do
for ts in "${tournsize[@]}"; do
for mf in "${mutationfactor[@]}"; do
for el in "${elitismo[@]}"; do

	./30tsp.sh $ps $gen $cx $ts $mf $el
    
done
done
done
done  
done  
done
