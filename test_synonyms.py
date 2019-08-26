import argparse
import random
from datetime import datetime

parser = argparse.ArgumentParser('Guess the word!')

parser.add_argument('--num_words', type=int, default=None,
                    help='How many words you want to predict?')
parser.add_argument('--input-file')


def export_families(input_file):
    # maps word to family
    word_families = {}

    # maps family to words
    family_words = {}
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            _split = line.split('=')
            word = _split[0]
            try:
                synonyms = _split[2]
            except:
                continue
            _synonyms = synonyms.split('/')

            family_id = None

            if word in word_families:
                family_id = word_families[word]
            else:
                for synonym in _synonyms:
                    synonym = synonym.strip(' ')
                    if synonym in word_families:
                        family_id = word_families[synonym]
                        break

            if family_id is None:
                family_id = word

            word_families[word] = family_id
            for synonym in _synonyms:
                synonym = synonym.strip(' ')
                word_families[synonym] = family_id

    for word, family_id in word_families.items():
        if family_id in family_words:
            if word not in family_words[family_id]:
                family_words[family_id].append(word)
        else:
            family_words[family_id] = [word]
    return word_families, family_words


def choose_the_correct_synonym(family_words, word_families, among=5):
    all_words = list(word_families.keys())
    global correct
    global total
    while True:
        possible_synonyms = []
        for i in range(among):
            # choose a random family
            indx = random.randint(0, len(all_words) - 1)
            key_word = word_families[all_words[indx]]
            family = family_words[key_word]

            # choose a random word from the family
            word = family[random.randint(0, len(family) - 1)]
            possible_synonyms.append(word)
            if i == among - 1:
                while True:
                    word = family[random.randint(0, len(family) - 1)]
                    if word != possible_synonyms[-1]:
                        real_word = word
                        break

        synonym = possible_synonyms[-1]
        random.shuffle(possible_synonyms)

        print('We are looking possible synonyms of ' + real_word)
        print(possible_synonyms)
        try:
            ans = int(input())
        except:
            finish()
        if 1 <= ans <= len(possible_synonyms) and possible_synonyms[ans-1] == synonym:
            print('Correct!')
            correct += 1
        else:
            print('The correct answer is: {}'.format(synonym))
        print()
        total += 1

def finish():
    global correct
    global total
    print('Signal caught! Exiting')
    print('{}/{} {}\%'.format(correct, total, correct / total * 100))
    exit()

if __name__ == '__main__':
    correct = 0
    total = 0
    args = parser.parse_args()
    random.seed(datetime.now())
    word_families, family_words = export_families(args.input_file)
    choose_the_correct_synonym(family_words, word_families)
