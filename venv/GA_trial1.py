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

# init_population = ["001000010100","011010100001",
#                    "101101011010","001111100100",
#                    "011000010101","100010101000",
#                    "000101010000","010111100101",
#                    "100000011010","000010100000"]

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
    return min_list

def fitness_calc(population):
    min_all_row=[0]*df.shape[0]
    for j in range(0,df.shape[0]):
        min_all_row[j]=min(split_str(population,j))
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

def check_support(str):
    a = 0
    for i in range(0,df.shape[0]):
        min_list = split_str(str,i)
        for j in range(0,len(min_list)):
            if min_list[j]>0.0:
                continue
            else:
                break

        if j==(len(min_list)-1):
            a = a+1
    return a


def calc_support(selected_pop):
    support_val = [0.0]*10
    for i in range(0,len(selected_pop)):
        support_val[i] = check_support(selected_pop[i])
    print support_val
    return support_val

def print_all_pop(final_pop,support_val):
    for i in range (0,len(final_pop)):
        pop = print_pop(final_pop[i])
        print('Population = ',pop,' Support = ',support_val[i])

def double_bit_conv(str):
    if str=="00":
        return 'L'
    elif str=="01":
        return 'M'
    elif str=="10":
        return 'H'
    else:
        return 'VH'

def st_bit_conv(str):
    if str=="00":
        return 'N'
    elif str=="01":
        return 'SA'
    else:
        return 'H'

def get_sex_conv(str):
    if str=="1":
        return 'M'
    else:
        return 'F'

def print_pop(population):
    pop = ""
    age = double_bit_conv(population[0]+population[1]+"")
    sex = get_sex_conv(population[2]+"")
    blood = double_bit_conv(population[3]+population[4]+"")
    chol = double_bit_conv(population[5] + population[6] + "")
    sugar = population[7]+""
    heart = double_bit_conv(population[8] + population[9] + "")
    st = st_bit_conv(population[10] + population[11] + "")
    pop = "Age = ",age," Sex = ",sex," Blood Pressure = ",blood," Cholesterol = ",chol," Blood Sugar = ",sugar," Heart Rate = ",heart," ST Depression = ",st,""
    return pop

def calc_top_ten(fit_all,pop_all):
    fitness_population_old = [0.0]*10
    population_old = [""]*10
    diff_val = [0.0]*20
    rand = random.uniform(min(fit_all), max(fit_all))
    print ('Random ',rand)

    for i in range(0,len(fit_all)):
        diff_val[i] = abs(rand-fit_all[i])

    print ("Diff ",diff_val)
    for i in range(0,10):
        min_val = min(diff_val)
        index = diff_val.index(min_val)
        print ('Index ',index)
        fitness_population_old[i] = fit_all[index]
        population_old[i] = pop_all[index]
        diff_val[index] = max(fit_all)

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

    i = 0
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
        print ('New population fitness = ', fitness_population_new)
        population_old = calc_top_ten(fit_all,pop_all)
        fitness_population_old = pop_fitness(population_old)
        fitness_population_new_max = max(fitness_population_old)
        print ('Max New = ', fitness_population_new_max)
        print ('New top 10 population fitness = ',fitness_population_old)
        print ('Population ',population_old)
        fitness_diff = abs(fitness_population_old_max-fitness_population_new_max)
        print ('Fitness Diff = ',fitness_diff)
        if(fitness_diff<0.001):
            support_val = calc_support(population_old)
            print_all_pop(population_old,support_val)
            exit(0)

