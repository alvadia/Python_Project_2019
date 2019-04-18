from randomB import random_surname, random_seed, random_name, random_address
from randomB import random_year, random_mail, random_telephone_number
from bookStore import BookStore
from settings import buyer_call_prob, buyer_email_prob


class Customer(object):
    __slots__ = 'name', 'surname', 'address', 'telephone_number', 'email', 'books', 'order', 'summ'

    def __init__(self, **kwargs):
        self.name = 'John'
        self.surname = 'Doe'
        self.address = 'nothing'
        self.telephone_number = '000-000-00-00'
        self.email = '0@null.com'
        for key, value in kwargs.items():
            attr = key.lower()
            if attr in self.__slots__:
                setattr(self, attr, value)
        BookStore.log(f'created buyer {str(self)} ')
        self.books = []
        self.order = 0
        self.summ = 0

    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.address + ' ' + self.telephone_number + ' ' + self.email

    def buyer_id(self):
        """Идентификация покупателя:

        либо ФИО; либо телефон + адрес; либо email + представление
        """
        seed = random_seed()
        if seed < buyer_email_prob:
            result = self.name + ' ' + self.email
        elif seed < buyer_email_prob + buyer_call_prob:
            result = self.surname + ' ' + self.address + ' ' + self.telephone_number
        else:
            result = self.surname + ' ' + self.name
        return result

    def statistic(self):
        temp = len([b for b in self.books if b.edition])
        return (f'{str(self)}\nзаключил {self.order} сделок на общую сумму {int(self.summ)},\nв общей сложности закупив {temp} книг.', int(self.summ))
