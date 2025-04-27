import spacy
import numpy as np
import faiss

class vector_manager:
    def __init__(self, model="ru_core_news_lg"):
        # Загружаем модель spaCy
        self.nlp = spacy.load(model)
        self.word_list = []
        self.vector_db = None

    def _get_word_vector(self, word):
        """Получение векторного представления слова"""
        doc = self.nlp(word)
        return doc.vector

    def create_vector_database(self, words):
        """Создание векторной базы данных из списка слов"""
        self.word_list = words
        vectors = np.array([self._get_word_vector(word) for word in words], dtype=np.float32)
        self.vector_db = vectors
        return self.vector_db

    def find_similar_words(self, query_word, k=5):
        """Поиск ближайших слов, схожих с запросом"""
        if self.vector_db is None:
            raise ValueError("Vector database is empty. Please create it first.")

        query_vector = self._get_word_vector(query_word).reshape(1, -1).astype(np.float32)  # Преобразуем в тип float32

        # Создаем FAISS индекс для поиска по L2 расстоянию
        index = faiss.IndexFlatL2(self.vector_db.shape[1])  # Индекс для L2 расстояния
        index.add(self.vector_db)  # Добавляем векторную базу данных
        
        # Поиск ближайших соседей
        distances, indices = index.search(query_vector, k)  # Найти k ближайших слов
        similar_words = [self.word_list[i] for i in indices[0]]
        return similar_words, distances[0]

    def compare_with_distance_threshold(self, words, threshold=20, vector_db = None):
        """
        Сравнивает массив слов с векторной базой данных.
        Возвращает 1, если хотя бы одно слово имеет дистанцию меньше порога, иначе 0.
        
        :param words: список слов для сравнения.
        :param threshold: пороговое значение для дистанции.
        :return: 1 или 0
        """
        if vector_db is not None:
            self.vector_db = vector_db
        index = faiss.IndexFlatL2(self.vector_db.shape[1])  # Индекс для L2 расстояния
        index.add(self.vector_db)  # Добавляем векторную базу данных
        for word in words:
            query_vector = self._get_word_vector(word).reshape(1, -1).astype(np.float32)
            
            # Поиск ближайших соседей
            distances, indices = index.search(query_vector, k=1)  # Найти ближайшее слово
            print(distances[0][0], word, self.word_list[indices[0][0]]   )
            if distances[0][0] < threshold:
                return 1  # Если расстояние меньше порога
        return 0  # Если ни одно слово не имеет расстояние ниже порога

if __name__ == "__main__":
    # Пример использования класса

    words = "Искусственный интеллект, экология, Глобализация, Космос, Блокчейн, Робототехника, Психология, Экономика, Образование, Биотехнологии, Миграция, Генетика, Музыка, Лидерство, Протезирование, Культура, Маркетинг, Климат, Электромобили, Интернет".split(',')
    vector_db = vector_manager() 
    vector_db.create_vector_database(words)
    # Поиск схожих слов
    query_word = "экологии"
    similar_words, distances = vector_db.find_similar_words(query_word)

    print(f"Слова, похожие на '{query_word}':")
    for word, distance in zip(similar_words, distances):
        print(f"{word} (расстояние: {distance})")

    # # Пример использования новой функции
    # query_words = [  "кокс", "динозавры"]   
    # threshold = 20
    # result = vector_db.compare_with_distance_threshold(query_words, threshold)

    # print(f"Результат сравнения с порогом {threshold}: {result}")
#[['экологии', 'году', 'организмов', 'экология', 'сообществ'], ['средой', 'наука', 'подход', 'изучения', 'условиях']]