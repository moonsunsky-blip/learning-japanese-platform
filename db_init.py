import os
import sqlite3 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "data", "japanese.db")

HIRAGANA_TXT = os.path.join(BASE_DIR, "data", "hiragana.txt")

KATAKANA_TXT = os.path.join(BASE_DIR, "data", "katakana.txt")
N5_WORDS = os.path.join(BASE_DIR, "data", "N5_words.txt")

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""

            CREATE TABLE IF NOT EXISTS alphabet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character TEXT NOT NULL,
            romaji TEXT NOT NULL,
            russian TEXT NOT NULL,
            type TEXT NOT NULL           
        )
    
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            words TEXT NOT NULL,
            romaji TEXT NOT NULL,
            russian TEXT NOT NULL,
            type TEXT NOT NULL            
        )
    """)

    conn.commit()
    conn.close()

def load_letters_from_file(file_path, alphabet_type):
    letters_list = []

    with open(file_path, "r", encoding = "utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split("|")
            if len(parts) == 3:
                letters_list.append((parts[0], parts[1], parts[2], alphabet_type))
                
    return letters_list





def main_init():
    create_tables()
    print("таблицы созданы")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT (*) FROM alphabet WHERE type = 'hiragana'")
    if cursor.fetchone()[0] == 0:

        if os.path.exists(HIRAGANA_TXT):
            hiragana_data = load_letters_from_file(HIRAGANA_TXT, "hiragana")

            cursor.executemany("""
                    INSERT INTO alphabet (character, romaji, russian, type)
                    VALUES (?, ?, ?, ?) 
                """, hiragana_data)
            print(f"успешно загружено {len(hiragana_data)} букв хираганы")
        else:
            print(f"Ошибка: файл не найден по пути {HIRAGANA_TXT} ")
    else:
        print("база данных уже содержит данные ... пропускаем =.=")
    
    

    cursor.execute("SELECT COUNT (*) FROM alphabet WHERE type = 'katakana'")
    if cursor.fetchone()[0] == 0:

        if os.path.exists(KATAKANA_TXT):
            katakana_data = load_letters_from_file(KATAKANA_TXT, "katakana")

            cursor.executemany("""
                    INSERT INTO alphabet (character, romaji, russian, type)
                    VALUES (?, ?, ?, ?)
                """, katakana_data)
            print(f"успешно загружено {len(katakana_data)} букв катаканы")
        else:
            print(f"Ошибка: файл не найден по пути {KATAKANA_TXT}")
    else:
        print("база данных уже содержит данные ... пропускаем =.=")


    cursor.execute("SELECT COUNT (*) FROM vocabulary WHERE type = 'N5_words'")
    if cursor.fetchone()[0] == 0:

        if os.path.exists(N5_WORDS):
            n5_words_data = load_letters_from_file(N5_WORDS, "N5_words")

            cursor.executemany("""
                INSERT INTO vocabulary(words, romaji, russian, type) 
                VALUES (?, ?, ?, ?)
                   """, n5_words_data)
            
            print(f"успешно загружено {len(n5_words_data)} слов словарного запаса")
        else:
            print(f"ошибка: файл не найден по пути {N5_WORDS}")
    else:
        print("база данных уже содержит данные ... пропускаем =.=")
        
    
    
    
    
    conn.commit()
    conn.close()




if __name__ == "__main__":
    main_init()
   