from django.db import models
from enum import Enum


# Create your models here.
class Provinces(models.Model):
    name = models.CharField(max_length=32, verbose_name="省份名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    edit_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")


class City(models.Model):
    """城市表，关联provinces省份表"""
    province = models.ForeignKey(
        Provinces,
        on_delete=models.SET_NULL,
        null=True,
        related_name="province_city",
        verbose_name="省份外键"
    )
    name = models.CharField(max_length=32, verbose_name="城市名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    edit_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")


class Community(models.Model):
    """社区表, 关联city城市表"""
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name="city_comm",
        verbose_name="城市外键"
    )
    name = models.CharField(max_length=64, verbose_name="社区名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    edit_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")


class User(models.Model):
    """用户信息表，与carport车位表是多对多的关系"""
    login_name = models.CharField(max_length=64, verbose_name="登录账号")
    login_passwd = models.CharField(max_length=128, verbose_name="登录密码")
    name = models.CharField(max_length=32, null=True, default=None, verbose_name="用户昵称")
    email = models.EmailField(verbose_name="用户邮箱")
    phone = models.IntegerField(max_length=11, verbose_name="手机号码", null=True, default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    edit_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")


class Sale_Status_Choice(Enum):
    on_sale = 0  # 挂牌中
    saled = 1  # 已完成
    undo = 2  # 撤销


class Sale_Type_Choice(Enum):
    rant = 0  # '出租',
    sales = 1  # '出售'


class Carport(models.Model):
    """车位信息表, 与user用户表示多对多的关系"""
    title = models.CharField(max_length=128, verbose_name="标题")
    city_area = models.CharField(max_length=128, verbose_name="区域")
    address = models.CharField(max_length=256, verbose_name="详细地址")
    in_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="租金成本价")
    rant_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="租金价")
    rant_unit = models.CharField(max_length=64, verbose_name="租金单位")
    lease = models.CharField(max_length=64, verbose_name="租期")
    area = models.IntegerField()
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comm_carport",
        verbose_name="社区外键"
    )
    type = models.IntegerField(
        choices=[(tag.name, tag.value) for tag in Sale_Type_Choice],
        default=0
    )
    status = models.IntegerField(
        [(tag.name, tag.value) for tag in Sale_Status_Choice],
        default=0
    )
    describe = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    edit_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    carport_user = models.ManyToManyField(User, through="Carport_User")


class Carport_Msg_Choice(Enum):
    release = 0  # "发布车位"
    lease = 1  # "租车位"


class Carport_User(models.Model):
    """自定义carport_user多对多关联表, 并标记信息类型"""
    carport = models.ForeignKey(Carport, on_delete=models.CASCADE, related_name="carport_msg")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_msg")
    type = models.IntegerField(
        choices=[(tag.name, tag.value) for tag in Carport_Msg_Choice],
        default=1
    )
