from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Book
from .forms import BookForm

# -----------------------------
#           Root Redirect
# -----------------------------
def base(request):
    return redirect("login")  # Redirect root (/) to login page

@login_required
def index(request):
    return render(request, 'myapp/base.html')  # Dashboard / home after login

# -----------------------------
#           FBVs
# -----------------------------
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
            return redirect('hello_fbv')
    else:
        form = BookForm(instance=book)
    return render(request, 'myapp/book_form.html', {'form': form, 'type': 'FBV Update'})

# ✅ FBV delete only for admin
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='index')
def book_delete_fbv(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('hello_fbv')
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
        form.instance.source_type = 2
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
        return reverse_lazy('hello_cbv')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'CBV Update'
        return context

# ✅ CBV delete only for admin
class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'myapp/book_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('hello_cbv')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'CBV'
        return context

    def test_func(self):
        return self.request.user.is_superuser

# -----------------------------
#     Form Selector (Optional)
# -----------------------------
@login_required
def book_form_selector(request):
    form = BookForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        book = form.save(commit=False)
        book.source_type = int(request.POST.get('source_type', 1))
        book.save()
        return redirect('hello_fbv' if book.source_type == 1 else 'hello_cbv')

    source_type = request.POST.get('source_type')
    type_label = "FBV Form" if source_type == "1" else "CBV Form" if source_type == "2" else "Book Form"

    return render(request, 'myapp/book_form.html', {'form': form, 'type': type_label})

# -----------------------------
#   Auth Views (Register/Login/Logout)
# -----------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")  # go to dashboard after register
    else:
        form = UserCreationForm()
    return render(request, "myapp/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "myapp/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")  # go to dashboard after login

@login_required
def logout_view(request):
    logout(request)
    return render(request, "myapp/logout.html")  # optional logout page
