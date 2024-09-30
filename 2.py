import requests
import re
import collections
import threading
import asyncio
import concurrent.futures
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

async def map_reduce_async(text, num_threads):
    chunk_size = len(text) // num_threads
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        loop = asyncio.get_running_loop()
        map_results = await asyncio.gather(
            *[loop.run_in_executor(executor, map_function, chunk) for chunk in chunks]
        )
    
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

async def main():
    url = input("Введіть URL для завантаження тексту: ")
    try:
        text = get_text_from_url(url)
        word_counts = await map_reduce_async(text, num_threads=4)
        visualize_top_words(word_counts, top_n=10)
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    asyncio.run(main())