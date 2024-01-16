import cypher
import os

global path, list_of_events


# Path and dir
def set_path(new_path: str) -> None:
    """Sets the working folder path and updates the list of events."""
    global path, list_of_events
    path = new_path
    list_of_events = get_list()


def get_list() -> list:
    """Returns a list of events located in the working folder."""
    global path
    list_of_files = []
    for file in os.listdir(path):
        if file[-4:] == ".txt":
            if read_file_text(file[:-4])[:5] == "event":
                list_of_files.append(file[:-4])
    return list_of_files


# Create and delete an event
def new_event(name: str) -> None:
    """Creates a new event with some name."""
    global path
    f = open(f"{path}{name}.txt", 'w', encoding="utf-8")
    text = "event" + "\n\n" * 5
    f.write(cypher.encrypt_text(text, cypher.get_gamma_filename(name)))
    f.close()


def remove_event(name: str) -> None:
    """Deletes an event with the selected name."""
    global path
    os.remove(f"{path}{name}.txt")


# File text
def write_file_text(name: str, text: str) -> None:
    """Writes text to a file using gamma cipher."""
    global path
    f = open(f"{path}{name}.txt", 'w', encoding="utf-8")
    f.write(cypher.encrypt_text(text, cypher.get_gamma_filename(name)))
    f.close()


def read_file_text(name: str) -> str:
    """Returns decrypted text from a file."""
    global path
    f = open(f"{path}{name}.txt", 'r', encoding="utf-8")
    text = cypher.encrypt_text(f.read(), cypher.get_gamma_filename(name))
    f.close()
    return text


# Events setters
def set_title(name: str, title: str) -> None:
    """Changes the event title."""
    text = read_file_text(name).split("\n\n")
    text[1] = title
    text = "\n\n".join(text)
    write_file_text(name, text)


def set_description(name: str, description: str) -> None:
    """Changes the event description."""
    text = read_file_text(name).split("\n\n")
    text[2] = description
    text = "\n\n".join(text)
    write_file_text(name, text)


def set_time(name: str, start_time: str, end_time: str) -> None:
    """changes the time of the event."""
    text = read_file_text(name).split("\n\n")
    text[3] = start_time + '/' + end_time
    text = "\n\n".join(text)
    write_file_text(name, text)


def set_max_number_of_visitors(name: str, max_number_of_visitors: int) -> None:
    """Changes the maximum number of event visitors."""
    text = read_file_text(name).split("\n\n")
    numbers = text[4].split('/')
    numbers[1] = str(max_number_of_visitors)
    numbers = '/'.join(numbers)
    text[4] = numbers
    text = "\n\n".join(text)
    write_file_text(name, text)


def set_audience_number(name: str, audience_number: str) -> None:
    """Changes the location of the event."""
    text = read_file_text(name).split("\n\n")
    text[5] = audience_number
    text = "\n\n".join(text)
    write_file_text(name, text)


# Events getters
def get_title(name: str) -> str:
    """Returns the event title."""
    text = read_file_text(name).split("\n\n")
    title = text[1]
    return title


def get_description(name: str) -> str:
    """Returns the event description."""
    text = read_file_text(name).split("\n\n")
    description = text[2]
    return description


def get_time(name: str) -> list:
    """Returns the time of the event. [start, end]"""
    text = read_file_text(name).split("\n\n")
    time = text[3].split('/')
    return time


def get_numbers_of_visitors(name: str) -> list:
    """Returns the current and maximum number of visitors to an event. [current, max]"""
    text = read_file_text(name).split("\n\n")
    numbers = []
    for number in text[4].split('/'):
        numbers.append(int(number))
    return numbers


def get_audience_number(name: str) -> str:
    """Returns the location of the event."""
    text = read_file_text(name).split("\n\n")
    audience_number = text[5]
    return audience_number


# Additional functions
def add_visitor(name: str) -> None:
    """Increases the number of current visitors by one."""
    text = read_file_text(name).split("\n\n")
    numbers = text[4].split('/')
    numbers[0] = str(int(numbers[0]) + 1)
    numbers = '/'.join(numbers)
    text[4] = numbers
    text = "\n\n".join(text)
    write_file_text(name, text)
