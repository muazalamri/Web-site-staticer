import requests
import os
def is_route(link, root):
    if not link:  # إذا كان link فارغًا
        return False
    
    if root:  # إذا كان root غير فارغ
        if len(link) >= len(root) and link.startswith(root):
            return True
    
    return link.startswith('/')
def is_link(text):
    if len(text.split('\n'))==1:
        if text[:4]=='http':
            return True 
        if text[:1]=='/':
            return True
    return False 
def extract_links(html,spliters=['"',"'",' ']):
    if len(spliters)>0:
        html=html.split(spliters[0])
    if len(spliters)>1:
        for i in spliters[1:]:
            new=[]
            for j in html:
                new+=j.split(i)
            html=new
    links=list(filter(is_link,html))
    return links
def index(root):
    url_data={}
    unscaned=[root]
    outers=[]
    problems={}
    
    while (len(unscaned)>0):
        url=unscaned[0]
        unscaned.pop(0)
        try:
            if url not in url_data.keys():
                text=requests.get(url).text
                links=extract_links(text)
                url_data[url]=text
                for link in links:
                    if is_route(link,root):
                        if link not in url_data.keys():
                            if link[0]=='/':link=root+link
                            unscaned.append(link)
                    else:outers.append(link)
        except Exception as e :
            problems[url]=str(e)
    #print(url_data.keys())
    #print(problems)
    return url_data
def put(root):
    data= index(root)
    for i in data.keys():
        print('i:',i)
        dir=[j for j in i[len(root):].split('/') if len(j)>0]
        print(dir)
        if len(dir)==0:
             open('index.html','w', encoding='utf-8').write(data[i])
             continue 
        elif len(dir)>0:
            for _index in range(len(dir)):
                os.makedirs('/'.join(dir[:_index+1]),exist_ok=True)
        if (len(dir[-1].split('.'))==1)and len(dir)>0:
            open(('/'.join(dir)+'/index.html'),'w',encoding='utf-8').write(data[i])
            #else:
#                open('/'.join(dir),'w',encoding='utf-8').write(data[i])
#index('http://127.0.0.1:5000')
put('http://127.0.0.1:5000/')