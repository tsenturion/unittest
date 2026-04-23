import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import heapq
import math
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

class CompressionVisualizerColab:
    def __init__(self):
        plt.rcParams['figure.dpi'] = 100
        self.setup_ui()
    
    def setup_ui(self):
        display(HTML("<h1>📊 Визуализация алгоритмов сжатия данных</h1>"))
        display(HTML("<h3>RLE (Run-Length Encoding) и Huffman Coding</h3>"))
        
        display(HTML("<h4>📝 Введите текст для сжатия:</h4>"))
        self.text_input = widgets.Textarea(
            value="AAAAABBBCCCCDDDDDEEEEFFFFFFFFFFFFFGGGGGHHHHIIIIIJJJKKKLLLMMMNNNOOOPPPQQQRRRSSSTTTUUUVVVWWWXXXYYYZZZ",
            placeholder="Введите текст здесь...",
            layout=widgets.Layout(width='100%', height='150px')
        )
        
        self.rle_btn = widgets.Button(
            description="Сжать RLE",
            button_style='primary',
            layout=widgets.Layout(width='200px', margin='10px')
        )
        
        self.huffman_btn = widgets.Button(
            description="Сжать Хаффманом",
            button_style='success',
            layout=widgets.Layout(width='200px', margin='10px')
        )
        
        self.clear_btn = widgets.Button(
            description="Очистить",
            button_style='warning',
            layout=widgets.Layout(width='150px', margin='10px')
        )
        
        button_box = widgets.HBox([self.rle_btn, self.huffman_btn, self.clear_btn])
        self.output_area = widgets.Output()
        
        self.rle_btn.on_click(self.compress_rle)
        self.huffman_btn.on_click(self.compress_huffman)
        self.clear_btn.on_click(self.clear_all)
        
        display(self.text_input)
        display(button_box)
        display(self.output_area)
        
        display(HTML("<i>💡 Совет: попробуйте ввести текст с повторяющимися символами для RLE или разнообразный текст для Хаффмана</i>"))
    
    def clear_all(self, b):
        self.text_input.value = ""
        with self.output_area:
            clear_output()
    
    def compress_rle(self, b):
        text = self.text_input.value
        if not text:
            with self.output_area:
                clear_output()
                print("⚠️ Пожалуйста, введите текст для сжатия")
            return
        
        with self.output_area:
            clear_output()
            
            # RLE сжатие
            compressed = []
            steps = []
            i = 0
            
            while i < len(text):
                count = 1
                while i + count < len(text) and text[i + count] == text[i]:
                    count += 1
                
                if count > 1:
                    compressed.append(f"{count}{text[i]}")
                    steps.append(f"'{text[i]}' повторяется {count} раз -> кодируем как '{count}{text[i]}'")
                else:
                    compressed.append(text[i])
                    steps.append(f"'{text[i]}' встречается 1 раз -> оставляем как есть")
                
                i += count
            
            compressed_str = ''.join(compressed)
            print("=" * 80)
            print("📦 RLE СЖАТИЕ")
            print("=" * 80)
            print(f"\n📝 Оригинальный текст:")
            print(f"\"{text[:200]}{'...' if len(text) > 200 else ''}\"")
            print(f"\n🔒 Сжатый текст (RLE):")
            print(f"\"{compressed_str[:200]}{'...' if len(compressed_str) > 200 else ''}\"")
            print(f"\n📋 Процесс сжатия:")
            for step in steps[:10]:
                print(f"  • {step}")
            if len(steps) > 10:
                print(f"  ... и еще {len(steps) - 10} шагов")

            original_size = len(text.encode('utf-8'))
            compressed_size = len(compressed_str.encode('utf-8'))
            ratio = (1 - compressed_size/original_size) * 100 if original_size > 0 else 0
            
            print(f"\n📈 Статистика:")
            print(f"  Исходный размер: {original_size} байт")
            print(f"  Размер после сжатия: {compressed_size} байт")
            print(f"  Степень сжатия: {ratio:.1f}%")
            print(f"  Коэффициент сжатия: {original_size/compressed_size:.2f}x")
            
            self.visualize_rle(text, compressed_str)
    
    def visualize_rle(self, original, compressed):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        show_len = min(100, len(original))
        orig_chars = list(original[:show_len])
        ax1.bar(range(len(orig_chars)), [1]*len(orig_chars), color='skyblue', alpha=0.7, edgecolor='black')
        ax1.set_title(f'📄 Оригинал (первые {show_len} из {len(original)} символов)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Позиция символа')
        ax1.set_ylim(0, 1.5)
        ax1.set_xlim(-1, show_len)

        show_len2 = min(100, len(compressed))
        comp_chars = list(compressed[:show_len2])
        ax2.bar(range(len(comp_chars)), [1]*len(comp_chars), color='lightgreen', alpha=0.7, edgecolor='black')
        ax2.set_title(f'🔒 После RLE (первые {show_len2} из {len(compressed)} символов)', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Позиция символа')
        ax2.set_ylim(0, 1.5)
        ax2.set_xlim(-1, show_len2)
        
        fig.suptitle('📊 Визуализация сжатия RLE', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def build_huffman_tree(self, text):
        freq = Counter(text)
        heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        
        return heap[0] if heap else None
    
    def generate_codes(self, node, code="", codes=None):
        if codes is None:
            codes = {}
        
        if node is None:
            return codes
        
        if node.char is not None:
            codes[node.char] = code
            return codes
        
        self.generate_codes(node.left, code + "0", codes)
        self.generate_codes(node.right, code + "1", codes)
        return codes
    
    def compress_huffman(self, b):
        text = self.text_input.value
        if not text:
            with self.output_area:
                clear_output()
                print("⚠️ Пожалуйста, введите текст для сжатия")
            return
        
        with self.output_area:
            clear_output()
            
            # Построение дерева Хаффмана
            root = self.build_huffman_tree(text)
            if not root:
                print("❌ Ошибка при построении дерева")
                return
            
            codes = self.generate_codes(root, "", {})
            compressed_bits = ''.join(codes[char] for char in text)
            
            print("=" * 80)
            print("🌳 СЖАТИЕ ХАФФМАНОМ")
            print("=" * 80)
            
            print(f"\n📝 Оригинальный текст:")
            print(f"\"{text[:200]}{'...' if len(text) > 200 else ''}\"")
            print(f"\n📊 Количество уникальных символов: {len(codes)}")
            
            print(f"\n📋 КОДЫ СИМВОЛОВ:")
            print("-" * 50)
            sorted_codes = sorted(codes.items(), key=lambda x: (len(x[1]), -Counter(text)[x[0]]))
            for char, code in sorted_codes[:20]:
                count = Counter(text)[char]
                display_char = repr(char) if char == '\n' else char
                print(f"  Символ: '{display_char}' | Частота: {count:4d} | Код: {code} | Длина: {len(code)} бит")
            if len(codes) > 20:
                print(f"  ... и еще {len(codes) - 20} символов")
            
            print(f"\n🔒 СЖАТЫЕ ДАННЫЕ:")
            print("-" * 50)
            print(f"  Всего бит: {len(compressed_bits)}")
            print(f"  Первые 200 бит: {compressed_bits[:200]}{'...' if len(compressed_bits) > 200 else ''}")
            
            # Подробная статистика
            original_size_bits = len(text) * 8
            compressed_size_bits = len(compressed_bits)
            ratio = (1 - compressed_size_bits/original_size_bits) * 100 if original_size_bits > 0 else 0
            entropy = self.calculate_entropy(text)
            avg_code_length = compressed_size_bits / len(text)
            
            print(f"\n📈 ПОДРОБНАЯ СТАТИСТИКА:")
            print("=" * 50)
            print(f"  📊 Исходный размер:     {original_size_bits:8d} бит ({original_size_bits//8:4d} байт)")
            print(f"  📊 Размер после сжатия: {compressed_size_bits:8d} бит ({compressed_size_bits//8 + (1 if compressed_size_bits%8 else 0):4d} байт)")
            print(f"  📊 Экономия:            {original_size_bits - compressed_size_bits:8d} бит")
            print(f"  📊 Степень сжатия:      {ratio:17.1f}%")
            print(f"  📊 Коэффициент сжатия:  {original_size_bits/compressed_size_bits:14.2f}x")
            print(f"  📊 Энтропия текста:     {entropy:17.2f} бит/символ")
            print(f"  📊 Средняя длина кода:  {avg_code_length:17.2f} бит/символ")
            print(f"  📊 Теоретический минимум: {entropy:.2f} бит/символ")
            print(f"  📊 Эффективность кода:  {(entropy/avg_code_length)*100:17.1f}%")
            
            # Визуализации
            print("\n🎨 Генерация визуализаций...")
            self.visualize_huffman_tree(root, codes, text)
            self.visualize_frequency_distribution(text, codes)
            self.visualize_compression_comparison(original_size_bits, compressed_size_bits)
            self.visualize_code_length_distribution(codes, text)
            
            print("\n✅ Все визуализации успешно созданы!")
    
    def calculate_entropy(self, text):
        freq = Counter(text)
        total = len(text)
        entropy = 0
        for count in freq.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy
    
    def visualize_huffman_tree(self, root, codes, text):
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))
        
        def plot_tree(node, x, y, dx, ax, level=0):
            if node is None:
                return
            
            if node.char is not None:
                label = f"'{node.char}'\n{node.freq}"
                color = 'lightgreen'
                size = 1500
            else:
                label = f"{node.freq}"
                color = 'lightblue'
                size = 1200
            
            ax.scatter(x, y, s=size, c=color, zorder=2, edgecolors='black', linewidth=1.5)
            ax.annotate(label, (x, y), ha='center', va='center', fontsize=9, fontweight='bold')
            
            if node.left:
                ax.plot([x, x - dx], [y, y - 1], 'k-', zorder=1, linewidth=1.5)
                mid_x = (x + (x - dx)) / 2
                mid_y = (y + (y - 1)) / 2
                ax.annotate('0', (mid_x, mid_y), ha='center', va='center', 
                           fontsize=10, color='red', fontweight='bold',
                           bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', edgecolor='red'))
                plot_tree(node.left, x - dx, y - 1, dx/2, ax, level+1)
            
            if node.right:
                ax.plot([x, x + dx], [y, y - 1], 'k-', zorder=1, linewidth=1.5)
                mid_x = (x + (x + dx)) / 2
                mid_y = (y + (y - 1)) / 2
                ax.annotate('1', (mid_x, mid_y), ha='center', va='center', 
                           fontsize=10, color='blue', fontweight='bold',
                           bbox=dict(boxstyle='circle,pad=0.2', facecolor='white', edgecolor='blue'))
                plot_tree(node.right, x + dx, y - 1, dx/2, ax, level+1)
        
        plot_tree(root, 0, 0, 5, ax)
        ax.set_title('🌳 Дерево Хаффмана (0 - левая ветка, 1 - правая ветка)', fontsize=14, fontweight='bold')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-8, 2)
        ax.axis('off')
        ax.grid(False)
        
        info_text = f"Всего символов: {len(text)}\nУникальных символов: {len(codes)}"
        ax.text(-9, -7, info_text, fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def visualize_frequency_distribution(self, text, codes):
        freq = Counter(text)
        chars = list(freq.keys())
        freqs = list(freq.values())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        bars = ax1.bar(range(len(chars)), freqs, color='skyblue', alpha=0.7, edgecolor='black')
        ax1.set_xticks(range(len(chars)))
        ax1.set_xticklabels([repr(c) if c == '\n' else c for c in chars], rotation=45, ha='right')
        ax1.set_title('📊 Частота символов в тексте', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Символ')
        ax1.set_ylabel('Частота')
        
        for bar, char in zip(bars, chars):
            if char in codes:
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                        codes[char], ha='center', va='bottom', fontsize=8, rotation=0,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(chars)))
        wedges, texts, autotexts = ax2.pie(freqs, labels=[repr(c) if c == '\n' else c for c in chars], 
                autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('🍕 Распределение символов', fontsize=12, fontweight='bold')
        
        plt.suptitle(f'Анализ частот и кодирование (всего символов: {len(text)})', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def visualize_compression_comparison(self, original_size, compressed_size):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        sizes = [original_size, compressed_size]
        labels = ['Исходный\n(8 бит/символ)', 'Сжатый\n(Хаффман)']
        colors = ['lightcoral', 'lightgreen']
        
        bars = ax1.bar(labels, sizes, color=colors, alpha=0.8, edgecolor='black')
        ax1.set_ylabel('Размер (биты)', fontsize=11)
        ax1.set_title('📏 Сравнение размера данных', fontsize=12, fontweight='bold')
        
        for bar, size in zip(bars, sizes):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(sizes)*0.02, 
                    f'{size} бит\n({size//8} байт)', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        saved = original_size - compressed_size
        if saved >= 0:
            ax2.pie([compressed_size, saved], labels=['Сжатые данные', f'Сэкономлено\n{saved} бит'], 
                    autopct='%1.1f%%', colors=['lightgreen', 'gold'], startangle=90)
            ax2.set_title('💾 Экономия памяти', fontsize=12, fontweight='bold')
        else:
            ax2.text(0.5, 0.5, 'Сжатие неэффективно\nдля данного текста', 
                    ha='center', va='center', transform=ax2.transAxes, fontsize=12)
            ax2.set_title('⚠️ Предупреждение', fontsize=12, fontweight='bold')
        
        efficiency = (1 - compressed_size/original_size) * 100
        plt.suptitle(f'Эффективность сжатия Хаффманом: {efficiency:.1f}%', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def visualize_code_length_distribution(self, codes, text):
        """Визуализация распределения длин кодов"""
        freq = Counter(text)
        code_lengths = [len(code) for code in codes.values()]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.hist(code_lengths, bins=range(min(code_lengths), max(code_lengths)+2), 
                alpha=0.7, color='purple', edgecolor='black')
        ax1.set_xlabel('Длина кода (биты)', fontsize=11)
        ax1.set_ylabel('Количество символов', fontsize=11)
        ax1.set_title('📏 Распределение длин кодов', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        counts = np.histogram(code_lengths, bins=range(min(code_lengths), max(code_lengths)+2))[0]
        for i, count in enumerate(counts):
            if count > 0:
                ax1.text(min(code_lengths) + i, count + 0.1, str(count), 
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        sorted_by_length = sorted(codes.items(), key=lambda x: len(x[1]))
        lengths = [len(code) for _, code in sorted_by_length]
        cumulative = np.cumsum([freq[char] for char, _ in sorted_by_length])
        cumulative_percent = cumulative / len(text) * 100
        
        ax2.plot(lengths, cumulative_percent, 'o-', linewidth=2, markersize=8, color='green')
        ax2.set_xlabel('Длина кода (биты)', fontsize=11)
        ax2.set_ylabel('Накопленный процент символов (%)', fontsize=11)
        ax2.set_title('📈 Накопленное распределение символов по длине кода', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 105)
        
        plt.suptitle('Анализ эффективности кодирования Хаффмана', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

print("🚀 Запуск визуализатора сжатия данных...")
print("📦 Проверка зависимостей...")
visualizer = CompressionVisualizerColab()
print("\n✅ Готово! Введите текст и нажмите кнопку для сжатия.")
print("📌 ВСЯ СТАТИСТИКА будет отображаться в текстовом виде выше графиков")