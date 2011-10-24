# -*- coding: utf-8 -*
from django.db import models

<<<<<<< HEAD
HurryLevel = (
	('M','immediately'),
	('A','At once'),
	('B','Hurry'),
	('C','Normal'),
	('N','Whenever'),
)

=======
>>>>>>> parent of 228915b... closes #5
class Needs(models.Model):
	pub_date = models.DateTimeField('date published')
	pay_by_school = models.BooleanField() #hoge
	price = models.CharField(max_length=20)
	shop = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
<<<<<<< HEAD
	properties = models.CharField(max_length=140)
	adress = models.CharField(max_length=140)
	level = models.CharField(max_length=1,choices=HurryLevel)
	url = models.CharField(max_length=200)
=======
	properties models.CharField(max_length=140)#型番や属性(抵抗値とか)
#	-種別
	adress = models.CharField(max_length=140)#登録者のメールアドレス
#	-至急度別の数
	url = models.CharField(max_length=200)#注意書きや解説記事へのリファレンス
>>>>>>> parent of 228915b... closes #5
	def __unicode__(self):
		return self.question

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()
	def __unicode__(self):
		return self.choice
