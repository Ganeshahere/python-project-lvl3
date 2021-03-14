import requests
import os
import logging
from page_loader.storage import save
from progress.bar import Bar


def download_resources(resources, dir_for_download):
    if resources:
        if os.path.isdir(dir_for_download):
            logging.warning(f"Directory '{dir_for_download}' "
                    f"already exists. Content may be changed.")
        else:
            os.mkdir(dir_for_download)
            logging.info(f"Directory '{dir_for_download}' is created.")
        bar = Bar('Downloading progress:', fill='*', suffix='%(percent)d%%',
                max=len(resources)
        for resource in resources:
            link, path_to_file = resource
            try:
                save(requests.get(link).content, path_to_file)
                bar.next()
            except requests.exceptions.RequestException as er:
                logging.warning(f"Some resources wasn't downloaded\n{er}")
                continue
        bar.finish()
        logging.debug(f"Resources was downloaded into '{dir_for_download}'")
    else:
        logging.debug('This page has no resources.')
