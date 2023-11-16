import json
import requests
from bs4 import BeautifulSoup
import openai
from time import sleep

from .config import openai_api_key
from .common import format_response

openai.api_key = openai_api_key

def get_news_data(interest):

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    url = f'https://www.google.com/search?q={interest}&gl=us&tbm=nws&num=15'
    response = requests.get(
        url, headers=headers
    )
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []
    
    for el in soup.select("div.SoaBEf"):
        news_results.append(
            {
                "link": el.find("a")["href"],
                "title": el.select_one("div.MBeuO").get_text(),
                "snippet": el.select_one(".GI74Re").get_text(),
                "date": el.select_one(".LfVVr").get_text(),
                "source": el.select_one(".NUnG9d span").get_text()
            }
        )
 
    return news_results

def gpt3_completion(prompt, system, model='gpt-3.5-turbo', temp=0.7, top_p=1.0, tokens=500, freq_pen=0, pres_pen=0.0, stop=['<<STOP>>']):
    
    max_retry = 3
    retry = 0
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages = [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                            ],
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response["choices"][0]["message"]["content"].strip()
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            sleep(1)

async def scrape_and_gpt3(interests, person):

    all_news = []
    for i in interests:
        all_news += get_news_data(i)
        
    text_list = ["title: " + news['title'] + "\nsnippet: " + news['snippet'] + "\nsource: " + news['source'] for news in all_news]
    context = "\n###\n".join(text_list)

    # defining prompt
    prompt = f"""
    Below are relevant news articles from today. Please give a roundup of the news as if you are {person}, providing your own commentary on each important story.
    Focus on the 3-4 stories that you, {person}, find most interesting or relevant. Be creative and respond however {person} would respond. Make sure to give your own take on each story.
    News articles:
    {context}"""

    system = f"""
    You are {person}. Your jobs is to write a roundup of news articles provided by a user. You should lean into your persona, involving as many manerisms of {person} as possible. Feel free to add your own commentary as {person} or take the roundup in a new direction if you feel that is how {person} would do it.
    In total, your news roundup must be less than one paragraph. Feel free to omit some articles or topics that seem less important or redundant, as deemed by you - {person}. Also feel free to cut content to keep the roundup under one paragraph.
    Remember... Only report the MOST interesting news and ALWAYS stay in character. You are {person}!
    """

    # running gpt3 completion
    gpt3_result = gpt3_completion(prompt, system)
    return gpt3_result

async def news_response(input):
    '''
    Interface function
    Args:
        input (dict) - user_query (str)

    Returns:
        dict with items:
        state (str) - overall status of process [DONE, FAILED]
        response_code (int) - http response code or custom code
        error_msg (str) - text of error message (option, if state = FAILED)
        result (dict) - output of process, must be json serializable (option, if state = DONE)
    '''

    # get user query
    query = input.get('user_query')
    interests = [query]
    person = input.get('user_person')
    try:
        result = await scrape_and_gpt3(interests, person)
    except Exception as err:
        return {"state": "FAILED", "response_code":521, "error_msg": str(err)}
    
    return format_response(result=result)