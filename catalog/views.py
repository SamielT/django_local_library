from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    # Initialize counts for books and genres containing the word
    num_books_containing_word = 0
    books_containing_word = []
    particular_word = ''

    if 'word' in request.GET:
        particular_word = request.GET['word']
        books_containing_word = Book.objects.filter(title__icontains=particular_word)
        num_books_containing_word = books_containing_word.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
        'num_books_containing_word': num_books_containing_word,
        'particular_word': particular_word,
        'books_containing_word': books_containing_word,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# All books
class BookListView(generic.ListView):
    model = Book
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book

# All authors
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
class StaffAllBorrowed(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing all books on loan."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )
