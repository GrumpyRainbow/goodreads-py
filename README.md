Python wrapper to communicate with Goodreads API.

[![Build Status](https://travis-ci.org/GrumpyRainbow/goodreads-py.png)](https://travis-ci.org/GrumpyRainbow/goodreads-py)

## Getting Started

``` python
import goodreads

client = goodreads.Client(client_id="abc123")

book = client.book_title(author='Chuck Palahniuk', title='Fight Club')
book.title # => 'Fight Club'
book.id    # => '5759'
book.authors # => [<goodreads.client.author.Author instance at 0x108dda7a0>]

author = book.authors[0]

author.name # => 'Chuck Palahniuk'
author.id   # => '2546'
author.average_rating # => '3.80'
```
