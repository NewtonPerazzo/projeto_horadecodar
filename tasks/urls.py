from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.taskslist, name='task-list'),
    path('dashboard/<int:id>', views.dashboard, name='dashboard'),
    path('tasks/<int:id>', views.taskView, name='task-view'),
    path('newtask/', views.newTask, name='newtask'),
    path('edit/<int:id>', views.editTask, name='edittask'),
    path('delete/<int:id>', views.deleteTask, name='deletetask'),
    path('changestatus/<int:id>', views.changeStatus, name='changestatus'),
]
