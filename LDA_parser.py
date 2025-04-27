import nltk
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
import re

from url_to_text_parser import parser

# Загрузка стоп-слов
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))


def extract_unique_topics_from_url(url, num_topics=5, num_words=5):
    """Извлекает уникальные темы из web-страницы по заданному URL-адресу.

    :param url: URL-адрес web-страницы
    :param num_topics: Количество тем, которые необходимо извлечь
    :param num_words: Количество слов, которые необходимо вывести для каждой темы
    :return: Список уникальных тем, где каждая тема — это список слов
    """
    # Получение уникальных тем
    topics = extract_topics_from_url(url, num_topics, num_words)
    unique_topics = []
    for topic in topics:
        if topic not in unique_topics:
            unique_topics.append(topic)
    return unique_topics


def extract_topics_from_url(url, num_topics=5, num_words=5):
    """
    Функция для извлечения тем из текста, полученного из web-страницы.

    :param url: URL-адрес web-страницы
    :param num_topics: Количество тем, которые необходимо извлечь
    :param num_words: Количество слов, которые необходимо вывести для каждой темы
    :return: Список тем, каждая тема - список слов
    """
    # Получение тем
    status, path = parser(url, 'temp.txt')
    if status == 'done':
        return _extract_topics_from_file(path, num_topics, num_words)
    else:
        raise Exception(path)


def _preprocess_text(text):
    # Удаление специальных символов и приведение к нижнему регистру
    text = re.sub(r'\W+', ' ', text.lower())
    # Удаление стоп-слов
    tokens = ' '.join([word for word in text.split() if word not in stop_words])
    return tokens


def _extract_topics_from_file(filename, num_topics=5, num_words=5):
    # Чтение текста из файла
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    # Предобработка текста
    processed_text = _preprocess_text(text)

    # Векторизация текста
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([processed_text])

    # Обучение модели LDA
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_model.fit(X)

    # Получение тем
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_features_ind = topic.argsort()[-num_words:][::-1]
        top_features = [vectorizer.get_feature_names_out()[i] for i in top_features_ind]
        topics.append(top_features)

    return topics


# Пример использования
if __name__ == "__main__":
    url = 'https://ru.wikipedia.org/wiki/Python'
    topics = extract_unique_topics_from_url(url, num_topics=5, num_words=5)

    for i, topic in enumerate(topics):
        print(f"Тема {i + 1}: {', '.join(topic)}")
