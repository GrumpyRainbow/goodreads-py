import book

class Author:
    def __init__(self, author_dict):
        for key, val in author_dict.items():
            if key == 'books':
                book_list = [book.Book(book_dict) for book_dict in
                    author_dict[key]['book']]
                self.__dict__[key] = book_list
                continue
            self.__dict__[key] = val
