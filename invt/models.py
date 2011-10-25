# -*- coding: utf-8 -*-
from django.db import models

parts_type = (
	('st','Subtrace'),#基板
	('wr','wiring'),#はんだ,錫メッキ線,ポリウレタン線
	('cn','connector'),#ピン,コネクタ,ケーブル
	('rt','resistor'),#抵抗
	('ss','sensor'),#センサ
	('ld','LED'),
	('ic','IC'),#三端子レギュレータ,オペアンプ,モータドライバ,AND,OR,PIC
	('fx','fixer'),#スペーサ,ナット,ねじ
	('mt','material'),#車体材料,10[Y/cm^3]
	('ot','otherparts'),#Other parts
)

class Needs(models.Model):
	pub_date = models.DateTimeField('date published')
	up_date = models.DateTimeField('date updated')
	pay_by_school = models.BooleanField()#部費か?
	price = models.CharField(max_length=20)
	shop = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
	properties = models.CharField(max_length=140)#型番や属性(抵抗値とか)
	partype = models.CharField(max_length=2,choices=parts_type)#種別
	adress = models.CharField(max_length=140)#登録者のメールアドレス
	#至急度別の数
	Mnum = models.IntegerField('Immediately')
	Hnum = models.IntegerField('Hurry')
	Nnum = models.IntegerField('Normal')
	Wnum = models.IntegerField('whenever')
	url = models.CharField(max_length=400)#注意書きや解説記事へのリファレンス

