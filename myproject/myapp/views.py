from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book
from .forms import BookForm

# -----------------------------
#           FBVs
# -----------------------------
def base(request):
    return render(request, 'myapp/base.html')


@login_required
def hello_fbv(request):
    books = Book.objects.filter(source_type=1)
    return render(request, 'myapp/hello_fbv.html', {'books': books})


@login_required
def book_create_fbv(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.source_type = 1  # Force FBV
            book.save()
            return redirect('hello_fbv')
    else:
        form = BookForm()
    return render(request, 'myapp/book_form.html', {'form': form, 'type': 'FBV Create'})


@login_required
def book_update_fbv(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('hello_fbv')  # Redirect to Hello FBV page
    else:
        form = BookForm(instance=book)
    return render(request, 'myapp/book_form.html', {'form': form, 'type': 'FBV Update'})


@login_required
def book_delete_fbv(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('hello_fbv')  # Redirect to Hello FBV page
    return render(request, 'myapp/book_confirm_delete.html', {'object': book, 'type': 'FBV'})


# -----------------------------
#           CBVs    
# -----------------------------
class HelloCBV(LoginRequiredMixin, View):
    def get(self, request):
        books = Book.objects.filter(source_type=2)
        return render(request, 'myapp/hello_cbv.html', {'books': books})
    

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/book_form.html'

    def form_valid(self, form):
        form.instance.source_type = 2  # Force CBV
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('hello_cbv')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'CBV Create'
        return context


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'myapp/book_form.html'

    def get_success_url(self):
        return reverse_lazy('hello_cbv')  # Redirect to Hello CBV page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'CBV Update'
        return context


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'myapp/book_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('hello_cbv')  # Redirect to Hello CBV page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'CBV'
        return context


# -----------------------------
#     Form Selector (Optional)
# -----------------------------
@login_required
def book_form_selector(request):
    form = BookForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            book = form.save(commit=False)
            # Get source_type from POST (default to 1 if not provided)
            book.source_type = int(request.POST.get('source_type', 1))
            book.save()

            if book.source_type == 1:
                return redirect('hello_fbv')
            elif book.source_type == 2:
                return redirect('hello_cbv')

    # Decide label based on selected source_type
    source_type = request.POST.get('source_type')
    if source_type == "1":
        type_label = "FBV Form"
    elif source_type == "2":
        type_label = "CBV Form"
    else:
        type_label = "Book Form"

    return render(request, 'myapp/book_form.html', {
        'form': form,
        'type': type_label
    })


# -----------------------------
#   Auth Views (Register/Login)
# -----------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ✅ auto-login after register
            return redirect("index")  # go to home after register
    else:
        form = UserCreationForm()
    return render(request, "myapp/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "myapp/login.html"   # ✅ your template location
    redirect_authenticated_user = True

    def get_success_url(self):
        # after login, go to book form selector (or change to hello_fbv/hello_cbv)
        return reverse_lazy("book_form")
