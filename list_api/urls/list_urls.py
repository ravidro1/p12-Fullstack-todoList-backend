from django.urls import path
from list_api.views.list_views import GetAllListTask, CreateNewList,DeleteList, CreateNewTask,DeleteTask, EditIsCompleteTask

urlpatterns = [
    path("get-all-list", GetAllListTask.as_view()),
    path("create-new-list", CreateNewList.as_view()),
    path("delete-list", DeleteList.as_view()),
    
    path("create-new-task", CreateNewTask.as_view()),
    path("delete-task", DeleteTask.as_view()),
    path("edit-is-complete-task", EditIsCompleteTask.as_view()),
]
