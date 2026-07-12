# language_python/list_analyzer.py


def main():
    # 1. Ask the user for input
    user_input = input("Enter 5 numbers separated by commas (e.g. 10,20,30,40,50): ")

    # 2. Split by commas, strip spaces, convert to int
    #    Handle possible empty entries by filtering (just in case)
    parts = [part.strip() for part in user_input.split(",") if part.strip()]
    numbers = [int(part) for part in parts]

    # 3. Store in a list (already a list)
    original = numbers[:]  # copy

    # 4. Print original list
    print(f"Original list: {original}")

    # 5. Sorted list
    sorted_list = sorted(original)
    print(f"Sorted list: {sorted_list}")

    # 6. Sum
    total = sum(original)

    # 7. Average (to 2 decimal places)
    average = total / len(original) if original else 0

    # 8. Maximum and minimum
    max_val = max(original) if original else None
    min_val = min(original) if original else None

    print(f"Sum: {total}")
    print(f"Average: {average:.2f}")
    print(f"Maximum: {max_val}")
    print(f"Minimum: {min_val}")

    # 9. Remove duplicates (preserve order)
    #    Using dict.fromkeys() to keep order (Python 3.7+)
    cleaned = list(dict.fromkeys(original))
    print(f"Cleaned list (duplicates removed): {cleaned}")

    # 10. Store statistics in a tuple
    stats = (total, average, max_val, min_val)

    # 11. Unpack and display
    sum_unpack, avg_unpack, max_unpack, min_unpack = stats
    print("\nStatistics (unpacked from tuple):")
    print(f"Sum = {sum_unpack}")
    print(f"Average = {avg_unpack:.2f}")
    print(f"Max = {max_unpack}")
    print(f"Min = {min_unpack}")


if __name__ == "__main__":
    main()
