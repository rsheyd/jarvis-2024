import time
from openai import OpenAI

client = OpenAI()

def main():
    human = 'Roman'
    prompt_for_input = '> Hello '+human+'. How are you?\n'
    messages = []
    instruction, messages = parse(wait_for_input(prompt_for_input), messages)
    while instruction != 'bye':
        prompt_for_input = instruction
        instruction, messages = parse(wait_for_input(prompt_for_input), messages)
    print('> Bye '+human)
    exit()


def wait_for_input(prompt_for_input):
    human_input = input(prompt_for_input+"# ")
    return human_input

def parse(instruction, messages):
    if instruction == 'bye':
        return 'bye', []
    messages.append({"role": "user", "content": instruction})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )  
    answer = completion.choices[0].message.content
    print('> '+answer)
    messages.append({"role": "assistant", "content": answer})
    return '', messages

main()