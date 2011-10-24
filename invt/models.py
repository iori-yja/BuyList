from django.db import models

HurryLevel = (
	('M','immediately'),
	('A','At once'),
	('B','Hurry'),
	('C','Normal'),
	('N','Whenever'),
)


class Needs(models.Model):
	pub_date = models.DateTimeField('date published')
	pay_by_school = models.BooleanField() #部費か？
	price = models.CharField(max_length=20)#値段
	shop = models.CharField(max_length=20)#どこで買うか
	name = models.CharField(max_length=20)
	properties models.CharField(max_length=140)#型番や属性(抵抗値とか)
#	-種別
	adress = models.CharField(max_length=140)#登録者のメールアドレス
#	-至急度別の数
	level = models.CharField(max_length=1,choices=HurryLevel)
	url = models.CharField(max_length=200)#注意書きや解説記事へのリファレンス
	def __unicode__(self):
		return self.name

