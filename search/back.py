from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests_cache
import urllib
import urllib2
#from urllib2 import Request, urlopen, URLError
import StringIO, json

ACCESS_TOKEN='7af939957801baa2ae77d3a3c1b6555f5a67a1e6e11c6cd1'
from job import Job
requests_cache.install_cache(cache_name='angelList_cache', backend='sqlite', expire_after=180)

def index(request):
    # return HttpResponse('welcome'+ACCESS_TOKEN)
    response = TemplateResponse(request, 'search.html', {})
    return response

def form_processing(request):
    location=request.POST.get('location',False)
    skill=request.POST.get('skill',False)
    startup=request.POST.get('startup',False)
    q=0
    if location and skill:
        q=1
    if startup and not location and not skill:
        q=1
    if q==0:
        response=HttpResponseRedirect('http://127.0.0.1:8000')
    else:
        master=[]
        if location and skill and not startup:
            loc=[]
            ski=[]
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
                    # loc.add(value['id'])
                    data='https://api.angel.co/1/tags/'+str(value['id'])+'/startups'
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
                            if k=='startups':
                                for x in v:
                                    # if x['hidden']=='false'
                                    loc.append(x['id'])

            data_url='https://api.angel.co/1/search?query='+skill+'&type=MarketTag'
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
                    # ski.add(value['id'])
                    data='https://api.angel.co/1/tags/'+str(value['id'])+'/startups'
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
                            if k=='startups':
                                for x in v:
                                    if x['id'] in loc:
                                        ski.append(x['id'])
            for i in ski:
                data='https://api.angel.co/1/startups/'+str(i)+'/jobs?access_token='+ACCESS_TOKEN
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
                        temp=Job()
                        temp.title=v['title']
                        temp.angellist_url=v['angellist_url']
                        temp.company_name=v['startup']['name']
                        master.append(temp)



        if startup and not location and not skill:
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
                            temp=Job()
                            temp.title=v['title']
                            temp.angellist_url=v['angellist_url']
                            temp.company_name=v['startup']['name']
                            master.append(temp)
        length=len(master)
        response=render_to_response('result.html', {"contacts": master,"sum":length})
    return response
    

#http://bootsnipp.com/snippets/featured/advanced-dropdown-search