import requests
from bs4 import BeautifulSoup


def get_first_google_link(query):
    base_url = "https://www.google.com/search"
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {
        "q": query,
        "hl": "ru"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        search_results = soup.find_all('div', class_='g')

        for result in search_results:
            link = result.find('a')
            if link and link.get('href'):
                href = link.get('href')
                if (href.startswith('http')
                        and not href.startswith('https://www.google.com')):
                    return href

        return None

    except requests.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return None
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")
        return None
