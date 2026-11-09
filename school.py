# List operations

# list casting
fruit = ["apple", "banana"]
copy = list(fruit)
print(copy)
# turn a string into a list
fruit = list("apple")
print(fruit)

# list operations
# + adds two lists
more_fruit = ["pear", "orange"]
all_fruit = fruit + more_fruit
print(all_fruit)
# *
spam = ["spam"]
spam = spam * 10
print(spam)

# math functions
nums = [1, 2, 3, 4]
print(sum(nums))
print(min(nums))

# string joining
letters = ["a", "b", "c", "d", "e", "f"]
print(" ".join(letters))

# passing lists as parameters
def remove_all(lst):
    lst.clear()
    return lst

# note: try tracing this
lst = remove_all(letters)
print(lst) # the list is returned
print(letters) # but the original list is also changed