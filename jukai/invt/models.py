# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
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

auxiliaryunit = (
	('G','G'),
	('M','M'),
	('K','K'),
	('',''),
	('m','m'),
	('u','μ'),
	('p','p'),
)
class news (models.Model):
	#text = models.	fileに実体をもたせるべき
	title = models.CharField(max_length=400)
	pub_date = models.DateTimeField(auto_now=True,auto_now_add=True)
	last_date = models.DateTimeField(auto_now=True,auto_now_add=False)

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
	user = models.ForeignKey(User,related_name='+')
	def __unicode__(self):
		return self.name

##########基板
class Subtrace(Part):
	bdsize  = models.CharField(max_length=20,blank=True)#AとかBとかCとか
	partype = models.CharField(max_length=20,blank=True)#ユニバーサルとかプリント基板とか
	def mkprop(self):
		prop=self.capasitor.partype+"  "+self.capasitor.volt
		return prop
##########配線
class Wiring(Part):
	partype = models.CharField(max_length=20)
	phi     = models.FloatField()
	length  = models.FloatField()
	lensuf  = models.CharField(max_length=2,choices=auxiliaryunit,blank=True)
	def mkprop(self):
		prop=str(self.wiring.phi)+"mm"+u"の"+self.wiring.partype+str(self.wiring.length)+u"m分"
		return prop

##########センサ
class Sensor(Part):###################################################################################
	pass
##########コネクタ
class Connector(Part):
	partype = models.CharField(max_length=200)
	def mkprop(self):
		return self.connector.partype
##########IC
class Regulater(Part):
	partnum = models.CharField(max_length=20)
	volt    = models.DecimalField(max_digits=4,decimal_places=3,blank=True)
	def mkprop(self):
		if self.regulater.volt == None:
			voltmsg=u"電圧未記入"
		else:
			voltmsg="("+str(self.regulater.volt)+")"
		prop=u"型番"+self.regulater.farad+u"の"+u"レギュレータ"+voltmsg
		return prop
class Motor_driver(Part):
	partype = models.CharField(max_length=20)
	def mkprop(self):
		return self.motor_driver.partype
class Mcu(Part):
	partype = models.CharField(max_length=30)
	def mkprop(self):
		return self.mcu.partype
##########回路素子
class Resistor(Part):
	ohm  = models.FloatField()
	ohmsuf = models.CharField(max_length=2,choices=auxiliaryunit,blank=True)
	watt = models.CharField(max_length=4) #next issue is here
	def mkprop(self):
		prop=str(self.resistor.ohm)+str(self.resistor.ohmsuf)+u"Ω  "+str(self.resistor.watt)+"W"
		return prop

class Capasitor(Part):
	partype = models.CharField(max_length=20,blank=True)
	volt    = models.IntegerField()
	farad   = models.FloatField()
	farsuf  = models.CharField(max_length=2,choices=auxiliaryunit,blank=True)
	def mkprop(self):
		prop=str(self.capasitor.farad)+self.capasitor.farsuf+"F"+u"の"+self.capasitor.partype+str(self.capasitor.volt)
		return prop
class Otherelement(Part):#####################################################################################
	pass

##########工具###################################################################################
class Tool(Part):
	partype = models.CharField(max_length=20)
	def mkprop(self):
		return self.tool.partype

##########モータ
class Motor(Part):
	partype = models.CharField(max_length=200)
	def mkprop(self):
		return self.motor.partype
##########スイッチ
class Switch(Part):
	partype = models.CharField(max_length=20)
	def mkprop(self):
		return self.switch.partype
##########車体
class Material(Part):
	partype = models.CharField(max_length=200)
	def mkprop(self):
		return self.material.partype
##########その他
class Other(Part):
	partype = models.CharField(max_length=200)
	def mkprop(self):
		return self.other.partype

class Req(models.Model):
	partype = models.ForeignKey(Part)
	pub_date = models.DateTimeField(auto_now=True,auto_now_add=True)
	up_date = models.DateTimeField(auto_now=True,auto_now_add=False)
	user = models.ForeignKey(User)
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
		exclude = ('user',)
class ReqForm(ModelForm):
	class Meta:
		model = Req
		exclude = ('partype','up_date','pub_date',)

class ResistorForm(ModelForm):
	class Meta:
		model = Resistor
		exclude = ('user',)
class WiringForm(ModelForm):
	class Meta:
		model = Wiring
		exclude = ('user',)
class CapasitorForm(ModelForm):
	class Meta:
		model = Capasitor
		exclude = ('user',)
class MotorForm(ModelForm):
	class Meta:
		model = Motor
		exclude = ('user',)
class McuForm(ModelForm):
	class Meta:
		model = Mcu
		exclude = ('user',)
class MaterialForm(ModelForm):
	class Meta:
		model = Material
		exclude = ('user',)
class Motor_driverForm(ModelForm):
	class Meta:
		model = Motor_driver
		exclude = ('user',)
class SwitchForm(ModelForm):
	class Meta:
		model = Switch
		exclude = ('user',)
class RegulaterForm(ModelForm):
	class Meta:
		model = Regulater
		exclude = ('user',)
class SubtraceForm(ModelForm):
	class Meta:
		model = Subtrace
		exclude = ('user',)
class ConnectorForm(ModelForm):
	class Meta:
		model = Connector
		exclude = ('user',)
class OtherForm(ModelForm):
	class Meta:
		model = Other
		exclude = ('user',)

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
admin.site.register(Regulater)
admin.site.register(Subtrace)
admin.site.register(Connector)
admin.site.register(Other)
