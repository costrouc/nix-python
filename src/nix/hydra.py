import logging
import subprocess
import json
import tarfile
import os
import io

import requests
import diskcache

logger = logging.getLogger(__name__)


class Hydra:
    ROOT_URL = 'https://hydra.nixos.org'

    def __init__(self, root_url=None):
        self.root_url = root_url or self.ROOT_URL
        self.cache = diskcache.Cache('hydra-cache.db')

    def _in_cache(self, key):
        return key in self.cache

    def _get_cache(self, key):
        return self.cache[key]

    def _set_cache(self, key, data, expire=None):
        self.cache.set(key, data, expire=expire)

    def request(self, url, format='json', force=False):
        if not force and self._in_cache(url):
            logger.info(f'getting url={url} from cache')
            return self._get_cache(url)
        logger.info(f'fetching url={url}')

        if format == 'json':
            response = request.get(url, headers={'Accept': 'application/json'})
            data = response.json()
        elif format == 'text':
            response = request.get(url)
            data = response.content
        else:
            raise ValueError(f'format={format} not supported')

        self._set_cache(url, data)
        return data

    def projects(self):
        return self.request(self.ROOT_URL)

    def project(self, project):
        return self.request(self.ROOT_URL + f'/project/{project}')

    def jobset(self, project, jobset):
        return self.request(self.ROOT_URL + f'/jobset/{project}/{jobset}')

    def evaluations(self, project, jobset):
        return self.request(self.ROOT_URL + f'/jobset/{project}/{jobset}/evals')

    def build(self, build):
        return self.request(self.ROOT_URL + f'/build/{build}')

    def build_log(self, build):
        return self.request(self.ROOT_URL + f'/build/{build}/nixlog/1/raw', format='text')


def print_project(project):
    print(f'project={project["name"]} displayname={project["name"]}')

def fetch_nixpkgs(evaluation):
    root_directory = '/tmp/hydra'
    os.makedirs(root_directory, exist_ok=True)

    revision = evaluation['jobsetevalinputs']['nixpkgs']['revision']
    nixpkgs_directory = os.path.join(root_directory, f'nixpkgs-{revision}')

    if not os.path.isdir(nixpkgs_directory):
        url = f'https://github.com/NixOS/nixpkgs/archive/{revision}.tar.gz'
        t = tarfile.open(fileobj=io.BytesIO(requests.get(url).content))
        t.extractall(root_directory)

    return nixpkgs_directory


def get_derivation(directory, attribute):
    output = subprocess.check_output(f'nix show-derivation -f {directory}/default.nix {attribute}', shell=True)
    return json.loads(output.decode('utf-8'))
