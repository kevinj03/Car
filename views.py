# -*- coding:utf-8 -*-
from django.db.models import Q

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
import time
from apps import Units, Departs
from apps.models import MineManager
from apps.office.cars.forms import CarsForm, UseRecordForm, CostRecordForm
from apps.office.cars.models import Cars, UseRecord, CostRecord
from apps.utils import upload


def car_list(request):
    """
    描述：车辆信息列表
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 1122 ##来源application
    #验证是否登录
    try:
        Mine = request.session['mine_object'] ## 取当前用户登录的对象 未登录取值为空对对象
        Mine.reload()
    except:
        Mine = MineManager()

    opera = Mine.auth(EVENT_RIGHT) #系统开发功能的操作，必须是超级管理员

    if type(opera) == type(''):
        return HttpResponse(opera)

    try:
        querys = Cars.objects.filter(un_id=Mine.Unit.id, status=200)
    except Exception,e:
        pass
    print  request.GET.get('id', '')
    keytype = request.GET.get('keytype', '')
    keyword = request.GET.get('keyword', '')
    statu = request.GET.get('statu', '')

    if keyword != '':
        if keytype == '1':
            querys = querys.filter(car__icontains=keyword)
        elif keytype == '2':
            querys = querys.filter(brand__icontains=keyword)
        elif keytype == '3':
            querys = querys.filter(site__icontains=keyword)

    if statu != '':
        querys = querys.filter(statu = int(statu))


    search={}
    search['keytype'] = keytype
    search['keyword'] = keyword
    search['statu'] = statu

    context = {
        'querys': querys,
        'request': request,
        'opera':opera,
        'search':search,
    }

    return render_to_response('cars_list.html', context)

def car_add(request):
    """
    描述：添加车辆信息
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 873 ##来源application
    #验证是否登录
    try:
        Mine = request.session['mine_object'] ## 取当前用户登录的对象 未登录取值为空对对象
        Mine.reload()
    except:
        Mine = MineManager()

    opera = Mine.auth(EVENT_RIGHT) #系统开发功能的操作，必须是超级管理员

    if type(opera) == type(''):
        return HttpResponse(opera)

    units = Units.objects.all()

    if request.method == 'POST':
        car = request.POST['car']
        brand = request.POST['brand']
        site = request.POST['site']
        time = request.POST['time']
        person = request.POST['person']
        un_id = request.POST['unit']
        statu = request.POST['statu']

        form = CarsForm(request.POST)
        if form.is_valid:
            try:
                #保存提交的文件
                image = request.FILES.get('file', None)
                dir = 'm/pact/'
                newcar = form.save(commit=False)
                if image is not None:
                    path = upload(image, dir)
                else:
                    path = None
                newcar.car = car
                newcar.brand = brand
                newcar.site = site
                newcar.path = path
                newcar.time = time
                newcar.person = person
                newcar.un_id = un_id
                newcar.statu = statu
                newcar.adder = Mine.to_adder() #添加人(id)姓名
                newcar.adderip = Mine.get_ipaddress(request)
                newcar.save()

                OPERA_ITEMS = []
                OPERA_ITEMS.append('<a href="%s">%s</a>'%('/office/cars/add', u'继续添加'))
                RePath = '<a href="%s">%s</a>' %('/office/cars/list/', u'返回列表')
                return render_to_response('xopera.html', {'OPERA_ITEMS':OPERA_ITEMS, 'RePath':RePath})
            except Exception, e:
                return HttpResponseRedirect('/message/dialog/error-0001')
        else:
            return HttpResponseRedirect('/message/dialog/error-0002')
    else:
        form = CarsForm()

        #给choices设置初始值
    form.base_fields['statu'].choices[0] = ('', u'请选择')

    context = {
        'units': units,
        'form': form,
        'opera':opera,
        }

    return render_to_response('cars_add.html', context)

def car_edit(request):
    """
    描述：修改车辆信息
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 874 ##来源application
    #验证是否登录
    try:
        Mine = request.session['mine_object'] ## 取当前用户登录的对象 未登录取值为空对对象
        Mine.reload()
    except:
        Mine = MineManager()

    opera = Mine.auth(EVENT_RIGHT) #系统开发功能的操作，必须是超级管理员

    if type(opera) == type(''):
        return HttpResponse(opera)

    id = request.GET.get('id',None)
    units = Units.objects.all()
    instance = Cars.objects.get(id=id)

    if request.method == 'POST':
        car = request.POST['car']
        brand = request.POST['brand']
        site = request.POST['site']
        time = request.POST['time']
        person = request.POST['person']
        un_id = request.POST['unit']
        statu = request.POST['statu']

        form = CarsForm(request.POST, instance = instance)
        if form.is_valid:
            try:
                image = request.FILES.get('file', None)
                dir = 'm/pact/'
                newcar = form.save(commit=False)
                if image is not None:
                    path = upload(image, dir)
                else:
                    path = None
                newcar.car = car
                newcar.brand = brand
                newcar.site = site
                newcar.path = path
                newcar.time = time
                newcar.person = person
                newcar.un_id = un_id
                newcar.statu = statu
                newcar.adder = Mine.to_adder() #添加人(id)姓名
                newcar.adderip = Mine.get_ipaddress(request)
                newcar.save()

                OPERA_ITEMS = []
                OPERA_ITEMS.append('<a href="%s">%s</a>'%('/office/cars/edit?id=%s'%id, u'继续修改'))
                RePath = '<a href="%s">%s</a>' %('/office/cars/list/', u'返回列表')
                return render_to_response('xopera.html', {'OPERA_ITEMS':OPERA_ITEMS, 'RePath':RePath})
            except Exception, e:
                return HttpResponseRedirect('/message/dialog/error-0001')
        else:
            return HttpResponseRedirect('/message/dialog/error-0002')
    else:
        form = CarsForm(instance = instance)

        #给choices设置初始值
    form.base_fields['statu'].choices[0] = ('', u'请选择')
    unitid = instance.un_id
    context = {
        'units' : units,
        'form' : form,
        'opera' : opera,
        'unitid' : unitid,
        'instance' : instance,
        }

    return render_to_response('cars_edit.html', context)

def car_del(request):
    """
    描述：删除车辆信息
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 875 ##来源application
    #验证是否登录
    try:
        Mine = request.session['mine_object'] ## 取当前用户登录的对象 未登录取值为空对对象
        Mine.reload()
    except:
        Mine = MineManager()

    opera = Mine.auth(EVENT_RIGHT) #系统开发功能的操作，必须是超级管理员

    if type(opera) == type(''):
        return HttpResponse(opera)

    if request.method == 'POST':
        try:
            ids = request.POST.getlist('id')
            Cars.objects.filter(id__in = ids,status = 200).update(status = 0)
            RePath = '<a href="%s">%s</a>' %('/office/cars/list/', u'返回列表')
            return render_to_response('xopera.html', {'RePath':RePath})
        except:
            return HttpResponseRedirect('/message/dialog/error-0001')

    ids = request.GET['id']
    cars = Cars.objects.filter(id__in=ids.split(','),status = 200)

    context={
        'cars': cars,
        'request': request,
        }
    return render_to_response('cars_del.html', context)

def sel(request):
    """
    描述：在车辆使用列表中两个下拉菜单关联方法
    作者：凯伦kevin
    """
    try:
        Mine = request.session['mine_object'] ## 取当前用户登录的对象 未登录取值为空对对象
        Mine.reload()
    except:
        Mine = MineManager()

    keytype = request.POST.get('keytype', '')

    if keytype == '1':
        departs = Departs.objects.filter(status=200, Unit_id__in=Mine.get_unit(format='ID_LIST')).order_by('orders')
        lst = []
        for dep in departs:
            try:
                lst.append({'id':dep.id, 'name':dep.name,'uname':dep.Unit.name[:1]})
            except:
                pass
    elif keytype == '2':
        cars = Cars.objects.filter(status=200, un_id=Mine.Unit.id)
        lst = []
        for c in cars:
            try:
                lst.append({'id':c.id, 'name':c.car})
            except:
                pass

    json = simplejson.dumps(lst)
    return HttpResponse(json)

def userecord_list(request):
    """
    描述：车辆使用记录列表
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 1124 ##来源application
    #验证是否登录
    try:
        Mine = request.session['mine_object'] ## 取当前用户登录的对象 未登录取值为空对对象
        Mine.reload()
    except:
        Mine = MineManager()

    opera = Mine.auth(EVENT_RIGHT) #系统开发功能的操作，必须是超级管理员

    if type(opera) == type(''):
        return HttpResponse(opera)

    try:
        querys = UseRecord.objects.filter(un_id=Mine.Unit.id).order_by('-stime')
    except Exception,e:
        pass

    keytype = request.GET.get('keytype', '')
    keyword = request.GET.get('keyword', '')

    if keyword != '':
        if keytype == '1':
                querys = querys.filter(depart=keyword)
        elif keytype == '2':
                querys = querys.filter(car=keyword)

    search={}
    search['keytype'] = keytype
    search['keyword'] = keyword

    context={
        'querys': querys,
        'opera': opera,
        'search': search,
        'request': request,
        }
    return render_to_response('userecord_list.html', context)

def userecord_edit(request):
    """
    描述：添加、修改车辆使用记录
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 1125 ##来源application

    EVENT_TYPE_INSERT = True
    instance = None

    id = request.GET.get('id',None)

    if id is not None: #表示修改操作
        instance = get_object_or_404(UseRecord, pk=id)
        EVENT_RIGHT = 1126
        EVENT_TYPE_INSERT = False
        #验证是否登录
    try:
        Mine = request.session['mine_object']
        Mine.reload()
    except:
        Mine = MineManager()

    opera = Mine.auth(EVENT_RIGHT)

    if type(opera) == type(''):
        return HttpResponse(opera)

        ###权限验证结束###

    departs = Departs.objects.filter(status=200, Unit_id__in=Mine.get_unit(format='ID_LIST')).order_by('orders')
    carid=UseRecord.objects.filter(ltime__isnull=True).values_list('car')
    cars = Cars.objects.filter(status=200, un_id=Mine.Unit.id).exclude(id__in=carid)

    if request.method == 'POST':
        depart = request.POST.get('depart',None)
        user = request.POST.get('user',None)
        car = request.POST.get('car',None)
        stime = request.POST.get('stime',None)
        ltime = request.POST.get('ltime',None)
        use = request.POST.get('use',None)
        mileage = request.POST.get('mileage',None)
        oilwear = request.POST.get('oilwear',None)
        remarks = request.POST.get('remarks',None)
        OPERA_ITEMS = []
        if id:
            ur = UseRecord.objects.get(id=id)
            ur.ltime = ltime
            ur.mileage = mileage
            ur.oilwear = oilwear
            ur.remarks = remarks
            ur.un_id = Mine.Unit.id
            ur.adder = Mine.to_adder() #添加人(id)姓名
            ur.adderip = Mine.get_ipaddress(request)
            ltime_timetuple=time.strptime(ur.ltime,'%Y-%m-%d %H:%M:%S')
            stime_time=time.strftime('%Y-%m-%d %H:%M:%S',ur.stime.timetuple())
            stime_timetuple=time.strptime(stime_time,'%Y-%m-%d %H:%M:%S')
            if(time.mktime(ltime_timetuple)<time.mktime(stime_timetuple)):
                return HttpResponseRedirect('/message/dialog/error-0001')
            ur.save()
            OPERA_ITEMS.append('<a href="%s">%s</a>'%('/office/cars/uedit?id=%s'%id, u'继续修改'))
            RePath = '<a href="%s">%s</a>' %('/office/cars/ulist/', u'返回列表')
            return render_to_response('xopera.html', {'OPERA_ITEMS':OPERA_ITEMS, 'RePath':RePath})
        form = UseRecordForm(request.POST, instance = instance)
        if form.is_valid:
            try:
                ur = form.save(commit=False)
                ur.depart_id = depart
                ur.user_id = user
                ur.car_id = car
                ur.stime = stime
                #ur.ltime = ltime
                ur.use = use
                #ur.mileage = mileage
                #ur.oilwear = oilwear
                ur.remarks = remarks
                ur.un_id = Mine.Unit.id
                ur.adder = Mine.to_adder() #添加人(id)姓名
                ur.adderip = Mine.get_ipaddress(request)
                ur.save()
                OPERA_ITEMS = []
                OPERA_ITEMS.append('<a href="%s">%s</a>'%('/office/cars/uedit', u'继续添加'))
                RePath = '<a href="%s">%s</a>' %('/office/cars/ulist/', u'返回列表')
                return render_to_response('xopera.html', {'OPERA_ITEMS':OPERA_ITEMS, 'RePath':RePath})
            except Exception, e:
                return HttpResponseRedirect('/message/dialog/error-0001')
        else:
            return HttpResponseRedirect('/message/dialog/error-0002')
    else:
        form = UseRecordForm(instance = instance)

    context={
        'departs': departs,
        'form': form,
        'cars': cars,
        'opera': opera,
        }
    return render_to_response('userecord_edit.html', context)

def costrecord_list(request):
    """
    描述：费用记录列表
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 1178 ##来源application
    #验证是否登录
    try:
        Mine = request.session['mine_object'] ## 取当前用户登录的对象 未登录取值为空对对象
        Mine.reload()
    except:
        Mine = MineManager()
    print  request.GET.get('id', '')

    opera = Mine.auth(EVENT_RIGHT) #系统开发功能的操作，必须是超级管理员

    if type(opera) == type(''):
        return HttpResponse(opera)

    try:
        querys = CostRecord.objects.filter(un_id=Mine.Unit.id).order_by('-addtime')
    except Exception,e:
        pass

    keytype = request.GET.get('keytype', '')
    keyword = request.GET.get('keyword', '')

    if keyword != '':
        if keytype == '1':
                querys = querys.filter(depart=keyword)
        elif keytype == '2':
                querys = querys.filter(car=keyword)

    search={}
    search['keytype'] = keytype
    search['keyword'] = keyword

    context={
        'querys': querys,
        'opera': opera,
        'search': search,
        'request': request,
        }
    return render_to_response('costrecord_list.html', context)

def costrecord_edit(request):
    """
    描述：添加、修改费用记录
    作者：凯伦kevin
    参数 : 无
    返回 : 无
    """
    #当前操作对应的权限
    EVENT_RIGHT = 1128 ##来源application

    EVENT_TYPE_INSERT = True
    instance = None

    id = request.GET.get('id',None)

    if id is not None: #表示修改操作
        instance = get_object_or_404(CostRecord, pk=id)
        EVENT_RIGHT = 1129
        EVENT_TYPE_INSERT = False
        #验证是否登录
    try:
        Mine = request.session['mine_object']
        Mine.reload()
    except:
        Mine = MineManager()

    opera = Mine.auth(EVENT_RIGHT)

    if type(opera) == type(''):
        return HttpResponse(opera)

        ###权限验证结束###

    departs = Departs.objects.filter(status=200, Unit_id__in=Mine.get_unit(format='ID_LIST')).order_by('orders')
    cars = Cars.objects.filter(status=200, un_id=Mine.Unit.id)
    if request.method == 'POST':
        user = request.POST.get('user',None)
        stype = request.POST.get('stype',None)
        stime = request.POST.get('stime',None)
        car = request.POST.get('car',None)
        cost = request.POST.get('cost',None)
        remarks = request.POST.get('cost',None)
        depart = request.POST.get('depart',None)
        OPERA_ITEMS = []
        if id:
            cr = CostRecord.objects.get(id=id)
            cr.user_id = user
            cr.depart_id = depart
            cr.stype = stype
            cr.stime = stime
            cr.car_id = car
            cr.cost = cost
            cr.remarks = remarks
            cr.un_id = Mine.Unit.id
            cr.adder = Mine.to_adder() #添加人(id)姓名
            cr.adderip = Mine.get_ipaddress(request)
            cr.save()
            OPERA_ITEMS.append('<a href="%s">%s</a>'%('/office/cars/cedit?id=%s'%id, u'继续修改'))
            RePath = '<a href="%s">%s</a>' %('/office/cars/clist/', u'返回列表')
            return render_to_response('xopera.html', {'OPERA_ITEMS':OPERA_ITEMS, 'RePath':RePath})
        form = CostRecordForm(request.POST, instance = instance)
        if form.is_valid:
            try:
                cr = form.save(commit=False)
                cr.user_id = user
                cr.depart_id = depart
                cr.stype = stype
                cr.stime = stime
                cr.car_id = car
                cr.cost = cost
                cr.remarks = remarks
                cr.un_id = Mine.Unit.id
                cr.adder = Mine.to_adder() #添加人(id)姓名
                cr.adderip = Mine.get_ipaddress(request)
                cr.save()
                OPERA_ITEMS = []
                OPERA_ITEMS.append('<a href="%s">%s</a>'%('/office/cars/cedit', u'继续添加'))
                RePath = '<a href="%s">%s</a>' %('/office/cars/clist/', u'返回列表')
                return render_to_response('xopera.html', {'OPERA_ITEMS':OPERA_ITEMS, 'RePath':RePath})
            except Exception, e:
                return HttpResponseRedirect('/message/dialog/error-0001')
        else:
            return HttpResponseRedirect('/message/dialog/error-0002')
    else:
        form = CostRecordForm(instance = instance)

    form.base_fields['stype'].choices[0] = ('', u'请选择')
    context={
        'departs': departs,
        'form': form,
        'cars': cars,
        'opera': opera,
        }
    return render_to_response('costrecord_edit.html', context)
