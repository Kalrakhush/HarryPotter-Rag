# main.py

from agents.harry_potter_crew import HarryPotterRAGCrew
import traceback

def interactive_mode():
    print("🪄 Welcome to the Harry Potter RAG Assistant!")
    print("Type 'exit' to leave the wizarding world.\n")

    crew_instance = HarryPotterRAGCrew()

    while True:
        try:
            # Get user input
            question = input("🔮 Ask your question: ")
            if question.lower() in ["exit", "quit"]:
                print("🧹 Exiting... See you at Hogwarts!")
                break

            character = input("🧙‍♂️ Which character should answer? (e.g., Harry, Hermione, Dumbledore): ")

            # Set inputs
            inputs = {
                "question": question,
                "character": character,
            }

            # Build the crew
            crew = crew_instance.crew()

            print("\n🚀 Kicking off the Harry Potter Crew...")
            final_output = crew.kickoff(inputs=inputs)

            print("\n🎤 In-character Response:\n")
            print(final_output)

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    interactive_mode()
