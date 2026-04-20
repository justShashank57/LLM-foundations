from client import stream_chat
def main():
    print("Welcome to the CLI Streaming Assistant!\n")
    print("Type 'exit' or 'quit' to end the session.")
    messages = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        messages.append({"role":"user", "content": user_input})

        print("AI: ", end="", flush=True)
        ai_response = stream_chat(messages)

        messages.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__": main()