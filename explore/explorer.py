import requests
import json
import os
import time
import csv


##First connection

# url = "https://openapi.etsy.com/v2/listings/active?limit=50&offset=0&api_key=bvpvd0ns8aqk63229f9baz9u"
# headers = {'user-agent': 'my-app/0.0.1'}

# r = requests.get(url, headers=headers)
# print('r: {}'.format(r))
# content = r.content
# print('content: {}'.format(content))


#===================================================================================================

#find 15 shops, 10 track, 5 alternates in case a shop closes down.

# state = True
# limit = 50
# offset = 0
# increment = 50
# count = 0
# stores = []
# while(state):
#     print('limit: {}, offset: {}'.format(limit, offset))
#     url = "https://openapi.etsy.com/v2/shops?limit={}&offset={}&api_key=bvpvd0ns8aqk63229f9baz9u".format(limit, offset)
#     headers = {'user-agent': 'my-app/0.0.1'}

#     r = requests.get(url, headers=headers)
#     print('r: {}'.format(r))
#     content = r.content
#     #print('content: {}'.format(content))
#     #print('content type: {}'.format(type(content)))
#     d_content = content.decode("utf-8")
#     #print('d_content type: {}'.format(type(d_content)))
#     content_json = json.loads(d_content)
#     #print("content_json type: {}".format(type(content_json)))
#     content_keys = content_json.keys()
#     print('keys: {}'.format(content_keys))
#     #print('count: {}'.format(content_json['count']))
#     #print('results: {}'.format(content_json['results']))
#     results = content_json['results']
#     #print("results type: {}".format(type(results)))
#     result = results[0]
#     #print('result type: {}'.format(type(result)))
#     result_keys = result.keys()
#     print("result keys: {}".format(result_keys))

#     input('stop')

#     for r in results:
#         if r['listing_active_count'] > 5:
#             count+=1 
#             print("shop id: {}, shop name: {}, listing active count: {}".format(r['shop_id'], r['shop_name'], r['listing_active_count']))
#             stores.append(r)
#         if count == 15:
#             print('exit condition met')
#             state = False
#             break
#     limit+=increment
#     offset+=increment        

# if not os.path.isfile("./stores.csv"):
#     print('make ./stores.csv')
#     with open("./stores.csv", "w", newline="") as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow(
#                 [
#                     "id"
#                     ,"shop_id"
#                     ,"shop_name"
#                     ,"listing_count"
#                     ,"e_time"
#                 ]
#             )

# count = 0
# with open("./stores.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     for store in stores:
#         count+=1
#         print('count: {}, shop id: {}, shop name: {}, listing count: {}'.format(count, store['shop_id'], store['shop_name'], store['listing_active_count']))
#         writer.writerow([count, store['shop_id'],store['shop_name'], store['listing_active_count']])

# ========================================================================================================



url = "https://openapi.etsy.com/v2/shops/21133149/listings/active?limit=25&offset=0&api_key=bvpvd0ns8aqk63229f9baz9u"
headers = {'user-agent': 'my-app/0.0.1'}

r = requests.get(url, headers=headers)
print('r: {}'.format(r))
content = r.content
#print('content: {}'.format(content))
print('content type: {}'.format(type(content)))
d_content = content.decode("utf-8")
print('d_content type: {}'.format(type(d_content)))
content_json = json.loads(d_content)
print("content_json keys: {}".format(content_json.keys()))
#print('results: {}'.format(content_json['results']))
results = content_json['results']
print("results type: {}".format(type(results)))
result = results[0]
print('result type: {}'.format(type(result)))
result_keys = result.keys()
print("result keys: {}".format(result_keys))
print('result 0: listing id: {}, title: {}, description: {}'.format(result['listing_id'],result['title'],result['description']))