import random
import time

neg = 0
generation = list()

first_state = []
all_first_states = []

# Easy Sudoku
in_state =    [ [neg, 3, neg, neg, neg, 8, 5, neg, neg],
                [neg, 7, neg, 2, neg, neg, 4, 9, 6],
                [2, 5, neg, neg, neg, 4, 8, neg, 1],
                [neg, neg, 1, 9, 8, neg, neg, neg, 6],
                [9, 6, neg, 1, 5, neg, neg, 4, 2],
                [3, 7, 5, neg, 6, neg, neg, neg, neg],
                [neg, neg, 2, 1, 7, neg, 8, 6, 4],
                [5, neg, neg, neg, neg, 3, neg, 1, neg],
                [neg, 1, 7, 9, neg, 8, neg, 2, neg] ]

all_first_states.append(in_state)

# Medium Sudoku
in_state =    [ [neg,7,neg,8,neg,neg,6,neg,1],
                [neg,neg,neg,5,neg,neg,neg,2,3],
                [6,neg,neg,9,neg,neg,neg,4,neg],
                [neg,2,neg,7,neg,3,neg,8,neg],
                [neg,6,neg,neg,5,4,neg,neg,9],
                [neg,8,neg,2,neg,neg,1,neg,neg],
                [5,neg,neg,neg,neg,2,neg,9,neg],
                [neg,neg,8,7,neg,neg,neg,4,neg],
                [neg,1,neg,neg,neg,6,neg,neg,3] ]

all_first_states.append(in_state)


# Hard Sudoku
in_state =    [ [7,neg,3,6,8,neg,1,neg,neg],
                [neg,9,neg,neg,1,5,2,neg,neg],
                [neg,neg,1,neg,3,neg,neg,7,neg],
                [8,3,neg,9,neg,4,neg,neg,neg],
                [4,neg,neg,neg,2,neg,1,neg,9],
                [neg,neg,neg,5,1,neg,neg,4,7],
                [neg,1,8,neg,6,neg,4,neg,neg],
                [neg,neg,2,9,4,neg,neg,6,neg],
                [neg,neg,6,neg,8,5,1,neg,3],
              ]

all_first_states.append(in_state)

def score_of_chromosome_two(chromosome): # goodness of columns + goodness of rows + goodness of subblocks
   
    score_row = 0
    score_column = 0
    rows_list = convert_to_main_form(chromosome)
    columns_list = []
    
    score_subblock = 0

    for i in range(9):
       score_subblock += len(set(chromosome[i]))

    for i in range(9):
       score_row += len(set(rows_list[i]))
       
    for i in range(9):
       column = []
       for j in range(9):
           column.append(rows_list[j][i])          
       columns_list.append(column)

    for i in range(9):
       score_column += len(set(columns_list[i]))
       
    return score_column + score_row + score_subblock

def score_of_chromosome(chromosome): # goodness of rows + goodness of columns
   
    score_row = 0
    score_column = 0
    rows_list = convert_to_main_form(chromosome)
    columns_list = []

    for i in range(9):
       score_row += len(set(rows_list[i]))
       
    for i in range(9):
       column = []
       for j in range(9):
           column.append(rows_list[j][i])          
       columns_list.append(column)

    for i in range(9):
       score_column += len(set(columns_list[i]))
       
    return list([score_row, score_column])


def is_answer(chromosome):    
    score_subblock = 0

    for i in range(9):
       score_subblock += len(set(chromosome[i]))
    
    lst_scores = score_of_chromosome(chromosome)
    total = score_subblock + lst_scores[0] + lst_scores[1]
    if(total == 243):
        return 1
    return 0


def convert_to_main_form(chromosome): # converts subblock notation to row notation
    children = []

    children.append(chromosome[0][0:3] + chromosome[1][0:3] + chromosome[2][0:3])
    children.append(chromosome[0][3:6] + chromosome[1][3:6] + chromosome[2][3:6])
    children.append(chromosome[0][6:9] + chromosome[1][6:9] + chromosome[2][6:9])
    
    children.append(chromosome[3][0:3] + chromosome[4][0:3] + chromosome[5][0:3])
    children.append(chromosome[3][3:6] + chromosome[4][3:6] + chromosome[5][3:6])
    children.append(chromosome[3][6:9] + chromosome[4][6:9] + chromosome[5][6:9])


    children.append(chromosome[6][0:3] + chromosome[7][0:3] + chromosome[8][0:3])
    children.append(chromosome[6][3:6] + chromosome[7][3:6] + chromosome[8][3:6])
    children.append(chromosome[6][6:9] + chromosome[7][6:9] + chromosome[8][6:9])
    
    return children
 
        
def initial_population(first_state, population_numbers): # initial -> unique numbers in each subblock
    for population_number in range(population_numbers):
        children = []
        for subblock_number in range(9):
            subblock = [t for t in first_state[subblock_number]]
            lst_index = [i for i in range(9) if subblock[i] == neg]
            lst_init_numbers = [subblock[i] for i in range(9) if i not in lst_index]
            lst_not_init_numbers = [number for number in range(1, 10) if number not in lst_init_numbers]
            for i in lst_index:
                subblock[i] = random.choice(lst_not_init_numbers)
                lst_not_init_numbers.remove(subblock[i])
            children.append(subblock)
        generation.append(children)


def not_uniques(lst): # it is used for giving a goodnes score to rows or columns of a subblock
    total = 0
    if lst[0] == lst[1]:
        total += 1
    if lst[0] == lst[2]:
        total += 1
    if lst[1] == lst[2]:
        total += 1
    total += 0
    if total == 0:
        return 0
    elif total == 1:
        return 3
    else:
        return 6


def get_score_row(chromosome, sub_block, row_number): # gives a goodness score to a row of a subblock
    if sub_block in [1,2,3] :
        list1 = [1, 2, 3]
        
    elif sub_block in [4, 5, 6] :
        list1 = [4, 5, 6]
        
    elif sub_block in [7, 8, 9] :
        list1 = [7, 8, 9]
        
    first_ind = row_number * 3 - 3
    last_ind = row_number * 3
    ind_list = [j-1 for j in list1 if j != sub_block]

    other_numbers_in_row = [chromosome[t][first_ind:last_ind] for t in ind_list]
    
    collision = len([a for a in chromosome[sub_block-1][first_ind:last_ind] if a in other_numbers_in_row[0] or a in other_numbers_in_row[1]])
    return 9-collision-not_uniques([a for a in chromosome[sub_block-1][first_ind:last_ind]])
    #minimum 9-collision is 6
        
        

def get_score_column(chromosome, sub_block, column_number): # gives a goodness score to a column of a subblock
    if sub_block in [1, 4, 7] :
        list1 = [1, 4, 7]
        
    elif sub_block in [2, 5, 8] :
        list1 = [2, 5, 8]
        
    elif sub_block in [3, 6, 9] :
        list1 = [3, 6, 9]
        
    first_ind = column_number - 1
    ind_list = [j-1 for j in list1 if j != sub_block]

    other_numbers_in_column = [chromosome[t][first_ind::3] for t in ind_list]
    
    collision = len([a for a in chromosome[sub_block-1][first_ind::3] if a in other_numbers_in_column[0] or a in other_numbers_in_column[1]])
    return 9-collision-not_uniques([a for a in chromosome[sub_block-1][first_ind::3]])
    #minimum 9-collision is 6


def get_subblock_row(parent, subblock, row_number):    # returns a row of a subblock
    first_ind = row_number * 3 - 3
    last_ind = row_number * 3
    return [a for a in parent[subblock-1][first_ind:last_ind]]


def get_subblock_column(parent, subblock, column_number):    # returns a column of a subblock
    first_ind = column_number -1
    return [a for a in parent[subblock-1][first_ind::3]]
        

# Builds subblocks of children#1 according to rows score of two parents according to crossover rate
def build_subblocks_child1(parent1, parent2, crossover_rate): 
    child = []
    for subblock_number in range(1, 10):
        child_subblock = []
        for subblock_row_number in range(1,4):
            
            random_number = random.choices([0, 1], weights=(100-crossover_rate, crossover_rate))
            random_number = random_number[0]
            score_parent1 = get_score_row(parent1, subblock_number, subblock_row_number)
            score_parent2 = get_score_row(parent2, subblock_number, subblock_row_number)
            
            if(score_parent1 >= score_parent2 or random_number == 0):
                row = get_subblock_row(parent1, subblock_number, subblock_row_number)
                
            else:
                row = get_subblock_row(parent2, subblock_number, subblock_row_number)                 

            child_subblock.append(row[0])
            child_subblock.append(row[1])
            child_subblock.append(row[2])
      
        child.append(child_subblock)
    return child



# Builds subblocks of children#1 according to columns score of two parents according to crossover rate
def build_subblocks_child2(parent1, parent2, crossover_rate): 
    child = []
    for subblock_number in range(1, 10):
        child_subblock = [0] * 9
        for subblock_column_number in range(1,4):
            
            random_number = random.choices([0, 1], weights=(100-crossover_rate, crossover_rate))
            random_number = random_number[0]
            score_parent1 = get_score_column(parent1, subblock_number, subblock_column_number)
            score_parent2 = get_score_column(parent2, subblock_number, subblock_column_number)
            
            if(score_parent2 >= score_parent1 or random_number == 0):
                column = get_subblock_column(parent2, subblock_number, subblock_column_number)
                
            else:
                column = get_subblock_column(parent1, subblock_number, subblock_column_number)
                
            child_subblock[subblock_column_number - 1 + 0] = column[0]
            child_subblock[subblock_column_number - 1 + 3] = column[1]
            child_subblock[subblock_column_number - 1 + 6] = column[2]
            
        child.append(child_subblock)
    return child



def mutation(initial_state, chromosome, mutation_rate): # mutates a chromosome according to the mutation rate
    children = []
    for subblock_number in range(9): # for each subblock we can perform mutation
        random_number = random.choices([0, 1], weights=(100 - mutation_rate, mutation_rate))
        subblock = [t for t in chromosome[subblock_number]]
        random_number = random_number[0]
        
        if random_number == 1:
            init_state = initial_state[subblock_number]
            list_mutable = [i for i in range(9) if init_state[i] == neg]
            random_index = random.choices(list_mutable, k=2)
            subblock[random_index[0]], subblock[random_index[1]] = subblock[random_index[1]], subblock[random_index[0]]
        children.append(subblock)
    return children
        
 
def check_whole_generation(generation):
    for chromosome in generation:
        if is_answer(chromosome) == 1:
            return chromosome
    return -1


def generate_child_one(parent1, parent2):
    build_subblocks_child2(parent1, parent2, crossover_rate)
    return 1

def show_menu():
    print("Which one do you want to solve ?")
    print(" 1. Easy Sudoku")
    print(" 2. Medium Sudoku")
    print(" 3. Hard Sudoku")

show_menu()

while 1:
    inp = int(input())
    if inp == 1 or inp == 2 or inp == 3 :
        first_state = all_first_states[inp-1]
        break

main_form_first = convert_to_main_form(first_state)
print("\nYour chosen sudoku is :")
for item in main_form_first:
    print(item)

start_time = time.time()

crossover_rate = 85
mutation_rate = 10
chromosome = -1
population_num = 1000


initial_population(first_state, population_num)
chromosome = check_whole_generation(generation)

while 1:
    
    if chromosome == -1 :
        
        for i in range(0, population_num, 2):
            child_one = build_subblocks_child1(generation[i], generation[i + 1], crossover_rate)
            child_two = build_subblocks_child2(generation[i], generation[i + 1], crossover_rate)
            
            child_one = mutation(first_state, child_one, mutation_rate)
            child_two = mutation(first_state, child_two, mutation_rate)
            
            generation[i] = child_one
            generation[i + 1] = child_two
            
            if is_answer(child_one) == 1:
                chromosome = child_one
                break
            
            if is_answer(child_two) == 1:
                chromosome = child_two
                break
            
            
        #list_weights = [score_of_chromosome(chrom)[0]+score_of_chromosome(chrom)[1] for chrom in generation]
        list_weights = [score_of_chromosome_two(chrom) for chrom in generation]
        new_generation = random.choices(generation, weights = list_weights, k = population_num)
        generation = [chrom for chrom in new_generation]
    

    else :
        break
    
chromosome = convert_to_main_form(chromosome)

total_time = time.time() - start_time
print("\nYour sudoku is solved !!")
print(f"time is : {round(total_time,1)} seconds\n")

for item in chromosome:
    print(item)
  

  
