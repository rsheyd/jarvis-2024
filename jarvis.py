import logging
from openai import OpenAI
from dotenv import load_dotenv

# load local .env file for the OPENAI_APY_KEY
load_dotenv()
client = OpenAI()

# keep the system assistant descriptions updated and previous descriptions logged
# add config


def main():
    logging.basicConfig(
        filename="personal/history.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    human = "Roman"
    prompt_for_input = "> Hello " + human + ". How are you?\n"
    messages = []
    instruction, messages = parse(wait_for_input(prompt_for_input), messages)
    while instruction != "bye":
        prompt_for_input = instruction
        instruction, messages = parse(wait_for_input(prompt_for_input), messages)
    bye_sequence(messages, human)
    return


def wait_for_input(prompt_for_input):
    human_input = input(prompt_for_input + "# ")
    return human_input


def parse(instruction, messages):
    if instruction == "bye":
        return "bye", messages
    messages.append({"role": "user", "content": instruction})
    answer = "> "
    print(answer, end="")
    stream = client.chat.completions.create(
        model="gpt-4", messages=messages, stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer_part = chunk.choices[0].delta.content
            answer += answer_part
            print(answer_part, end="")
    print()
    messages.append({"role": "assistant", "content": answer})
    return "", messages


def bye_sequence(messages, human):
    print("> Summarizing conversation and checking for requested changes...")
    instruction = "Can you give me a summary, which is shorter than 50 words, of our conversation?"
    messages.append({"role": "user", "content": instruction})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    summary = completion.choices[0].message.content
    log(f"Summary of our conversation: {summary}")
    instruction = "Was there anything I asked you to change about your responses, such as making them shorter, or presenting them in a different way? If yes, please also write a description, which is shorter than 50 words, of a perfect assistant for someone who requests the type of changes I asked you to make. And please write it from a 'you' perspective, so the description should start out with 'You are an assistant for...' If no, please write 'No changes were requested for my responses.'"
    messages.append({"role": "user", "content": instruction})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    requested_changes = completion.choices[0].message.content
    log(f"Requested changes: {requested_changes}")
    print("> Bye " + human)
    return


def log(text):
    logging.info(text)


main()
