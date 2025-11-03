from django.urls import path
from .views import PostNewsView, EditNewsView, DeleteNewsView, NewsListView, NewsSearchView

urlpatterns = [
    path('post/', PostNewsView.as_view(), name='post_news'),
    path('edit/<int:pk>/', EditNewsView.as_view(), name='edit_news'),  #the pk is the primary key of the news item to be edited i.e. its id(of the news item not the chief editor)
    path('delete/<int:pk>/', DeleteNewsView.as_view(), name='delete_news'),
    path('list/', NewsListView.as_view(), name='list_news'),
    path('search/', NewsSearchView.as_view(), name='search_news'),
]
