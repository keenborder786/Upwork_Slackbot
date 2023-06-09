import time


def parse_generate_event_response(body):
    """
    
    
    """
    response = body.get('view','').get('state','').get('values','')
    parameters = {}
    for _,value in response.items():
        param_name = list(value.keys())[0]
        parameters[param_name] = value.get(param_name,'').get('value','')
    return parameters

def get_job_data(upwork_bot , job_title):
    """
    
    
    
    
    
    
    """
    html_data = upwork_bot.get_data(job_title)
    jobs_data = upwork_bot.parse_data(html_data)
    formatted_response = upwork_bot.format_data(jobs_data)
    return formatted_response
