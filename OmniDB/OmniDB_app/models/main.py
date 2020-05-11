from django.db import models
from django.contrib.auth.models import User

class Technology(models.Model):
    name = models.CharField(max_length=50, blank=False)

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, blank=False,default='light')
    font_size = models.IntegerField(blank=False,default=12)
    csv_encoding = models.CharField(max_length=50, blank=False, default='utf-8')
    csv_delimiter = models.CharField(max_length=10, blank=False, default=';')
    welcome_closed = models.BooleanField(default=False)

class Connection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology,on_delete=models.CASCADE)
    server = models.CharField(max_length=200, blank=False, default='')
    port = models.CharField(max_length=50, blank=False, default='')
    database = models.CharField(max_length=200, blank=False, default='')
    username = models.CharField(max_length=200, blank=False, default='')
    password = models.CharField(max_length=200, blank=False, default='')
    alias = models.CharField(max_length=200, blank=False, default='')
    ssh_server = models.CharField(max_length=200, blank=False, default='')
    ssh_port = models.CharField(max_length=50, blank=False, default='')
    ssh_user = models.CharField(max_length=200, blank=False, default='')
    ssh_password = models.CharField(max_length=200, blank=False, default='')
    ssh_key = models.TextField(blank=False, default='')
    use_tunnel = models.BooleanField(default=False)
    conn_string = models.TextField(blank=False, default='')
