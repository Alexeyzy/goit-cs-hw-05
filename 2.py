import requests
import re
import collections
import multiprocessing
import matplotlib.pyplot as plt
from functools import reduce

def get_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())  
    return collections.Counter(words)

def reduce_function(counter1, counter2):
    return counter1 + counter2

def map_reduce(text, num_processes):
    chunk_size = len(text) // num_processes
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    with multiprocessing.Pool(num_processes) as pool:
        map_results = pool.map(map_function, chunks)

    final_result = reduce(reduce_function, map_results)
    return final_result

def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)

    plt.bar(words, counts)
    plt.title(f"Топ {top_n} найчастіших слів")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    url = input("Введіть URL для завантаження тексту: ")
    # url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    try:
        text = get_text_from_url(url)
        word_counts = map_reduce(text, num_processes=4)
        visualize_top_words(word_counts, top_n=10)
    except Exception as e:
        print(f"Помилка: {e}")
