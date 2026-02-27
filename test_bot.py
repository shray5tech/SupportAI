import time
from rag_engine import initialize_bot

def main():
    print("=" * 50)
    print("  SupportAI - Customer Support Agent")
    print("  Type 'quit' to exit")
    print("=" * 50)

    chain = initialize_bot()

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot: Thank you for contacting Nexus Support. Goodbye!")
            break

        if not user_input:
            continue

        for attempt in range(3):
            try:
                response = chain.invoke({"question": user_input})
                print(f"\nSupportAI: {response['answer']}")
                break
            except Exception as e:
                if "500" in str(e) and attempt < 2:
                    print(f"  [Retrying... attempt {attempt + 2}/3]")
                    time.sleep(2)
                else:
                    print(f"\nSupportAI: I'm having trouble connecting right now. Please try again.")
                    break

if __name__ == "__main__":
    main()
