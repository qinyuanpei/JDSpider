
from bs4 import BeautifulSoup
import re,csv,requests,json

class JDSpider:

    def __init__(self,id):
        self.id = id

    def request(self,session,page):
        url = 'https://club.jd.com/comment/productPageComments.action'
        data = {
            'callback':'fetchJSON_comment98vv61',
	        'productId':self.id,
	        'score':0,
	        'sortType':5,
	        'pageSize':10,
	        'isShadowSku':0,
	        'page':page
        }

        try:
            text = session.get(url,params = data).text
            text = re.search(r'(?<=fetchJSON_comment98vv61\().*(?=\);)',text).group(0)
            return text
        except Exception as e:
            return None

    def download(self,folder,fileName):
        page = 0
        session = requests.session()
        headers = ['nickname','referenceTime','content','referenceName','userClientShow']
        with open(fileName,'w',newline='') as csvFile:
            writer = csv.DictWriter(csvFile, headers)
            writer.writeheader()
            while(True):
                data = self.request(session,page)
                print(u'正在抓取第{}页评论...'.format(str(page)))
                if(data != None):
                    json_data = json.loads(data)
                    comments = json_data['comments']
                    for comment in comments:
                        newRow = {
                            'nickname':comment['nickname'],
                            'referenceTime':comment['referenceTime'],
                            'content':comment['content'],
                            'referenceName':comment['referenceName'],
                            'userClientShow':comment['userClientShow']
                        }
                    writer.writerow(newRow)
                    page+=1
                else:
                    break


id = input('Please input a ProductId from jd.com:')
spider = JDSpider(str(id))
spider.download('',"{}.csv".format(id))