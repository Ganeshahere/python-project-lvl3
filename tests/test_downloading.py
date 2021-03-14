import sys
from os.path import abspath, join
from os import listdir
import tempfile
from page_loader import download
import requests_mock
from urllib.parse import urljoin as urlj

with open(abspath('tests/fixtures/page_with_local_links.html')) as file:
    expected_page = file.read()

with open(abspath('tests/fixtures/page_with_global_links.html')) as file:
    testing_page = file.read()

with open(abspath('tests/fixtures/files/image.png')) as image:
    expected_image = image.read()

with open(abspath('tests/fixtures/files/styles.css')) as styles:
    expected_styles_file = styles.read()

with open(abspath('tests/fixtures/java_script/js')) as js:
    expected_js_file = js.read()

URL = 'https://test.com'
RESOURCES_LINK = {URL: testing_page,
                  urlj(URL, 'assets/professions/nodejs.png'): expected_image,
                  urlj(URL, 'assets/application.css'): expected_styles_file,
                  urlj(URL, 'packs/js/runtime.js'): expected_js_file}


def test_download():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            for url, content in RESOURCES_LINK.items():
                if isinstance(content, bytes):
                    m.get(url, content=content)
                else:
                    m.get(url, text=content)
            file_path = download(URL, tmpdirname)
            dir_path = join(tmpdirname, 'test-com_files')
            with open(file_path, 'r') as file:
                page = file.read()
            with open(f"{dir_path}/test-"
                      f"com-assets-professions-"
                      f"nodejs.png", 'rb') as image:
                recived_image = image.read()
            with open(f"{dir_path}/test-"
                      f"com-assets-"
                      f"application.css", 'r') as s:
                recived_styles_file = s.read()
            with open(f"{dir_path}/test-"
                      f"com-packs-js-"
                      f"runtime.js", 'r') as js:
                recived_js_file = js.read()
            assert page == expected_page
            assert recived_image == expected_image
            assert recived_styles_file == expected_styles_file
            assert recived_js_file == expected_js_file
            assert len(listdir(tmpdirname)) == 2
            assert len(listdir(join(tmpdirname, 'test-com_files'))) == 3
