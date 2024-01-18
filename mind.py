import logging, re, datetime, os, time, configparser
from subprocess import call

memory_file_path_absolute = ""

def main():
    config = load_config()

    logging.basicConfig(
            format="%(asctime)s %(levelname)s - %(message)s",
            filename=memory_file_path_absolute,
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    log("Jarvis is starting")

    human = config.get('Settings', 'human')
    today2pm = datetime.datetime.now().replace(
        hour=14, minute=0, second=0, microsecond=0
    )
    if not datetime.datetime.now() > today2pm:
        log(human + " probably hasn't left yet; too early to welcome him back")
    elif not welcomed_after(today2pm):
        welcome_human_audio()
    exit()

def load_config():
    config_file_relative = 'personal/config.ini'
    config = configparser.ConfigParser()
    config.read(config_file_relative)
    config_file_directory = os.path.dirname(os.path.abspath(config_file_relative))
    memory_file_relative = config.get('Settings', 'memory_file_path')
    global memory_file_path_absolute
    memory_file_path_absolute = os.path.join(config_file_directory, memory_file_relative)
    return config


def welcomed_after(time_cutoff):
    memory = remember("welcoming")
    if memory is not None and memory > time_cutoff:
        log("Remembered that already welcomed after " + str(time_cutoff))
        return True
    log("Did not welcome yet today after " + str(time_cutoff))
    return False


def remember(action):
    log("Trying to remember if {action} before".format(action=action))
    for full_memory in reversed(open(memory_file_path_absolute).readlines()):
        # cut off log time and log type
        memory = full_memory[27:]
        if ("Did " + action) in memory and not memory.startswith("Remembered: "):
            log("Remembered: " + memory.rstrip())
            return when(full_memory)
    return None


def when(memory):
    memory_datetime = datetime.datetime.strptime(memory[:19], "%Y-%m-%d %H:%M:%S")
    log("Memory was at: " + str(memory_datetime))
    return memory_datetime


def welcome_human_audio():
    log("Trying to welcome")
    # # play ogg file
    # log("Playing welcome audio")
    # call(
    #     ["amixer", "sset", """'OMA2130 - A2DP'""", "90%"], stdout=open(os.devnull, "wb")
    # )
    # time.sleep(3)
    # call(
    #     ["omxplayer", "-o", "alsa", "/home/pi/rekognize/welcomehome.ogg"],
    #     stdout=open(os.devnull, "wb"),
    # )
    # log("Did welcoming")


def log(text):
    print(text)
    logging.info(text)


def exit():
    log("Jarvis shutting down")


main()
