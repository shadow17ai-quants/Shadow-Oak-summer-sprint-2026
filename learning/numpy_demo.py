# language_python/numpy_demo.py
# NumPy basics – arrays, operations, broadcasting

import numpy as np

print("===== CREATING ARRAYS =====")
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)
arr2 = np.zeros(5)
print(arr2)
arr3 = np.ones(5)
print(arr3)
arr4 = np.arange(0, 10, 2)
print(arr4)

print("\n===== ARRAY OPERATIONS =====")
print(arr1 + 10)
print(arr1 * 2)
print(arr1.mean())
print(arr1.std())
print(arr1.sum())

print("\n===== 2D ARRAYS =====")
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix)
print(matrix.shape)
print(matrix[0, 1])  # row 0, col 1 = 2
print(matrix[:, 1])  # column 1

print("\n===== BROADCASTING =====")
arr = np.array([1, 2, 3, 4, 5])
print(arr * 2)  # Broadcasting: scalar applied to all elements

print("\n===== STATISTICAL OPERATIONS =====")
data = np.array([10, 20, 30, 40, 50])
print(f"Mean: {data.mean():.2f}")
print(f"Std: {data.std():.2f}")
print(f"Min: {data.min()}")
print(f"Max: {data.max()}")
print(f"Sum: {data.sum()}")
