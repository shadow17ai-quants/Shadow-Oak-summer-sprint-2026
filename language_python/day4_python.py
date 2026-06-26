# day4_python.py – Dictionaries, Emoji Converter, Functions intro

print("===== DICTIONARIES =====")
# Key-value pairs – like a real-world dictionary
customer = {
    "name": "Ryan Kaushal",
    "age": 20,
    "is_verified": True
}
print(customer["name"])          # Ryan Kaushal
print(customer.get("age"))       # 20
print(customer.get("birthdate")) # None (doesn't crash)

# Update / add
customer["age"] = 21
customer["city"] = "Kharar"
print(customer)                  # {'name': 'Ryan Kaushal', 'age': 21, 'is_verified': True, 'city': 'Kharar'}

print("\n===== EMOJI CONVERTER (basic) =====")
# Map text emoticons to actual emojis
emoji_map = {
    ":)" : "😊",
    ":(" : "😢",
    ":D" : "😄",
    "<3" : "❤️"
}

message = input("Enter a message with emoticons (e.g. Hello :) ): ")
words = message.split(" ")
output = ""
for word in words:
    output += emoji_map.get(word, word) + " "
print("Converted:", output)