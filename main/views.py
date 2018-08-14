from django.shortcuts import render, get_object_or_404
from .models import *
import markdown
from django.core.paginator import Paginator
import random
from django.contrib.auth.decorators import login_required

Host = "https://alex-1256236352.cos.ap-beijing.myqcloud.com"	#静态文件主机地址，便于更改

def pagination_data_fun(paginator, page, is_paginated):
		if not is_paginated:
			return {}

		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False
		page_number = page.number
		total_pages = paginator.num_pages
		page_range = paginator.page_range

		if page_number == 1:
			right = page_range[page_number:page_number + 2]
			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
			 	first = True
		else:
			left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last = True

			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
			}

		return data


def index(request):
	try:
		page = int(request.GET.get('page'))
	except:
		page = 1
	background_image = "/static/img/diary_" +  str(random.randint(0,2)) + ".jpg"
	article_list = Article.objects.all().order_by('-time')				
	paginator = Paginator(article_list, 5)
	nowPage = paginator.page(page)
	is_paginated = (paginator.num_pages > 1)
	context = {'article_list':nowPage.object_list,
			   'is_paginated':is_paginated,
			   'page_obj':nowPage,
			   'Host':Host,
			   'background_image':background_image,
			   'paginator':paginator,
			   }
	pagination_data = pagination_data_fun(paginator, nowPage, is_paginated)
	context.update(pagination_data)
	return render(request,'index.html',context)

def about(request):
	introduction = AboutMe.objects.all()[0]
	context = {
		'introduction':introduction,
		'Host':Host,
	}
	return render(request,'about.html',context)

def detail(request,pk):
	article = get_object_or_404(Article,pk=pk)
	article.viewIncrease(request,pk)
	cover_url = Host + article.cover.url
	return render(request,'detail.html',context={'article':article,
												 'cover_url':cover_url})


def photo(request):
	try:
		page = int(request.GET.get('page'))
	except:
		page = 1	
	photoList = Album.objects.all().order_by('-id')
	paginator = Paginator(photoList,8)
	nowPage = paginator.page(page)
	is_paginated = (paginator.num_pages > 1)
	context = {'photoList':nowPage.object_list,
			   'is_paginated':is_paginated,
			   'page_obj':nowPage,
			   'Host':Host,
			   'paginator':paginator,
			   }
	pagination_data = pagination_data_fun(paginator, nowPage, is_paginated)
	context.update(pagination_data)
	return render(request,'photo.html',context)

@login_required
def diary(request):
	try:
		page = int(request.GET.get('page'))
	except:
		page = 1
	diary_list = Diary.objects.order_by('-time')
	paginator = Paginator(diary_list,10)
	nowPage = paginator.page(page)
	is_paginated = (paginator.num_pages > 1)
	background_image = "/static/img/diary_" +  str(random.randint(0,2)) + ".jpg"
	diary_list = nowPage.object_list
	context = {
	           'diary_list':nowPage.object_list,
	           'is_paginated':is_paginated,
	           'page_obj':nowPage,
	           'Host':Host,
	           'background_image':background_image,
	           'paginator':paginator,
	}
	pagination_data = pagination_data_fun(paginator, nowPage, is_paginated)
	context.update(pagination_data)
	return render(request,'diary.html',context)

def checkout(request):
	"""检查是否登录"""
	import json
	from django.http import HttpResponse
	if request.user.is_authenticated():
		return HttpResponse(json.dumps({'status':1}))
	else:
		return HttpResponse(json.dumps({'status':0}))

def page_not_found(request):
	return render(request,'404.html')









