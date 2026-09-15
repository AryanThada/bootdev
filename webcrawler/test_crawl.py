import unittest
from crawl import normalize_url
from crawl import get_heading_from_html
from crawl import get_first_paragraph_from_html
from crawl import get_urls_from_html
from crawl import get_images_from_html
from crawl import extract_page_data

class TestCrawl(unittest.TestCase):

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual  = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_http_url(self):
        input_url = "http://www.boot.dev/blog/path"
        actual  = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_url_with_query(self):
        input_url = "https://www.boot.dev/blog/path?search=python" 
        actual = normalize_url(input_url) 
        expected = "www.boot.dev/blog/path" 
        self.assertEqual(actual, expected)

    def test_url_with_fragment(self):
        input_url = "https://www.boot.dev/blog/path#section" 
        actual = normalize_url(input_url) 
        expected = "www.boot.dev/blog/path" 
        self.assertEqual(actual, expected)

    def test_root_url(self):
        input_url = "https://www.boot.dev/" 
        actual = normalize_url(input_url) 
        expected = "www.boot.dev/" 
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual , expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
                            <p>Outside paragraph.</p>
                            <main>
                                <p>Main paragraph.</p>
                            </main>
                        </body></html>"""

        actual= get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual , expected)

    def test_get_first_paragraph_from_html_main_priority2(self):
        input_body = """<html><body>
                            <p>Outside paragraph.</p>
                            
                        </body></html>"""

        actual= get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual , expected)


    def test_get_first_paragraph_from_html_main_priority3(self):
        input_body = """<html><body>
                            <main>
                                <h1>NO para here</h1>
                            </main>

                            <p>Outside Fallback paragraph.</p>
                            
                        </body></html>"""

        actual= get_first_paragraph_from_html(input_body)
        expected = "Outside Fallback paragraph."
        self.assertEqual(actual , expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"

        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'

        actual = get_urls_from_html(input_body , input_url)

        expected= ["https://crawler-test.com"]

        self.assertEqual(actual , expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"

        input_body = '<html><body><a href="/page1.html"><span>Boot.dev</span></a></body></html>'

        actual = get_urls_from_html(input_body , input_url)

        expected= ["https://crawler-test.com/page1.html"]

        self.assertEqual(actual , expected)

    def test_get_urls_from_html_multiple_links(self):
        input_url = "https://crawler-test.com" 
        input_body = ''' <html> <body> 
                        <a href="/about">About</a> 
                        <a href="/contact">Contact</a> 
                        <a href="https://example.com">Example</a> 
                        </body> </html> '''
        actual = get_urls_from_html(input_body, input_url) 
        expected = [ "https://crawler-test.com/about", "https://crawler-test.com/contact", "https://example.com", ] 
        self.assertEqual(actual, expected)


    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img  alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                        <h1>Test Title</h1>
                        <p>This is the first paragraph.</p>
                        <a href="/link1">Link 1</a>
                        <img src="/image1.jpg" alt="Image 1">
                    </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
                    "url": "https://crawler-test.com",
                    "heading": "Test Title",
                    "first_paragraph": "This is the first paragraph.",
                    "outgoing_links": ["https://crawler-test.com/link1"],
                    "image_urls": ["https://crawler-test.com/image1.jpg"],
                }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()