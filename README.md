Python wrapper to communicate with Goodreads API.

[![Build Status](https://travis-ci.org/GrumpyRainbow/goodreads-py.png)](https://travis-ci.org/GrumpyRainbow/goodreads-py)

## Getting Started

#### Basic Setup and Requests
``` python
import goodreads

client = goodreads.Client(client_id="abc123", client_secret="IsolemnlyswearIamuptonogood") # Secret is optional
```
 Retrieve books:
``` python
book = client.book_title(author='Chuck Palahniuk', title='Fight Club')
book.title # => 'Fight Club'
book.id    # => '5759'
book.authors # => [<goodreads.client.author.Author instance at 0x108dda7a0>]
```
 Retrieve authors:
``` Python
author = book.authors[0]
author.name # => 'Chuck Palahniuk'
author.id   # => '2546'
author.average_rating # => '3.80'
```
 Convert author name to/from ID:
``` Python
author_id = client.get_author_id('Chuck Palahniuk') # => '2546'
client.author_by_id(author_id).name # => 'Chuck Palahniuk'
```
 Convert book ISBN to ID:
``` Python
book_id = client.get_book_id('0393327345') # => '5759'
```
#### OAuth Setup
 Some methods require Open Authentication (OAuth)
 If you already have access tokens, then you can authenticate directly:
``` python
client.authenticate(access_token='Fizzing',
                    access_token_secret='Whizbee')
```
 If you don't have access tokens, then authentication is a two step process.
 (Callbacks are not yet supported)
``` Python
client.authenticate()
>To authorize access visit: http://www.goodreads.com/oauth/authorize?oauth_token=SherbetLemon
```
 Note: this url will automatically be opened in your browser.
 After authorizing goodreads enter 'y' in to the console.
``` Python
>Have you authorized me? (y/n) y
access_token, access_token_secret = client.get_access_tokens() # Save these for later!
```
##### OAuth Examples:
 Get information about the authenticated user:
```Python
user_id, user_name = client.get_auth_user() # => ('1337', 'Neville Longbottom')
```
 Get a user's friends from a user ID:
``` Python
friends = client.get_friends('1374963', num=30) # => (('1338', 'Hannah Abbott'), ('666', ' Bellatrix Lestrange'))
```
 Compare authenticated user's books to another's:
``` Python
comparison = client.compare_books('8118135')
comparison.not_in_common #> 70
comparison.your_library_percent #> 8.16
comparison.their_library_percent #> 31.37
comparison.your_total_books_count #> 392
comparison.their_total_books_count #> 102
comparison.common_count #> 32
comparison.reviews[10]['title'] #> The Time Machine
comparison.reviews[10]['your_rating'] #> 4
comparison.reviews[10]['their_rating'] #> 3
```
