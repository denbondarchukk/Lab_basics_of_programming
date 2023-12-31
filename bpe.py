import urllib.request
import re
from collections import defaultdict


def load_corpus(target_url):
    if target_url is None:
        raise TypeError("Invalid file URL provided")
    downloaded_content = urllib.request.urlopen(target_url)

    lines = []

    for line in downloaded_content:
        decoded_line = line.decode("utf-8")
        lines.append(decoded_line)

    return "".join(lines)


corpus_text = load_corpus(
    "https://github.com/brown-uk/corpus/raw/master/data/good/A_Ekho_Sitchenko_Lebedyna_virnist_2018.txt")


# byte-pair encoding

def get_pairs(vocab):  # функція для отримання пар символів
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[(symbols[i], symbols[i + 1])] += freq
    return pairs


def merge_vocab(pair, vocab_input):  # функція, яка замінює пару символів на один об'єднаний токен
    vocab_output = {}
    pair_str = ' '.join(pair)
    for word in vocab_input:
        if pair_str in word:
            updated_word = word.replace(pair_str, ''.join(pair))
            vocab_output[updated_word] = vocab_input[word]
        else:
            vocab_output[word] = vocab_input[word]

    if pair_str not in vocab_output:  # уникнення повторного злиття одних і тих самих пар символів
        vocab_output[pair_str] = 1

    return vocab_output


def byte_pair_encoding(text, k):
    tokens = re.findall(r"\b[А-ЯІЇЄа-яіїє'-]+\b", text)  # знаходження всіх слів у тексті

    vocab = defaultdict(int)
    for token in tokens:
        vocab[' '.join(token) + ' #'] = 1  # Створення словника та ініціалізація частоти входження

    for i in range(k):
        pairs = get_pairs(vocab)
        if not pairs:
            break

        most_freq = max(pairs, key=pairs.get)
        vocab = merge_vocab(most_freq, vocab)

    token_dict = set()
    for token in vocab.keys():
        token_list = token.split()
        for symbol in token_list:
            if symbol not in token_dict:
                token_dict.add(symbol)

    sorted_token_dict = sorted(token_dict)
    return sorted_token_dict


while True:
    try:
        k_input = input("Введіть кількість сполучень (або 'вихід'): ")
    except KeyboardInterrupt:
        break

    if k_input.lower() == "вихід":
        break

    try:
        k = int(k_input)
        result = byte_pair_encoding(corpus_text, k)
        print(f"Результати виконання алгоритму byte-pair encoding після {k} сполучень:")
        for item in result:
            print(item)
    except ValueError:
        print("Будь ласка, введіть ціле число або 'вихід'.")
