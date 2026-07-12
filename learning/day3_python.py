# day3_python.py – Lists, 2D Lists, List Methods, Tuples, Unpacking

print("===== LISTS =====")
numbers = [1, 2, 3, 4, 5]
print(numbers)  # [1, 2, 3, 4, 5]
print(numbers[0])  # 1
print(numbers[-1])  # 5
print(numbers[1:3])  # [2, 3]
print(numbers[:3])  # [1, 2, 3]
print(numbers[2:])  # [3, 4, 5]

print("\n===== LIST METHODS =====")
numbers.append(6)  # add to end
print(numbers)  # [1, 2, 3, 4, 5, 6]
numbers.insert(0, 0)  # insert at index 0
print(numbers)  # [0, 1, 2, 3, 4, 5, 6]
numbers.remove(3)  # remove first occurrence of 3
print(numbers)  # [0, 1, 2, 4, 5, 6]
numbers.pop()  # remove last element
print(numbers)  # [0, 1, 2, 4, 5]
numbers.pop(1)  # remove at index 1
print(numbers)  # [0, 2, 4, 5]
numbers.sort()  # ascending
print(numbers)  # [0, 2, 4, 5]
numbers.reverse()  # descending
print(numbers)  # [5, 4, 2, 0]
print(numbers.index(4))  # 1
print(numbers.count(2))  # 1
copy = numbers.copy()
print(copy)  # [5, 4, 2, 0]
numbers.clear()
print(numbers)  # []

print("\n===== 2D LISTS =====")
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[0][1])  # 2
matrix[1][1] = 99
print(matrix[1])  # [4, 99, 6]

print("\n===== TUPLES (immutable) =====")
coordinates = (1, 2, 3)
# coordinates[0] = 10     # ❌ TypeError – tuples cannot be changed
print(coordinates[0])  # 1

print("\n===== UNPACKING =====")
x, y, z = coordinates
print(f"x={x}, y={y}, z={z}")  # x=1, y=2, z=3

# Unpacking with lists works too
items = [10, 20, 30]
a, b, c = items
print(f"a={a}, b={b}, c={c}")  # a=10, b=20, c=30
