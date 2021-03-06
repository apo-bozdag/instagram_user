# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import urlencode
import json
from instagram_user.items import InstagramUserItem
from instagram_user import settings
import requests
import re

script = """
function main(splash, args)
  splash:set_custom_headers(HEADERS)
  splash.images_enabled = True
  splash:go(args.url)
  return splash:html()
end
"""

headers = {
    'Host': 'www.instagram.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.instagram.com/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}


def get_params(instagram_user_id, next_page=''):
    param = {
        'query_hash': 'e769aa130647d2354c40ea6a439bfc08',
        'variables': '{"id":"' + str(instagram_user_id) + '","first":50, "after":"' + next_page + '"}',
    }
    return param


def get_userid(name):
    find_id_url = 'https://www.instagram.com/' + name
    response = requests.get(find_id_url, headers=headers)
    result = re.search('"profilePage_(.*?)"', response.text)
    return result[1]


class UserCrawlerSpider(scrapy.Spider):
    name = 'user_crawler'
    allowed_domains = ['www.instagram.com']
    base_url = 'https://www.instagram.com/graphql/query/?'

    def __init__(self, continue_url=None, *args, **kwargs):
        super(UserCrawlerSpider, self).__init__(*args, **kwargs)
        self.continue_url = continue_url

    def start_requests(self):
        if self.continue_url:
            yield Request(self.continue_url, headers=headers, callback=self.parse)
        else:
            for userid in settings.USERID:
                url = self.base_url + urlencode(get_params(userid))
                yield Request(url, headers=headers, callback=self.parse)
            for name in settings.USERNAME:
                userid = get_userid(name)
                url = self.base_url + urlencode(get_params(userid))
                yield Request(url, headers=headers, callback=self.parse)

    def parse(self, response, **kwargs):
        data_json = json.loads(response.text)
        data = data_json.get('data').get('user').get('edge_owner_to_timeline_media')
        userid = 0
        for user_detail in data.get('edges'):
            user_node = user_detail.get('node')
            item = InstagramUserItem()
            item['postid'] = user_node.get('id')
            item['shortcode'] = user_node.get('shortcode')
            item['username'] = user_node.get('owner').get('username')
            userid = user_node.get('owner').get('id')
            item['userid'] = userid
            item['liked'] = user_node.get('edge_media_preview_like').get('count')
            try:
                item['caption'] = user_node.get('edge_media_to_caption').get('edges')[0].get('node').get('text')
            except Exception:
                item['caption'] = ''
            item['comment'] = user_node.get('edge_media_to_comment').get('count')

            video_link = ''
            images_link = ''
            if user_node.get('edge_sidecar_to_children'):
                child_edges = user_node.get('edge_sidecar_to_children').get('edges')
                for child in child_edges:
                    node = child.get('node')
                    if user_node.get('is_video'):
                        # get video link
                        video_link += node.get('video_url') + ';'
                    else:
                        images_link += node.get('display_url') + ';'
            else:
                if user_node.get('is_video'):
                    video_link = user_node.get('video_url') + ';'
                else:
                    images_link = user_node.get('display_url') + ';'
            item['image_list'] = images_link
            item['video_list'] = video_link

            yield item

        # get next page and send request
        page_info = data.get('page_info')
        if page_info.get('has_next_page'):
            next_page = page_info.get('end_cursor')
            url = self.base_url + urlencode(get_params(userid, next_page))
            yield Request(url, headers=headers, callback=self.parse)
