from bookStore import BookStore
from randomB import random_seed
from settings import probability_new  # 0.1


class Order(object):
    """Общий класс заказа: хранит информацию о заказчике, и потребных ему.

    книгах.
    """
    __slots__ = 'buyer', 'wishes'

    def __init__(self, buyer, wishlist):
        """создание заказа: покупатель и пожелания."""
        self.buyer = buyer
        self.wishes = wishlist
        self.buyer.order += 1
        self.buyer.books.extend(wishlist)
        BookStore.log(f'created buyer {buyer} {[str(wish) for wish in wishlist]}')

    def booking(self):
        """оформление заказа."""
        # каждая книга обрабатывается
        summ = 0
        flag = True
        for wish in self.wishes:
            edition = wish.one_book.get_edition()
            if (edition is None):
                flag = False
            else:
                summ += edition.booking()
        BookStore.log((str(self), flag), 'Order')
        self.buyer.summ += summ
        return summ

    def __str__(self):
        """Строковое представление заявки."""
        temp = self.buyer.buyer_id() + ':\n'
        for wish in self.wishes:
            edition = wish.get_edition()
            if edition is None:
                temp += '\t!'+str(wish.one_book.sec_title())+';\n'
            else:
                temp += '\t'+str(edition)+';\n'
        return temp


class Wish(object):
    """
    Общий класс пожелания - один автор с перечнем книг. Мб затребована самая новая (get_last).
    """
    __slots__ = 'author', 'one_book', 'edition', 'new'

    def __init__(self, store):
        seed = random_seed()
        author = store.get_author()
        if seed < probability_new:
            self.new = True
            one_book = author.get_last()
        else:
            one_book = store.get_book()
        self.author = author
        self.one_book = one_book

    def __str__(self):
        return str(self.one_book)

    def get_edition(self):
        self.edition = self.one_book.get_edition()
        return self.edition
