from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)  # ==> VARCHAR(100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) #"@ include in email"
    age = models.PositiveIntegerField()  # age always > 0 # ==> int
    is_active = models.BooleanField(default=True) # ==> bool
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"