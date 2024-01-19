import time

def main():
    human = 'Roman'
    prompt_for_input = 'Hello '+human+'. How are you?\n'
    instruction = parse(wait_for_input(prompt_for_input))
    while instruction != 'bye':
        prompt_for_input = instruction
        instruction = parse(wait_for_input(prompt_for_input))
    print('Bye '+human)
    exit()
    

def wait_for_input(prompt_for_input):
    human_input = input(prompt_for_input)
    return human_input

def parse(instruction):
    if instruction == 'bye':
        return 'bye'
    return "That's interesting. Tell me more.\n"

main()