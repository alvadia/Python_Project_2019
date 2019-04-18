import logging
from randomB import random_seed, random_choice, get_wish, random_time, markup, random_norm
from settings import range_order, sigma_order  # 100, 3
from settings import start_cash  # 0
from settings import low_book_count_threshold  # 15
from math import trunc, sqrt
from collections import defaultdict


class BookStore(object):
    """Главный класс магазина, основные параметры и индексы."""
    book_index = []
    buyer_index = []
    publisher_index = {}
    author_index = {}
    buyers = []
    query = {}
    bid_book_list = []
    textlog = ''
    log_file = './log_file.txt'
    orderlog = []
    params = {'cash': 0, 'day': 0, 'withdraw': 0, 'income': 0}
    logger = logging.getLogger('BookStore')

    def assortiment(self, kwargs):
        pass

    def __init__(self, csv_path='./'):
        self.__dir__ = BookStore.__dir__
        BookStore.book_index = []
        BookStore.buyer_index = []
        BookStore.publisher_index = {}
        BookStore.author_index = {}
        BookStore.buyers = []
        BookStore.query = {}
        BookStore.bid_book_list = []
        BookStore.textlog = ''
        BookStore.log_file = './log_file.txt'
        BookStore.orderlog = []
        BookStore.params = {'cash': 0, 'day': 0, 'income': 0}
        BookStore.buyer_index = []
        BookStore.textlog = ''
        BookStore.orderlog = []
        BookStore.current_day = 0
        BookStore.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('BookStore.log')
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('\
            %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        BookStore.logger.addHandler(file_handler)
        BookStore.logger.addHandler(stream_handler)
        BookStore.params['cash'] = start_cash
        BookStore.query = defaultdict(lambda: [])
        random_seed()
        from csv import DictReader as csv_reader
        with open(csv_path+'books.csv', 'r') as file_obj:
            reader = csv_reader(file_obj, delimiter=',')
            from book import Book
            for line in reader:
                book = Book(**line)
                temp = BookStore.register_book(book)
        BookStore.book_index, BookStore.publisher_index, self.author_index = temp
        with open(csv_path+'buyers.csv', 'r') as file_obj:
            reader = csv_reader(file_obj, delimiter=',')
            from customer import Customer
            for line in reader:
                buyer = Customer(**line)
                temp = BookStore.register_buyer(buyer)
        BookStore.buyer_index = temp

    def tick(self):
        """Один шаг моделирования."""
        BookStore.textlog = ''
        BookStore.orderlog = []
        BookStore.current_day += 1
        BookStore.log(f"Current cash is {self.params['cash']} ")
        from wishOrder import Order
        for order in [
                Order(random_choice(BookStore.buyer_index), get_wish(self))
                for i in range(random_norm(range_order, sqrt(sigma_order)))
        ]:
            self.top_up(order.booking())
        BookStore.query = self.make_request()
        self.recalculate(BookStore.query)
        return BookStore.textlog

    def get_bids(self):
        """
        Получение списка заявок в издательство в человеческом виде - отсортированный по времени список заявок.
        Заявки одного издательства с разными номерами не сливаются!
        """
        result = []
        for key, value in BookStore.query.items():
            delta = key - BookStore.current_day
            if delta > 0:
                if delta == 1:
                    temp = f'Заявки, которые придут на следующий день:\n'
                elif delta % 10 == 1:
                    temp = f'{delta} день до исполнения следующих заявок:\n'
                elif delta == 2:
                    temp = f'Через день ожидается прибытие заявок:\n'
                elif delta == 3:
                    temp = f'Через двое суток ожидается прибытие заявок:\n'
                elif delta == 4:
                    temp = f'В течении 96 часов будут выполнены заявки:\n'
                elif delta % 10 > 1 and delta % 10 <= 4:
                    temp = f'Через {delta-1} дня придут заказанные книги:\n'
                elif delta > 5 and delta < 9:
                    temp = f'Через {delta-1} суток прибудут заявки:\n'
                else:
                    temp = f'{delta} дней осталось до прибытия заказов:\n'
                for application in value:
                    temp += str(application)
                result += [(delta, temp)]
        if result:
            output = []
            for i, s in sorted(result, key=(lambda a: a[0])):
                output += [s + '\n']
            return output
        else:
            return ['']

    def make_request(self):
        """Формулирование заявки в издательство: проход по имеющимся изданиям,

        заказ тех, число которых критично мало.
        """
        items = self.publisher_index.items()
        for application in [
            Application(publisher)
            for name, publisher in items
        ]:
            if application.editions:
                day = application.delivery_day
                self.query[day].append(application)
        return self.query

    def recalculate(self, query):
        """Сдвиг очереди заявок на сутки."""
        arrived_order = self.query[self.current_day]
        summ = sum([application.arrive()
                    for application
                    in arrived_order])
        BookStore.log(f'Payed {summ} for arrived books')
        self.write_off(summ)
        BookStore.log(f"Current cash is {self.params['cash']} ")
        return

    def log(string, n=None):
        """Ведение логов."""
        if n:
            if n == 'Order':
                BookStore.orderlog.append(string)
        else:
            BookStore.textlog += '\n' + string
        # BookStore.logger.info(string)

    def write_off(self, count):
        """Списывание со счёта."""
        self.params['cash'] -= count

    def top_up(self, count):
        """Пополнение счёта."""
        self.params['cash'] += count
        self.params['income'] += count

    def register_buyer(buyer):
        """Регистрация нового покупателя в магазине."""
        BookStore.buyer_index.append(buyer)
        return BookStore.buyer_index

    def register_book(book):
        """Регистрация новой книги в магазине."""
        BookStore.book_index.append(book)
        BookStore.log(str(book))
        for edition in book.editions:
            if (BookStore.publisher_index.get(edition.publisher, False)):
                BookStore.publisher_index[edition.publisher].add(edition)
            else:
                from publisher import Publisher
                publisher = Publisher(edition.publisher)
                publisher.add(edition)
                BookStore.publisher_index[edition.publisher] = publisher
        if (BookStore.author_index.get(book.author, False)):
            BookStore.author_index[book.author].add(book)
        else:
            from author import Author
            author = Author(book.author)
            author.add(book)
            BookStore.author_index[book.author] = author
        return BookStore.book_index, BookStore.publisher_index, BookStore.author_index

    def bid_book(book):
        """Офорление требования на книгу, которую не удалось заказать."""
        BookStore.bid_book.append(book)
        print(BookStore.bid_book)
        return book

    def get_author(self):
        """Генерация автора из числа представленных в магазине."""
        temp = [i for i in self.author_index.values()]
        return random_choice(temp)

    def get_book(self):
        """Выдача книги из числа имеющихся в списке магазина (с любым.

        фактическим количеством)
        """
        return random_choice(self.book_index)

    def applicate_count(edition):
        """Дозаказ новых книг на основе полученной выручки."""
        from math import ceil
        print(edition)
        return ceil(markup(edition.is_frozen))

    def book_statistic(self):
        """Сбор статистики книг."""
        temp = sorted([book.statistic() for book in self.book_index],
                      key=lambda x: x.income, reverse=True)
        temp = [x.to_string(i) for i, x in enumerate(temp)]
        return temp

    def buyer_statistic(self):
        """Сбор статистики книг."""
        temp = sorted([buyer.statistic() for buyer in self.buyer_index],
                      key=lambda x: x[1], reverse=True)
        temp = [x[0] for i, x in enumerate(temp)]
        return temp


class Application(object):
    """Класс заявки в издательство."""
    __slots__ = 'editions', 'bid_day', 'delivery_day', 'publisher'

    def __init__(self, publisher):
        """Создание и формулировка заявки, её отправка в издательство и.

        получение ответа, содержащего время выполнения заказа.
        """
        self.publisher = publisher
        self.bid_day = BookStore.current_day
        self.delivery_day = self.bid_day + publisher.time()
        self.editions = [
            (one_edition.freeze(), BookStore.applicate_count(one_edition))
            for one_edition
            in publisher.editions
            if (one_edition.sold > 0)
            and (one_edition.count < low_book_count_threshold)
            and not one_edition.is_frozen
        ]
        return None

    def arrive(self):
        """Прибытие заявки, возвращает сумму заказа."""
        print(self.editions)
        summ = sum([one_edition.arrive(count)
                    for one_edition, count
                    in self.editions])
        BookStore.log(f'Application sum is {summ}.')
        return summ

    def __str__(self):
        temp = '\t' + self.publisher.name + ':\n'
        for edition, count in self.editions:
            temp += f'\t\t{count} экз. {str(edition)}\n'
        return temp
