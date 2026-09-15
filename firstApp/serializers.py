from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', "first_name", "last_name", "email", "age", "is_active"]
        # fields = "__all__" # get all fields
        read_only_fields = ['id']

    def validate_email(self, value):
        """
        Custom validation for email field.
        this runs during both create and update operations
        """
        # check if we're updating an existing instance ==> instance == row in table
        if self.instance:
            # for update : if email is changed, check if it exists for other students
            if self.instance.email != value:
                if Student.objects.filter(email=value).exists():
                    raise serializers.ValidationError('A student with email already exists.') 
        else:
            # for creates: check if email exist for any student
            if Student.objects.filter(email=value).exists():
                raise serializers.ValidationError('A student with email already exists.') 
            
        return value

    def validate_age(self, value):
        """
        Custom validation for age field.
        """
        if value < 1 or value > 120:
            raise serializers.ValidationError('Age must be between 1 and 120') 
        
        return value