from bookStore import BookStore


class Author(object):
    __slots__ = 'author', 'bibliography', 'sorted'

    def __init__(self, name):
        """создание нового автора, с заданным именем и пустой библиографией."""
        self.author = name
        self.bibliography = []
        BookStore.log(f'author {name} created/n')

    def add(self, one_book):
        """добавление книги в библиографию."""
        self.bibliography.append(one_book)
        BookStore.log(f'author{self.author} book {one_book.title} added')

    def __str__(self):
        """перевод в строковое представление."""
        temp = self.author + ' '
        for one_book in self.bibliography:
            temp += str(one_book)
        return temp

    def get(self, wish=None):
        """получение книги автора."""
        BookStore.log(f'book {wish} got from {self.author}')
        temp = None
        for book in self.bibliography:
            if wish.title == book.title:
                temp = book
                if temp.count > 0:
                    return temp
        return temp

    def get_last(self):
        """получение самой новой книги автора."""
        return max(self.bibliography, key=lambda book: book.first_published)
