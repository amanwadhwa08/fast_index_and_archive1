import logging
import re
import azure.functions as func
from datetime import datetime, timedelta

from usp.tree import sitemap_tree_for_homepage
def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('url')
    now = datetime.now()
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('url')
    logging.info('Python HTTP trigger function processed a request.')
    try:
        
        tree = sitemap_tree_for_homepage(name)
        Cur_time=now+timedelta(minutes=3)
        output=""
        count =0
        for page in tree.all_pages():
            found=""
            m = re.search('url=(.+?), ', str(page))
            if(datetime.now() > Cur_time):
                break
            if m:
                found = m.group(1)
            if str(found) not in output:
                output+="\""+str(found)+"\""+","
                count+=1
                
        output="["+output[:-1]+"]"
        print(output)
        print(count)
    except:
        output="Something went wrong"

    if (output==""):
        return func.HttpResponse(
            "Please pass a url"
        )
    else:
        return func.HttpResponse(output)
            
