# -*- coding:utf-8 -*-

from django.db import models
from apps import utils, Departs
from apps.models import Users


class Cars(models.Model):
    """
    描述：车辆信息模型
    作者：凯伦kevin
    """

    STATU_CHOICE = (
        (0, '空闲中'),
        (1, '使用中'),
    )

    un_id = models.IntegerField(u'机构编号', db_column='un_id', blank=True, null=True) #机构编号，由session写入
    car = models.CharField(u'车牌号', max_length=10)
    brand = models.CharField(u'车辆品牌',max_length=20, blank=True, null=True)
    site = models.IntegerField(u'座位数', max_length=2, blank=True, null=True)
    path = models.ImageField(u'车辆图片',upload_to='/', blank=True, null=True)
    company = models.CharField(u'保险公司', max_length=30, blank=True, null=True)
    time = models.DateTimeField(u'投保时间', blank=True, null=True)
    person = models.CharField(u'经办人', max_length=5, blank=True, null=True)
    statu = models.IntegerField(u'使用状态',choices=STATU_CHOICE, blank=True, null=True)

    adder = models.CharField(u'添加人', max_length = 100) #添加人(id)姓名
    #系统保留信息
    addtime = models.DateTimeField(auto_now_add = True) #添加时间
    adderip = models.IPAddressField(default = u'0.0.0.0') #添加人当前IP地址
    status  = models.IntegerField(choices = utils.CHOICES_STATUS, default = 200) #状态；0：逻辑删除；200：正常；

    class Meta:
        db_table = 'office_cars'

class UseRecord(models.Model):
    """
    描述：车辆使用记录
    作者：凯伦kevin
    """

    user = models.ForeignKey(Users, verbose_name = u'申请人')
    depart = models.ForeignKey(Departs, verbose_name = u'申请部门')
    car = models.ForeignKey(Cars, verbose_name = u'借用车辆')
    stime = models.DateTimeField(u'借用时间', blank=True, null=True)
    ltime = models.DateTimeField(u'归还时间', blank=True, null=True)
    use = models.CharField(u'用途', blank=True, null=True, max_length=50)
    mileage = models.DecimalField(u'里程', max_digits=12, decimal_places=2, blank=True, null=True)
    oilwear = models.DecimalField(u'油耗', max_digits=12, decimal_places=2, blank=True, null=True)
    remarks = models.CharField(u'备注', blank=True, null=True, max_length=100)

    #系统保留信息
    un_id = models.IntegerField(u'机构编号', db_column='un_id', blank=True, null=True) #机构编号，由session写入
    adder = models.CharField(u'添加人', max_length = 100) #添加人(id)姓名
    addtime = models.DateTimeField(auto_now_add = True) #添加时间

    adderip = models.IPAddressField(default = u'0.0.0.0') #添加人当前IP地址

    class Meta:
        db_table = 'office_userecord'

class CostRecord(models.Model):
    """
    描述：车辆费用记录
    作者：凯伦kevin
    """

    SERVICE_CHOICE = (
        (0, '加油'),
        (1, '维修'),
        (2, '保养'),
        (3, '保险'),
        (4, '其他'),
    )
    car = models.ForeignKey(Cars, verbose_name = u'车辆')
    stype = models.IntegerField(u'服务类型',choices=SERVICE_CHOICE, blank=True, null=True)
    stime = models.DateTimeField(u'时间', blank=True, null=True)
    cost = models.DecimalField(u'费用', max_digits=12, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(Users, verbose_name = u'经办人')
    remarks = models.CharField(u'备注', blank=True, null=True, max_length=100)
    depart = models.ForeignKey(Departs, verbose_name = u'申请部门')
    #系统保留信息
    un_id = models.IntegerField(u'机构编号', db_column='un_id', blank=True, null=True) #机构编号，由session写入
    adder = models.CharField(u'添加人', max_length = 100) #添加人(id)姓名
    addtime = models.DateTimeField(auto_now_add = True) #添加时间
    adderip = models.IPAddressField(default = u'0.0.0.0') #添加人当前IP地址

    class Meta:
        db_table = 'office_costrecord'
