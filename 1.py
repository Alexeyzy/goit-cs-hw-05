import argparse
import asyncio
import os
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(file_path, output_folder):
    try:
        ext = file_path.suffix[1:] 
        target_folder = output_folder / ext

        target_folder.mkdir(parents=True, exist_ok=True)

        shutil.copy(file_path, target_folder / file_path.name)
        logging.info(f"Файл {file_path.name} скопійовано до {target_folder}")
    except Exception as e:
        logging.error(f"Помилка під час копіювання файлу {file_path}: {e}")

async def read_folder(source_folder, output_folder):
    tasks = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_folder))
    
    await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source_folder", type=str, help="Вихідна папка з файлами")
    parser.add_argument("output_folder", type=str, help="Папка для збереження файлів")

    args = parser.parse_args()
    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Папка {source_folder} не існує або не є папкою.")
        return

    asyncio.run(read_folder(source_folder, output_folder))
    logging.info("Сортування файлів завершено.")

if __name__ == "__main__":
    main()
"""python 1.py D:\WWW\GoIT\CompSystems\VsCode\goit-cs-hw-05\goit-cs-hw-05\111 
D:\WWW\GoIT\CompSystems\VsCode\goit-cs-hw-05\goit-cs-hw-05\222"""