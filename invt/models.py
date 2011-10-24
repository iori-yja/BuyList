from django.db import models

class Needs(models.Model):
	pub_date = models.DateTimeField('date published')
#	-部費か否か
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
	pay_by_school = models.BooleanField()
	price = models.CharField(max_length=20)
	shop = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
#	-型番もしくは属性(抵抗値やワット数など)
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
