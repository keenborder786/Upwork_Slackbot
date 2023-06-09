import time

import upwork_bot

from typing import Dict,Any


def parse_generate_event_response(body:Dict[str,Any]) -> Dict[str,str]:
    """Parses the response body gotten from `Generate-Events` modal and extracts
    the relevant parameters needed to start the job notiifer.
    
    Parameters
    -----------

    body : Dict[str,Any]
        The main body given by the `Generate-Events` modal
    
    Returns
    -------

    Dict[str,str]
        The parameters needed to start our job-notifier.
    
    """
    response = body.get('view','').get('state','').get('values','')
    parameters = {}
    for _,value in response.items():
        param_name = list(value.keys())[0]
        parameters[param_name] = value.get(param_name,'').get('value','')
    return parameters

def get_job_data(upwork_bot:upwork_bot.UpworkBot, job_title: str) -> str:
    """Gets,Parses and Format the data by utilizing UpworkBot instance

    Parameters
    ----------

    upwork_bot : upwork_bot.UpworkBot
        The UpworkBot instance
    
    job_title : str
        The main job title for UpworkBot instance is scrapping the data.
    

    Returns
    --------

    str
        The formatted job details that we will be sending to the user
    """
    html_data = upwork_bot.get_data(job_title)
    jobs_data = upwork_bot.parse_data(html_data)
    formatted_response = upwork_bot.format_data(jobs_data)
    return formatted_response
