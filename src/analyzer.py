import os,csv

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
    pass

def main():
    timestamp = get_recent()
    if not timestamp == 0:
        shops = get_shops(timestamp)
        for shop in shops:
            print('shop: {}'.format(shop['id']))
    else:
        print("Please run 'scraper.py' first.")
if __name__ == "__main__":
    main()