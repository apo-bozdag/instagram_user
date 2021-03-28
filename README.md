# Instagram User Profile Crawler

Create a crawler to download Profile detail into the local folder via the username or user id.

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

## Run

Start the crawler, store the image and information in local

```bash
scrapy crawl user_crawler
```

If you want to save the results in a file

```bash
scrapy crawl user_crawler -o results.json
```
