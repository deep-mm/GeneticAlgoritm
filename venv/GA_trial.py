import pandas as pd
import numpy as np
import random

columns = ["sex", "chest_pain", "blood_sugar", "restecg", "exang",
           "slope", "ca", "thal", "num","age_low", "age_med", "age_high",
           "bp_low", "bp_med", "bp_high", "bp_vhigh", "chol_low",
           "chol_med", "chol_high", "chol_vhigh", "maxrate_low", "maxrate_med",
           "maxrate_high", "ST_low", "ST_med", "ST_high"]

singlebit = [2,7]
doublebit=[0,3,5,8,10]

df = pd.read_csv("/Users/deepmehta/Deep/Projects/Parakh/venv/output.csv", sep=',', header=None,names=columns)

df=df.drop(["chest_pain","restecg", "exang",
           "slope", "ca", "thal", "num"],axis=1)

init_population = ["001000010000","011010100101",
                   "101101011010","001111100000",
                   "011000010101","100010101010",
                   "000101010000","010111100101",
                   "100000011010","000010100000"]

#initialize crossover points
crossover_points = [3,4,6,8,9,11]

def crossover_updated(population_old,fitness_population_old,selected_population):
    offspring = [""]*2
    selected_pt = random.choice(crossover_points)-1 #since points are from 1 to 12 and array index start with 0
    parent1 = selected_population[0]
    parent2 = selected_population[1]
    offspring[0] = parent1[0:selected_pt]+parent2[selected_pt:len(parent2)]
    offspring[1] = parent2[0:selected_pt]+parent1[selected_pt:len(parent1)]

    if not check_validity(offspring[0]):
        pop_index = population_old.index(parent1)
        select_pop = select_population(population_old,fitness_population_old,True,pop_index)
        offspring = crossover_updated(population_old,fitness_population_old,select_pop)
        return offspring

    elif not check_validity(offspring[1]):
        pop_index = population_old.index(parent1)
        select_pop = select_population(population_old,fitness_population_old,True, pop_index)
        offspring = crossover_updated(population_old,fitness_population_old,select_pop)
        return offspring

    else:
        return offspring


def select_population(population_old,fitness_population_old,ignore,j):
    rand = random.uniform(0.0,1.0)
    select_population_list = [""]*2
    new_list = [0]*10

    for i in range(0, len(fitness_population_old)):
        new_list[i] = abs(rand-fitness_population_old[i])

    if ignore:
        new_list[j] = 1

    min_index = new_list.index(min(new_list))
    select_population_list[0] = population_old[min_index]
    new_list[min_index] = 1

    min_index = new_list.index(min(new_list))
    select_population_list[1] = population_old[min_index]
    return select_population_list


def check_validity(offspring):
    char_offspring = list(offspring)
    age = char_offspring[0] + char_offspring[1] + ""
    heart = char_offspring[8] + char_offspring[9] + ""
    st = char_offspring[10] + char_offspring[11] + ""
    if(age=="11" or heart=="11" or st=="11"):
        return False
    
    return True

def mutation(str):
    orig = str
    value = [0]*7

    for i in range(0,7):
        value[i] = random.uniform(0.0,1.0)

    char_offspring = list(str)
    myiter = iter(range(0,(len(str)-1)))
    for j in myiter:
        for k in range(0,7):
            if(value[k]>0.5 and j in singlebit):
                next(myiter, None)
                if (char_offspring[j] is '0'):
                    char_offspring[j]='1'
                else:
                    char_offspring[j]='0'

            elif(value[k]>0.5 and j in doublebit):
                next(myiter, None)
                next(myiter, None)
                selectbit=random.choice((j,j+1))
                if (char_offspring[selectbit] is '0'):
                    char_offspring[selectbit]='1'
                else:
                    char_offspring[selectbit]='0'

    str = ''.join(char_offspring)

    #return str
    if not check_validity(str):
        str = mutation(orig)
        return str
    else:
        return str

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
    min_list=[0]*7
    min_list[0]=age_value(str1[0]+str1[1]+"",j)
    min_list[1]=singlebit_value(str1[2] + "", j, 'sex')
    min_list[2]=bp_value(str1[3]+str1[4]+"",j)
    min_list[3]=chol_value(str1[5]+str1[6]+"",j)
    min_list[4] = singlebit_value(str1[7] + "", j, 'blood_sugar')
    min_list[5]=heartrate_value(str1[8]+str1[9]+"",j)
    min_list[6]=st_value(str1[10]+str1[11]+"",j)
    return min(min_list)

def fitness_calc(population):
    min_all_row=[0]*df.shape[0]
    for j in range(0,df.shape[0]):
        min_all_row[j]=split_str(population,j)
    fitness_of_population = fitness_sum(min_all_row)
    return fitness_of_population

def fitness_sum(min_all_row):
    return sum(min_all_row)

def pop_fitness(population_calc):
    fitness_pop = [0.0]*10
    for i in range(0,len(population_calc)):
        fitness_pop[i] = fitness_calc(population_calc[i])

    return fitness_pop

def cross_mutate_selected(population_old,fitness_population_old):
    pop_list = [""]*2
    select_pop_list = select_population(population_old,fitness_population_old,False,0)
    pop_list_cross = crossover_updated(population_old,fitness_population_old,select_pop_list)
    pop_list[0] = mutation(pop_list_cross[0])
    pop_list[1] = mutation(pop_list_cross[1])
    return pop_list

def calc_top_ten(fit_all,pop_all):
    fitness_population_old = [0.0]*10
    population_old = [""]*10
    for i in range(0,10):
        fitness_population_old[i] = max(fit_all)
        index = fit_all.index(fitness_population_old[i])
        population_old[i] = pop_all[index]
        fit_all[index] = 0

    return population_old

if __name__ == '__main__':
    population_new = [""] * 10
    fitness_population_new = [0.0] * 10
    population_old = [""] * 10
    fitness_population_old = [0.0] * 10
    fitness_population_old_max = 0
    fitness_population_new_max = 0

    population_old = init_population
    fitness_population_old = pop_fitness(population_old)
    fitness_population_old_max = max(fitness_population_old)

    while True:
        fitness_population_old_max = max(fitness_population_old)
        print ('Max Old = ',fitness_population_old_max)
        print ('Old population fitness = ', fitness_population_old)
        for i in range(0,10,2):
            pop_list = cross_mutate_selected(population_old,fitness_population_old)
            population_new[i] = pop_list[0]
            population_new[i+1] = pop_list[1]
            fitness_population_new[i] = fitness_calc(population_new[i])
            fitness_population_new[i+1] = fitness_calc(population_new[i+1])

        fit_all = fitness_population_old + fitness_population_new
        pop_all = population_old + population_new
        population_old = calc_top_ten(fit_all,pop_all)
        fitness_population_old = pop_fitness(population_old)
        fitness_population_new_max = max(fitness_population_old)
        print ('Max New = ', fitness_population_new_max)
        print ('New top 10 population fitness = ',fitness_population_old)
        fitness_diff = abs(fitness_population_old_max-fitness_population_new_max)
        print ('Fitness Diff = ',fitness_diff)
        if(fitness_diff<0.001):
            exit(0)

