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


class Sp (models.Model):
	decent = models.CharField(max_length=10,choices=decent_spp)
	def __unicode__(self):
		return self.decent
##	def sptype(self):
#		if self.decent == 'wiring':
#			return 'wiring'
#		elif self.decent == 'resistor':
#			return 'resistor'
#		elif self.decent ==  '':
#			return 'wiring'
#		elif self.decent ==  '':
#			return 'wiring'
#		elif self.decent ==  '':
#			return 'wiring'
#		elif self.decent ==  '':
#			return 'wiring'
#		elif self.decent ==  '':
#			return 'wiring'
#		elif self.decent ==  '':
#			return 'wiring'
#		elif self.decent ==  '':
#			return 'wiring'
#		elif self.decent ==  '':
#			return 'wiring'

class Part (models.Model):
	species = models.ForeignKey(Sp)
	name = models.CharField(max_length=20)
	properties = models.CharField(max_length=140)#型番や属性(抵抗値とか)
	price = models.IntegerField()
	shop = models.CharField(max_length=20)
	adress = models.EmailField(max_length=140,blank=True)#登録者のメールアドレス
	url = models.CharField(max_length=400,blank=True)#注意書きや解説記事へのリファレンス
	pay_by_school = models.BooleanField()#部費か?
	def __unicode__(self):
		return self.name

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
admin.site.register(Sp)

