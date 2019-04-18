from random import random, randrange, choice, normalvariate, lognormvariate
from numpy.random import poisson
from settings import standart_markup_const  # 0.5
from settings import novice_markup_const  # 1.0
from settings import sigma_normal  # 100
from settings import old_year, start_year  # 2000, 2018
from settings import ave_pages, sig_pages  # 500, 100
from settings import lognorm_mu, lognorm_sigma, lognorm_threshold  # 0, 1, 200
from settings import ave_sum_mu, ave_sum_sigma  # 10000, 2000
from settings import start_book_sum
from settings import assort_wish
from math import trunc, ceil


def random_mail():
    return '23456@mail.ru'


def random_name():
    return 'John'


def random_surname():
    return 'Doe'


def random_seed():
    return random()


def random_time(AVT):
    return random_norm(AVT, AVT/sigma_normal)


def random_count(price):
    result = ceil(start_book_sum / price)
    if result <= 0:
        result = 1
    return result


def random_norm(mu, sigma):
    return abs(trunc(normalvariate(mu, sigma)))


def random_year():
    return randrange(old_year, start_year-1)


def random_pages():
    return random_norm(ave_pages, sig_pages)


def random_price(edition):
    temp = lognormvariate(lognorm_mu, lognorm_sigma) * \
        (lognorm_threshold*edition.pages_used/ave_pages)
    if temp < lognorm_threshold:
        temp = lognorm_threshold-1
    else:
        temp = trunc(temp)
    return temp


def markup(price):
    return price+price*standart_markup_const


def novice_markup(price):
    return price+price*novice_markup_const


def random_sum(ave_sum_mu):
    return normalvariate(ave_sum_mu, ave_sum_sigma)


def applicate_count(book):
    return trunc(book.sold*book.retail_markup/book.price)


def random_choice(lst):
    return choice(lst)


def random_telephone_number():
    return '+7\
-{random.randint(0,999):03}\
-{random.randint(0,999):03}\
-{random.randint(0,99):02}\
-{random.randint(0,99):02}'


def random_address():
    return 'Nowhere, 3'


def get_wish(store):
    from wishOrder import Wish
    summ = random_sum(ave_sum_mu *
        (1.0+random() * len(store.book_index)*assort_wish)
        )
    if summ < 0:
        summ = 1
    wishes = []
    while summ > 0:
        temp = Wish(store)
        wishes.append(temp)
        edition = temp.one_book.get_edition()
        if edition is None:
            summ -= lognorm_mu * lognorm_threshold
        else:
            summ -= edition.price
    return wishes
