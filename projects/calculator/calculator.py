# Calculator

a = float(input("First number: "))
b = float(input("Second number: "))
op = input("Operator (+, -, *, /): ")

if op == "+":
    print(f"{a} + {b} = {a + b}")
elif op == "-":
    print(f"{a} - {b} = {a - b}")
elif op == "*":
    print(f"{a} * {b} = {a * b}")
elif op == "/":
    if b == 0:
        print("Cannot divide by zero.")
    else:
        print(f"{a} / {b} = {a / b}")
else:
    print("Invalid operator.")
