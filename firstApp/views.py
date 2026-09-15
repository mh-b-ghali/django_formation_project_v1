# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from firstApp.models import Student
# import json
# # Create your views here.
# #CRUD 1/ R <==> read ==> rest api ==> GET

# @csrf_exempt
# def get_students(request):
#     if request.method == "GET":
#         students = Student.objects.all() # select * from students
#         # convert to list of dictionaries
#         print({"students":students})
#         students_list = []
#         for student in students:
#             print({"student":student.last_name})
#             students_list.append({
#                 "id": student.id,
#                 "first_name": student.first_name,
#                 "last_name": student.last_name,
#                 "age":student.age,
#                 "email": student.email,
#                 "is_active": student.is_active
#             })
#         # return JsonResponse({"students":students},status=200)
#         return JsonResponse({"students":students_list, "count": len(students_list)},status=200)
#     return JsonResponse({"error":"Method not allowed"}, status=405)

# @csrf_exempt
# def get_student(request, pk):
#     if request.method == "GET":
#         try:
#             student = Student.objects.get(id=pk) # select * from students where id=pk
#         except Exception as e:
#             print({"msg_error": str(e)})
#             return JsonResponse({"error": "student not exist"}, status=404)
#         student_data= {
#             "id": student.id,
#             "first_name": student.first_name,
#             "last_name": student.last_name,
#             "age": student.age,
#             "email": student.email,
#             "is_active": student.is_active
#         }
#         return JsonResponse({"student": student_data}, status=200)
#     return JsonResponse({"error":"Method not allowed"}, status=405)

# #CRUD 2/ C <==> create ==> rest api ==> POST

# @csrf_exempt
# def create_student(request):
#     if request.method == "POST":
#         print({"request.body":request.body})
#         print(type(request.body))
#         data = json.loads(request.body)
#         print({"data":data})
#         print({"age": data["age"]})
#         print({"email": data["email"]})
#         # validate required fields 
#         required_fields = ['age', 'first_name', 'last_name', 'email']
#         for field in required_fields:
#             if  field not in data:
#                 return JsonResponse({"error": f"Missing field {field}"}, status=400)

#         # create student
#         student = Student.objects.create(
#             first_name=data["first_name"],
#             last_name= data['last_name'],
#             email=data['email'],
#             age=data['age'],
#             is_active=data.get('is_active',True)
#         )
#         """
#         INSERT INTO student (first_name,last_name,email,age,is_active)
#         VALUES(data["first_name"],data["last_name"],data["email"],data["age"],data["is_active"])
#         """
#         student_data = {
#             "id": student.id,
#             "first_name": student.first_name,
#             "last_name": student.last_name,
#             "email": student.email,
#             "age": student.age,
#             "is_active": student.is_active,
#         }
#         return JsonResponse({"student": student_data}, status=201)
#     return JsonResponse({"error":"Method not allowed"}, status=405)

# #CRUD 3/ U <==> update ==> rest api ==> PUT or PATCH

# @csrf_exempt
# def update_student(request, pk):
#     if request.method == "PUT":
#         data = json.loads(request.body)
#         try:
#             student = Student.objects.get(id=pk)
#         except Exception:
#             return JsonResponse({"error": "student not exist"}, status=404)

#         # update only provided fields:
#         if 'first_name' in data:
#             student.first_name = data['first_name']
#         if 'last_name' in data:
#             student.last_name = data['last_name']
#         if 'email' in data:
#             student.email = data['email']
#         if 'age' in data:
#             student.age = data['age']
#         if 'is_active' in data:
#             student.is_active = data['is_active']

#         student.save()
#         """
#         UPDATE student SET 
#         first_name=new_first_name, last_name=new_last_name,age=new_age, email=new_email, is_active=new_is_active
#         where id = pk
#         """

#         return JsonResponse({"message":"student updated successfully"}, status=200)
#     return JsonResponse({"error":"Method not allowed"}, status=405)


# #CRUD 4/ D <==> delete ==> rest api ==> DELETE

# @csrf_exempt
# def delete_student(request, student_id):
#     if request.method == "DELETE":
#         try:
#             student = Student.objects.get(id=student_id)
#         except Exception:
#             return JsonResponse({"error": "student not exist"}, status=404)
        
#         student.delete()
#         return JsonResponse({"message":"student deleted successfully"}, status=200)
#     return JsonResponse({"error":"Method not allowed"}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from firstApp.models import Student
from firstApp.serializers import StudentSerializer
import json

@csrf_exempt
@require_http_methods(["GET"])
def get_students(request):
    """ GET: list all students"""
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return JsonResponse({"students": serializer.data, "count": len(serializer.data)}, status = 200)

@csrf_exempt
@require_http_methods(["GET"])
def get_student(request, pk):
    """GET: retrieve a student"""
    try:
        student = Student.objects.get(id=pk)
        serializer = StudentSerializer(student)
        return JsonResponse ({"student": serializer.data},status=200)
    except Student.DoesNotExist:
        return JsonResponse({"error": "student not found"}, status=404)

@csrf_exempt
@require_http_methods(['POST'])
def create_student(request):
    """POST: create a new student"""
    json_data = json.loads(request.body)
    serializer = StudentSerializer(data=json_data)
    if serializer.is_valid():
        student = serializer.save()
        student_data = StudentSerializer(student).data

        return JsonResponse({
            "message": "student created successfully",
            "student": student_data
        },status= 201)
    return JsonResponse({"error": serializer.errors},status=400)

@csrf_exempt
@require_http_methods(['PUT', 'PATCH'])
def update_student(request, student_id):
    """PUT/PATCH: update  a student"""
    data = json.loads(request.body)
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "student not found"}, status=404)

    update_serializer = StudentSerializer(student, data=data)

    if update_serializer.is_valid():
        student = update_serializer.save()
        student_data = StudentSerializer(student).data
        return JsonResponse({
            "message": "student updated successfully",
            "student": student_data
        },status=200)
    return JsonResponse({"error": update_serializer.errors},status=400) 

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_student(request, pk):
    """DELETE: delete a student"""
    try:
        student = Student.objects.get(id=pk)
        student.delete()
        return JsonResponse({"message": "student deleted successfully"}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({"error": "student not found"}, status=404)
    