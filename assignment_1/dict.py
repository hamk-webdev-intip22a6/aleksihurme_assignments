import json

file_path = "dictdata.json"


def empty_json_check(file_path):
    try:
        with open(file_path, "r") as file:
            return not bool(file.read()) #True jos tyhjä.
    except FileNotFoundError:
        print("Error: File was not found")
    except PermissionError:
        print("Error: You do not have permission to read this file: " + file_path)
    
def input_validator(word):
    
    if any(char.isdigit() for char in word):
        print("Invalid input. Do not use numbers")
        return False
    
    elif any(char.isupper() for char in word[1:]):
        print("Invalid input. Write word in the following ways: 'example' or 'Example'")
        return False
    
    elif " " in word:
        print("Invalid input. Do not add spaces to the word")
        return False
    
    else:
        return True
    

def search():
    while True:
        print("Give me a word (or type 'q' to quit)")
        given_word = input()

        if given_word.lower() == "q":
            break

        else:
            validity = input_validator(given_word)
            if validity:
                if given_word in dict.keys():
                    print(given_word, " = ", dict[given_word])
                    #search()

                else:
                    print("Word not found in dictionary. Give translation.")
                    translation = input()
                    validity = input_validator(translation)
                    if validity:
                        dict[given_word] = translation
                        try:
                            with open("dictdata.json", "w") as outfile:
                                json.dump(dict, outfile)
                            print(dict)
                        except PermissionError:
                            print("Error: You do not have permission to write to this file: " + file_path)
                        except OSError:
                            print("Error: could not write to the file: " + file_path)
            else:
                break




if empty_json_check(file_path):                 #Pääkoodi
    dict = {"cat": "kissa", "dog": "koira"}     #Jos tiedosto tyhjä antaa alustavan sanaston
else:
    try:
        with open(file_path, "r") as file:
            data = file.read()
            print("File content:", data)
            dict = json.loads(data)
            print("Loaded dictionary:", dict)
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
search()