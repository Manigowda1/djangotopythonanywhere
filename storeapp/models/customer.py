from django.db import models


class Customer(models.Model):#2
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.name

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False
