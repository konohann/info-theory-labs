import time

# ==================== LZ77 ====================
class LZ77:
    def __init__(self, window_size=4096, buffer_size=16):
        self.window_size = window_size
        self.buffer_size = buffer_size
    
    def compress(self, text):
        tokens = []
        i = 0
        while i < len(text):
            match = self._find_longest_match(text, i)
            if match[1] == 0:
                tokens.append((0, 0, text[i]))
                i += 1
            else:
                tokens.append(match)
                i += match[1]
        return tokens
    
    def _find_longest_match(self, text, position):
        start = max(0, position - self.window_size)
        end = position
        max_length = 0
        best_offset = 0
        
        for i in range(start, end):
            length = 0
            while (position + length < len(text) and 
                   text[i + length] == text[position + length] and
                   length < self.buffer_size):
                length += 1
            if length > max_length:
                max_length = length
                best_offset = position - i
        
        return (best_offset, max_length, text[position] if max_length == 0 else '')
    
    def decompress(self, tokens):
        text = []
        for offset, length, char in tokens:
            if length == 0:
                text.append(char)
            else:
                start = len(text) - offset
                for i in range(length):
                    text.append(text[start + i])
        return ''.join(text)
    
    def get_compressed_size_bits(self, tokens):
        # offset (12 bits) + length (4 bits) + char (8 bits) = 24 bits per token
        # Overhead словаря минимален (фиксированные размеры окна и буфера)
        return len(tokens) * 24


# ==================== LZ78 ====================
class LZ78:
    def __init__(self):
        self.dictionary = {}
    
    def compress(self, text):
        self.dictionary = {'': 0}
        tokens = []
        current = ''
        
        for char in text:
            if current + char in self.dictionary:
                current += char
            else:
                self.dictionary[current + char] = len(self.dictionary)
                tokens.append((self.dictionary[current], char))
                current = ''
        
        if current:
            tokens.append((self.dictionary[current], ''))
        
        return tokens
    
    def decompress(self, tokens):
        dictionary = ['']
        text = []
        
        for index, char in tokens:
            if index < len(dictionary):
                entry = dictionary[index] + char
            else:
                entry = dictionary[index]
            text.append(entry)
            dictionary.append(entry)
        
        return ''.join(text)
    
    def get_compressed_size_bits(self, tokens):
        # index (12 bits) + char (8 bits) = 20 bits per token
        # Overhead словаря: каждая запись = индекс (12 бит) + символ (8 бит) = 20 бит
        dict_overhead = (len(self.dictionary) - 1) * 20
        return len(tokens) * 20 + dict_overhead


# ==================== LZW ====================
class LZW:
    def __init__(self):
        self.dictionary = {}
    
    def compress(self, text):
        self.dictionary = {chr(i): i for i in range(256)}
        tokens = []
        current = ''
        
        for char in text:
            if current + char in self.dictionary:
                current += char
            else:
                tokens.append(self.dictionary[current])
                self.dictionary[current + char] = len(self.dictionary)
                current = char
        
        if current:
            tokens.append(self.dictionary[current])
        
        return tokens
    
    def decompress(self, tokens):
        dictionary = {i: chr(i) for i in range(256)}
        text = []
        current = chr(tokens[0])
        text.append(current)
        
        for code in tokens[1:]:
            if code in dictionary:
                entry = dictionary[code]
            else:
                entry = current + current[0]
            text.append(entry)
            dictionary[len(dictionary)] = current + entry[0]
            current = entry
        
        return ''.join(text)
    
    def get_compressed_size_bits(self, tokens):
        # 12 bits per code
        # Overhead словаря: начальная инициализация 256 записей по 8 бит = 2048 бит
        dict_overhead = 256 * 8
        return len(tokens) * 12 + dict_overhead


# ==================== Тестирование ====================
def test_algorithms():
    test_strings = [
        ("abracadabra", "Короткий текст"),
        ("a" * 100, "Повторяющийся текст"),
        ("abcdef123456", "Уникальные символы")
    ]
    
    lz77 = LZ77()
    lz78 = LZ78()
    lzw = LZW()
    
    results = []
    
    for text, description in test_strings:
        print(f"\n{'='*60}")
        print(f"Тест: {description}")
        print(f"Строка: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"{'='*60}")
        
        original_size = len(text) * 8  # bits
        
        # LZ77
        start = time.time()
        lz77_tokens = lz77.compress(text)
        lz77_time = time.time() - start
        lz77_size = lz77.get_compressed_size_bits(lz77_tokens)
        lz77_decompressed = lz77.decompress(lz77_tokens)
        
        # LZ78
        start = time.time()
        lz78_tokens = lz78.compress(text)
        lz78_time = time.time() - start
        lz78_size = lz78.get_compressed_size_bits(lz78_tokens)
        lz78_decompressed = lz78.decompress(lz78_tokens)
        
        # LZW
        start = time.time()
        lzw_tokens = lzw.compress(text)
        lzw_time = time.time() - start
        lzw_size = lzw.get_compressed_size_bits(lzw_tokens)
        lzw_decompressed = lzw.decompress(lzw_tokens)
        
        print(f"\nLZ77:")
        print(f"  Токенов: {len(lz77_tokens)}")
        print(f"  Размер: {lz77_size} бит")
        print(f"  Степень сжатия: {lz77_size/original_size:.4f}")
        print(f"  Время: {lz77_time*1000:.2f} мс")
        print(f"  Проверка: {'OK' if text == lz77_decompressed else 'FAIL'}")
        
        print(f"\nLZ78:")
        print(f"  Токенов: {len(lz78_tokens)}")
        print(f"  Размер: {lz78_size} бит (с overhead словаря: {(len(lz78.dictionary) - 1) * 20} бит)")
        print(f"  Степень сжатия: {lz78_size/original_size:.4f}")
        print(f"  Время: {lz78_time*1000:.2f} мс")
        print(f"  Проверка: {'OK' if text == lz78_decompressed else 'FAIL'}")
        
        print(f"\nLZW:")
        print(f"  Токенов: {len(lzw_tokens)}")
        print(f"  Размер: {lzw_size} бит (с overhead словаря: 2048 бит)")
        print(f"  Степень сжатия: {lzw_size/original_size:.4f}")
        print(f"  Время: {lzw_time*1000:.2f} мс")
        print(f"  Проверка: {'OK' if text == lzw_decompressed else 'FAIL'}")
        
        results.append({
            'text': text,
            'description': description,
            'original_size': original_size,
            'lz77': {'tokens': len(lz77_tokens), 'size': lz77_size, 'ratio': lz77_size/original_size, 'time': lz77_time},
            'lz78': {'tokens': len(lz78_tokens), 'size': lz78_size, 'ratio': lz78_size/original_size, 'time': lz78_time},
            'lzw': {'tokens': len(lzw_tokens), 'size': lzw_size, 'ratio': lzw_size/original_size, 'time': lzw_time}
        })
    
    return results


if __name__ == "__main__":
    results = test_algorithms()