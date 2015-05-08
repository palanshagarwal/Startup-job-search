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
                                    temp=Job()
                                    temp.title=x['title']
                                    temp.angellist_url=x['angellist_url']
                                    temp.company_name=x['startup']['name']
                                    master.append(temp)


