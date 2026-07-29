import itertools

# amounts = [1000,2500,3000]
# running_accumulation = itertools.accumulate(amounts)

# print(list(running_accumulation))

# for i, j in itertools.product(range(3), range(3)):
#     print(i, j)

# fruits_vegetables = [{"name": "apple", "type": "fruits"}, {"name": "broccoli", "type": "vegetables"}, {"name": "banana", "type": "fruits"}, {"name": "tomato", "type": "vegetables"}]

# groupby_types = itertools.groupby(fruits_vegetables, key=lambda x: x["type"])

# for group_key, items in groupby_types:
#     if group_key == "fruits":
#         print([item for item in items])

# numbers1 = [1,2,3]
# numbers2 = [4,5,6]

# print(list(itertools.chain(numbers1, numbers2)))

# numbers = [1,2,3,4,5,6,7,8,9]

# sliced_numbers = itertools.islice(numbers, 3)
# print(list(sliced_numbers))

# c = itertools.count(10, 2)
# print(next(c))
# print(next(c))