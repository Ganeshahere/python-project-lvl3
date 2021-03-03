import sys
from os.path import abspath, join
from os import listdir
import tempfile
from page_loader.loading import download
import requests_mock
from urllib.parse import urljoin


with open(abspath('tests/fixtures/page_with_local_links.html')) as file:
    expected_page = file.read()


URL = 'https://ru.hexlet.io/cources'
RESOURCES_LINK = [urljoin(URL, 'assets/professions/nodejs.png'),
                  urljoin(URL, 'assets/application.css'),
                  urljoin(URL, 'packs/js/runtime.js')]


def test_download():
    with open(abspath('tests/fixtures/page_with_global_links.html')) as file:
        testing_page = file.read()
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(URL, text=testing_page)
            m.get(RESOURCES_LINK[0], text=RESOURCES_LINK[0])
            m.get(RESOURCES_LINK[1], text=RESOURCES_LINK[1])
            m.get(RESOURCES_LINK[2], text=RESOURCES_LINK[2])
            file_path = download(URL, tmpdirname)
            with open(file_path, 'r') as file:
                page = file.read()
            assert page == expected_page
            assert len(listdir(tmpdirname)) == 2
            assert len(listdir(join(tmpdirname, 'test-com_file'))) == 3
