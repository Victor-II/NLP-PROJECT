import spacy
import re

def read_file(path:str) -> str:
    text = ''
    with open(path, 'r') as f:
        text = f.read()
    return text

def discard_extra_spaces(text:str) -> str:
    text = ' '.join(text.splitlines())
    return re.sub(' +', ' ', text)


def preprocess(text:str) -> list[list]:
    res = []
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text.lower())
    for sentence in doc.sents:
        s = [token.text for token in sentence if not (token.is_stop or token.is_punct)]
        if s:
            res.append(s)
    return res

def epiphora_search(chapter:list[list]) -> list[list[list]]:
    res = []
    epiphora = []

    for i in range(len(chapter)-1):
        if chapter[i][-1] == chapter[i+1][-1]:
            if not epiphora:
                epiphora = [chapter[i], chapter[i+1]]
            else:
                epiphora.append(chapter[i+1])
        elif epiphora:
            res.append(epiphora)
            epiphora = []
    if epiphora:
        res.append(epiphora)

    return res

def anaphora_search(chapter:list[list]) -> list[list[list]]:
    res = []
    anaphora = []

    for i in range(len(chapter)-1):
        if chapter[i][0] == chapter[i+1][0]:
            if not anaphora:
                anaphora = [chapter[i], chapter[i+1]]
            else:
                anaphora.append(chapter[i+1])
        elif anaphora:
            res.append(anaphora)
            anaphora = []
    if anaphora:
        res.append(anaphora)

    return res

def epanalepsis_search(chapter:list[list]) -> list[list[list]]:
    res = []

    for i in range(len(chapter)):
        if chapter[i][0] == chapter[i][-1] and len(chapter[i]) > 2 and chapter[i][0] != chapter[i][len(chapter[i])//2]:
            res.append(chapter[i])

    return res

if __name__ == '__main__':
    t = read_file('sirens.txt')
    t = discard_extra_spaces(t)
    t = preprocess(t)
    e = epanalepsis_search(t)
    print(e[:5])