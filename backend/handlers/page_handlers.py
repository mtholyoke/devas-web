from __future__ import absolute_import
import datetime
import matplotlib
import numpy as np
import os
import tornado.web
from collections import defaultdict
from superman.baseline import BL_CLASSES

from .base import BaseHandler

MPL_JS = sorted(os.listdir(os.path.join(matplotlib.__path__[0],
                                        'backends/web_backend/jquery/js')))


def compute_step(lb, ub, kind):
  if kind == 'integer':
    return 1
  if kind == 'log':
    lb, ub = np.log10((lb, ub))
  return (ub - lb) / 100.

blr_kwargs = dict(
    bl_classes=sorted((key, bl()) for key, bl in BL_CLASSES.items()),
    compute_step=compute_step, log10=np.log10)


class MainPage(BaseHandler):
  def get(self):
    logged_in = self.current_user is not None
    # tuples of (title, relative_url, description) for subpages
    subpage_info = [(p.title, link[1:], p.description) for link, p in routes
                    if issubclass(p, Subpage) and (logged_in or p.public)]
    self.render('index.html', page_title='Project Superman: Web Interface',
                subpage_info=subpage_info, mpl_js=MPL_JS, logged_in=logged_in)


class LoginPage(BaseHandler):
  def get(self):
    if self.get_argument('logout', False):
      self.clear_cookie('user')
      self.redirect('/')
    else:
      self.render('login.html',
                  message=self.get_argument('msg', ''),
                  next=self.get_argument('next', '/'))

  def post(self):
    password = self.get_argument('pw')
    if password == 'superman':  # Elite security
      # Doesn't matter what value it has, just needs to be there.
      self.set_secure_cookie('user', 'authenticated')
      self.redirect(self.get_argument('next', '/'))
    else:
      self.clear_cookie('user')
      self.redirect('/login?msg=Login%20failed')


class Subpage(BaseHandler):
  '''Base class which renders the common template arguments for subpages.
  Requires that subclasses define the following properties:
   * template    - name of template html file
   * title       - title of the page
   * description - sentence describing the page
   * figsize     - figure size in inches, as a tuple of (width, height)
  '''
  figsize = None
  public = True

  def render(self, **kwargs):
    kwargs['page_title'] = self.title
    kwargs['mpl_js'] = MPL_JS
    if self.figsize is not None:
      kwargs['ws_uri'] = "ws://{req.host}/".format(req=self.request)
      if 'fig_id' not in kwargs:
        kwargs['fig_id'] = self.application.register_new_figure(self.figsize)
    return BaseHandler.render(self, self.template, **kwargs)


class DatasetsPage(Subpage):
  template = 'datasets.html'
  title = 'Datasets'
  description = 'Browse all spectroscopy datasets.'

  def get(self):
    self.render(dt=datetime.datetime.fromtimestamp,
                datasets=self.all_datasets())


class DataExplorerPage(Subpage):
  template = 'explorer.html'
  title = 'Dataset Explorer'
  description = 'Filter and plot datasets.'
  figsize = (14, 6)

  def get(self):
    ds_tree = defaultdict(dict)
    for ds in self.all_datasets():
      is_traj = ds.num_dimensions() is None
      ds_tree[ds.kind][ds.name] = (hash(ds), is_traj)
    self.render(ds_tree=ds_tree, logged_in=(self.current_user is not None),
                ds_kind=self.get_argument('ds_kind', ''),
                ds_name=self.get_argument('ds_name', ''), **blr_kwargs)


class BaselinePage(Subpage):
  template = 'baseline.html'
  title = 'Baseline Correction'
  description = 'Explore baseline correction algorithms.'
  figsize = (8, 8)

  def get(self):
    # Do the figure creation manually, due to subplot shenanigans
    fignum = self.application.register_new_figure(self.figsize)
    fig_data = self.application.figure_data[fignum]
    fig = fig_data.figure
    ax1 = fig.add_subplot(211)
    fig.add_subplot(212, sharex=ax1)
    self.render(datasets=self.all_datasets(), fig_id=fignum, **blr_kwargs)


class SearcherPage(Subpage):
  template = 'search.html'
  title = 'Spectrum Matching'
  description = 'Match a spectrum against a target dataset.'
  figsize = (8, 4)

  def get(self):
    pkey_ds = [d for d in self.all_datasets() if d.pkey is not None]
    self.render(datasets=pkey_ds, **blr_kwargs)


class PeakFitPage(Subpage):
  template = 'peakfit.html'
  title = 'Peak Fitting'
  description = 'Explore peak fitting algorithms.'
  figsize = (8, 4)

  def get(self):
    self.render(datasets=self.all_datasets(), **blr_kwargs)


class DatasetImportPage(Subpage):
  template = 'import.html'
  title = 'Dataset Import'
  description = 'Upload new datasets to Superman.'
  public = False

  @tornado.web.authenticated
  def get(self):
    self.render(ds_kinds=self.dataset_kinds())


class DebugPage(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.render('debug.html', page_title='Debug View', mpl_js=[],
                figure_data=self.application.figure_data)


# Define the routes for each page.
routes = [
    (r'/', MainPage),
    (r'/datasets', DatasetsPage),
    (r'/explorer', DataExplorerPage),
    (r'/baseline', BaselinePage),
    (r'/search', SearcherPage),
    (r'/peakfit', PeakFitPage),
    (r'/login', LoginPage),
    (r'/import', DatasetImportPage),
    (r'/debug', DebugPage),
]