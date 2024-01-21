import time
from openai import OpenAI

client = OpenAI()

# summarize and log our conversations
# keep the system assistant descriptions updated and previous descriptions logged
# add config and log files

def main():
    human = 'Roman'
    prompt_for_input = '> Hello '+human+'. How are you?\n'
    messages = []
    instruction, messages = parse(wait_for_input(prompt_for_input), messages)
    while instruction != 'bye':
        prompt_for_input = instruction
        instruction, messages = parse(wait_for_input(prompt_for_input), messages)
    bye_sequence(messages, human)


def wait_for_input(prompt_for_input):
    human_input = input(prompt_for_input+"# ")
    return human_input

def parse(instruction, messages):
    if instruction == 'bye':
        return 'bye', messages
    messages.append({"role": "user", "content": instruction})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )  
    answer = completion.choices[0].message.content
    print('> '+answer)
    messages.append({"role": "assistant", "content": answer})
    return '', messages

def bye_sequence(messages, human):
    instruction = "Can you give me a summary, which is shorter than 50 words, of our conversation? Also, was there anything I asked you to change about your responses, such as making them shorter, or present them in a different way? If yes, please also write a description, which is shorter than 50 words, of a perfect assistant for someone who requests the type of changes I asked you to make. And please write it from a 'you' perspective, so the description should start out with 'You are an assistant for...'"
    messages.append({"role": "user", "content": instruction})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )  
    answer = completion.choices[0].message.content
    print('> '+answer)
    print('> Bye '+human)
    exit()

main()