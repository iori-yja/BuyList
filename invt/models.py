# -*- coding: utf-8 -*-
from django.db import models

class Needs(models.Model):
	pub_date = models.DateTimeField('date published')
	pay_by_school = models.BooleanField()#部費か?
	price = models.CharField(max_length=20)
	shop = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
	properties = models.CharField(max_length=140)#型番や属性(抵抗値とか)
#	-種別
	adress = models.CharField(max_length=140)#登録者のメールアドレス
#	-至急度別の数
	Mnum = models.IntegerField('How we need it tomorrow')
	Inum = models.IntegerField('How we need it immediately')
	Hnum = models.IntegerField('Hurry')
	Nnum = models.IntegerField('Normal')
	Wnum = models.IntegerField('whenever')
	url = models.CharField(max_length=200)#注意書きや解説記事へのリファレンス
