from django.contrib import admin
from . import models
from .qcloud import QcloudCos
import os
from bs4 import BeautifulSoup
from django.utils.html import strip_tags

def drawHtml(obj, html_url):
	with open(html_url) as f:
		fileContent = f.read()
		bsObj = BeautifulSoup(fileContent)
		content = str(bsObj.find("div",{"id":"write"}))
		obj.content = content[31:][:-6]		#去除最外层div标签
		obj.save()

#文章管理
@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title','time','views')
	list_display_links = ('title','time','views')
	actions = ['delete_selected']
	exclude = ('views','abstract','content')
	verbose_name = '文章管理'
	def delete_selected(self, request, queryset):
		"""覆盖父类的删除方法"""
		for obj in queryset:
			self.deleteFile(obj)
			obj.delete()
	delete_selected.short_description = "删除所选的文章"


	def save_model(self, request, obj, form, change):
		obj.save()
		father_path = os.getcwd()	
		html_url = obj.html_file.url
		drawHtml(obj, father_path + html_url)
		obj.abstract = strip_tags(obj.content)[:54] + "..."
		obj.save()
		#服务器本地存储图片，备份
		img_url = obj.cover.url
		
		#图片上传对象存储服务器
		qcloudCos = QcloudCos()
		qcloudCos.put(father_path + img_url,img_url)

	def delete_model(self, request, obj):
		self.deleteFile(obj)
		obj.delete()

	def deleteFile(self,obj):
		img_url = obj.cover.url
		html_url = obj.html_file.url
		qcloudCos = QcloudCos()
		qcloudCos.delete(img_url)			#删除云文件
		father_path = os.getcwd()
		img_url = father_path + img_url		#获取图片绝对地址
		html_url = father_path + html_url 	#获取html文件绝对地址
		os.remove(html_url)
		os.remove(img_url)					#删除本地文件

#相册管理
@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
	list_display = ('photo','description','time')
	list_display_links = ('photo','description','time')
	actions = ['delete_selected']
	verbose_name = '相册管理'
	def delete_selected(self, request, queryset):
		"""覆盖父类的删除方法"""
		for obj in queryset:
			self.deleteImage(obj)
			obj.delete()
	delete_selected.short_description = "删除所选的图片"


	def save_model(self, request, obj, form, change):
		#服务器本地存储图片，备份
		obj.save()
		img_url = obj.photo.url
		#获取工作目录，即工程根目录
		father_path = os.getcwd()	
		#图片上传对象存储服务器
		qcloudCos = QcloudCos()
		qcloudCos.put(father_path + img_url,img_url)

	def delete_model(self, request, obj):
		self.deleteImage(obj)
		obj.delete()

	def deleteImage(self,obj):
		img_url = obj.photo.url
		qcloudCos = QcloudCos()
		qcloudCos.delete(img_url)			#删除云文件
		father_path = os.getcwd()
		img_url = father_path + img_url		#获取图片根地址
		os.remove(img_url)					#删除本地文件


@admin.register(models.AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
	list_display = ('title','time','cover')
	list_display_links = ('title','time','cover')
	actions = ['delete_selected']
	exclude = ('content',)
	verbose_name = '关于我'
	def delete_selected(self, request, queryset):
		"""覆盖父类的删除方法"""
		for obj in queryset:
			self.deleteFile(obj)
			obj.delete()
	delete_selected.short_description = "删除所选"


	def save_model(self, request, obj, form, change):
		#服务器本地存储图片，备份
		obj.save()
		img_url = obj.cover.url
		html_url = obj.html_file.url
		#获取工作目录，即工程根目录
		father_path = os.getcwd()
		drawHtml(obj, father_path + html_url)	
		#图片上传对象存储服务器
		qcloudCos = QcloudCos()
		qcloudCos.put(father_path + img_url,img_url)

	def delete_model(self, request, obj):
		self.deleteFile(obj)
		obj.delete()

	def deleteFile(self,obj):
		img_url = obj.cover.url
		qcloudCos = QcloudCos()
		qcloudCos.delete(img_url)			#删除云文件
		father_path = os.getcwd()
		html_url = father_path + obj.html_file.url
		img_url = father_path + img_url		#获取图片根地址
		os.remove(img_url)					#删除本地文件
		os.remove(html_url)

@admin.register(models.Diary)
class DiaryAdmin(admin.ModelAdmin):
	verbose_name = '日记管理'
	list_display = ('time','diary_content')
	actions = ['delete_selected']
	exclude = ('content',)

	def diary_content(self, obj):
		return strip_tags(obj.content)
		
	def delete_selected(self, request, queryset):
		for obj in queryset:
			self.deleteFile(obj)
			obj.delete()

	def save_model(self, request, obj, form, change):
		obj.save()
		html_url = obj.html_file.url
		father_path = os.getcwd()
		drawHtml(obj, father_path + html_url)
		

	def delete_model(self, request, obj):
		self.deleteFile(obj)
		obj.delete()

	def deleteFile(self,obj):
		father_path = os.getcwd()
		html_url = father_path + obj.html_file.url
		os.remove(html_url)

@admin.register(models.IpRecord)
class IpRecordAdmin(admin.ModelAdmin):
	verbose_name = '访问IP管理'
	list_display = ('ip','title','time')

	def title(self,obj):
		return '%s' % obj.article.title
	title.short_description = '标题'


admin.site.site_header = 'Alex博客后台管理'
admin.site.site_title = "Alex's blog"
