from datetime import datetime, timedelta
import requests
import json
import os


# 1.1 MOUNTING URL

# Stablish a standard format
TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.00Z'

# Get the current time and convert to the previously defined time stamp format  
end_time = datetime.now().strftime(TIMESTAMP_FORMAT)

# Calculate and convert difference of time
start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)

# The string that will in query be used
query = 'artificial intelligence'  

# Get the fields
tweet_fields = 'tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text'
user_fields = 'expansions=author_id&user.fields=id,name,username,created_at'
url_raw = f'https://labdados.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}'


# 1.2 MOUNT HEADERS
bearer_token = os.environ.get('BEARER_TOKEN')
headers = {'Authorization': 'Bearer {}'.format(bearer_token)}
response = requests.request('GET', url_raw, headers=headers)

# 1.3 PRINT JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))

# 1.4 PAGINATE
while 'next_token' in json_response.get('meta', {}):
    next_token = json_response['meta']['next_token']
    url = f'{url_raw}&next_token={next_token}'
    response = requests.request('GET', url, headers=headers)
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))
