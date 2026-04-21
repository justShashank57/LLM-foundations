from client import json_generator


def main():
    print("Structured JSON Generator (type 'exit/quit' to quit)\n")

    while True:
        user_input = input("Enter text: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        result = json_generator(user_input)

        if result:
            print("\n✅ Parsed JSON:\n")
            print(result)
        else:
            print("\n❌ Could not generate valid JSON\n")


if __name__ == "__main__":
    main()