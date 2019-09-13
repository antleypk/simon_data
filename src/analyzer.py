import os,csv, requests, json, time

def get_recent_run():
    pprint('--get recent run')
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
        pprint('Data Folder is missing shop lists') 
        return 0

def get_shops(pv_timestamp):
    pprint("--get shops, pv_timestamp: {}".format(pv_timestamp))
    lcl_path = "./data/shops_{}.csv".format(pv_timestamp)
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
    pprint("--word counter, shop_id: {}".format(shop_id))
    url = "https://openapi.etsy.com/v2/shops/{}/listings/active?limit=25&offset=0&api_key=bvpvd0ns8aqk63229f9baz9u".format(shop_id)
    headers = {'user-agent': 'my-app/0.0.1'}

    r = requests.get(url, headers=headers)
    r_status=r.status_code
    pprint("r status: {}".format(r_status))
    if r_status == 200:
        pprint('API RESPONSE: {}'.format(r))
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
                if not i["word"] == '':
                    return_list.append(i)
                    r_count+=1
            if r_count ==5:
                break
        pprint("     Top Terms: {}".format(return_list))
        return return_list
    else:
        return_list = []
        return_dict = {}
        return_dict["word"] = 'Error Code Status {}'.format(r_status)
        return_dict["count"] = 1
        return_list.append(return_dict)
        return return_list

def read(pv_list):
    pprint("--read")
    for item in pv_list:
        pprint(item)
    return pv_list

def save(distributions, path):
    pprint("--save")
    s_t = '{}'.format(time.time())
    time_split = s_t.split('.')
    e = time_split[0]
    lcl_path = path+'_{}.csv'.format(e)
    pprint('make {}'.format(lcl_path))
    with open(lcl_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "id"
                    ,"shop_id"
                    ,"e_time"
                ]
            )
            lcl_id = 1
            for d in distributions:
                lcl_list = [lcl_id, d['id'], d['distribution'], str(time.time())]     
                writer.writerow(lcl_list)
                lcl_id+=1    

def pprint(string):
    print(string)
    if not os.path.isdir("./data"):
        os.makedirs("./data")
    if not os.path.isfile("./data/logs.csv"):
        os.system("touch ./data/logs.csv")
    with open("./data/logs.csv","a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(time.time()), string])

def main():
    pprint('--main, analyzer.py')
    timestamp = get_recent_run()
    pprint('timestamp: {}'.format(timestamp))
    distributions = []
    save_path = './data/distribution'
    if not timestamp == 0:
        shops = get_shops(timestamp)
        for shop in shops:
            lcl_id = shop['id']          
            lcl = {}
            lcl['id'] = lcl_id
            lcl['distribution'] = word_counter(lcl_id)
            distributions.append(lcl)
        save(read(distributions), save_path)
    else:
        pprint("Please run 'scraper.py' first.")
if __name__ == "__main__":
    main()