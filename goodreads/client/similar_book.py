class SimilarBook:
    def __init__(self, similar_book_dict):
        for key, val in similar_book_dict.items():
            self.__class__.__dict__[key] = val
