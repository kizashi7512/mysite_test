from django.urls import path

from . import views
app_name = 'thread'

urlpatterns = [
  path('create_topic/', views.TopicCreateView.as_view(), name='create_topic'),
  # path('<int:pk>/', views.TopicDetailView.as_view(), name='topic'),
  path('<int:pk>/', views.TopicAndCommentView.as_view(), name='topic'),
  path('category/<str:url_code>/', views.CategoryView.as_view(), name='category'),
  
  #3/14
  # コメントをしようとしたらnameとmessageが出てくるはずだが、コメントのボタンしか出てこない
  #おそらく、line8を消して、TopicDetailViewを消すか、下に移動させればできそう
  #3/15
  #コメント投稿してもエラーが出なくなった。しかし、user_nameは投稿できたが、messageが投稿できなかった
]