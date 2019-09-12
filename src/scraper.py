import requests, json, csv, os, time

def get_shops(pv_count, pv_listing_count):
    state = True
    limit = 50
    offset = 0
    increment = 50
    count = 0
    stores = []
    store_ids = set()
    while(state):
        #print('limit: {}, offset: {}'.format(limit, offset))
        url = "https://openapi.etsy.com/v2/shops?limit={}&offset={}&api_key=bvpvd0ns8aqk63229f9baz9u".format(limit, offset)
        headers = {'user-agent': 'my-app/0.0.1'}
        r = requests.get(url, headers=headers)
        print('---- API response code: {}, Limit: {}, Offset: {}'.format(r, limit, offset))
        content = r.content
        d_content = content.decode("utf-8")
        content_json = json.loads(d_content)
        content_keys = content_json.keys()
        results = content_json['results']
        result = results[0]
        result_keys = result.keys()       

        for r in results:
            if r['listing_active_count'] > pv_listing_count:
                lcl_id = r['shop_id']
                if not lcl_id in store_ids:
                    count+=1
                    store_ids.add(lcl_id) 
                    print("Shop ID: {}, Shop Name: {}, Active Listings: {}, Count: {}".format(r['shop_id'], r['shop_name'], r['listing_active_count'], count))
                    stores.append(r)
            if len(stores) == pv_count:
                state = False
                break
        limit+=increment
        offset+=increment
        print(' ')
    print(' ')
    return stores    


def save(shops, path):
    s_t = '{}'.format(time.time())
    time_split = s_t.split('.')
    e = time_split[0]
    lcl_path = path+'_{}.csv'.format(e)
    if not os.path.isfile(path):
        print('make {}'.format(lcl_path))
        with open(lcl_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        "id"
                        ,"shop_id"
                        ,"shop_name"
                        ,"listing_count"
                        ,"e_time"
                    ]
                )
                lcl_id = 1
                for shop in shops:
                    lcl_list = [lcl_id, shop['shop_id'], shop['shop_name'], shop['listing_active_count'], str(time.time())]     
                    writer.writerow(lcl_list)
                    lcl_id+=1

def main():
    shop_count = 10
    min_active_listing = 25
    save_path = './data/shops'
    shops = get_shops(shop_count,min_active_listing)
    for shop in shops:
        print('shop: {}'.format(shop['shop_name']))
    print(' ')
    save(shops, save_path)


if __name__ == "__main__":
    main()

    #156831598
    #1568313742