probability_new = 0.1
range_order, sigma_order = 100, 3
start_cash = 0
low_book_count_threshold = 15
start_book_sum = 50000
start_year = 2019
start_newness = 60
standart_markup_const, novice_markup_const = 0.5, 1.0
finalDay = 90
sigma_normal = 100
old_year, start_year = 2000, 2018
ave_pages, sig_pages = 500, 100
lognorm_mu, lognorm_sigma, lognorm_threshold = 0, 1, 200
ave_sum_mu, ave_sum_sigma = 1500, 1000
buyer_call_prob, buyer_email_prob = 0.1, 0.2
assort_wish = 1/100
_const_DEBUG = True
_strings = {'finalDay': ('I', 1, -1, 'Последний день'),
            'probability_new': ('R', 0.0, 1.0, 'Вероятность требования новой книги'),
            'range_order': ('I', 1, -1, 'Среднее число заказов в сутки'),
            'sigma_order': ('I', 1, -1, 'Дисперсия числа заказов в сутки'),
            'start_cash': ('I', 0, -1, 'Начальный наличный капитал магазина'),
            'start_book_sum': ('I', 1, -1, 'Начальный капитал (на одно издание) в магазине'),
            'low_book_count_threshold': ('I', 1, -1, 'Порог заказа издания книги'),
            'old_year': ('I', 1500, -1, 'Год самого старого издания'),
            'start_year': ('I', 1500, -1, 'Год выхода новинок'),
            'start_newness': ('I', 1, -1, 'Время жизни новинки'),
            'standart_markup_const': ('R', 0.0, -1.0, 'Стандартная наценка в розницу'),
            'novice_markup_const': ('R', 0.0, -1.0, 'Наценка на новинки'),
            'ave_pages': ('I', 100, -1, 'Среднее число страниц одного издания'),
            'sig_pages': ('I', 1, 100, 'Корень дисперсии объёма книги'),
            'sigma_normal': ('I', 1, 2**30, 'Отношение E(x)/sqrt(D(x)) при определении времени прибытия заявки'),
            'lognorm_mu': ('R', 0.0, 2.0, 'Центральный момент себестоимости книги'),
            'lognorm_sigma': ('R', 0.0, 2.0, 'Корень дисперсии логнормального распределения цен'),
            'lognorm_threshold': ('I', 1, -1, 'Масштаб цены одной книги'),
            'ave_sum_mu': ('I', 1, -1, 'Средняя сумма покупок одного покупателя'),
            'ave_sum_sigma': ('I', 1, -1, 'Корень дисперсии суммы покупок одного покупателя'),
            'buyer_call_prob': ('R', 0., 1., 'Вероятность заказа через городскую телекоммуникационную сеть'),
            'buyer_email_prob': ('R', 0., 1., 'Вероятность заказа через мировую информационную сеть'),
            'assort_wish': ('R', 0., 1., 'Отношение процентного увеличения суммы заказа к ассортименту магазина'),
            }
