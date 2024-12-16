from django.shortcuts import render
from django.http import JsonResponse
from .models import Company, Saved_Company, Salary, New_Job
from django.contrib.auth.decorators import login_required
from datetime import datetime

#####################################[ views ]#################################################
@login_required(login_url='/')
def placement(request):
	params = {
		'Company' : Company.objects.all(),
		'User_Company' : Saved_Company.objects.all(),
		'Salary' : Salary.objects.all(),
		}
	return render(request, 'placement/placement_index.html', params)

@login_required(login_url='/')
def newJobs(request):
	params = {
		'Jobs' : New_Job.objects.all().order_by('-date_updated')
		}
	return render(request, 'placement/new_jobs.html', params)

@login_required(login_url='/')
def savedCompany(request):
	user = request.user

	saved_companies = Saved_Company.objects.filter(user_id = user).order_by('-last_open')
	salary_count = []

	for company in saved_companies:
		salary = len(Salary.objects.filter(company_id = company.company_id))
		salary_count.append(salary)

	params = {
		"SavedCompany" : zip(saved_companies,salary_count)
	}
	return render(request, 'placement/saved_company.html', params)


@login_required(login_url='/')
def allCompany(request):
	params = {
		'page' : 'allCompany',
		'Companies' : Company.objects.all(),
		'SavedCompany' : [i.company_id.id for i in Saved_Company.objects.filter(user_id = request.user)],
	}
	return render(request, 'placement/all_company.html', params)


@login_required(login_url='/')
def addNew(request):
	params = {
		'companies' : Company.objects.all(),
		'locations' : set([i.location for i in New_Job.objects.all()]),
		'positions' : set([i.position for i in New_Job.objects.all()]),
		}
	return render(request, 'placement/add_new.html', params)



#####################################[ Set Data ]#################################################
@login_required(login_url='/')
def addCompany(request):
	if request.method == "GET":
		name = request.GET.get('name','')
		desc = request.GET.get('desc','')
		link = request.GET.get('link','')
		icon = request.GET.get('icon','')
		Company(name=name, desc=desc, link=link, icon_url=icon).save();
		return JsonResponse(data= {'status':'Success'})	
	return JsonResponse(data= {'status':'Failed'})

@login_required(login_url='/')
def addSalary(request):
	if request.method == "GET":
		company_id = request.GET.get('company_id','')
		position   = request.GET.get('position','')
		country    = request.GET.get('country','')
		base       = request.GET.get('base','')
		bonus      = request.GET.get('bonus','')
		stock      = request.GET.get('stock','')

		company = Company.objects.filter(id = company_id)[0]
		Salary(company_id = company, position = position, country = country, base = base, bonus = bonus, stock = stock).save();
		return JsonResponse(data= {'status':'Success'})	
	return JsonResponse(data= {'status':'Failed'})

@login_required(login_url='/')
def addJob(request):
	if request.method == "GET":
		company_id = request.GET.get('company_id','')
		position   = request.GET.get('position','')
		location   = request.GET.get('location','')
		job_id     = request.GET.get('job_id','')
		link       = request.GET.get('link','')
		date       = datetime.now()

		company = Company.objects.filter(id = company_id)[0]
		New_Job(company_id = company, position = position, location = location, job_id = job_id, link = link, date_updated = date).save();
		return JsonResponse(data= {'status':'Success'})	
	return JsonResponse(data= {'status':'Failed'})

@login_required(login_url='/')
def addSavedCompany(request):
	if request.method == 'GET':
		company_id = request.GET.get('company_id','');
		
		company = Company.objects.filter(id = company_id)[0]
		user = request.user

		saved_company = Saved_Company.objects.filter(user_id = user, company_id = company)

		if (saved_company.exists()):
			saved_company.delete()
			return JsonResponse(data = {'status': 'unsaved'})
		else:
			Saved_Company(user_id = user, company_id = company, last_open = datetime.now()).save()
			return JsonResponse(data = {'status': 'saved'})

	return JsonResponse(data = {'status': 'None'})


#####################################[ Get Data ]#################################################
@login_required(login_url='/')
def getAllCompany(request):
	data = {
		'name':'getAllCompany',
		'list': []
	}
	all_companies = Company.objects.all();

	for company in all_companies:
		salary_list = []
		for salary in Salary.objects.filter(company_id = company):
			salary_list.append({'position' : salary.position,
								'country' : salary.country,
								'base'    : salary.base,
								'bonus'   : salary.bonus,
								'stock'   : salary.stock,})

		company_and_selery = {
			'company' : {'id'   : company.id,
					     'name' : company.name,
						 'desc' : company.desc,
						 'link' : company.link },
			'seleries' : salary_list
		}
		data['list'].append(company_and_selery)

	return JsonResponse(data = data)


@login_required(login_url='/')
def getSavedCompany(request):
	data = {
		'name':'getSavedCompany',
		'list': []
	}

	user = request.user
	saved_companyies = Saved_Company.objects.filter(user_id = user);

	for saved_company in saved_companyies:
		salary_list = []
		for salary in Salary.objects.filter(company_id = saved_company.company_id):
			salary_list.append({'position' : salary.position,
								'country' : salary.country,
								'base'    : salary.base,
								'bonus'   : salary.bonus,
								'stock'   : salary.stock,})

		company_and_selery = {
			'company' : {'id'   : saved_company.company_id.id,
						 'name' : saved_company.company_id.name,
						 'desc' : saved_company.company_id.desc,
						 'link' : saved_company.company_id.link,
						 'last_open' : saved_company.last_open },
			'seleries' : salary_list
		}
		data['list'].append(company_and_selery)

	return JsonResponse(data = data)


@login_required(login_url='/')
def getSalary(request):
	company_id = request.GET.get('company_id');

	salary_list = []
	company = Company.objects.filter(id = company_id)[0];	

	for salary in Salary.objects.filter(company_id = company):
		salary_list.append({'position' : salary.position,
							'country' : salary.country,
							'base'    : salary.base,
							'bonus'   : salary.bonus,
							'stock'   : salary.stock,})
		
	data = {
		'name': company.name,
		'length' : len(salary_list),
		'salaryList': salary_list
	}
	return JsonResponse(data = data)

@login_required(login_url='/')
def getJobData(request):
	job_id = request.GET.get('job_id');
	job = New_Job.objects.filter(id = job_id)[0];	

	data = {
		'position': job.position,
		'company': job.company_id.name,
		'location': job.location,
		'date': job.date_updated,
		'logo': job.company_id.icon_url,
		'job_link': job.link,
		'career_link': job.company_id.link,
		'company_id': job.company_id.id
	}
	return JsonResponse(data = data)

#################################[ Update ]###########################

@login_required(login_url='/')
def updateDatetime(request):
	company_id = request.GET.get('company_id');
	company = Company.objects.filter(id = company_id)[0]
	user = request.user

	saved_company = Saved_Company.objects.filter(company_id = company, user_id = user)[0]
	saved_company.last_open = datetime.now();
	saved_company.save();

	data = {
		'status':'Success',
	}
	return JsonResponse(data = data)