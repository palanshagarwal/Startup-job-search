from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import requests_cache
import urllib
import urllib2
#from urllib2 import Request, urlopen, URLError
import StringIO, json

ACCESS_TOKEN='7af939957801baa2ae77d3a3c1b6555f5a67a1e6e11c6cd1'
market=set()
startup_ids=set()
# from job import Job
#requests_cache.install_cache(cache_name='angelList_cache', backend='sqlite', expire_after=180)

def index(request):
    response = TemplateResponse(request, 'search.html', {})
    return response

def form_processing(request):
    location=request.POST.get('location',False)
    skill=request.POST.get('skill',False)
    startup=request.POST.get('startup',False)
    q=0
    if location:
        q=1
    if startup and not location:
        q=1
    if q==0:
        response=HttpResponseRedirect('/')
    else:
        master=[]
        if location and not startup:
            loc=[]
            ski=[]
            location=location.replace(" ","-")
            data_url='https://api.angel.co/1/search?query='+location+'&type=LocationTag'
            try:
                j = urllib2.urlopen(data_url)
                j_obj = json.load(j)
                j.close()
                z1=1
            except ValueError:
                z1=2
                pass
            except urllib2.URLError:
                z1=3
                pass
            else:
                for value in j_obj:
                    data='https://api.angel.co/1/tags/'+str(value['id'])+'/jobs?access_token='+ACCESS_TOKEN
                    try:
                        ji = urllib2.urlopen(data)
                        j_ob = json.load(ji)
                        ji.close()
                    except ValueError:
                        pass
                    except urllib2.URLError:
                        pass
                    else:
                        for k,v in j_ob.items():
                            if k=='jobs':
                                for x in v:
                                    temp=dict()
                                    temp['title']=x['title']
                                    temp['angellist']=x['angellist_url']
                                    temp['company_name']=x['startup']['name']
                                    master.append(temp)

        if startup :
	    startup=startup.replace(" ","-")
            data_url='https://api.angel.co/1/search?query='+startup+'&type=Startup'
            try:
                j = urllib2.urlopen(data_url)
                j_obj = json.load(j)
                j.close()
                z1=1
            except ValueError:
                z1=2
                pass
            except urllib2.URLError:
                z1=3
                pass
            else:
                for value in j_obj:
                    data='https://api.angel.co/1/startups/'+str(value['id'])+'/jobs?access_token='+ACCESS_TOKEN
                    try:
                        ji = urllib2.urlopen(data)
                        j_ob = json.load(ji)
                        ji.close()
                    except ValueError:
                        pass
                    except urllib2.URLError:
                        pass
                    else:
                        for v in j_ob:
                            temp=dict()
                            temp['title']=v['title']
                            temp['angellist']=v['angellist_url']
                            temp['company_name']=v['startup']['name']
                            master.append(temp)
        length=len(master)
        response=render_to_response('result.html', {"contacts": master,"sum":length})
    return response
    

#http://bootsnipp.com/snippets/featured/advanced-dropdown-search