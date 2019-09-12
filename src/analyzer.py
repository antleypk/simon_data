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
    date = dates[0]
    return date

def get_shops(timestamp):
    lcl_path = "./data/shops_{}.csv".format(timestamp)

    with open(lcl_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
        for row in reader:
            print(row)


def main():
    timestamp = get_recent()
    get_shops(timestamp)

if __name__ == "__main__":
    main()