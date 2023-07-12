from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class invoice(models.Model):
    Sender = models.ForeignKey(User, on_delete=models.CASCADE)
    Reciever = models.CharField(max_length=50)
    Date_shippment = models.DateField()
    price_of_shipping = models.DecimalField(max_digits = 55,decimal_places = 6)
    price_of_product= models.DecimalField(max_digits = 55,decimal_places = 6)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    order_status = models.BooleanField()
    
    def __str__(self):
        return self.Reciever +" status of shippment "+ str(self.order_status)