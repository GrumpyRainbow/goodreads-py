import book

class Author:
    def __init__(self, author_dict):
        for key, val in author_dict.items():
            if key == 'books':
                books = []
                for book_dict in author_dict[key]['book']:
                    print book_dict['title']
                    books.append(book.Book(book_dict))
                self.__class__.__dict__[key] = books
                continue
            self.__class__.__dict__[key] = val

