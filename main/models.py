from django.db import models
from .storage import ImageStorage
from django.utils.html import strip_tags
from datetime import datetime,timedelta

class Article(models.Model):
	"""博客内容"""
	title = models.CharField(max_length=100,null=True)
	html_file = models.FileField(upload_to='markdown/',null=True,storage=ImageStorage())
	content = models.TextField(max_length=10000,null=True,blank=True)
	time = models.DateTimeField('发表时间',auto_now_add=True)
	views = models.PositiveIntegerField(default=0)
	abstract = models.CharField('摘要',max_length=60,null=True,blank=True)
	cover = models.ImageField('封面',upload_to='article_img',storage=ImageStorage())


	def viewIncrease(self,request,article_id):
		article = Article.objects.get(id=article_id)
		try:
			record = IpRecord.objects.get(ip=request.META['REMOTE_ADDR'],article=article)
		except:
			record = None
		if record:
			last = datetime.now() - record.time
			expiration = timedelta(seconds = 60 * 5)
			if last > expiration:
				self.views += 1
				self.save(update_fields=['views'])
				record.time = datetime.now()
				record.save(update_fields=['time'])
			else:
				record.time = datetime.now()
				record.save(update_fields=['time'])

		else:
			record = IpRecord(ip=request.META['REMOTE_ADDR'],article=article,time=datetime.now())
			record.save()
			self.views += 1
			self.save(update_fields=['views'])

	def __str__(self):
		return self.title


class Album(models.Model):
	photo = models.ImageField('照片',upload_to='album',storage=ImageStorage())
	time = models.DateTimeField('时间',auto_now_add=True)
	description = models.CharField(max_length=100,null=True,blank=True)

class AboutMe(models.Model):
	title = models.CharField(max_length=100)
	abstract = models.CharField(max_length=100)
	html_file = models.FileField(upload_to="markdown/",null=True,storage=ImageStorage())
	content = models.TextField(max_length=10000,null=True,blank=True)
	time = models.DateTimeField('时间',auto_now_add=True)
	cover = models.ImageField('封面',upload_to='aboutMe',storage=ImageStorage())

class Diary(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	html_file = models.FileField(upload_to="markdown/",null=True,storage=ImageStorage())
	content = models.TextField(max_length=10000,null=True,blank=True)

class IpRecord(models.Model):
	ip = models.CharField(max_length=18)
	article = models.ForeignKey(Article)
	time = models.DateTimeField()
		
				