from django.db import models


# Create your models here.
# 用户
class User(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True, db_index=True)


# 收入与支出的类别：餐饮、交通、服饰、购物。。。
class Category(models.Model):
    category_name = models.CharField(verbose_name="类别", max_length=32)


# 收支记录
class Record(models.Model):
    type_choices = ((1, "收入"), (2, "支出"))
    type = models.IntegerField(verbose_name="分类", choices=type_choices)

    ctime=models.DateField(verbose_name="创建时间", auto_now_add=True)
    money=models.DecimalField(verbose_name="金额", decimal_places=2, max_digits=20, default=0)
    note=models.TextField(verbose_name="备注")
    category=models.ForeignKey(verbose_name="类别", to="Category",on_delete=models.CASCADE)
    user=models.ForeignKey(verbose_name="用户", to="User", on_delete=models.CASCADE)
