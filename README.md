# Instagram User Profile Crawler

Create a crawler to download Profile detail into the local folder via the username or user id.

**INSTALLATION**

``pip install -r requirements.txt``

# Settings

Enter username or userid to caption the profile:

```python
USERID = '[Enter instagram userid]'
USERNAME = '[Enter instagram username]'
```

Setup the item pipelines:

```python
ITEM_PIPELINES = {
    'instagram_user.pipelines.FilePipeline': 301,
}

FILES_STORE = './user'
```

# Run

Start the crawler, store the image and information in local

```bash
scrapy crawl user_crawler
```

If you want to save the results in a file

```bash
scrapy crawl user_crawler -o results.json
```

If you want to pause and continue from json url

```bash
scrapy crawl user_crawler -a continue_url="https://www.instagram.com/graphql/query/?example" -o results2.json
```

# Result Example

```json
[
  {
    "postid": "544109137850911213",
    "shortcode": "eNEGDIpcnt",
    "username": "fenerbahce",
    "userid": "544022417",
    "liked": 9412,
    "caption": "#Fenerbahce Instagram'da!",
    "comment": 3617,
    "image_list": "https://instagram.fadb5-1.fna.fbcdn.net/v/t51.2885-15/e15/11372296_1482408185383472_2111744389_n.jpg?tp=1&_nc_ht=instagram.fadb5-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=ho2Ti7etdMYAX8QPKjq&ccb=7-4&oh=31289d2306d12e2c76df451f3f6b65ba&oe=608A9359&_nc_sid=86f79a;",
    "video_list": ""
  }
]
```