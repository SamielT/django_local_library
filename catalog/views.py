from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Initialize counts for books and genres containing the word
    num_books_containing_word = 0
    books_containing_word = []
    particular_word = ''

    if 'word' in request.GET:
        particular_word = request.GET['word']
        books_containing_word = Book.objects.filter(title__icontains=particular_word)
        num_books_containing_word = Book.objects.filter(title__icontains=particular_word).count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_containing_word': num_books_containing_word,
        'particular_word': particular_word,
        'books_containing_word': books_containing_word,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
