from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index , name="index"),

    path("", views.home , name="home"), 

    path("notes/", views.notes , name="notes"),
    path("deletenote/<int:pk>", views.deletenote , name="deletenote"),
    path("notesdetails/<int:pk>", views.NotesDetailsView.as_view() , name="notesdetails"),
    path("homework/", views.homework , name="homework"),
    path("updatehomework/<int:pk>", views.update_homework , name="updatehomework"), 
    path("deletehomework/<int:pk>", views.delete_homework , name="deletehomework"),
    path("youtube/", views.youtube , name="youtube"),
    path("todo/", views.todo , name="todo"),
    path("update_todo/<int:pk>", views.update_todo , name="update_todo"),
    path("deletetodo/<int:pk>", views.delete_todo , name="deletetodo"),
    path("books/", views.books , name="books"),
    path("dictinory/", views.dictinory , name="dictinory"),
    path("wiki/", views.wiki , name="wiki"),
    path('convert/', views.unit_conversion_view, name='unit_conversion'),
    path("profile/",views.user_profile, name="profile"),
]
