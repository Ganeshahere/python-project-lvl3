import tempfile
import sys
import requests_mock
from page_loader import download
from os.path import abspath, join
from os import listdir
from urllib.parse import urljoin


URL = 'https://test.com'
DIR_NAME = 'test-com_files'
RESOURCES_URL = [urljoin(URL, '/assets/application.css'),
                 urljoin(URL, '/assets/professions/nodejs.png'),
                 urljoin(URL, '/runtime.js')]

EXPECTED_CONTENT = RESOURCES_URL[:]


with open(abspath('tests/fixtures/page_with_local_links.html')) as file:
    expected_page = file.read()


def test_page_loading():
    with open(abspath('fixtures/page_with_global_links.html.html'),
              'r') as file:
        testing_page = file.read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(URL, text=testing_page)
            [m.get(url, text=content) for url, content
             in zip(RESOURCES_URL, EXPECTED_CONTENT)]
            file_path = download(URL, tmpdirname)
            with open(file_path, 'r') as file:
                page = file.read()
            assert len(listdir(tmpdirname)) == 2
            assert len(listdir(join(tmpdirname, DIR_NAME))) == 3
            assert page == expected_page
