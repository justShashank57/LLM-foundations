from client import run_agent

def main():
    print(f"Your personal LLM agent is ready to help! (type 'exit/quit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = run_agent(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()
        