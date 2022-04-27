from requests_html import HTMLSession
from json import loads
from numpy import array

#https://duckduckgo.com/i.js?q=millie%20bobby%20brown&o=json&s=0&p=1&u=bing&f=,,,,,&l=us-en&vqd=3-19084058480156129700725331011721974472-105276110364342771415585942728392589116


from duckduckgo_search import ddg_images, ddg,ddg_news

class Scrape:

    def __init__(self,query):
        self.query = query
        

    def img(self,page):
        try:
            items = []
            url = f"https://www.bing.com/images/async?q={self.query}&first={page}&count=100&cw=1177&ch=671&relo=15&relp=295&tsc=ImageHoverTitle&datsrc=I&layout=ColumnBased&mmasync=1&dgState=c*6_y*14546s14641s14779s14694s14600s14605_i*506_w*186&IG=B37DF1A9037E493A8330B37B32916699&SFX=15&iid=images.6108&SafeSearch=Off"
            s = HTMLSession()
            r = s.get(url,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)' +
            'AppleWebKit/537.36 (KHTML,' +
            'like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
            img_div = r.html.find('div.imgpt')
            
            for img_element in img_div:
                try:
                    img_a = loads(img_element.find('a.iusc',first=True).attrs['m'])
                    jpg = [ img_a.get('murl') ]
                    img_url = [ img_a.get('purl') ]
                    img_title = [ img_a.get('t') ]
                    thumbnail = [ img_element.find('img.mimg',first=True).attrs['src'] ]
                    all_items = jpg+img_url+img_title+thumbnail

                    items.append(all_items)
                except:
                    pass

        
            return array(items)
        except:
            pass


    def normal_search(self):
        results = []
        searchs = ddg(self.query, region='wt-wt',safesearch='Moderate', time=None, max_results=100, save_csv=False)
        
        for search in array(searchs):
            title_n=[search.get('title')]
            href= [search.get('href')]
            body= [search.get('body')]
            all_items = title_n+href+body
            results.append(all_items)
        return results

    def news(self,max_results):
        all_news = []
        search_news = ddg_news(self.query, region='wt-wt', safesearch='Moderate', time=None, max_results=max_results, save_csv=False)
        for news in search_news:
            date = [news.get('date').split("T")]
            title = [news.get('title')]
            body = [news.get('body')]
            url = [news.get('url')]
            image = [news.get('image')]

            news_items = date+title+body+url+image
            all_news.append(news_items)

        return all_news


    def videos(self,page):
        url = f"https://www.bing.com/videos/asyncv2?q={self.query}&SafeSearch=Off&async=content&first={str(page)}&count=35&dgst=RowIndex_u54*ColumnIndex_u2*TotalWidth_u574*OrdinalPosition_u210*ThumbnailWidth_u259*HeroContainerWidth_u1121*HeroContainerHeight_u275*HeroOnPage_b0*SlidesGridOnPage_b0*arn_u6*ayo_u1598*cry_u14798*&IID=video.1&SFX=8&IG=1224D883F14D4323AD9CE0AF65DF43AA&CW=1177&CH=729&bop=88&form=QBVR"
        s = HTMLSession()
        r = s.get(url,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)' +
           'AppleWebKit/537.36 (KHTML,' +
           'like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        items = []
        
        
        for video in r.html.find('div.dg_u'):

            try:
                data = loads(video.find('div.vrhdata',first=True).attrs['vrhm'])
                img_div = video.find('div.cico',first=True)
                img = [img_div.find('img',first=True).attrs['src']]


                url = [ data.get('pgurl') ] 

                duration =[video.find('div.mc_bc_rc.items',first=True).text]

                title_vid = [ data.get('vt')[:40] ]

                text_div =  video.find('div.mc_vtvc_meta',first=True)
                posted_time = [ text_div.find('span.meta_pd_content',first=True).text ]
                publisher = [ text_div.find('div.mc_vtvc_meta_row')[1].find('span',first=True).text ]
                all_item = url+img+title_vid+duration+posted_time+publisher
            
                items.append(all_item)
                
            except Exception as e:

                print(e) 

        
        return array(items)