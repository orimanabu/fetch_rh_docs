import unittest
from fetch_rh_docs import *

class FetchRHDocsTest(unittest.TestCase):
    session = {}
    url1 = 'https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/'
    url2 = 'https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/'
    username = 'mori1@redhat.com'
    password = None

    def setUp(self):
        self.session = requests.Session()

    def test_get_all_product_urls(self):
        product_urls = get_all_product_urls(self.session, product_index)
        self.assertEqual(len(product_urls), 55, msg='# of URLs')

    def test_fetch_top_page(self):
        content = fetch_top_page(self.session, self.url1)
        title = html.fromstring(content).xpath('//title')[0].text
        self.assertEqual(title, 'Red Hat Enterprise Linux')

    def test_parse_pdf_urls(self):
        content = fetch_top_page(self.session, self.url1)
        urls = parse_pdf_urls(content, None)
        self.assertEqual(len(urls), 185)

    def test_parse_kb_urls(self):
        content = fetch_top_page(self.session, self.url2)
        urls = parse_kb_urls(content, None)
        self.assertEqual(len(urls), 43)

    def test_fetch_kb_content(self):
        content = fetch_top_page(self.session, self.url2)
        urls = parse_kb_urls(content, None)
        title, content = fetch_kb_content(self.session, urls[0], self.username, self.password)
        self.assertEqual(title, 'Red Hat Enterprise Linux OpenStack Platform 6 - Top New Features - Red Hat Customer Portal')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
