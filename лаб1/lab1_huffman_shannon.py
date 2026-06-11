import heapq
from collections import Counter

def get_frequencies(text: str) -> dict:
    return dict(Counter(text))

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encode(frequencies: dict) -> dict:
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        node = heapq.heappop(heap)
        return {node.char: '0'}

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    root = heapq.heappop(heap)
    codes = {}
    
    def generate_codes(node, current_code):
        if node is None: return
        if node.char is not None:
            codes[node.char] = current_code
            return
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(root, "")
    return codes

def shannon_fano_encode(frequencies: dict) -> dict:
    sorted_chars = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    codes = {}

    def build_codes(char_list, current_code):
        if len(char_list) == 1:
            codes[char_list[0][0]] = current_code if current_code else '0'
            return

        total_freq = sum(freq for _, freq in char_list)
        left_sum = 0
        split_idx = 0
        min_diff = float('inf')

        for i in range(len(char_list) - 1):
            left_sum += char_list[i][1]
            right_sum = total_freq - left_sum
            diff = abs(left_sum - right_sum)
            if diff < min_diff:
                min_diff = diff
                split_idx = i + 1

        left_part = char_list[:split_idx]
        right_part = char_list[split_idx:]

        build_codes(left_part, current_code + "0")
        build_codes(right_part, current_code + "1")

    build_codes(sorted_chars, "")
    return codes

def get_compressed_size(text, codes):
    freq = get_frequencies(text)
    return sum(freq[char] * len(code) for char, code in codes.items())

def get_average_length(text, codes):
    total_bits = get_compressed_size(text, codes)
    return total_bits / len(text)

def analyze_text(text, label=""):
    print(f"\n{'='*60}")
    if label:
        print(f"АНАЛИЗ: {label}")
    print(f"Строка: '{text}'")
    print(f"{'='*60}")

    freq = get_frequencies(text)
    print(f"1. Частоты символов: {freq}")

    huff_codes = huffman_encode(freq)
    sf_codes = shannon_fano_encode(freq)
    print(f"2. Коды Хаффмана:     {huff_codes}")
    print(f"   Коды Шеннона-Фано: {sf_codes}")

    huff_avg = get_average_length(text, huff_codes)
    sf_avg = get_average_length(text, sf_codes)
    
    print(f"3. Средняя длина кода Хаффмана:     L = {huff_avg:.4f}")
    print(f"   Средняя длина кода Шеннона-Фано: L = {sf_avg:.4f}")

    huff_bits = get_compressed_size(text, huff_codes)
    sf_bits = get_compressed_size(text, sf_codes)
    original_bytes = len(text.encode('utf-8'))
    original_bits = original_bytes * 8
    
    print(f"4. Исходный размер: {original_bits} бит ({original_bytes} байт)")
    print(f"   Сжатый размер (Хаффман):     {huff_bits} бит")
    print(f"   Сжатый размер (Шеннон-Фано): {sf_bits} бит")

    if sf_avg > huff_avg:
        print(f"   РАЗЛИЧИЕ: Шеннон-Фано хуже на {(sf_avg - huff_avg):.4f} бит/символ")
    else:
        print(f"   РЕЗУЛЬТАТ: Средняя длина кодов совпадает")

# --- ПУНКТ 1 ---
print("### ПУНКТ 1: Реализация функций построения кодов ###")
example_freq = {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
print(f"Входные частоты: {example_freq}")
print(f"Коды Хаффмана:    {huffman_encode(example_freq)}")
print(f"Коды Шеннона-Фано: {shannon_fano_encode(example_freq)}")

# --- ПУНКТ 2 ---
print("\n\n### ПУНКТ 2: Базовые тестовые строки ###")
for t in ["abracadabra", "Hello World!", "aaaabbbccd"]:
    analyze_text(t)

# --- ПУНКТ 3 (Пользовательские строки) ---
print("\n\n### ПУНКТ 3: ###")
user_strings = [
    ("chechnya doooooooooon", "chechnya doooooooooon"),
    ("алгоритм доты2", "алгоритм доты2"),
    ("просто z", "просто z")
]
for label, text in user_strings:
    analyze_text(text, label)

# --- ПУНКТ 3 (Примеры неоптимальности) ---
print("\n\n### ПУНКТ 3: Примеры неоптимальности Шеннона-Фано ###")
analyze_text("AAAAAAABBBCCCDDDEEE", "Пример 1 (частоты: A=7, B=3, C=3, D=3, E=3)")
analyze_text("AAAAAABBBBCCCD", "Пример 2 (частоты: A=6, B=4, C=3, D=1)")