# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm

#parts_type = (
#	('st','Subtrace'),#基板
#	('wr','wiring'),#はんだ,錫メッキ線,ポリウレタン線
#	('cn','connector'),#ピン,コネクタ,ケーブル
#	('rt','resistor'),#抵抗
#	('ss','sensor'),#センサ
#	('ld','LED'),
#	('ic','IC'),#三端子レギュレータ,オペアンプ,モータドライバ,AND,OR,PIC
#	('fx','fixer'),#スペーサ,ナット,ねじ
#	('mt','material'),#車体材料,10[Y/cm^3]
#	('ot','otherparts'),#Other parts
#)

decent_spp = (
	('wiring','wiring'),
	('resistor','resistor'),
	('capacitor','capacitor'),
	('motor','motor'),
	('mcu','mcu'),
	('material','material'),
	('motor_driver','motor_driver'),
	('switch','switch'),
	('regulater','regulater'),
	('subtrace','subtrace'),
	('connector','connector'),
	('other','otherelectorical parts'),
)

class Part (models.Model):
	name = models.CharField(max_length=20)
	price = models.IntegerField()
	shop = models.CharField(max_length=20)
	adress = models.EmailField(max_length=140,blank=True)#登録者のメールアドレス
	url = models.CharField(max_length=400,blank=True)#注意書きや解説記事へのリファレンス
	pay_by_school = models.BooleanField()#部費か?
	def __unicode__(self):
		return self.name

class Resistor(Part):
	ohm  = models.IntegerField()
	watt = models.IntegerField()
class Wiring(Part):
	partype = models.CharField(max_length=20)
	phi     = models.IntegerField()
	length  = models.IntegerField()
class Capasitor(Part):
	partype = models.CharField(max_length=20,blank=True)
	volt    = models.IntegerField()
	farad   = models.IntegerField()
class Motor(Part):
	partype = models.CharField(max_length=200)
class Mcu(Part):
	partype = models.CharField(max_length=30)
class Material(Part):
	partype = models.CharField(max_length=200)
class Motor_driver(Part):
	partype = models.CharField(max_length=20)
class Switch(Part):
	partype = models.CharField(max_length=20)
class Requlater(Part):
	partnum = models.CharField(max_length=20)
	volt    = models.IntegerField(blank=True)
class Subtrace(Part):
	bdsize  = models.CharField(max_length=20)
	partype = models.CharField(max_length=20)
class Connector(Part):
	partype = models.CharField(max_length=200)
class Other(Part):
	partype = models.CharField(max_length=200)

class Req(models.Model):
	partype = models.ForeignKey(Part)
	pub_date = models.DateTimeField(auto_now=True,auto_now_add=True)
	up_date = models.DateTimeField(auto_now=True,auto_now_add=False)
	#至急度別の数
	Mnum = models.IntegerField('Immediately')
	Anum = models.IntegerField('Hurry')
	Bnum = models.IntegerField('Normal')
	Cnum = models.IntegerField('whenever')
	def allneeds(self):
		return self.Mnum+self.Anum+self.Bnum+self.Cnum
	def hurryup(self):
		return self.Mnum+self.Bnum
	def hurrycost(self):
		return self.price*(self.hurryup())

class Butsutsu(ModelForm):
	user = models.EmailField(max_length=140)
	post = models.TextField()
class PartForm(ModelForm):
	class Meta:
		model = Part
class ReqForm(ModelForm):
	class Meta:
		model = Req
		exclude = ('up_date','pub_date',)

from django.contrib import admin
admin.site.register(Part)
admin.site.register(Req)
admin.site.register(Resistor)
admin.site.register(Wiring)
admin.site.register(Capasitor)
admin.site.register(Motor)
admin.site.register(Mcu)
admin.site.register(Material)
admin.site.register(Motor_driver)
admin.site.register(Switch)
admin.site.register(Requlater)
admin.site.register(Subtrace)
admin.site.register(Connector)
admin.site.register(Other)
