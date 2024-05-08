from django.urls import path
from . import views

app_name = 'polls'  # 앱 이름 추가

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.goal_list, name='goal_list'),  # 'goals/' 대신 빈 문자열 사용
    path('<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),  # 'goals/<int:goal_id>/delete/' 대신 '<int:goal_id>/delete/' 사용
    path('<int:goal_id>/complete/', views.complete_goal, name='complete_goal'),  # 'goals/<int:goal_id>/complete/' 대신 '<int:goal_id>/complete/' 사용
    path('history/', views.history, name='history'),
    path('<int:goal_id>/reflection/', views.add_reflection, name='add_reflection'),
]