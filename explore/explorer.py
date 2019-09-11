import requests
import json


##First connection

# url = "https://openapi.etsy.com/v2/listings/active?limit=50&offset=0&api_key=bvpvd0ns8aqk63229f9baz9u"
# headers = {'user-agent': 'my-app/0.0.1'}

# r = requests.get(url, headers=headers)
# print('r: {}'.format(r))
# content = r.content
# print('content: {}'.format(content))


#===================================================================================================

#find 15 shops, 10 track, 5 alternates in case a shop closes down.

state = True
limit = 50
offset = 0
increment = 50
count = 0
stores = []
while(state):
    print('limit: {}, offset: {}'.format(limit, offset))
    url = "https://openapi.etsy.com/v2/shops?limit={}&offset={}&api_key=bvpvd0ns8aqk63229f9baz9u".format(limit, offset)
    headers = {'user-agent': 'my-app/0.0.1'}

    r = requests.get(url, headers=headers)
    print('r: {}'.format(r))
    content = r.content
    #print('content: {}'.format(content))
    #print('content type: {}'.format(type(content)))
    d_content = content.decode("utf-8")
    #print('d_content type: {}'.format(type(d_content)))
    content_json = json.loads(d_content)
    #print("content_json type: {}".format(type(content_json)))
    content_keys = content_json.keys()
    #print('keys: {}'.format(content_keys))
    #print('count: {}'.format(content_json['count']))
    #print('results: {}'.format(content_json['results']))
    results = content_json['results']
    #print("results type: {}".format(type(results)))
    result = results[0]
    #print('result type: {}'.format(type(result)))
    result_keys = result.keys()
    #print("result keysL: {}".format(result_keys))

    for r in results:
        if r['listing_active_count'] > 5:
            count+=1 
            print("shop id: {}, shop name: {}, listing active count: {}".format(r['shop_id'], r['shop_name'], r['listing_active_count']))
            stores.append(r)
        if count == 15:
            print('exit condition met')
            state = False
            break
    limit+=increment
    offset+=increment        

count = 0
for store in stores:
    count+=1
    print('count: {}, store id: {}, listing count: {}'.format(count, store['shop_id'], store['listing_active_count']))