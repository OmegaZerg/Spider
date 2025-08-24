import unittest
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html

class TestCrawl(unittest.TestCase):
    def test_normalize_url_1(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_2(self):
        input_url = "http://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_3(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_4(self):
        input_url = "http://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_5(self):
        input_url = "blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_6(self):
        input_url = "blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_7(self):
        input_url = "HTTPS://BLOG.booT.DEV/PATH/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_8(self):
        input_url = ""
        try:
            actual = normalize_url(input_url)
        except ValueError as e:
            assert str(e) == "The normalize url function must not be called with an empty string!"
            
    def test_get_h1_from_html_1(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_2(self):
        input_body = '<html><body><h1></h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_3(self):
        input_body = '<html><body><p>Test paragraph</p></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_4(self):
        input_body = '<html><body><h1>Test Title</h1><h1>A second h1!</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_5(self):
        input_body = '<html><body><h1>    Test Title Spaces    </h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title Spaces"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority_1(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority_2(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p></p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority_3(self):
        input_body = '''<html><body>
            <p></p>
            <main>
                <p></p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority_4(self):
        input_body = '''<html><body>
            <p>We want this to be returned!</p>
            <stuff>
                <p>This shouldnt be returned</p>
            </stuff>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "We want this to be returned!"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority_5(self):
        input_body = '''<html><body>
            <h1>This is a header</h1>
            <stuff>
                <h2>This is a smaller header</h2>
            </stuff>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()