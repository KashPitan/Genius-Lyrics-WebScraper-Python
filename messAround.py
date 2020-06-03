list = [1,3,5,7,9,11]
list2 = [12,33,53,45,9,131]
list3 = [0.1,7,9.2,11.3]

def mean_of_list(list):
    list_sum = sum(list)
    number_of_list_items = len(list)
    mean_list = list_sum/number_of_list_items
    return mean_list


print(mean_of_list(list))
print(mean_of_list(list2))
print(mean_of_list(list3))