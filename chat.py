import requests 
from requests import get
from config import api_key1


# chat1('generate a python prograam for virtual asssistant')
def chat2(query,urls): 
    messages = []
    system_message = 'You are a qna bot, you are created to give the answe of user asked question based on the data provided to you, you are like a chatbot. you have to answer of the question based on this youtube video {urls} ' 
    message= {  'role': 'User','parts': [{'text': system_message+' '+query}]}
    messages.append(message)
    data = {'contents': messages }
    url= 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key='+api_key1
    response=requests.post(url,json=data)

    t2= response.json()
    t2=t2.get('candidates')[0].get('content').get('parts')[0].get('text')
    t2=t2.replace('*','')
    # print(t2)

    return t2

