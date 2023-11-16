# eeyore-news-bot
Does what it says in the name. Build an API to have Eeyore read you the news on a topic of your choosing. Very entertaining.

## Prerequisites:

- First, to run the script you must have Python installed. I recommend Python 3.9.0 or later download [here](https://www.python.org/downloads/). With earlier versions you may run into issues with package installation.
- Next, you will need to make sure you have an active OpenAI account so you can use their API. Your API Key should be added to the config file in the backend folder (eeyore_backend/config.py). This will allow the backend to use your OpenAI subscription.
- Finally, you will need to set up a virtual environment and download the requirements file. You can achieve that via the code below.
##### create virtual environment
`python3 -m venv eeyore_venv`
##### activate virtual environment
`source eeyore_venv/bin/activate`
##### install package requirements
`pip install -r requirements.txt`

## Running:

To deploy the API locally, simply open a terminal and navigate to the main eeyore-news-bot folder. Then to run the app enter the command `uvicorn main:app`. The app should launch on a local host. If you add "/docs" to the end of the local host url, you'll be able to access the FastAPI docs and test the API. You can also test it via curl or any other method. Whether testing via the FastAPI docs, curl, or some other means, you will need to authenticate the API by providing the API Key as defined in config.py. Feel free to update this key as it suits you.

In the FastAPI docs, you'll be able to see the API schema, which I'll provide below as well.

```
{
  "user_query": "",
  "user_person": ""
}
```

This is how the API expects information to be provided. The **user_query** field should be provided with a news topic that you want to search on (for example, "philadelphia eagles" or "taylor swift"). The **user_person** field should be provided with a character or person who you would like to deliver the news to you (for example, "eeyore" or "tony soprano"). Alas, it is not just an Eeyore news bot. You can get the news from whomever you would like!