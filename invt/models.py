from django.db import models

class Needs(models.Model):
	pub_date = models.DateTimeField('date published')
	pay_by_school = models.BooleanField() #部費か？
	price = models.CharField(max_length=20)#値段
	shop = models.CharField(max_length=20)#どこで買うか
	name = models.CharField(max_length=20)
#	-型番もしくは属性(抵抗値やワット数など)
	properties models.CharField(max_length=140)
#	-種別
#	-登録者
#	-至急度別の数
#	-注意書きや解説記事へのリファレンス
	url = models.CharField(max_length=200)
	def __unicode__(self):
		return self.question

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choice = models.CharField(max_length=200)
	votes = models.IntegerField()
	def __unicode__(self):
		return self.choice
