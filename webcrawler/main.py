import sys 
import asyncio
# from crawl import get_html
# from crawl import crawl_page
from crawl import crawl_site_async
from json_report import write_json_report

async def main():
    # print("Hello from webcrawler!")

    # print("Script name:", sys.argv[0])
    # print("Argument:", sys.argv[1])

    if(len(sys.argv) < 2):
        print("no website provided")
        sys.exit(1)
        return

    elif(len(sys.argv) >4):
        print("too many arguments provided")
        sys.exit(1)
        return

    else :
        print(f"starting crawl of: {sys.argv[1]}")

        # html_doc = get_html(sys.argv[1])
        
        # print(html_doc)
        
        # crawled_page_data= crawl_page(base_url= sys.argv[1] , current_url = None , page_data = None)

        base_url = sys.argv[1]
        max_concurrency = 5
        max_pages = 10

        if(len(sys.argv) > 2):
            max_concurrency = int(sys.argv[2])
        if(len(sys.argv) > 3):
            max_pages = int(sys.argv[3])
        
        
        
        crawled_page_data = await crawl_site_async(base_url , max_concurrency ,max_pages)

        # print(f"Found {len(crawled_page_data)} pages:")

        # for page in crawled_page_data.values():
        #     print(page)


        write_json_report(crawled_page_data)
        
    return      

# if __name__ == "__main__":
#     main()

asyncio.run(main())
