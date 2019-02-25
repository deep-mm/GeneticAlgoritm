import pandas as pd
import numpy as np
import random

columns = ["sex", "chest_pain", "blood_sugar", "restecg", "exang",
           "slope", "ca", "thal", "num","age_low", "age_med", "age_high",
           "bp_low", "bp_med", "bp_high", "bp_vhigh", "chol_low",
           "chol_med", "chol_high", "chol_vhigh", "maxrate_low", "maxrate_med",
           "maxrate_high", "ST_low", "ST_med", "ST_high"]



df = pd.read_csv("C:/Users/parak/PycharmProjects/Python/HeartDisease/output.csv", sep=',', header=None,names=columns)

df.loc[298]=[1,1,1,0,0,1,0,1,0,0.2,0.0,0.0,0.4,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.7,0.0,0.0,0.3,0.0,0.0]
#initialize population
init_population = ["00100000010000000010001","01101010100101101100110",
                   "10110101011010010111011","00111111100000100011101",
                   "01100000010101001100010","10001010101010110110111",
                   "00010101010000000011001","01011111100101101101110",
                   "10000000011010010110011","00001010100000100010101"]

#initialize crossover points
crossover_points = [3,4,6,8,10,11,13,15,16,18,20,22]

#crossover
offspring = [0 for x in range(0, len(init_population))]
def crossover():
    for i in range(0,len(init_population)-1,2):
        #selection of crossover point randomly
        selected_pt = random.choice(crossover_points)
        parent1 = init_population[i]
        parent2 = init_population[i+1]
        offspring[i] = parent1[0:selected_pt]+parent2[selected_pt:len(parent2)]
        offspring[i+1] = parent2[0:selected_pt]+parent1[selected_pt:len(parent1)]
    return offspring


def mutation(offspring_crossover):
    for i in range(0, len(offspring_crossover)):
        selected_posn = random.choice(np.arange(0, 23))
        char_offspring=list(offspring_crossover[i])
        if (char_offspring[selected_posn] is '0'):
            char_offspring[selected_posn]='1'
            #offspring_crossover[i].replace(offspring_crossover[i][selected_posn], "1")
        else:
            char_offspring[selected_posn] = '0'
        offspring_crossover[i]=''.join(char_offspring)
    init_population=offspring_crossover
    return offspring_crossover

def age_value(str,j):
    if(str=="00"):
        age=df['age_low'][j]
    elif(str=="01"):
        age=df['age_med'][j]
    else:
        age=df['age_high'][j]
    return age

def bp_value(str,j):
    if(str=="00"):
        bp=df['bp_low'][j]
    elif(str=="01"):
        bp=df['bp_med'][j]
    elif(str=="10"):
        bp=df['bp_high'][j]
    else:
        bp=df['bp_vhigh'][j]
    return bp

def chol_value(str,j):
    if(str=="00"):
        chol=df['chol_low'][j]
    elif(str=="01"):
        chol=df['chol_med'][j]
    elif(str=="10"):
        chol=df['chol_high'][j]
    else:
        chol=df['chol_vhigh'][j]
    return chol

def heartrate_value(str,j):
    if(str=="00"):
        hr=df['maxrate_low'][j]
    elif(str=="01"):
        hr=df['maxrate_med'][j]
    else:
        hr=df['maxrate_high'][j]
    return hr

def st_value(str,j):
    if(str=="00"):
        st=df['ST_low'][j]
    elif(str=="01"):
        st=df['ST_med'][j]
    else:
        st=df['ST_high'][j]
    return st

def singlebit_value(str2,j,col_name):
    st = str(df[col_name][j])
    if (str2 == st):
        value=1
    else:
        value=0
    return value

def doublebit_value(str,j,col_name):
    st = (df[col_name][j])
    if (int(str,2) == st):
        value=1
    else:
        value=0
    return value

def chestpain(str,j,col_name):
    st = (df[col_name][j])
    if ((int(str,2)+1) == st):
        value=1
    else:
        value=0
    return value


def split_str(str,j):
    str1=list(str)
    min_list=[0]*13
    min_list[0] = age_value(str1[0]+str1[1]+"",j)
    min_list[1] = singlebit_value(str1[2] + "", j, 'sex')
    min_list[3]=bp_value(str1[5]+str1[6]+"",j)
    min_list[4]=chol_value(str1[7]+str1[8]+"",j)
    min_list[7]=heartrate_value(str1[12]+str1[13]+"",j)
    min_list[9]=st_value(str1[15]+str1[16]+"",j)
    min_list[2]=chestpain(str1[3]+str1[4]+"",j,'chest_pain')
    min_list[5]=singlebit_value(str1[9]+"",j,'blood_sugar')
    min_list[6]=doublebit_value(str1[10]+str1[11]+"",j,'restecg')
    min_list[8]=singlebit_value(str1[14]+"",j,'exang')
    min_list[10]=doublebit_value(str1[17]+str1[18]+"",j,'slope')
    min_list[11]=doublebit_value(str1[19]+str1[20]+"",j,'ca')
    min_list[12]=doublebit_value(str1[21]+str1[22]+"",j,'thal')
    return min(min_list)

def min_of_df(population):
    fitness_of_population=[0]*10
    for i in range(0,len(population)):
        str=population[i]
        min_all_row=[0]*df.shape[0]
        for j in range(0,df.shape[0]):
            min_all_row[j]=split_str(str,j)
        fitness_of_population[i]=fitness(min_all_row)
    return fitness_of_population

def fitness(min_all_row):
    return sum(min_all_row)

if __name__ == '__main__':
    print("Fitness for generation",0," is: ",min_of_df(init_population))
    for i in range(1,500):
        print("Fitness for generation",i," is: ",min_of_df(mutation(crossover())))


