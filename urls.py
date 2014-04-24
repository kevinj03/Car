# -*- coding:utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^list/$', 'apps.office.cars.views.car_list'), #车辆信息列表 /office/cars/list/
    (r'^add', 'apps.office.cars.views.car_add'), #添加车辆信息/office/cars/add
    (r'^edit', 'apps.office.cars.views.car_edit'), #修改车辆信息 /office/cars/edit/
    (r'^dele', 'apps.office.cars.views.car_del'), #删除车辆信息 /office/cars/dele
    #车辆使用
    (r'^ulist/$', 'apps.office.cars.views.userecord_list'), #车辆使用记录 /office/cars/ulist/
    (r'^uedit', 'apps.office.cars.views.userecord_edit'), #增加、修改使用记录 /office/cars/uedit
    (r'^sel', 'apps.office.cars.views.sel'),#列表中级联查找/office/cars/sel
    #费用记录
    (r'^clist/$', 'apps.office.cars.views.costrecord_list'), #费用记录浏览 /office/cars/clist/
    (r'^cedit', 'apps.office.cars.views.costrecord_edit'), #增加、修改使用记录 /office/cars/cedit
     (r'^gtime/$', 'apps.office.cars.views.gtime'),
)
