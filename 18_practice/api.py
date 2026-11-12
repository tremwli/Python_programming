import requests
import pprint

def get_post(q, limit):
    try:
        url = "https://openlibrary.org/search.json"

        limit = int(limit) 

        params = {
            "q" : q,
            "fields" : 'title,author_name',
            "limit" : limit
        }

        response = requests.get(url, params=params,timeout=10)
        data = response.json()

        pprint.pprint(data)
        res = []

        # book = data["docs"][0]
        # res = [{
        #     "작가": book["author_name"][0],
        #     "제목": book["title"],
        # }]
        # return res        

        for post in data['docs']:
             res.append({
                         "작가" :  post["author_name"][0],           # 일자
                         "제목"  :   post["title"],        # 구분
                                    # 메뉴
                                 # 칼로리
                        })

        return res
   
    except Exception as e:
        print(e)
        raise


