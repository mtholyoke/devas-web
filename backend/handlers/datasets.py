from __future__ import absolute_import, print_function, division
import logging
import os
import tornado.web
import yaml

from .common import BaseHandler
from ..thread_pool import run_in_thread
from ..web_datasets import DATASETS


class RefreshHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('''<form action='refresh' method='POST'>
                  <input type='submit' value='Refresh Data'>
                  </form>''')

    async def post(self):
        logging.info('Refreshing datasets')
        for ds in self.all_datasets():
            await run_in_thread(ds.reload)
        self.redirect('/datasets')


class RemovalHandler(BaseHandler):
    def post(self):
        ds = self.request_one_ds('kind', 'name')
        if not ds.user_added:
            return self.visible_error(403, 'Cannot remove this dataset.')
        logging.info('Removing user-added dataset: %s', ds)
        del DATASETS[ds.kind][ds.name]
        self.redirect('/datasets')
        # Remove the dataset from user-uploaded files.
        config_path = os.path.join(os.path.dirname(__file__),
                                   '../../uploads/user_data.yml')
        if os.path.exists(config_path):
            config = yaml.safe_load(open(config_path))
            entry = config[ds.kind].pop(ds.name)
            os.remove(entry['file'])
            yaml.safe_dump(config, open(config_path, 'w'), allow_unicode=True)


class NightlyRefreshHandler(BaseHandler):
    async def post(self):
        ip = self.request.remote_ip
        allowed_ips = self.application.settings['nightly_refresh_ips']
        if ip not in allowed_ips:
            logging.info('Invalid remote ip {} for nightly refresh'.format(ip))
            self.redirect('/login?next=%2Frefresh')
            return
        logging.info('Refreshing datasets for ip {} after nightly'.format(ip))
        for ds in self.all_datasets():
            await run_in_thread(ds.reload)
        return


routes = [
    (r'/_remove_dataset', RemovalHandler),
    (r'/refresh', RefreshHandler),
    (r'/nightly-refresh', NightlyRefreshHandler),
]
