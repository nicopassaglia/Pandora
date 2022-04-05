import time
from requests import get

urls = {'https://www.google.com': 10, 'https://www.facebook.com': 50, 'https://www.tumblr.com': 30, 'https://www.instagram.com': 20}

total = 0
for url in urls:
    total += urls.get(url)
print(f"Total requests to make is {total}")

total = 0
counts_not_empty = True
while counts_not_empty:
    counts_not_empty = False
    for url in urls:
        count = urls.get(url)
        if count > 0:
            urls.update({url: count - 1})
            response = get(url)
            print(response)
            #time.sleep(10)
            total += 1
            counts_not_empty = True

print(f"Total requests was {total}")