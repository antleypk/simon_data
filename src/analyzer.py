import os,csv, requests , json 

def get_recent():
    files = os.listdir("./data")
    dates = []
    for f in files:
        sub_f = f[:-15]
        if sub_f == "shops":
            lcl_t = f[6:]
            lcl_t = lcl_t[:-4]
            dates.append(lcl_t)

    dates = sorted(dates, reverse=True)
    try:
        date = dates[0]
        return date
    except IndexError:
        print('Data Folder is missing shop lists') 
        return 0

def get_shops(timestamp):
    lcl_path = "./data/shops_{}.csv".format(timestamp)
    shops = []
    with open(lcl_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        count = 0
        for row in reader:
            shop = {}
            if count > 0:
                shop['count'] = row[0]
                shop['id'] = row[1]
                shop['name'] = row[2]
                shop['listings'] = row[3]
                shops.append(shop)
            count+=1
    return shops

def word_counter(shop_id):
    url = "https://openapi.etsy.com/v2/shops/{}/listings/active?limit=25&offset=0&api_key=bvpvd0ns8aqk63229f9baz9u".format(shop_id)
    headers = {'user-agent': 'my-app/0.0.1'}

    r = requests.get(url, headers=headers)
    print('r: {}'.format(r))
    content = r.content
    d_content = content.decode("utf-8")
    content_json = json.loads(d_content)
    results = content_json['results']
    result = results[0]
    result_keys = result.keys()
    result_string = ''
    result_string+=str(result['title'])
    result_string+=str(result['description'])
    result_list = result_string.lower().split(' ')

    word_set = set()
    clean_words = []


    for item in result_list:
        item = item.strip(',')
        item = item.strip('.')
        item = item.strip('\n')
        word_set.add(item)
        clean_words.append(item)


    word_gram  = []
    for w_set in word_set:
        tmp_word = w_set
        count = 0
        for w_word in clean_words:
            if w_set == w_word:
                count+=1
        word_frame = {}
        word_frame['word'] = tmp_word
        word_frame['count'] = count
        word_gram.append(word_frame)

    sorted_gram = sorted(word_gram, key = lambda i:i["count"], reverse=True)

    return_list = []
    r_count = 0
    for i in sorted_gram:
        if r_count < 5:
            return_list.append(i)
            r_count+=1
        if r_count ==5:
            break

    return return_list


def main():
    timestamp = get_recent()
    print('timestamp: {}'.format(timestamp))
    distributions = []
    if not timestamp == 0:
        shops = get_shops(timestamp)
        for shop in shops:
            lcl_id = shop['id']          
            lcl = {}
            lcl['id'] = lcl_id
            lcl['distribution'] = word_counter(lcl_id)
            distributions.append(lcl)
        for distro in distributions:
            print(distro)
    else:
        print("Please run 'scraper.py' first.")
if __name__ == "__main__":
    main()