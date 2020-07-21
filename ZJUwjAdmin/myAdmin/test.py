#coding:utf8
from django.core.management.base import BaseCommand
from models import User
 
class Command(BaseCommand):
 
    def handle(self, *args, **options):
        from django.core.management.color import no_style   
        #Style是用来输出语句时着色的，没什么用
 
        from django.db import connection
        from django.db.backends import creation
        #这里面有个类BaseDatabaseCreation，就是用来生成SQL语句的。
        
        #c = creation.BaseDatabaseCreation(connection)
        #for model in [User]:
            #T = model()
            #print c.sql_create_model(T,no_style())[0][0]
 