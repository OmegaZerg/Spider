import unittest
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html

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

    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_relative(self):
        input_url = "https://www.boot.dev"
        input_body = '<html><body><a href="/courses"><span>Boot.dev Courses</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://www.boot.dev/courses"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_multiple(self):
        input_url = "https://www.boot.dev"
        input_body = '<html><body><a href="/courses"><span>Boot.dev Courses</span></a><a href="/dashboard"><span>Boot.dev Dashboard></span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://www.boot.dev/courses", "https://www.boot.dev/dashboard"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative_missing_href(self):
        input_url = "https://www.boot.dev"
        input_body = '<html><body><a href="/courses"><span>Boot.dev Courses</span></a><a href=""><span>Boot.dev Dashboard</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://www.boot.dev/courses"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Boot.dev Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Boot.dev Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_multiple(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Boot.dev Logo"><img src="/boots.png" alt="Boots the bear"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png", "https://blog.boot.dev/boots.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative_missing_src(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="" alt="Boot.dev Logo"><img src="/boots.png" alt="Boots the bear"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/boots.png"]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()