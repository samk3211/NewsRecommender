from flask_restful import Resource, reqparse
from flask import request
from newsapi import NewsApiClient
from model import Model

import json, os

class Feed(Resource):
    __newsapi__ = NewsApiClient(api_key='810ba56767d949dca95e671988826b48')
    __model__ = Model()

    def hasFields(self, obj, fields):
        for field in fields:
            if field not in obj or obj[field] is None:
                return False
        return True 

    def get(self):
        response = self.__newsapi__.get_top_headlines(
            sources='hacker-news,wired,ars-technica,engadget,techcrunch,techradar,recode,the-next-web,new-scientist,the-verge,next-big-future',
            page_size=100)
        print(response)
        candidates = [x for x in response['articles'] if self.hasFields(x, ['title', 'description', 'content', 'urlToImage'])]

        for x in candidates:
            x['score'] = self.__model__.score(x)

        #top = candidates[:100] 
        top = sorted(candidates, key=lambda x: x['score'], reverse=True)[:20]

        os.makedirs('logs', exist_ok=True)
        with open('logs/requests.txt', 'a') as f:
            for x in top:
                json.dump(x, f)
                f.write('\n')

        return {'articles':top}, 200
