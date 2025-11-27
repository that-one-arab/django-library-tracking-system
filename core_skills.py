import random
rand_list = [random.randint(1, 100) for _ in range(20)]

# list comprehension
list_comprehension_below_10 = [num for num in rand_list if num < 10]

# filter
list_comprehension_below_10 = list(filter(lambda num: num < 10, rand_list))