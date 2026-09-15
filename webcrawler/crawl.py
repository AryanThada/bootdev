from urllib.parse import urlsplit , urljoin
from bs4 import BeautifulSoup , Tag
from typing import TypedDict

import requests
import sys
import asyncio
import aiohttp


class PageData(TypedDict):
    url:str
    heading:str
    first_paragraph:str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str)-> str:

    url_object = urlsplit(url)

    url_normalize_string = f"{url_object.netloc}{url_object.path}"


    return url_normalize_string

# def get_html(url):

#     response_object = requests.get(url , 
#                                    headers = {"User-Agent" : "BootCrawler/1.0"} ,
#                                     timeout = 10)

    

#     response_object.raise_for_status()

#     content_type = response_object.headers.get("Content-Type" , "")

#     if "text/html" not in content_type:
#         raise ValueError("response is not HTML")

#     return response_object.text


# def crawl_page(base_url , current_url = None , page_data = None):

    
#     if(current_url == None):
#         current_url = base_url 

#     if page_data is None:
#         page_data = {}
    
#     base_url_object = urlsplit(base_url)
#     curr_url_object = urlsplit(current_url)

#     if base_url_object.hostname != curr_url_object.hostname :
#         print("GONE OUTSIDE DOMAIN RETURING")
#         return 

#     normalize_curr_url = normalize_url(current_url) 

#     if normalize_curr_url in page_data :
#         print("DON'T Want to crawl same page twice")
#         return 

#     curr_html = get_html(current_url)

#     curr_page_data  = extract_page_data(curr_html,current_url )

#     page_data[normalize_curr_url] = curr_page_data 

#     curr_outgoing_links_list = curr_page_data["outgoing_links"]

#     print(f"Currently crawling: {current_url}")
#     print(f"Pages collected: {len(page_data)}")

#     for link in curr_outgoing_links_list :

#         try:
#             crawl_page(base_url , link , page_data)

#         except Exception as e:
#             print(f"Error Crawling {link} : {e}")
#             continue

#     return page_data




def get_heading_from_html(html_doc: str)->str:

    soup = BeautifulSoup(html_doc , 'html.parser')

    if(soup.find("h1")):
        return soup.h1.get_text()
    
    elif (soup.find("h2")):
        return soup.h2.get_text()

    else: return ""


def get_first_paragraph_from_html(html_doc: str)->str:

    soup = BeautifulSoup(html_doc , 'html.parser')

    main_tag = soup.find("main")

    if(main_tag):
        para_ptag = main_tag.find("p")

        if(para_ptag):
            return para_ptag.get_text()


    para_ptag = soup.find("p")

    if(para_ptag):
        return para_ptag.get_text()

    return ""

def get_urls_from_html(html , base_url):

    soup = BeautifulSoup(html, 'html.parser')
    all_a_tags = soup.find_all('a')

    all_links = []

    for link in all_a_tags :
        link = link.get('href')
        if not link :
            continue 

        absolute_link = urljoin(base_url , link)
        all_links.append(absolute_link)

    return all_links

def get_images_from_html(html , base_url):
    soup = BeautifulSoup(html, 'html.parser')
    all_img_tags = soup.find_all('img')
    
    all_links = []
    
    for img_link in all_img_tags :
        img_link = img_link.get('src')
        if not img_link :
                continue 
    
        absolute_link = urljoin(base_url , img_link)
        all_links.append(absolute_link)
    
    return all_links


def extract_page_data(html_doc: str , page_url: str):

    url =  page_url
    heading = get_heading_from_html(html_doc)
    first_paragraph = get_first_paragraph_from_html(html_doc) 
    outgoing_links = get_urls_from_html(html_doc , page_url)
    image_urls = get_images_from_html(html_doc , page_url) 

    page_data : PageData = {

        "url": url ,
        "heading":heading,
        "first_paragraph": first_paragraph , 
        "outgoing_links": outgoing_links ,
        "image_urls": image_urls

        }

    return page_data 





    # ASYNC FUNCTIONALITY

class AsyncCrawler:

    def __init__(self ,base_url , max_concurrency ,max_pages):

        self.base_url = base_url
        self.base_domain = urlsplit(base_url).hostname
        self.page_data = {}
        self.visited = set()
        self.lock  = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks =set()



    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type , exc_val , exc_tb):
        await self.session.close()


    async def add_page_visit(self , normalized_url):

        async with self.lock:

            if self.should_stop :
                return False

            if len(self.visited) >= self.max_pages:

                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                return False

            
            if(normalized_url in self.visited):
                print("DON'T Want to crawl same page twice")
                return False
            
            self.visited.add(normalized_url)
            return True
            
    async def get_html(self , curr_url):

        async with self.session.get(curr_url , raise_for_status= True) as response:

            content_type = response.headers.get("Content-Type" ,"")

            if "text/html" not in content_type:
                raise RuntimeError("response is not HTML")

            text = await response.text()

            return text


    
    async def crawl_page(self , current_url):

        

        # if(current_url == None):
        #         current_url = self.base_url 

        # if self.page_data is None:
        #         self.page_data = {}
            
        # base_url_object = urlsplit(self.base_url)

        if(self.should_stop):
            return 

        
        curr_url_object = urlsplit(current_url)

        if self.base_domain != curr_url_object.hostname :
                print("GONE OUTSIDE DOMAIN RETURING")
                return 

        normalized_curr_url = normalize_url(current_url) 

        # if normalize_curr_url in page_data :
        #     print("DON'T Want to crawl same page twice")
        #     return 


        was_added = await self.add_page_visit(normalized_curr_url)

        if not was_added  : 
             return 


        async with self.semaphore:
             

            curr_html = await self.get_html(current_url)

            curr_page_data  = extract_page_data(curr_html,current_url)

            async with self.lock:

                self.page_data[normalized_curr_url] = curr_page_data 

            curr_outgoing_links_list = curr_page_data["outgoing_links"]

            print(f"Currently crawling: {current_url}")
            print(f"Pages collected: {len(self.page_data)}")


            try:
                many_tasks = []

                for link in curr_outgoing_links_list :

                    task = asyncio.create_task(self.crawl_page(link))
                    many_tasks.append(task)
                    self.all_tasks.add(task)

                await asyncio.gather(*many_tasks)

            finally:
                current_task = asyncio.current_task()
                self.all_tasks.discard(current_task)


        


    async def crawl(self):
        await self.crawl_page(self.base_url)

        return self.page_data
        

            

async def crawl_site_async(base_url , max_concurrency , max_pages):
        async with AsyncCrawler(base_url , max_concurrency , max_pages) as crawler :

            page_data = await crawler.crawl()
            
            return page_data

       


# crawl_page()
#     "How do I crawl a page?"

# crawl()
#     "How do I start this crawler?"

# crawl_site_async()
#     "How do I safely create, run, and shut down this crawler?"



        pass