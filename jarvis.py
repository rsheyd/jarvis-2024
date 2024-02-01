import logging
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load local .env file for the OPENAI_APY_KEY
load_dotenv()
client = OpenAI()

LOG_FILE_PATH = "personal/history.log"
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
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    prev_convo = review_prev_convo()

    prompt_for_input = f"> Hello {HUMAN}.{prev_convo} How can I help?\n"
    messages = [{"role": "system", "content": ASSISTANT_DESCRIPTION}]

    instruction, messages = get_stream_answer(wait_for_input(prompt_for_input), messages)

    while instruction != "bye":
        prompt_for_input = instruction
        instruction, messages = get_stream_answer(wait_for_input(prompt_for_input), messages)

    if len(messages)>1:
        bye_sequence(messages, HUMAN)

def review_prev_convo():
    try:
        with open(LOG_FILE_PATH, "r") as log_file:
            lines = log_file.readlines()
            for line in reversed(lines):
                if "Short Summary:" in line:
                    # remove log meta information
                    summary_part = line.split("Short Summary:")[1].strip()
                    summary_part = summary_part[0].lower() + summary_part[1:]
                    return f" Last time {summary_part}"
            log("error","No previous short conversation summary found.")
            return ""
                    
    except FileNotFoundError:
        log("error","No log file found when checking for previous conversation summary.")
        return ""

def wait_for_input(prompt_for_input):
    return input(f"{prompt_for_input}& ")


def get_stream_answer(instruction, messages):
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
    summary_instruction = "Can you give me 2 summaries of our conversation? The first one should be prepended 'Detailed Summary:' and anywhere between 1 and 10 sentences long. The second summary should be prepended 'Short Summary:', concise, and 1 sentence long. Both summaries should be written from your perspective, e.g. 'You talked to me about...'"

    summary = get_answer(summary_instruction, messages)
    log(summary)

    changes_instruction = "Was there anything I asked you to change about your responses, such as making them shorter, or presenting them in a different way? If yes, please also write a description, which is shorter than 50 words, of a perfect assistant for someone who requests the type of changes I asked you to make. And please write it from a 'you' perspective, so the description should start out with 'You are an assistant for...' If no, please write 'No changes were requested for my responses.'"

    messages.append({"role": "user", "content": changes_instruction})
    assistant_description = get_answer(messages)
    log(f"Assistant description based on requested changes: {assistant_description}")

    # If changes were requested, save new description to the config file
    if assistant_description != "No changes were requested for my responses.":
        config["assistant_description"] = assistant_description
        with open(CONFIG_FILE_PATH, "w") as config_file:
            json.dump(config, config_file, indent=2)

    print(f"> Bye {human}")


def get_answer(instruction, messages):
    messages.append({"role": "user", "content": instruction})
    completion = client.chat.completions.create(model=GPT_MODEL, messages=messages)
    return completion.choices[0].message.content


def log(type="info",text=""):
    if type == "info":
        logging.info(text)
    elif type == "error":
        logging.error(text)


if __name__ == "__main__":
    main()
