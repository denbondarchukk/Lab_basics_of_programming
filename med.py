# min_edit_distance

def deletion_cost(sym):
    return 1


def insertion_cost(sym):
    return 1


def substitution_cost(sym1, sym2):
    if sym1 == sym2:
        return 0
    else:
        return 1


def min_edit_distance(source, target):
    source_length = len(source)
    target_length = len(target)
    D = [[0] * (target_length + 1) for _ in range(source_length + 1)]

    for i in range(1, source_length + 1):
        D[i][0] = D[i - 1][0] + deletion_cost(source[i - 1])
    for j in range(1, target_length + 1):
        D[0][j] = D[0][j - 1] + insertion_cost(target[j - 1])

    for i in range(1, source_length + 1):
        for j in range(1, target_length + 1):
            deletion = D[i - 1][j] + deletion_cost(source[i - 1])
            substitution = D[i - 1][j - 1] + substitution_cost(source[i - 1], target[j - 1])
            insertion = D[i][j - 1] + insertion_cost(target[j - 1])
            D[i][j] = min(deletion, substitution, insertion)

    return D


words = ["калина", "ожина", "країна", "травинка", "сніжинка"]

min_distance = float('inf')  # змінна для збереження мінімальної відстані редагувань, встановлена на нескінченність
closest_word_pairs = []
distance_tables = {}  # словник для збереження таблиць

for i in range(len(words)):
    for j in range(i + 1, len(words)):
        distance_table = min_edit_distance(words[i], words[j])
        distance_tables[(words[i], words[j])] = distance_table  # зберігання таблиці обчислень у словник
        distance = distance_table[len(words[i])][len(words[j])]

        if distance < min_distance:  # порівняння поточної відстані редагування з мінімальною
            min_distance = distance
            closest_word_pairs = [(words[i], words[j])]
        elif distance == min_distance:
            closest_word_pairs.append((words[i], words[j]))

print(f"Найближча пара слів з мінімальною відстанню редагування: {closest_word_pairs} з дистанцією {min_distance}.")

print("\nВідповідні таблиці обчислення:")
for word_pair, table in distance_tables.items():
    print(f"Таблиця для слів: {word_pair}")
    for row in table:
        print(row)
    print("\n")
