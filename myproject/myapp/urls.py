from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.base, name='index'),

    # Hello Pages
    path('hello-fbv/', views.hello_fbv, name='hello_fbv'),
    path('hello-cbv/', views.HelloCBV.as_view(), name='hello_cbv'),

    # FBV Create/Update/Delete
    path('books/create-fbv/', views.book_create_fbv, name='book-create-fb'),
    path('books/<int:pk>/edit-fbv/', views.book_update_fbv, name='book-update-fb'),
    path('books/<int:pk>/delete-fbv/', views.book_delete_fbv, name='book-delete-fb'),

    # CBV Create/Update/Delete
    path('books/create-cbv/', views.BookCreateView.as_view(), name='book-create-cb'),
    path('books/<int:pk>/edit-cbv/', views.BookUpdateView.as_view(), name='book-update-cb'),
    path('books/<int:pk>/delete-cbv/', views.BookDeleteView.as_view(), name='book-delete-cb'),

    # Selector
    path('book-form/', views.book_form_selector, name='book_form'),

    # Auth
    path("register/", views.register, name="register"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="myapp/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]

