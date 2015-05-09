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
market_include={'business':1,'finance':1,'manage':1,'customer':1,'sales':1,'operation':1,'marketing':1,'human resource':1}
market_exclude={'developer':1,'engineer':1}

def index(request):
    response = TemplateResponse(request, 'search.html', {})
    return response

def filter_market(tags):
    Skillflag=False
    sflag=False
    rflag=False
    for i in tags:
        if i['tag_type']=='SkillTag':
            for j in market_include:
                if j in (i['name']):
                    Skillflag=True
                    break
    for i in tags:
        if i['tag_type']=='RoleTag':
            for j in market_exclude:
                if j in (i['name']):
                    Skillflag=False
                    rflag=True
                    break

    if Skillflag==False and rflag==False:
        for i in tags:
            if i['tag_type']=='RoleTag':
                for j in market_include:
                    if j in (i['name']):
                        Skillflag=True
                        break
    # print Skillflag
    return Skillflag

def filter_keyword(tags,key):
    Skillflag=False
    sflag=False
    rflag=False
    for i in tags:
        if i['tag_type']=='SkillTag':
            if key in (i['name']):
                Skillflag=True
                break
    for i in tags:
        if i['tag_type']=='RoleTag':
            for j in market_exclude:
                if j in (i['name']):
                    Skillflag=False
                    rflag=True
                    break

    if Skillflag==False and rflag==False:
        for i in tags:
            if i['tag_type']=='RoleTag':
                if key in (i['name']):
                    Skillflag=True
                    break
    # print Skillflag
    return Skillflag



def form_processing(request):
    location=request.POST.get('location',False)
    keyword=request.POST.get('keyword',False)
    #startup=request.POST.get('startup',False)
    q=0
    if location and keyword:
        q=1
    if location and not keyword:
        q=2
    if q==0:
        response=HttpResponseRedirect('/')
    elif q==2:
        master=[]
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
                                if filter_market(x['tags']):
                                    temp=dict()
                                    temp['title']=x['title']
                                    temp['angellist']=x['angellist_url']
                                    temp['company_name']=x['startup']['name']
                                    master.append(temp)
        length=len(master)
        response=render_to_response('result.html', {"contacts": master,"sum":length})

    elif q==1:
        master=[]
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
                                if filter_keyword(x['tags'],keyword.lower()):
                                    temp=dict()
                                    temp['title']=x['title']
                                    temp['angellist']=x['angellist_url']
                                    temp['company_name']=x['startup']['name']
                                    master.append(temp)
        length=len(master)
        response=render_to_response('result.html', {"contacts": master,"sum":length})

     #    if startup :
        # startup=startup.replace(" ","-")
     #        data_url='https://api.angel.co/1/search?query='+startup+'&type=Startup'
     #        try:
     #            j = urllib2.urlopen(data_url)
     #            j_obj = json.load(j)
     #            j.close()
     #            z1=1
     #        except ValueError:
     #            z1=2
     #            pass
     #        except urllib2.URLError:
     #            z1=3
     #            pass
     #        else:
     #            for value in j_obj:
     #                data='https://api.angel.co/1/startups/'+str(value['id'])+'/jobs?access_token='+ACCESS_TOKEN
     #                try:
     #                    ji = urllib2.urlopen(data)
     #                    j_ob = json.load(ji)
     #                    ji.close()
     #                except ValueError:
     #                    pass
     #                except urllib2.URLError:
     #                    pass
     #                else:
     #                    for v in j_ob:
     #                        temp=dict()
     #                        temp['title']=v['title']
     #                        temp['angellist']=v['angellist_url']
     #                        temp['company_name']=v['startup']['name']
     #                        master.append(temp)
        
    return response
    

#http://bootsnipp.com/snippets/featured/advanced-dropdown-search
