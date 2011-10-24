# -*- coding: utf-8 -*-
from django.db import models

parts_type = (
	('',''),
	('',''),
	('',''),
	('',''),
	('',''),
)

class Needs(models.Model):
	pub_date = models.DateTimeField('date published')
	up_date = models.DateTimeField('date updated')
	pay_by_school = models.BooleanField()#部費か?
	price = models.CharField(max_length=20)
	shop = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
	properties = models.CharField(max_length=140)#型番や属性(抵抗値とか)
#	-種別
	partype = models.CharField(max_length=2,choises=parts_type)
	adress = models.CharField(max_length=140)#登録者のメールアドレス
#	-至急度別の数
	Mnum = models.IntegerField('Immediately')
	Hnum = models.IntegerField('Hurry')
	Nnum = models.IntegerField('Normal')
	Wnum = models.IntegerField('whenever')
	url = models.CharField(max_length=400)#注意書きや解説記事へのリファレンス

