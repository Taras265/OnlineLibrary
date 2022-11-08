from django.urls import path
from users.views import ReaderListView, ReaderDetailView, CreateReaderView, UpdateReaderView, DeleteReaderView

urlpatterns = [
    path('readers/', ReaderListView.as_view(), name='readers_list'),
    path('readers/<int:pk>/', ReaderDetailView.as_view(), name='reader_detail'),
    path('readers/create/', CreateReaderView.as_view(), name='create_reader'),
    path('readers/<int:pk>/update/', UpdateReaderView.as_view(), name='update_reader'),
    path('readers/<int:pk>/delete/', DeleteReaderView.as_view(), name='delete_reader'),
]
