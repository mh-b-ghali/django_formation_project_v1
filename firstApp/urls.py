from django.urls import path
from . import views

urlpatterns = [
    path('all_students', views.get_students, name="get_students"),
    # path('student_by_id/<int:pk>', views.get_student),
    # path('create_student', views.create_student),
    # path('update_student/<int:pk>', views.update_student),
    # path('delete_student/<int:student_id>', views.delete_student),
]
