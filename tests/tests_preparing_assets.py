import sys
import requests_mock
from page_loader.assets import prepare_assets
from urllib.parse import urljoin
import requests
import tempfile
from os.path import abspath, join


BASE_URL = 'https://test.com'
DIR_NAME = 'test-com_files'
RESOURCES_URL = [urljoin(BASE_URL, '/assets/application.css'),
                 urljoin(BASE_URL, '/assets/professions/nodejs.png'),
                 urljoin(BASE_URL, '/runtime.js')]

EXPECTED_CONTENT = RESOURCES_URL[:]

with open(abspath('tests/fixtures/page_with_local_links.html.html'), 'r') as file:
    expected_page = file.read()


def test_page_loading():
    with open(abspath('tests/fixtures/page_with_global_links.html.html'),
              'r') as file:
        testing_page = file.read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(BASE_URL, text=testing_page)
            [m.get(url, text=content) for url, content
             in zip(RESOURCES_URL, EXPECTED_CONTENT)]
            resources, page = prepare_assets(BASE_URL, testing_page,
                                             join(tmpdirname,
                                                  DIR_NAME))
            for resource, content in zip(resources, EXPECTED_CONTENT):
                link, _ = resource
                assert requests.get(link).text == content
            assert page == expected_page
