import aiohttp

from config import KINOPOISK_API_TOKEN

MOVIE_API_URL = "https://api.kinopoisk.dev/v1.4/"


async def get_movie_by_query(query):
    async with (aiohttp.ClientSession() as session):
        params = {
            "query": query,
        }
        async with session.get(MOVIE_API_URL + "movie/search",
                   params=params,
                   headers={"X-API-KEY": KINOPOISK_API_TOKEN}
                               ) as search_response:
            if search_response.status == 200:
                search_data = await search_response.json()
                if search_data["docs"]:
                    movie = search_data["docs"][0]

                    title = movie["name"]
                    rating = movie.get("rating").get("kp", "Нет рейтинга")
                    poster = movie.get('poster').get('previewUrl')
                    overview = movie.get("shortDescription"
                                         ) or movie.get("description",
                                                        "Нет обзора")
                    return title, rating, poster, overview
                else:
                    return "Такого фильма не найдено."
            else:
                return "Ошибка."
