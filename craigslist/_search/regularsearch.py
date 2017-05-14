import logging
from collections import namedtuple
from craigslist._search import get_query_url

logger = logging.getLogger(__name__)

RegularSearchPost = namedtuple('RegularSearchPost', [
    'id',
    'title',
    'url',
    'repost_id',
    'price',
    'bedrooms',
    'date',
    'area'])

def get_current_offset_from_response(doc):
    return int(doc.cssselect("#searchform span.pagenum span.rangeFrom")[0].text)

def get_number_of_posts_on_current_page_from_response(doc):
    return int(doc.cssselect("#searchform span.pagenum span.rangeTo")[0].text)

def get_num_total_posts_from_response(doc):
    return int(doc.cssselect("#searchform span.pagenum span.totalcount")[0].text)

def parse_post(post):
    pid = int(post.get('data-pid'))
    respost_pid = int(post.get('data-repost-of')) if post.get('data-repost-of') else None
    date = arrow.get(post.cssselect('time')[0].get('datetime'))
    url = post.cssselect("span > span > a")[0].get('href')
    title = post.cssselect("span > span > a")[0].text
    price_el = get_only_first_or_none(post.cssselect("span > span > span.price"))
    price_raw = price_el.text if price_el is not None else None
    price = int(price_raw.replace("$", "")) if price_raw else None
    housing_el = get_only_first_or_none(post.cssselect("span > span > span.housing"))
    housing = [x.strip() for x in housing_el.text.split("-\n") \
        if x.strip()] if housing_el is not None else []
    bedrooms_raw = get_only_first_or_none([x for x in housing if "br" in x])
    num_bedrooms = int(bedrooms_raw.replace("br", "")) if bedrooms_raw else None
    area_raw = get_only_first_or_none([x for x in housing if "ft" in x])
    area = int(area_raw.replace("ft", "")) if area_raw else None
    return RegularSearchPost(**{
        "id": pid,
        "title": title,
        "url": url,
        "respost_id": respost_pid,
        "price": price,
        "bedrooms": num_bedrooms,
        "date": date,
        "area": area,
    })

def process_page_url(url, get):
    logger.debug("downloading %s" % url)
    body = get(url)
    return parse_page_url_output(body)

# def get_posts_from_response(doc):
#     for post in doc.cssselect("#sortable-results > div.rows > p"):
#         yield parse_post(post)

def parse_page_url_output(body):
    return body

from concurrent.futures import as_completed
from craigslist.utils import import_class
from craigslist.io import requests_get
from craigslist._search import get_query_url
from craigslist.post import process_post_url

def regularsearch(
    area,
    category,
    sort,
    cache,
    cachedir,
    executor,
    get,
    **kwargs):
    doc = lxml.html.fromstring(get(get_query_url(
        area, "search", offset=0, sort=sort, **kwargs)))
    num_total_posts = get_num_total_posts_from_response(doc)
    num_posts_on_page = get_number_of_posts_on_current_page_from_response(doc)
    yield from get_posts_from_response(doc)
    for offset in range(100, num_total_posts, 100):
        doc = lxml.html.fromstring(get(get_query_url(
            area, "search", offset=offset, sort=sort, **kwargs)))
        num_posts_on_page = get_number_of_posts_on_current_page_from_response(doc)
        yield from get_posts_from_response(doc)