#https://medium.com/@lejczak.learn/get-your-strava-activity-data-using-python-2023-%EF%B8%8F-b03b176965d0
client_id = '186208'
client_secret = '9f6974f7e03bf8e6637c5e2e2e6f512d32bca037'
auth_url = 'https://www.strava.com/oauth/authorize?client_id=186208&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all'
# visit url above and click "verify"
# then redirected to this url
redirect_block = 'http://localhost/exchange_token?state=&code=867b2fea877f8d411c8aec58f17b6a9312cc4ea7&scope=read,activity:read_all'
code = '867b2fea877f8d411c8aec58f17b6a9312cc4ea7'

# use curl to exchange the code:
"""
 curl -X POST https://www.strava.com/oauth/token \
 -F client_id=186208 \
 -F client_secret=9f6974f7e03bf8e6637c5e2e2e6f512d32bca037 \
 -F code=867b2fea877f8d411c8aec58f17b6a9312cc4ea7 \
 -F grant_type=authorization_code
"""

authorization_code = '{"token_type":"Bearer","expires_at":1763601745,"expires_in":21600,"refresh_token":"7502d0a6c6972f6ac53cd0ca643f6b1f6d57e4a5","access_token":"455f9d31f12eef420d71cc0dd0129d118b2af896","athlete":{"id":90783628,"username":"carter_coughlin","resource_state":2,"firstname":"Carter","lastname":"Coughlin","bio":"🤠 just running around","city":"Charlotte","state":"North Carolina","country":"United States","sex":"M","premium":false,"summit":false,"created_at":"2021-08-18T11:21:46Z","updated_at":"2025-11-17T16:01:17Z","badge_type_id":0,"weight":61.2348,"profile_medium":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/90783628/32484985/2/medium.jpg","profile":"https://dgalywyr863hv.cloudfront.net/pictures/athletes/90783628/32484985/2/large.jpg","friend":null,"follower":null}}'
refresh_token = '7502d0a6c6972f6ac53cd0ca643f6b1f6d57e4a5'
access_token = '455f9d31f12eef420d71cc0dd0129d118b2af896'

# clone this github repo
"""
git clone https://github.com/Cloudy17g35/strava-api.git
cd strava-activity-retrieval
"""