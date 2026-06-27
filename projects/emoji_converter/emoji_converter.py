# language_python/emoji_converter.py
# Full Emoji Converter – maps text emoticons to actual emojis

def convert_emojis(message):
    # Define emoji map
    emoji_map = {
        ":)" : "😊",
        ":(" : "😢",
        ":D" : "😄",
        "<3" : "❤️",
        ";)" : "😉"
    }
    words = message.split(" ")
    output = ""
    for word in words:
        output += emoji_map.get(word, word) + " "
    return output.strip()

# Main
user_input = input("Enter a message: ")
result = convert_emojis(user_input)
print("Converted:", result)