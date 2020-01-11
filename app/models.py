from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class store_tinyurl(models.Model):

	short_key = models.CharField(primary_key=True, max_length=50, null=False)
	url = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	iskeepforever = models.IntegerField(default=0)
	creator = models.ForeignKey(User , on_delete=models.CASCADE, null=True)
	
	class Meta:
		unique_together = (('short_key'),)