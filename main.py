import wordfreq
import random

word_list = wordfreq.top_n_list('en', 20000)


def code_gen(num: int) -> list:
    code = []
    for _ in range(num):
        code.append(random.randint(1, 9))

    return code


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

print(decode("The wind whispered through the trees as the sun dipped below the horizon, casting a golden glow"
             " over the quiet village. A cat stretched lazily on a windowsill, uninterested in the distant sound"
             " of laughter from the children chasing fireflies. Everything seemed paused in a moment of calm, as"
             " if the world were holding its breath before nightfall.", 15484627917))
