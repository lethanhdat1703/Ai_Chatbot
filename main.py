import json
from difflib import get_close_matches


# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, question: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, question, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('you:').lower()

        if user_input.lower() == 'q':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answers: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answers}')
        else:
            print('Bot: Tôi không biết điều đó, Bạn có thể dạy cho tôi?')
            new_answer: str = input('Nhập câu trả lời hoặc nhập "s" để bỏ qua: ')

            if new_answer.lower() != 's':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Cảm ơn bạn! Tôi đã học được câu trả lời!')


if __name__ == '__main__':
    chat_bot()
