# language_python/pandas_demo.py
# Corey Schafer Pandas Tutorial – Videos 1-6

import pandas as pd

print("===== VIDEO 1: INTRODUCTION =====")
# Creating DataFrames from dictionaries
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [25, 30, 35, 40],
    "Salary": [50000, 60000, 70000, 80000],
}
df = pd.DataFrame(data)
print(df)

print("\n===== VIDEO 2: SERIES =====")
# Series are like columns
print(df["Name"])
print(df["Salary"].mean())

print("\n===== VIDEO 3: DATAFRAMES =====")
# Inspecting DataFrames
print(df.head())
print(df.info())
print(df.describe())

print("\n===== VIDEO 4: INDEXING & SELECTING =====")
# Selecting columns and rows
print(df["Name"])  # Single column
print(df[["Name", "Age"]])  # Multiple columns
print(df.iloc[0])  # Row by index position
print(df.loc[0])  # Row by label

print("\n===== VIDEO 5: FILTERING =====")
# Filtering data
print(df[df["Age"] > 30])
print(df[(df["Age"] > 25) & (df["Salary"] > 60000)])

print("\n===== VIDEO 6: GROUPBY =====")
# Grouping data
grouped = df.groupby("Age")["Salary"].mean()
print(grouped)
