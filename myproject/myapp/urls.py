from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Root redirect → login
    path("", views.base, name="root_redirect"),

    # Explicit login URL
    path("accounts/login/", auth_views.LoginView.as_view(template_name="myapp/login.html"), name="login"),

    # Dashboard / Home
    path("home/", views.index, name="index"),  # shows base.html after login

    # Hello Pages
    path("hello-fbv/", views.hello_fbv, name="hello_fbv"),
    path("hello-cbv/", views.HelloCBV.as_view(), name="hello_cbv"),

    # FBV Create/Update/Delete
    path("books/create-fbv/", views.book_create_fbv, name="book-create-fb"),
    path("books/<int:pk>/edit-fbv/", views.book_update_fbv, name="book-update-fb"),
    path("books/<int:pk>/delete-fbv/", views.book_delete_fbv, name="book-delete-fb"),

    # CBV Create/Update/Delete
    path("books/create-cbv/", views.BookCreateView.as_view(), name="book-create-cb"),
    path("books/<int:pk>/edit-cbv/", views.BookUpdateView.as_view(), name="book-update-cb"),
    path("books/<int:pk>/delete-cbv/", views.BookDeleteView.as_view(), name="book-delete-cb"),

    # Selector
    path("book-form/", views.book_form_selector, name="book_form"),

    # Auth
    path("register/", views.register, name="register"),

    # Logout page
    path("logout/", views.logout_view, name="logout"),
]
