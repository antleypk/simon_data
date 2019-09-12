import requests, json, csv, os

def get_companies(pv_count):
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
        d_content = content.decode("utf-8")
        content_json = json.loads(d_content)
        content_keys = content_json.keys()
        results = content_json['results']
        result = results[0]
        result_keys = result.keys()
       

        for r in results:
            if r['listing_active_count'] > 5:
                count+=1 
                print("Shop ID: {}, Shop Name: {}, Active Listings: {}".format(r['shop_id'], r['shop_name'], r['listing_active_count']))
                stores.append(r)
            if count == 15:
                state = False
                break
        limit+=increment
        offset+=increment
    print(' ')
    return stores    


def main():
    company_count = 10
    companies = get_companies(10)
    for company in companies:
        print('company: {}'.format(company['shop_name']))



if __name__ == "__main__":
    main()