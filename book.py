from randomB import random_pages, random_price, markup, novice_markup, random_norm, random_choice, random_count
from settings import start_year  # 2019
from settings import start_newness  # 60
from settings import low_book_count_threshold  # 60
from bookStore import BookStore
from math import trunc
from collections import namedtuple


class Edition(object):
    """Основной класс издания: часть дуальной природы публикации, отвечающая
    её.

    физическому воплощению.
    """
    __slots__ = 'sold', 'book', 'publisher', 'year', 'pages_used', 'price', 'retail_markup', 'demand', 'newness', 'count', 'is_frozen'

    def __init__(self, book, **kwargs):
        """Инициализация по списку параметров, определение неустановленных.

        параметров.
        """
        self.book = book
        for key, value in kwargs.items():
            attr = key.lower()
            set_value = value
            if value.isdigit():
                set_value = int(value)
            if (attr == 'topics') or (attr == 'categories'):
                set_value = value.split()
            if attr in self.__slots__:
                setattr(self, attr, set_value)
        self.pages_used = random_pages()
        self.price = random_price(self)
        self.retail_markup = markup(self.price)
        self.demand = 0
        self.sold = 0
        self.newness = 0
        self.count = random_count(self.price)
        self.is_frozen = 0
        BookStore.log(f'created book {str(self)} ')

    def new(self):
        """Новинка имеет маркер новизны, и повышенную стоимость."""
        self.year = start_year
        self.newness = start_newness
        self.retail_markup = novice_markup(self.price)

    def set_count(self, summ):
        """Постановка количества изданий в начале времени."""
        self.count = trunc(summ/self.price)
        if self.count == 0:
            self.count = -1

    def booking(self):
        """Заказ издания."""
        if self.count > 0:
            self.count -= 1
            self.demand += 1
            self.sold += 1
            self.book.income += self.retail_markup
            BookStore.log(f'bought book {str(self)} for {self.retail_markup}')
            return self.retail_markup
        else:
            self.demand += 1
            BookStore.bid_book(self)
            BookStore.log(f"can't buy book {str(self)} ")
            return 0

    def freeze(self):
        """Заморозка издания: заявка в издательство уже отправлена, надо.

        подождать её прибытия, но не докучать новыми письмами.
        """
        self.is_frozen = self.sold
        self.sold = 0
        return self

    def __str__(self):
        return f'{self.book.sec_title()} {self.publisher}, {str(self.year)}г.'

    def arrive(self, count):
        """Прибытие новой партии книг данного издания."""
        self.count += count
        self.is_frozen = 0
        summ = count*self.price
        BookStore.log(f'arrived book {str(self)} {count}. It has value {summ} with {self.retail_markup}.')
        return summ


class Book(object):
    """
    Основной класс книги - здесь содержится информация об авторе, названии и тематике, всё то, что независит от издательства
    """
    __slots__ = 'author', 'title', 'first_published', 'topics', 'category', 'editions', 'income'

    def __init__(self, **kwargs):
        """Инициализация по списку параметров, определение списка изданий и.

        прочих параметров.
        """
        self.editions = []
        self.author = 'nobody'
        self.title = 'nothing'
        self.first_published = 2019
        self.income = 0
        for key, value in kwargs.items():
            attr = key.lower()
            if (attr == 'year'):
                temp = int(value)
                if temp < self.first_published:
                    self.first_published = temp
            elif (attr == 'topics') or (attr == 'category'):
                set_value = value.split()
            else:
                set_value = value
            if attr in self.__slots__:
                setattr(self, attr, set_value)
        self.editions = [Edition(self, **kwargs)]
        BookStore.log(f'created book {str(self)} ')

    def is_low_count(self):
        """Предикат."""
        from settings import low_book_count_threshold
        return (self.count() < low_book_count_threshold)

    def count(self):
        """Число экземпляров по всем изданиям книги-"""
        if self.editions:
            summ = sum([exemplar.count for exemplar in self.editions])
            return summ
        else:
            return 0

    def __str__(self):
        if self.editions:
            return self.author + ': ' + self.title + ' в количестве ' + str(self.count()) + ' экз.'
        else:
            return self.sec_title()

    def sec_title(self):
        """Сокращённое название."""
        return self.author + ': ' + self.title

    def __eq__(self, other):
        """Сравнение книг: книга есть сущность, у которой есть автор и.

        заглавие.
        """
        return self.author == other.author and self.title == other.title

    def get_edition(self):
        """Получение какого-то издания книги."""
        temp = random_choice(self.editions)
        if temp.count > 0:
            return temp
        else:
            for ed in self.editions:
                if ed.count > 0:
                    return ed
            return None

    def statistic(self):
        """Получение статистики по книге."""
        temp = sum([exemplar.demand for exemplar in self.editions])
        f = namedtuple('Stat', ['income', 'summ', 'book', 'to_string', 'price'])(
            book=self,
            summ=temp,
            income=self.income,
            price=self.income/temp,
            to_string=lambda i: winning(f, i)
        )
        return f


def winning(f, i):
    if i == 0:
        return f'Книга {f.book.sec_title()} стоимостью {int(f.price)}\nпринесла наибольшую выручку в размере {int(f.income)},\n и была продана в количестве {f.summ} шт.'
    elif i == 1:
        return f'На втором месте по выручке находится {f.book.sec_title()}\n с общим числом продаж {f.summ} шт. и общей суммой сделок {int(f.income)}\n(стоимость единицы хранения {int(f.price)}).'
    else:
        return f'{f.book.sec_title()},\nЦена продажи {int(f.price)}.\tПродано {f.summ} экз.\tОбщая выручка {int(f.income)}.'
