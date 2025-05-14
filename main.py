from string import ascii_lowercase, punctuation
from nltk.corpus import words
import wordfreq
import random

word_list = wordfreq.top_n_list('en', 20000)
eng_words = words.words()
letter_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 'c',
               'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']

# generate a random code for the encryption method encode
def code_gen(num: int) -> list:
    code = []
    for _ in range(num):
        code.append(random.randint(1, 9))

    return code


# encodes a piece of text in some random string of words by using a code
def encode(text: str):
    text_word = text.split(" ")
    rule = code_gen(len(text_word))
    leny = sum(rule)+random.randint(0, 10)
    sample = []
    for _ in range(leny):
        filler = random.choice(word_list)
        sample.append(filler)

    x = 0
    for i in rule:
        x += i
        sample[x-1] = text_word.pop(0)

    encoded_text = " ".join(sample)

    encryption_code = 0
    for j in range(len(rule)):
        add = rule[j]*(10**j)
        encryption_code += add

    encryption_code = int(str(encryption_code)[::-1])
    return [encoded_text.lower(), encryption_code]


# decodes a random string of words to get a secret message using a secret code
def decode(text: str, code: int):
    code_list = list(str(code))
    rule = [int(thing) for thing in code_list]

    text = text.lower()
    msg_list = text.split(" ")
    result = ""

    x = 0
    for i in rule:
        x += i
        result += " " + msg_list[x-1]

    return result


# gives the key with the maximum value in a dictionary
def dict_max(simple: dict):
    high = -1
    high_key = " "
    for i in simple:
        if simple[i] > high:
            high = simple[i]
            high_key = i
    return high_key


# shifts every letter in a string forward by some amount (ceaser cipher)
def rotate(texty, num: int, care=False):
    texty = texty.lower()
    lst = list(ascii_lowercase)
    result = ""
    for i in texty:
        try:
            result += lst[(lst.index(i) + num) % 26]
        except ValueError:
            if care:
                if i == " ":
                    result += " "
                else:
                    result += " " + i + " "
            else:
                result += i

    return result


# grades or gives score to a list of strings based on how many english words are there in that list
def grade(plain):
    sc = 0
    for i in plain:
        if i in eng_words:
            sc += 1

    return sc


# cracks any ceaser cipher by using english word recognition and returns the plain text
def crack(text: str):
    text = text.lower()
    score = []
    for i in range(0, 26):
        trial_text = rotate(text, i, care=True)
        wordly = trial_text.split(" ")
        score.append(grade(wordly))

    best_match = max(score)
    plain_text = rotate(text, score.index(best_match))

    return plain_text


# generates a random key for assignment cipher
def key_gen():
    result = {}
    for i in ascii_lowercase:
        result[i] = random.choice(list(ascii_lowercase))


# assigns certain letters to other letters based on frequency (used to crack assignment cipher)
def assign(counter):
    key = {}
    for i in letter_freq:
        key[dict_max(counter)] = i
        counter[dict_max(counter)] = -1

    print(key)
    return key


# decrypts or encrypts a given text based on a given key using assignment cipher
def assign_cipher(text, key_dict=key_gen()):
    result = ""
    for i in text.lower():
        if i in key_dict:
            result += key_dict[i]
        else:
            result += i

    return result


# cracks a cipher text(assignment cipher) using frecuency analysis (Efficiency increases with the amount of text)
def alpha_fra(text):
    lst = list(text.lower())
    symbols = set(lst)
    symbols.remove(" ")
    for i in punctuation:
        if i in symbols:
            symbols.remove(i)
    symbols = list(symbols)
    occur_count = {key: lst.count(key) for key in symbols}
    return assign_cipher(text, assign(occur_count))


# performs the frecuency analysis given number of times on a give text.
def repeater(text, num=1):
    result = text
    for _ in range(num):
        result = alpha_fra(result)

    return result
