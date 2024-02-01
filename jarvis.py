import logging
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load local .env file for the OPENAI_APY_KEY
load_dotenv()
client = OpenAI()

# Read configuration from config.json
CONFIG_FILE_PATH = "personal/config.json"
with open(CONFIG_FILE_PATH, "r") as config_file:
    config = json.load(config_file)

GPT_MODEL = config.get("GPT_MODEL", "gpt-3.5-turbo")
HUMAN = config.get("HUMAN", "human")
ASSISTANT_DESCRIPTION = config.get(
    "ASSISTANT_DESCRIPTION", "You are a helpful assistant."
)


def main():
    logging.basicConfig(
        filename="personal/history.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    prompt_for_input = f"> Hello {HUMAN}. How can I help?\n"
    messages = [{"role": "system", "content": ASSISTANT_DESCRIPTION}]

    instruction, messages = parse(wait_for_input(prompt_for_input), messages)

    while instruction != "bye":
        prompt_for_input = instruction
        instruction, messages = parse(wait_for_input(prompt_for_input), messages)

    bye_sequence(messages, HUMAN)


def wait_for_input(prompt_for_input):
    return input(f"{prompt_for_input}# ")


def parse(instruction, messages):
    if instruction == "bye":
        return "bye", messages

    messages.append({"role": "user", "content": instruction})

    print("> ", end="")

    stream = client.chat.completions.create(
        model=GPT_MODEL, messages=messages, stream=True
    )

    gpt_answer = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer_part = chunk.choices[0].delta.content
            gpt_answer += answer_part
            print(answer_part, end="")

    print()

    messages.append({"role": "assistant", "content": gpt_answer})
    return "", messages


def bye_sequence(messages, human):
    print("> Summarizing conversation and checking for requested changes...")
    summary_instruction = "Can you give me a summary, which is shorter than 50 words, of our conversation?"

    messages.append({"role": "user", "content": summary_instruction})
    summary = get_completion_answer(messages)
    log(f"Summary of our conversation: {summary}")

    changes_instruction = "Was there anything I asked you to change about your responses, such as making them shorter, or presenting them in a different way? If yes, please also write a description, which is shorter than 50 words, of a perfect assistant for someone who requests the type of changes I asked you to make. And please write it from a 'you' perspective, so the description should start out with 'You are an assistant for...' If no, please write 'No changes were requested for my responses.'"

    messages.append({"role": "user", "content": changes_instruction})
    assistant_description = get_completion_answer(messages)
    log(f"Assistant description based on requested changes: {assistant_description}")

    # If changes were requested, save new description to the config file
    if assistant_description != "No changes were requested for my responses.":
        config["assistant_description"] = assistant_description
        with open(CONFIG_FILE_PATH, "w") as config_file:
            json.dump(config, config_file, indent=2)

    print(f"> Bye {human}")


def get_completion_answer(messages):
    completion = client.chat.completions.create(model=GPT_MODEL, messages=messages)
    return completion.choices[0].message.content


def log(text):
    logging.info(text)


if __name__ == "__main__":
    main()
