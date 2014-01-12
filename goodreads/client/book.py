import author
import similar_book

class Book:
    def __init__(self, book_dict):
        for key, val in book_dict.items():
            if key == 'authors':
                authors = []
                for author_dict in book_dict[key].values():
                    authors.append(author.Author(author_dict))
                self.__dict__[key] = authors
                continue
            if key == 'similar_books':
                sim_books = []
                for sim_book_list in book_dict[key].values():
                    for sim_book_dict in sim_book_list:
                        sim_books.append(similar_book.SimilarBook(sim_book_dict))
                self.__dict__[key] = sim_books
                continue
            self.__dict__[key] = val

    def publication_date(self):
        year = int(self.publication_year)
        month = int(self.publication_month)
        day = int(self.publication_day)
        return datetime.date(year, month, day)
