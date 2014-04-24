# -*- coding:utf-8 -*-

from django.forms import ModelForm
from apps import forms
from apps.office.cars.models import Cars, UseRecord, CostRecord


class CarsForm(ModelForm):

    class Meta:
        model =  Cars
        exclude = ('un_id','adder','addtime', 'adderip', 'status')

    def clean(self):
        cleaned_data = super(CarsForm, self).clean()
        car = cleaned_data.get('car')
        site = cleaned_data.get('site')
        company = cleaned_data.get('company')
        person = cleaned_data.get('person')
        if car is None:
            self._errors["car"] = self.error_class([u'请输入车牌号!'])
        if site is None:
            self._errors["site"] = self.error_class([u'请输入车辆座位数!'])
        if company is None:
            self._errors["company"] = self.error_class([u'请输入车辆投保的保险公司名称!'])
        if person is None:
            self._errors["person"] = self.error_class([u'请输入经办人姓名!'])
        return cleaned_data

class UseRecordForm(ModelForm):

    class Meta:
        model = UseRecord
        exclude = ('un_id','adder','addtime', 'adderip')

class CostRecordForm(ModelForm):

    class Meta:
        model = CostRecord
        stype = forms.CheckboxSelectMultiple()
        fields=('car','stype','stime','cost','user','remarks','depart')
        exclude = ('un_id','adder','addtime', 'adderip')