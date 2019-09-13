import os, csv, requests, json, time, sys
import scraper

def get_recent_run():
    scraper.pprint('--get recent run')
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
        scraper.pprint('Data Folder is missing shop lists') 
        return 0

def get_shops(pv_timestamp, key):
    scraper.pprint("--get shops, pv_timestamp: {}".format(pv_timestamp))
    lcl_path = "./data/shops_{}.csv".format(pv_timestamp)
    shops = []
    try:
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
        
    except FileNotFoundError:
        scraper.pprint("FILE NOT FOUND ERROR!! Did you provide an incorrect timestamp?")
        scraper.pprint(" ")
        shop = {}
        shop['count'] = 0
        shop['id'] = 0
        shop['name'] = "Error, FILE NOT FOUND"
        shop['listings'] = "0"
        shops.append(shop)
    return shops
def word_counter(shop_id, key):
    #returns a distribution chart of the 5 most common terms related to one shop
    scraper.pprint("--word counter, shop_id: {}".format(shop_id))

    #gather data
    url = "https://openapi.etsy.com/v2/shops/{}/listings/active?limit=25&offset=0&api_key={}".format(shop_id, key)
    headers = {'user-agent': 'my-app/0.0.1'}

    r = requests.get(url, headers=headers)
    r_status=r.status_code
    scraper.pprint("r status: {}".format(r_status))
    if r_status == 200:
        scraper.pprint('API RESPONSE: {}'.format(r))
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
        
        #process data
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
        scraper.pprint("     Top Terms: {}".format(return_list))
        return return_list
    else:
        return_list = []
        return_dict = {}
        return_dict["word"] = 'Error Code Status {}'.format(r_status)
        return_dict["count"] = 1
        return_list.append(return_dict)
        return return_list

def read(pv_list):
    scraper.pprint("--read")
    for item in pv_list:
        scraper.pprint(item)
    return pv_list

def save(distributions, path):
    scraper.pprint("--save")
    s_t = '{}'.format(time.time())
    time_split = s_t.split('.')
    e = time_split[0]
    lcl_path = path+'_{}.csv'.format(e)
    scraper.pprint('make {}'.format(lcl_path))
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


def main():
    scraper.pprint("--'main, analyzer.py'")
    key = scraper.get_key()
    distributions = []
    save_path = './data/distribution'
    arg_length = len(sys.argv)
    if not arg_length == 2:
        timestamp = get_recent_run()
    if arg_length == 2:
        timestamp = sys.argv[1]
    scraper.pprint('timestamp: {}'.format(timestamp))
    if not timestamp == 0:
        shops = get_shops(timestamp,key)
        for shop in shops:
            lcl_id = shop['id']          
            lcl = {}
            lcl['id'] = lcl_id
            lcl['distribution'] = word_counter(lcl_id, key)
            distributions.append(lcl)
        save(read(distributions), save_path)
    else:
        scraper.pprint("Please run 'scraper.py' first.")

if __name__ == "__main__":
    main()
