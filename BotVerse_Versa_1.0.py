import json
import os
import datetime
import random

KNOWLEDGE_FILE = "knowledge.json"
MEMORY_FILE = "memory.json"

def load_knowledge():
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_knowledge(knowledge):
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(knowledge, f, indent=4)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def emotional_response(answer):
    positive_words = ["good", "great", "awesome", "love", "happy"]
    negative_words = ["bad", "sad", "hate", "angry", "upset"]

    if any(word in answer.lower() for word in positive_words):
        emojis = ["😊", "😄", "👍"]
    elif any(word in answer.lower() for word in negative_words):
        emojis = ["😢", "☹️", "😔"]
    else:
        emojis = ["🤖", "🧠"]

    return random.choice(emojis) + " " + answer

def chat():
    print("🤖 BotVerse™ - Versa 1.0 (Smart Learn + Memory Mode)")
    print("Type 'exit' to quit.\n")

    knowledge = load_knowledge()
    memory = load_memory()

    user = input("Enter your name (or just press Enter to stay anonymous): ").strip().lower() or "anonymous"
    if user not in memory:
        memory[user] = {
            "questions_asked": [],
            "verified_answers": []
        }

    while True:
        question = input("You: ").strip().lower()
        if question == "exit":
            print("Versa: Goodbye, friend! 👋")
            break

        found = False
        for q in knowledge:
            if question in q or q in question:
                entry = knowledge[q]
                found = True
                if entry.get("approved", False):
                    print("Versa:", emotional_response(entry["answer"]))
                else:
                    if q in memory[user]["verified_answers"]:
                        print("Versa:", emotional_response(entry["answer"]))
                    else:
                        print(f"Versa: Someone said the answer is '{entry['answer']}'. Do you think this is correct? (yes/no)")
                        feedback = input("You: ").strip().lower()
                        if feedback == "yes":
                            entry["times_verified"] = entry.get("times_verified", 0) + 1
                            memory[user]["verified_answers"].append(q)
                            if entry["times_verified"] >= 2:
                                entry["approved"] = True
                                print("Versa: Thanks! This answer is now verified and trusted. ✅")
                            else:
                                print("Versa: Got it! Thanks for helping me verify that. 🧠")
                        else:
                            correct = input("Versa: Okay! What should be the correct answer? 🧐\nYou: ").strip()
                            entry["answer"] = correct
                            entry["approved"] = False
                            entry["times_verified"] = 0
                            print("Versa: Thanks! I've updated my memory with the new info. 🧠")

                memory[user]["questions_asked"].append(question)
                break

        if not found:
            new_answer = input("Versa: I don't know that yet. Can you teach me? 🤔\nYou: ").strip()
            knowledge[question] = {
                "answer": new_answer,
                "learned_on": str(datetime.datetime.now()),
                "approved": False,
                "times_verified": 0
            }
            print("Versa: Thanks! I’ve saved that, but I’ll verify it with others before trusting it fully. 🔐")
            memory[user]["questions_asked"].append(question)

        save_knowledge(knowledge)
        save_memory(memory)

if __name__ == "__main__":
    chat()
