import requests
import bs4
from fake_headers import Headers

KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def contains_keywords(text, keywords):
    """Функция для проверки наличия ключевых слов в тексте"""
    return any(keyword.lower() in text.lower() for keyword in keywords)


url = 'https://habr.com/ru/articles/'
headers = Headers(browser='chrome', os='win', headers=True).generate()
response = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(response.text, features='lxml')

# Находим все статьи на странице
articles = soup.find_all('article', class_='tm-articles-list__item')

parsed_data = []
for article in articles:
    link = 'https://habr.com' + article.find('a', class_='tm-title__link').get('href')
    title = article.find('a', class_='tm-title__link').text
    date = article.find('a', class_='tm-article-datetime-published').find('time').get('title')

    # Получаем текст статьи
    article_response = requests.get(link, headers=headers)
    article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')
    article_content = article_soup.find('div', class_='tm-article-body').get_text(strip=True)

    # Проверяем наличие ключевых слов
    if contains_keywords(article_content, KEYWORDS):
        parsed_data.append(f"{date} – {title} – {link}")

print(*parsed_data, sep='\n')
