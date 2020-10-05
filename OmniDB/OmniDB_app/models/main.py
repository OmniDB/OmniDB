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

class Shortcut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=200, blank=False)
    os = models.CharField(max_length=200, blank=False)
    ctrl_pressed = models.BooleanField(default=False)
    shift_pressed = models.BooleanField(default=False)
    alt_pressed = models.BooleanField(default=False)
    meta_pressed = models.BooleanField(default=False)
    key = models.CharField(max_length=200, blank=False)

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

class SnippetFolder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, blank=False, default='')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()

class SnippetFile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    parent = models.ForeignKey(SnippetFolder,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, blank=False, default='')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    text = models.TextField(blank=False, default='')


class Tab(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection,on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, default='')
    snippet = models.TextField(blank=False, default='')

class QueryHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection,on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.TextField(blank=False, default='')
    status = models.TextField(blank=False, default='')
    snippet = models.TextField(blank=False, default='')

class ConsoleHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection,on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    snippet = models.TextField(blank=False, default='')

class Group(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, default = '')

class GroupConnection(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'connection'], name='unique_group_connection')
        ]

class MonUnits(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    technology = models.ForeignKey(Technology,on_delete=models.CASCADE)
    script_chart = models.TextField(blank=False, default='')
    script_data = models.TextField(blank=False, default='')
    type = models.TextField(blank=False, default='')
    title = models.TextField(blank=False, default='')
    is_default = models.BooleanField(default=False)
    interval = models.IntegerField(blank=False,default=60)

class MonUnitsConnections(models.Model):
    unit = models.IntegerField(blank=False,default=60)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection,on_delete=models.CASCADE)
    interval = models.IntegerField(blank=False,default=60)
    plugin_name = models.TextField(blank=False, default='')
