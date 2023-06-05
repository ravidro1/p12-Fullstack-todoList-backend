

from rest_framework.views import APIView
from list_api.models import Task, List
from list_api.serializers.list_serializer import  ListSerializer,TaskSerializer
from list_api.serializers.user_serializer import  UserSerializer
from rest_framework.response import Response
from rest_framework import status

from list_api.authentication import JWTAuthentication


class GetAllListTask(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        user_id = user_serializer.data["id"]
        lists = List.objects.filter(ownerUserID=user_id)        

        serializer = ListSerializer(lists, many=True)

        data = []

        for i in serializer.data:
            try:
                tempList = i.copy()

                tasks = Task.objects.filter(ownerListID=i["id"])
                tasks_serializer = TaskSerializer(tasks, many=True)
                tempList["tasks"] = tasks_serializer.data
                data.append(tempList)
            except Exception as e:
                print(e)

        return Response(data)

#[name]
class CreateNewList(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
    
        data = request.data.copy()
        user_serializer = UserSerializer(request.user)
        data['ownerUserID'] = user_serializer.data["id"]
        print(data)
        serializer = ListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# [list_id]
class DeleteList(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            list = List.objects.get(pk=request.data["list_id"])
        except:
            return Response({"Error": "Task Not Found"}, status=status.HTTP_400_BAD_REQUEST)

        list.delete()
        return Response({"massage": "Item Delete Successfully"})

# [title, content, start_date, end_date, ownerListID]
class CreateNewTask(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# [task_id]
class DeleteTask(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            task = Task.objects.get(pk=request.data["task_id"])
        except:
            return Response({"Error": "Task Not Found"}, status=status.HTTP_400_BAD_REQUEST)

        task.delete()
        return Response({"massage": "Item Delete Successfully"})

# [task_id, is_complete]
class EditIsCompleteTask(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        try:
            task = Task.objects.get(pk=request.data["task_id"])
            task.is_complete = request.data['is_complete']
            task.save()
            serializer = TaskSerializer(task)

            return Response(serializer.data)
        except Exception as error:
            return Response({'message': error},status=status.HTTP_400_BAD_REQUEST)

