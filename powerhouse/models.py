from django.db import models
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.http import Http404

class Tree:
    def __init__(self, data):
        self.data = data
        self.themes = list()
        self.populate_tree()

    def to_json(self):
      return {
        'themes': [x.to_json() for x in self.themes]
      }

    def populate_tree(self):
      for x in self.data:
        self.themes.append(Theme(x['id'], x['name'], x['sub_themes']))

    def prune(self, indicator_ids):
      for t in self.themes:
        for st in t.sub_themes:
          for c in st.categories:
            for i in c.indicators:
              if i.id in indicator_ids:
                i.usable = c.usable = st.usable = t.usable = True

            c.indicators = [x for x in c.indicators if x.usable]
          st.categories = [x for x in st.categories if x.usable]
        t.sub_themes = [x for x in t.sub_themes if x.usable]
      self.themes = [x for x in self.themes if x.usable]

class Theme:
    def __init__(self, id, name, sub_themes):
      self.id = id
      self.name = name
      self.sub_themes = list()
      self.populate_sub_themes(sub_themes)
      self.usable = False

    def to_json(self):
      return {
          'id': self.id,
          'name': self.name,
          'sub_themes': [x.to_json() for x in self.sub_themes]
      }

    def populate_sub_themes(self, sub_themes):
      for x in sub_themes:
        self.sub_themes.append(SubTheme(x))

class SubTheme:
    def __init__(self, sub_theme):
      self.id = sub_theme['id']
      self.name = sub_theme['name']
      self.categories = list()
      self.populate_categories(sub_theme['categories'])
      self.usable = False

    def to_json(self):
      return {
          'categories': [x.to_json() for x in self.categories],
          'id': self.id,
          'name': self.name
      }

    def populate_categories(self, categories):
      for x in categories:
        self.categories.append(Category(x))

class Category:
    def __init__(self, category):
      self.indicators = list()
      self.id = category['id']
      self.name = category['name']
      self.unit = category['unit']
      self.populate_indicators(category['indicators'])
      self.usable = False

    def to_json(self):
      return {
          'id': self.id,
          'indicators': [x.to_json() for x in self.indicators],
          'name': self.name,
          'unit': self.unit
      }

    def populate_indicators(self, indicators):
      for x in indicators:
        self.indicators.append(Indicator(x['id'], x['name']))


class Indicator:
  def __init__(self, id, name):
    self.id = id
    self.name = name
    self.usable = False

  def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class TreeAPI():
    def __init__(self, name):
        self.url = 'https://kf6xwyykee.execute-api.us-east-1.amazonaws.com/production/tree/'+name

    def get(self):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 500 ])
        s.mount('https://', HTTPAdapter(max_retries=retries))
        res = s.get(url = self.url)
        if res.status_code == 404:
          raise Http404()
        else:
          return s.get(url = self.url).json()
