import csv
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import sys

path = sys.argv[1]
data1 = [np.array([]) for _ in range(2)]
data2 = [np.array([]) for _ in range(2)]
data3 = [np.array([]) for _ in range(2)]
data4 = [np.array([]) for _ in range(2)]
data5 = [np.array([]) for _ in range(2)]
data6 = [np.array([]) for _ in range(2)]
data7 = [np.array([]) for _ in range(2)]
data8 = [np.array([]) for _ in range(2)]
data9 = [np.array([]) for _ in range(2)]
itr = 0
for filename in glob.glob(os.path.join(path, '*.lol')):
    with open(filename) as inf:
        reader = csv.reader(inf, delimiter="\t")
        aux1 = list(zip(*reader))
        data1[itr] = aux1[0][0:]#geracoes        
        data2[itr] = aux1[1][0:]#populacao
        data3[itr] = aux1[2][0:]#repetidos
        data4[itr] = aux1[3][0:]#piores
        data5[itr] = aux1[4][0:]#melhores
        data6[itr] = aux1[5][0:]#desv_padrao
        data7[itr] = aux1[7][0:]#Fit_max
        data8[itr] = aux1[9][0:]#Fit_medio
        data9[itr] = aux1[11][0:]#Fit_min
        itr = itr+1


minvalues1 = np.mean(np.array(data9).astype(float), axis=0)
meanvalues1 = np.mean(np.array(data8).astype(float), axis=0)
maxvalues1 = np.mean(np.array(data7).astype(float), axis=0)
desv_values = np.mean(np.array(data6).astype(float), axis=0)
melhores = np.mean(np.array(data5).astype(float), axis=0)
aux2 = []

for i in data4:
    for j in i:
        for k in j:
            if(k == '0' or k == '1'):
                aux2.append(k)

aux2 = [float(i) for i in aux2]
piores = np.mean(np.array(aux2).astype(float), axis=0)

repeated_individuals = np.mean(np.array(data3).astype(float), axis=0)
population = np.mean(np.array(data2).astype(float), axis=0)
diversidade = [(1-(i/j))*100 for i,j in zip(repeated_individuals,population)]
piores_values = [(i/j)*100 for i,j in zip(aux2,population)]
melhores_values = [(i/j)*100 for i,j in zip(melhores,population)]
geracoes_values = np.mean(np.array(data1).astype(float), axis=0)
print("minvalues1 + meanvalues1 + maxvalues1 + desv_values + melhores + piores + repeated_individuals + population + diversidade + piores_values + melhores_values")
print(minvalues1 + meanvalues1 + maxvalues1 + desv_values + melhores + piores + repeated_individuals + population + diversidade + piores_values + melhores_values)


ax = plt.subplot()
plot_minimo = ax.plot(minvalues1,color='#B22222', label="Minimo")
plot_maximo = ax.plot(maxvalues1,color='#006400', label="Maximo")
plot_medio = ax.plot(meanvalues1,color='#FF8C00', label="Media")
ax2 = ax.twinx()
ax2.set_ylabel('Diversity/Better/Worse')
ax2.yaxis.set_ticks(np.arange(0, 101, 5))
#range bays29
#ax.yaxis.set_ticks(np.arange(0, 0.0004951, 0.00002475))

#range brazil58
#ax.yaxis.set_ticks(np.arange(0, 0.00003939, 0.000001969))

#range gr96
#ax.yaxis.set_ticks(np.arange(0, 0.00001812, 0.0000009055))

#range bier127
#ax.yaxis.set_ticks(np.arange(0, 0.00000846, 0.00000042271858))
ax2.plot(diversidade,'|',color='#CC00CC', label="Diversidade")
ax2.plot(melhores_values,'r|', label="Piores")#melhores pais
ax2.plot(piores_values,'b|', label="Melhores")#piores pais, ta ao contrario mesmo
ax.set_ylabel('Fitness')
ax.set_xlabel('NofGenerations')

# ask matplotlib for the plotted objects and their labels
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=6, mode="expand", borderaxespad=0., fontsize = 'small')
plt.savefig(path+sys.argv[0]+'_plot.png')

#with open(path+'avg_min_Fitness.csv', 'wb') as myfile:
#    wr = csv.writer(myfile, delimiter="\t")
#   wr.writerow(minvalues1)
#ith open(path+'diversidade.csv', 'wb') as myfile:
#   wr = csv.writer(myfile, delimiter="\t")
#   wr.writerow(population)
#ith open(path+'repeated_ind.csv', 'wb') as myfile:
#   wr = csv.writer(myfile, delimiter="\t")
#   wr.writerow(repeated_individuals)
