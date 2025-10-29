from collections import Counter
from datetime import datetime
import requests
from bs4 import BeautifulSoup 
import pytest
import time
import re
'''
    Реализованные методы класса Movies:
        - Вывод информации о всех фильмах (show_all)
        - Сортировка назований фильмов в алфавитном порядке
        - Группировка по жанрам
        - Поиск по названию фильма или id  
        - Гистограмма фильмы каких жанров каждые 5 лет наиболее часто встречаются(снимаются) в дата сете
        - Метод возвращает dict или OrderedDict, где ключи - годы, а значения - количество фильмов. Нужно извлечь годы из названий. Отсортировать по количеству по убыванию.
        - Метод возвращает dict, где ключи - жанры, а значения - количество фильмов. Отсортировать по количеству по убыванию.
        - Метод возвращает dict с top-n фильмами, где ключи - названия фильмов, а значения - количество жанров у фильма. Отсортировать по количеству по убыванию.

'''
class Movies:
    def __init__(self, path_to_the_file):
        self.movies = list()
        with open(path_to_the_file, encoding='utf-8') as file:
            rows = csv.DictReader(file, delimiter=',')
            for i, row in enumerate(rows):
                if i < 1000:  
                    row['movieId'] = int(row['movieId'])
                    self.movies.append(row)

    def show_all(self):
        for elem in self.movies:
            print(f"Фильм {elem['title']} относится к жанру {elem['genres']} и имеет id {elem['movieId']}")

    def sort_by_title(self):
        self.sorted_movies = sorted(self.movies, key = lambda x: x['title'])
        return self.sorted_movies

    def group_by_genres(self):
        genres = dict()
        for movie in self.movies:
            genres_list = movie['genres'].split('|')
            for genre in genres_list:
                if genre not in genres:
                    genres[genre] = []
                genres[genre].append(movie['title'])  
        return genres

    def find_info(self):
        print('Введите movieId или название фильма для поиска информации')
        find_elem = input()
        flag = False 
        try:
            find_elem = int(find_elem)
        except ValueError:
            pass
        for elem in self.movies:
            if elem['movieId'] == find_elem:
                print(f"По Вашему запросу найден фильм {elem['title']} с жанром {elem['genres']} и id {elem['movieId']}")
                flag = True
                break
            elif elem['title'] == find_elem:
                print(f"По Вашему запросу найден фильм {elem['title']} с жанром {elem['genres']} и id {elem['movieId']}")
                flag = True
                break
        if flag == False:
            print('Фильм по Вашему запросу не найден')
    
    def statistics_by_genre(self):
        year_dict = dict()
        for elem in self.movies:
            indx_start = elem['title'].rindex('(')
            if indx_start != -1:
                indx_end = elem['title'].rindex(')')
            if indx_end != -1:
                if indx_end > indx_start:
                    tmp_year = (elem['title'])[indx_start+1:indx_end].strip()
                    try:
                        tmp_year = int(tmp_year)
                        if tmp_year not in year_dict:
                            year_dict[tmp_year] = list()
                        genres = elem['genres'].split('|')
                        year_dict[tmp_year].extend(genres)
                    except ValueError:
                        pass

        min_year = min(year_dict.keys())
        max_year = max(year_dict.keys())
        year_dict = sorted(year_dict.items(), key=lambda x: x[0])
        num_segments = ((int(max_year) - int(min_year)) // 5 ) + 1

        period_dict = {}
        
        for i in range(num_segments):

            period_start = min_year + i * 5
            period_end = period_start + 4
            period_key = f"{period_start}-{period_end}"
            period_dict[period_key] = [] 

            for year, genres in year_dict:
                if period_start <= year <= period_end:
                    period_dict[period_key].extend(genres)

        print("\n" + "="*66)
        print("ГИСТОГРАММА НАБОЛЕЕ ЧАСТОВСТРЕЧАЮЩИХСЯ ЖАНРОВ ПО 5-ЛЕТНИМ ПЕРИОДАМ")
        print("="*66)
        
        for period in period_dict.keys():
            print(f"\nПериод: {period}")
            print("-" * 30)

            genre_count = Counter(period_dict[period])
            
            for genre, count in genre_count.most_common(5): 
                print(f"{genre:<15} {'*' * (count // 3)} ({count})")
    
        return period_dict

    def dist_by_release(self):
        year_dict = dict()

        for elem in self.movies:
            indx_start = elem['title'].rindex('(')
            if indx_start != -1:
                indx_end = elem['title'].rindex(')')
            if indx_end != -1:
                if indx_end > indx_start:
                    tmp_year = (elem['title'])[indx_start+1:indx_end].strip()
                    try:
                        tmp_year = int(tmp_year)
                        if tmp_year not in year_dict:
                            year_dict[tmp_year] = list()
                        year_dict[tmp_year].append(elem['title'])
                    except ValueError:
                        pass

        result_dict = dict()
        for key, value in year_dict.items():
            result_dict[key] = len(value)
        result_dict = dict(sorted(result_dict.items(), key = lambda x: x[1], reverse = True))
        
        return result_dict

    def dist_by_genres(self):
        genres_dict = dict()
        for elem in self.movies:
            genres = elem['genres'].split('|')
            for genre in genres:
                if genre not in genres_dict:
                    genres_dict[genre] = []
                genres_dict[genre].append(elem['title'])
        for key, value in genres_dict.items():
            genres_dict[key] = len(value)
        genres_dict = dict(sorted(genres_dict.items(), key = lambda x: x[1], reverse = True))
        return genres_dict

    def most_genres(self, n):
        count_genres = dict()
        for elem in self.movies:
            genres = elem['genres'].split('|')
            count_genres[elem['title']] = len(genres)
        count_genres = Counter(count_genres)
        result = dict(count_genres.most_common(n))
        return result

'''
    Реализованные методы класса:
       -  Метод возвращает список списков [movieId, поле1, поле2, поле3, ...] для переданного списка фильмов (movieId).
        Например, [movieId, Режиссер, Бюджет, Суммарные мировые сборы, Продолжительность].
        Значения должны быть получены с веб-страниц IMDB соответствующих фильмов.
        Отсортируйте по movieId в порядке убывания.
        - Метод возвращает словарь с top-n режиссерами, где ключи - режиссеры, 
        а значения - количество фильмов, созданных ими. Отсортируйте по количеству фильмов в порядке убывания.
        - Метод возвращает словарь с top-n фильмами, где ключи - названия фильмов,
        а значения - их бюджеты. Отсортируйте по бюджетам в порядке убывания.
        -  Метод возвращает словарь с top-n фильмами, где ключи - названия фильмов,
        а значения - разница между суммарными мировыми сборами и бюджетом.
        Отсортируйте по разнице в порядке убывания.
        - Метод возвращает словарь с top-n фильмами, где ключи - названия фильмов,
        а значения - их продолжительность. Если есть несколько версий - выберите любую.
        Отсортируйте по продолжительности в порядке убывания.
        - Метод возвращает словарь с top-n фильмами, где ключи - названия фильмов,
        а значения - бюджет, деленный на продолжительность. Бюджеты могут быть в разных валютах - не обращайте на это внимания.
        Значения должны быть округлены до 2 десятичных знаков. Отсортируйте по результату деления в порядке убывания.
        - Гистограмма суммарных кассовых сборов по годам выпуска фильмов. Использует названия и годы из класса Movies

'''

class Links:
    def __init__(self, path_to_the_file, movies_instance=None): 
        self.links = list()
        self.movie_id_to_imdb = {}
        self.movies_instance = movies_instance 
        with open(path_to_the_file, 'r', encoding='utf-8') as file:
            file_reader = csv.DictReader(file, delimiter=',')
            for i, row in enumerate(file_reader):
                if i < 1000: 
                    row['movieId'] = int(row['movieId'])
                    self.links.append(row)
                    self.movie_id_to_imdb[row['movieId']] = row['imdbId']

    def _get_imdb_value(self, imdb_id, field):

        url = f"https://www.imdb.com/title/tt{imdb_id}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        request = requests.get(url, headers=headers)

        if request.status_code != 200:
            raise Exception(f"URL {url} не отвечает")

        soup = BeautifulSoup(request.text, 'html.parser')
        field = field.lower()

    def _get_imdb_value(self, imdb_id, field):
        url = f"https://www.imdb.com/title/tt{imdb_id}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        request = requests.get(url, headers=headers)

        if request.status_code != 200:
            raise Exception(f"URL {url} не отвечает")

        soup = BeautifulSoup(request.text, 'html.parser')
        field = field.lower()

        if field in ['director', 'режиссер']:
            credit_block = soup.find('li', {"data-testid": "title-pc-principal-credit"})
            if credit_block:
                directors = [a.text.strip() for a in credit_block.find_all('a')]
                return ", ".join(directors)
            return "N/A"

        elif field in ['budget', 'бюджет']:
            budget_block = soup.find('li', {"data-testid": "title-boxoffice-budget"})
            if budget_block:
                value = budget_block.find('span', class_="ipc-metadata-list-item__list-content-item")
                return value.text.strip() if value else "N/A"
            return "N/A"

        elif field in ['worldwide gross', 'сборы', 'gross']:
            gross_block = soup.find('li', {"data-testid": "title-boxoffice-cumulativeworldwidegross"})
            if gross_block:
                value = gross_block.find('span', class_="ipc-metadata-list-item__list-content-item")
                return value.text.strip() if value else "N/A"
            return "N/A"

        elif field in ['box office', 'кассовые сборы']:
            selectors = [
                'li[data-testid="title-boxoffice-openingweekendgross"]',
                'li[data-testid="title-boxoffice-grossdomestic"]',
                'li[data-testid="title-boxoffice-grossuscanada"]',
            ]
            for selector in selectors:
                block = soup.select_one(selector)
                if block:
                    value = block.find('span', class_="ipc-metadata-list-item__list-content-item")
                    if value:
                        return value.text.strip()
            return "N/A"

        elif field in ['runtime', 'продолжительность']:
            runtime_block = soup.find('li', {"data-testid": "title-techspec_runtime"})
            if runtime_block:
                value = runtime_block.find('div', class_="ipc-metadata-list-item__content-container")
                return value.text.strip() if value else "N/A"
            return "N/A"

        elif field in ['rating', 'рейтинг']:
            rating_span = soup.find('span', {"data-testid": "hero-rating-bar__aggregate-rating__score"})
            if rating_span:
                return rating_span.text.strip()
            return "N/A"

        else:
            return "N/A"

    def get_imdb(self, list_of_movies, list_of_fields):
        result = []
        
        for movie_id in list_of_movies:
            if movie_id not in self.movie_id_to_imdb:
                raise Exception(f"Фильм с movieId {movie_id} не найден")
            
            imdb_id = self.movie_id_to_imdb[movie_id]
            movie_data = [movie_id]
            
            for field in list_of_fields:
                value = self._get_imdb_value(imdb_id, field)
                movie_data.append(value)
            
            result.append(movie_data)
            time.sleep(1)
        result.sort(key=lambda x: x[0], reverse=True)
        return result

    def top_directors(self, n):
        directors_count = {}
        successful = 0
        for i, link in enumerate(self.links):
            if i >= 1000 and successful > 0:
                break
            movie_id = link['movieId']
            imdb_id = link['imdbId']
            try:
                director = self._get_imdb_value(imdb_id, 'Director')
                if director != "N/A":
                    directors_count[director] = directors_count.get(director, 0) + 1
                    successful += 1
                time.sleep(1)
            except Exception:
                print(f"Ошибка при получении режиссера для фильма {movie_id}")
        sorted_directors = sorted(directors_count.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_directors[:n])

    def most_expensive(self, n):
        price = {}
        for i, link in enumerate(self.links):
            if i >= 1000:
                break
            movie_id = link['movieId']
            imdb_id = link['imdbId']
            try:
                budget_str = self._get_imdb_value(imdb_id, 'Budget')
                if budget_str == "N/A":
                    budget_str = self._get_imdb_value(imdb_id, 'Box office')  
                if budget_str == "N/A":
                    budget_str = self._get_imdb_value(imdb_id, 'Gross') 
                
                if budget_str != "N/A":
                    budget_num = 0
                    try:
                        multiplier = 1
                        if 'million' in budget_str.lower():
                            multiplier = 1000000
                        elif 'billion' in budget_str.lower():
                            multiplier = 1000000000

                        clean_str = budget_str.split('(')[0].replace('$', '').replace(',', '').replace(' ', '')
                        clean_str = clean_str.replace('million', '').replace('billion', '').strip()

                        if clean_str and clean_str.replace('.', '').isdigit():
                            budget_num = int(float(clean_str) * multiplier)
                        else:
                            budget_num = 0
                            
                    except (ValueError, AttributeError):
                        print(f"Ошибка парсинга {budget_str}")
                        budget_num = 0

                    if budget_num > 0:
                        movie_title = None
                        for movie in self.movies_instance.movies:
                            if movie['movieId'] == movie_id:
                                movie_title = movie['title']
                                break
                        if movie_title is not None:
                            price[movie_title] = budget_num
                            #print(f"✅ {movie_title}: {budget_str} -> {budget_num}")  
            except Exception:
                print(f"Ошибка для фильма {movie_id}")
        
        sorted_price = sorted(price.items(), key=lambda x: x[1], reverse=True)

        result = {}
        for movie, budget_num in sorted_price[:n]:
            if budget_num >= 1000000000:
                formatted = f"${budget_num/1000000000:.1f}B"
            elif budget_num >= 1000000:
                formatted = f"${budget_num/1000000:.1f}M"
            else:
                formatted = f"${budget_num:,}"
            result[movie] = formatted
        return result

    def most_profitable(self, n):
        profits = {}
        
        for i, link in enumerate(self.links):
            if i >= 1000:
                break
            movie_id = link['movieId']
            imdb_id = link['imdbId']
            try:
                budget_str = self._get_imdb_value(imdb_id, 'Budget')
                gross_str = self._get_imdb_value(imdb_id, 'Worldwide Gross')
                
                if budget_str != "N/A" and gross_str != "N/A":
                    budget_num = 0
                    gross_num = 0
                    try:
                        multiplier_budget = 1
                        if 'million' in budget_str.lower():
                            multiplier_budget = 1000000
                        elif 'billion' in budget_str.lower():
                            multiplier_budget = 1000000000
                        clean_budget = budget_str.split('(')[0].replace('$', '').replace(',', '').replace(' ', '')
                        clean_budget = clean_budget.replace('million', '').replace('billion', '').strip()
                        number_str_budget = ""
                        for char in clean_budget:
                            if char.isdigit() or char == '.':
                                number_str_budget += char
                            elif number_str_budget:
                                break
                        if number_str_budget:
                            budget_num = int(float(number_str_budget) * multiplier_budget)
                    except (ValueError, AttributeError):
                        budget_num = 0
                    try:
                        multiplier_gross = 1
                        if 'million' in gross_str.lower():
                            multiplier_gross = 1000000
                        elif 'billion' in gross_str.lower():
                            multiplier_gross = 1000000000
                        
                        clean_gross = gross_str.split('(')[0].replace('$', '').replace(',', '').replace(' ', '')
                        clean_gross = clean_gross.replace('million', '').replace('billion', '').strip()
                        
                        number_str_gross = ""
                        for char in clean_gross:
                            if char.isdigit() or char == '.':
                                number_str_gross += char
                            elif number_str_gross:
                                break
                        
                        if number_str_gross:
                            gross_num = int(float(number_str_gross) * multiplier_gross)
                    
                    except (ValueError, AttributeError):
                        gross_num = 0
                    
                    if budget_num > 0 and gross_num > 0:
                        profit_num = gross_num - budget_num
                        
                        movie_title = None
                        for movie in self.movies_instance.movies:
                            if movie['movieId'] == movie_id:
                                movie_title = movie['title']
                                break
                        if not movie_title:
                            movie_title = f"Movie_{movie_id}"
                        
                        profits[movie_title] = profit_num      
                time.sleep(1)
            except Exception:
                print(f"Ошибка для фильма {movie_id}")

        sorted_profits = sorted(profits.items(), key=lambda x: x[1], reverse=True)
 
        result = {}
        for movie, profit_num in sorted_profits[:n]:
            if profit_num >= 1000000000:
                formatted = f"${profit_num/1000000000:.1f}B прибыль"
            elif profit_num >= 1000000:
                formatted = f"${profit_num/1000000:.1f}M прибыль"
            else:
                formatted = f"${profit_num:,} прибыль"
            result[movie] = formatted
        
        return result

    def longest(self, n):
        runtimes = {}
        for i, link in enumerate(self.links):
            if i >= 1000:  
                break
            movie_id = link['movieId']
            imdb_id = link['imdbId']
            try:
                runtime = self._get_imdb_value(imdb_id, 'Runtime')
                if runtime and runtime != "N/A":
                    match = re.search(r"\((\d+)\s*min\)", runtime)
                    if not match:
                        continue
                    runtime_value = int(match.group(1))
                    movie_title = next(
                        (m['title'] for m in self.movies_instance.movies if m['movieId'] == movie_id),
                        f"Movie_{movie_id}"
                    )
                    runtimes[movie_title] = runtime_value
            except Exception:
                print(f"Ошибка для фильма {movie_id}")
            time.sleep(1)

        sorted_runtimes = dict(sorted(runtimes.items(), key=lambda x: x[1], reverse=True)[:n])
        return sorted_runtimes

    def top_cost_per_minute(self, n):
        costs = {}
        for i, link in enumerate(self.links):
            if i >= 1000: 
                break
            movie_id = link['movieId']
            imdb_id = link['imdbId']
            try:
                budget = self._get_imdb_value(imdb_id, 'Budget')
                runtime = self._get_imdb_value(imdb_id, 'Runtime')

                if budget and budget != "N/A" and runtime and runtime != "N/A":
                    budget_clean = (
                        budget.replace("$", "")
                            .replace(",", "")
                            .replace("(estimated)", "")
                            .strip()
                    )
                    if not budget_clean.isdigit():
                        continue
                    budget_value = int(budget_clean)

                    match = re.search(r"\((\d+)\s*min\)", runtime)
                    if not match:
                        continue
                    runtime_value = int(match.group(1))

                    if runtime_value == 0:
                        continue

                    movie_title = next(
                        (m['title'] for m in self.movies_instance.movies if m['movieId'] == movie_id),
                        f"Movie_{movie_id}"
                    )

                    cost_per_minute = budget_value / runtime_value
                    costs[movie_title] = round(cost_per_minute, 2) 

                time.sleep(1)
            except Exception:
                print(f"Ошибка для фильма {movie_id}")

        sorted_costs = dict(sorted(costs.items(), key=lambda x: x[1], reverse=True)[:n])
        return sorted_costs

    def box_office_by_year(self):
        year_gross = {}
        for i, link in enumerate(self.links):
            if i >= 1000:
                break
            movie_id = link['movieId']
            imdb_id = link['imdbId']
            movie_title = None
            movie_year = None
            
            for movie in self.movies_instance.movies:
                if movie['movieId'] == movie_id:
                    movie_title = movie['title']
                    if '(' in movie_title and ')' in movie_title:
                        try:
                            year_str = movie_title[movie_title.rfind('(')+1:movie_title.rfind(')')]
                            movie_year = int(year_str)
                        except ValueError:
                            pass
                    break
            
            if movie_year and movie_title:
                gross_str = self._get_imdb_value(imdb_id, 'Worldwide Gross')
                if gross_str != "N/A":
                    digit = gross_str.lower().replace(' ', '')
                    mult = 10**6 if 'million' in digit else 10**9 if 'billion' in digit else 1
                    num = ''.join(c for c in digit.replace('million','').replace('billion','') if c.isdigit() or c == '.')
                    numeric_gross = int(float(num) * mult) if num else 0
                    if numeric_gross > 0:
                        if movie_year not in year_gross:
                            year_gross[movie_year] = {
                                'total_gross': 0,
                                'movie_count': 0,
                                'movies': []  
                            }
                        year_gross[movie_year]['total_gross'] += numeric_gross
                        year_gross[movie_year]['movie_count'] += 1
                        year_gross[movie_year]['movies'].append({
                            'title': movie_title,
                            'gross': numeric_gross
                        })

        sorted_years = dict(sorted(year_gross.items()))

        print("\n" + "="*70)
        print("ГИСТОГРАММА КАССОВЫХ СБОРОВ ПО ГОДАМ ВЫПУСКА")
        print("="*70)
        
        if not sorted_years:
            print("Нет данных о кассовых сборах")
            return sorted_years

        max_gross = max(stats['total_gross'] for stats in sorted_years.values())
        max_movies = max(stats['movie_count'] for stats in sorted_years.values())
        
        print(f"\n{'Год':<6} {'Сборы':<15} {'Гистограмма':<40} {'Фильмы'}")
        print("-" * 70)
        
        for year, stats in sorted_years.items():
            total_gross = stats['total_gross']
            movie_count = stats['movie_count']

            gross_bar_length = int((total_gross / max_gross) * 40) if max_gross > 0 else 0
            movies_bar_length = int((movie_count / max_movies) * 20) if max_movies > 0 else 0
    
            gross_formatted = f"${total_gross:,.0f}" if total_gross >= 1000000 else f"${total_gross:,.0f}"
            print(f"{year:<6} {gross_formatted:<15} {'▇' * gross_bar_length} ({movie_count} фильмов)")

            if stats['movies']:
                top_movie = max(stats['movies'], key=lambda x: x['gross'])
                print(f"Лучший: {top_movie['title']} - ${top_movie['gross']:,.0f}")
        
        return sorted_years

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file, path_to_movies_file):
        """
        Put here any fields that you think you will need.
        """
        self.file = []
        try:
            with open(path_to_the_file, 'r') as f:
                        for en,i in enumerate(f.readlines()):
                            if en == 0:
                                continue
                            self.file.append(i.rstrip('\n').split(','))
                            if en == 1000:
                                break
            self.movies_names = {}
        except FileNotFoundError:
            print(f'файл [{path_to_the_file}] не найден')
        try:
            with open(path_to_movies_file) as f:
                movies_file = csv.reader(f)
                for i in movies_file:
                    self.movies_names[i[0]] =i[1]
        except FileNotFoundError:
            print(f'файл [{path_to_movies_file}] не найден')

    class Movies:    
        def __init__(self, file, movies_names):
            self.file = file
            self.movies_names = movies_names

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            dict_year = Counter(datetime.fromtimestamp(int(i[-1])).year for i in self.file)
            ratings_by_year = dict(sorted(dict_year.items(), key=lambda i: i[0]))
            return ratings_by_year
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
         Sort it by ratings ascendingly.
            """
            dict_year = Counter(float(i[2]) for i in self.file)
            ratings_distribution = dict(sorted(dict_year.items(), key=lambda i: i[0]))
            return ratings_distribution

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            dict_movies = Counter(i[1] for i in self.file) 
            movie_rat_counts = {self.movies_names[id]: count for id, count in dict_movies.items()} 
            top_movies = dict(sorted(movie_rat_counts.items(), key=lambda i: i[1], reverse=True)[:n])

            return top_movies 

        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            movies_rat = {}
            for i in self.file:
                movies_rat.setdefault(i[1], []).append(float(i[2])) 
            movie_named_rat = {self.movies_names[id]: count for id, count in movies_rat.items()} 

            top_movies = {}
            for key, val_list in movie_named_rat.items():
                if metric == 'average':
                    rat = round(sum(val_list)/len(val_list), 2)
                elif metric == 'median':
                    sorted_ratings = sorted(val_list)
                    l = len(val_list)
                    if l % 2 == 0:
                        rat = round((sorted_ratings[l // 2 - 1] + sorted_ratings[l // 2]) / 2, 2)
                    else:
                        rat = round(sorted_ratings[l // 2], 2)
                else:
                    raise Exception('не та метрика')
                top_movies[key] = rat

            top_movies = dict(sorted(top_movies.items(), key=lambda i: i[1], reverse=True)[:n])
            return top_movies
        
        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            movies_rat = {}
            for i in self.file:
                movies_rat.setdefault(i[1], []).append(float(i[2])) 
            movie_named_rat = {self.movies_names[id]: count for id, count in movies_rat.items()}

            movie_var = {}
            for key, val_list in movie_named_rat.items():
                l = len(val_list)
                mean_v = sum(val_list) / l
                if l>1:
                    variance = sum((i - mean_v) ** 2 for i in val_list) / (l-1)
                    variance = round(variance, 2)
                    movie_var[key] = variance
                else:
                    movie_var[key] = 0

            top_movies = dict(sorted(movie_var.items(), key=lambda i: i[1], reverse=True)[:n])

            return top_movies

        def dist_by_month(self):
            """
            для бонусной части
            """
            dict_month = Counter(datetime.fromtimestamp(int(i[-1])).month for i in self.file)
            ratings_by_year = dict(sorted(dict_month.items(), key=lambda i: i[0]))
            return ratings_by_year
        
        def top_by_month(self, metric='average'):
            """
            еще для бонусной части
            """
            month_dist = {}
            for i in self.file:
                month_dist.setdefault(datetime.fromtimestamp(int(i[-1])).month, []).append(float(i[2])) 
            # month_dist = {self.movies_names[id]: count for month, count in mnonth_dist.items()} 

            top_months = {}
            for key, val_list in month_dist.items():
                l = len(val_list)
                if metric == 'average':
                    rat = round(sum(val_list)/l, 2)
                elif metric == 'median':
                    sorted_ratings = sorted(val_list)
                    if l % 2 == 0:
                        rat = round((sorted_ratings[l // 2 - 1] + sorted_ratings[l // 2]) / 2, 2)
                    else:
                        rat = round(sorted_ratings[l // 2], 2)
                else:
                    raise Exception('не та метрика')
                top_months[key] = rat

            top_months = dict(sorted(top_months.items(), key=lambda i: i[0]))
            return top_months

    class Users(Movies):
        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
     Inherit from the class Movies. Several methods are similar to the methods from it.
        """
        def users_by_num_rat(self):
            users_counts = Counter(i[0] for i in self.file)
            return dict(sorted(users_counts.items(), key=lambda i: i[1], reverse=True))

        def users_by_rat(self, metric='average'):
            users_rat = {}
            for i in self.file:
                users_rat.setdefault(i[0], []).append(float(i[2])) 

            top_users = {}
            for key, val_list in users_rat.items():
                l = len(val_list)
                if metric == 'average':
                    rat = round(sum(val_list)/l, 2)
                elif metric == 'median':
                    sorted_ratings = sorted(val_list)
                    if l % 2 == 0:
                        rat = round((sorted_ratings[l // 2 - 1] + sorted_ratings[l // 2]) / 2, 2)
                    else:
                        rat = round(sorted_ratings[l // 2], 2)
                else:
                    raise Exception('не та метрика')
                top_users[key] = rat

            top_users = dict(sorted(top_users.items(), key=lambda i: i[1], reverse=True))
            return top_users

        def users_var(self, n):
            users_rat = {}
            for i in self.file:
                users_rat.setdefault(i[0], []).append(float(i[2])) 

            top_users = {}
            for key, val_list in users_rat.items():
                l = len(val_list)
                mean_v = sum(val_list) / l
                if l>1:
                    variance = sum((i - mean_v) ** 2 for i in val_list) / (l-1)
                    variance = round(variance, 2)
                    top_users[key] = variance
                else:
                    top_users[key] = 0

            top_users = dict(sorted(top_users.items(), key=lambda i: i[1], reverse=True)[:n])

            return top_users


class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.file = []
        try:
            with open(path_to_the_file, 'r') as f:
                        for en,i in enumerate(f.readlines()):
                            if en == 0:
                                continue
                            self.file.append(i.rstrip('\n').split(','))
                            if en == 1000:
                                break
        except FileNotFoundError:
            print(f'файл [{path_to_the_file}] не найден')


    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        tag_set = set([i[2] for i in self.file])
        tags_lens = {i: len(i.split()) for i in tag_set} 
        big_tags = dict(sorted(tags_lens.items(), key=lambda i: i[1], reverse=True)[:n])
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        tag_set = set([i[2] for i in self.file])
        tags_lens = {i: len(i) for i in tag_set}
        big_tags = [i[0] for i in(sorted(tags_lens.items(), key=lambda i: i[1], reverse=True)[:n])]
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        count_words = set(self.most_words(n))
        count_symb = set(self.longest(n))
        big_tags = count_words & count_symb
        big_tags = list(big_tags)
        return big_tags
        
    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        tag_count = Counter(i[2] for i in self.file)
        popular_tags = dict(sorted(tag_count.items(), key=lambda i: i[1], reverse=True)[:n])
        return popular_tags
        
    def tags_with(self, word:str):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        tag_set = set([i[2] for i in self.file])
        tags_with_word = []
        for i in tag_set:
            if word.lower() in i.lower():
                tags_with_word.append(i)

        tags_with_word = sorted(tags_with_word)
        return tags_with_word
    
    def tag_by_year(self):
            """
            для бонусной части
            """
            tag_year = Counter(datetime.fromtimestamp(int(i[-1])).year for i in self.file)
            tag_by_year = dict(sorted(tag_year.items(), key=lambda i: i[0]))
            return tag_by_year

class TestMovielens:

    @pytest.fixture
    def ratings_file(self):
        return Ratings('../datasets/ratings.csv', '../datasets/movies.csv')

    @pytest.fixture
    def tags_file(self):
        return Tags("../datasets/tags.csv")

    @pytest.fixture
    def movies_file(self):
        return Movies("../datasets/movies.csv")

    @pytest.fixture
    def links_file(self, movies_file):
        return Links("../datasets/links.csv", movies_instance=movies_file)


    def test_dist_by_year(self, ratings_file):
        m = ratings_file.Movies(ratings_file.file, ratings_file.movies_names)
        out = m.dist_by_year()
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, int)
            assert isinstance(value, int)
        assert list(out.keys()) == sorted(out.keys())

    def test_dist_by_rating(self, ratings_file):
        m = ratings_file.Movies(ratings_file.file, ratings_file.movies_names)
        out = m.dist_by_rating()
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, float)
            assert isinstance(value, int)
        assert list(out.keys()) == sorted(out.keys(), key=lambda i: i)

    def test_top_by_num_of_ratings(self, ratings_file):
        m = ratings_file.Movies(ratings_file.file, ratings_file.movies_names)
        out = m.top_by_num_of_ratings(2)
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, int)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_top_by_ratings_average(self, ratings_file):
        m = ratings_file.Movies(ratings_file.file, ratings_file.movies_names)
        out = m.top_by_ratings(2, metric='average')
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, float)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_top_controversial(self, ratings_file):
        m = ratings_file.Movies(ratings_file.file, ratings_file.movies_names)
        out = m.top_controversial(2)
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, float)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_users_by_num_rat(self, ratings_file):
        u = ratings_file.Users(ratings_file.file, ratings_file.movies_names)
        out = u.users_by_num_rat()
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, int)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_users_by_rat(self, ratings_file):
        u = ratings_file.Users(ratings_file.file, ratings_file.movies_names)
        out = u.users_by_rat(metric='average')
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, float)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_users_var(self, ratings_file):
        u = ratings_file.Users(ratings_file.file, ratings_file.movies_names)
        out = u.users_var(2)
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, float)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_dist_by_month(self, ratings_file):
        m = ratings_file.Movies(ratings_file.file, ratings_file.movies_names)
        out = m.dist_by_month()
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, int)
            assert isinstance(value, int)
        assert list(out.keys()) == sorted(out.keys())

    def test_top_by_month(self, ratings_file):
        m = ratings_file.Movies(ratings_file.file, ratings_file.movies_names)
        out = m.top_by_month(metric='average')
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, int)
            assert isinstance(value, float)
        assert list(out.keys()) == sorted(out.keys())


    def test_most_words(self, tags_file):
        out = tags_file.most_words(5)
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, int)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_longest(self, tags_file):
        out = tags_file.longest(5)
        assert isinstance(out, list)
        for i in out:
            assert isinstance(i, str)
        check_sort = [len(tag) for tag in out]
        assert check_sort == sorted(check_sort, reverse=True)

    def test_most_words_and_longest(self, tags_file):
        out = tags_file.most_words_and_longest(2)
        assert isinstance(out, list)
        for i in out:
            assert isinstance(i, str)

    def test_most_popular(self, tags_file):
        out = tags_file.most_popular(5)
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, int)
        check_sort = list(out.values())
        assert check_sort == sorted(check_sort, reverse=True)

    def test_tags_with(self, tags_file):
        out = tags_file.tags_with("funny")
        assert isinstance(out, list)
        for i in out:
            assert isinstance(i, str)
        assert out == sorted(out)

    def test_tag_by_year(self, tags_file):
        out = tags_file.tag_by_year()
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, int)
            assert isinstance(value, int)
        assert list(out.keys()) == sorted(out.keys())


    def test_movies_dist_by_year(self, movies_file):
        out = movies_file.dist_by_release()
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, int)
            assert isinstance(value, int)

    def test_movies_dist_by_genres(self, movies_file):
        out = movies_file.dist_by_genres()
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

    def test_most_genres(self, movies_file):
        out = movies_file.most_genres(5)
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, str)
            assert isinstance(value, int)


    def test_links_list(self, links_file):
        out = links_file.links
        assert isinstance(out, list)
        for link in out:
            assert "movieId" in link
            assert "imdbId" in link
            assert "tmdbId" in link

    def test_links_mapping(self, links_file):
        out = links_file.movie_id_to_imdb
        assert isinstance(out, dict)
        for key, value in out.items():
            assert isinstance(key, int)
            assert isinstance(value, str)

if __name__ == '__main__':
    pass