from bookStore import BookStore
from randomB import random_time


class Publisher(object):
    __slots__ = 'AVT', 'name', 'editions', 'cash'
    """
    создание издателя с средним временем доставки AVT,
    именем и пустым списком книг
    """

    def __init__(self, name):
        self.AVT = 3
        self.name = name
        self.editions = []
        self.cash = 0
        BookStore.log(f'Publisher {name} created')
    """
    добавление книги в библиографию
    """

    def add(self, one_edition):
        self.editions += [one_edition]
        BookStore.log(f'{self.name} added {one_edition.book.title}')
    """
    перевод в строковое представление
    """

    def __str__(self):
        temp = self.name + ' ' + str(self.AVT) + ' '
        for one_edition in self.editions:
            temp += str(one_edition)
        return temp

    def time(self):
        return random_time(self.AVT)

    def arrive(self, editionlist):
        for edition, count in editionlist:
            self.cash += edition.arrive(count)
            BookStore.log(f'{self.name} book {edition.book.title} arrived ')
