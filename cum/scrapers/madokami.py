from bs4 import BeautifulSoup
from contextlib import closing
from cum import config, exceptions
from cum.scrapers.base import BaseChapter, BaseSeries
from urllib.parse import urljoin
import re
import requests

fallback_re = re.compile(r'\- (.*) (?:\[(.*)\])?')
name_re = re.compile(r'-? c([0-9-]+).*?(?: \[(.*)\])?\.')


class MadokamiSeries(BaseSeries):
    url_re = re.compile(r'https://manga\.madokami\.al/(?:Manga|Raws)/[^.]+$')

    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(*config
                                                        .get().madokami.login)
        r = self.session.get(url)
        if r.status_code == 401:
            raise exceptions.LoginError('Madokami login error')
        self.soup = BeautifulSoup(r.text, config.get().html_parser)
        self.chapters = self.get_chapters()

    def get_chapters(self):
        try:
            rows = (self.soup
                    .find('table', class_='mobile-files-table')
                    .find_all('tr'))
        except AttributeError:
            raise exceptions.ScrapingError()
        chapters = []
        for row in rows[1:]:
            # If the Read link cannot be found in the current row, the row is
            # assumed to be a non-manga file uploaded to the directory and will
            # thus be skipped.
            if not row.find('a', text='Read'):
                continue

            link = row.find('a')

            url = urljoin(self.url, link.get('href'))

            name = link.string
            name_parts = re.search(name_re, name)
            if not name_parts:
                name_parts = re.search(fallback_re, name)
            try:
                chapter = name_parts.group(1)
            except AttributeError:
                continue
            if name_parts.group(2):
                groups = name_parts.group(2).split('][')
            else:
                groups = []

            c = MadokamiChapter(name=self.name, alias=self.alias,
                                chapter=chapter, url=url, groups=groups,
                                session=self.session)
            chapters.append(c)
        return chapters

    @property
    def name(self):
        return self.soup.find('span', class_='title').string


class MadokamiChapter(BaseChapter):
    url_re = re.compile(r'https://manga\.madokami\.al/Manga/.*/.*/.*\..*')
    uses_pages = False

    def __init__(self, *args, **kwargs):
        self.session = kwargs.get("session", requests.Session())
        super().__init__(*args, **kwargs)

    def download(self):
        if not self.session.auth:
            self.session.auth = requests.auth.HTTPBasicAuth(*config
                                                            .get()
                                                            .madokami.login)
        with closing(self.session.get(self.url, stream=True)) as r:
            if r.status_code == 401:
                raise exceptions.LoginError('Madokami login error')
            total_length = r.headers.get('content-length')
            with open(self.filename, 'wb') as f:
                if total_length is None:
                    f.write(r.content)
                else:
                    total_length = int(total_length)
                    with self.progress_bar(total_length) as bar:
                        for chunk in r.iter_content(chunk_size=4096):
                            if chunk:
                                bar.update(len(chunk))
                                f.write(chunk)
                    f.flush()

    def from_url(url):
        series_url = re.search(r'(.*manga\.madokami\.al/.*/)', url).group(1)
        series = MadokamiSeries(series_url)
        for chapter in series.chapters:
            if chapter.url == url:
                return chapter
        return None


# !LM Do I need BaseWatchlist here?
class MadokamiWatchlist():
    watched_re = re.compile(r'https://manga\.madokami\.al/user/watched.opml')
    url_re = re.compile(r'https://manga\.madokami\.al/Manga/[^.]+$')

    def __init__(self, url, **kwargs):
        super().__init__()
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(*config
                                                        .get().madokami.login)
        r = self.session.get(url)
        if r.status_code == 401:
            raise exceptions.LoginError('Madokami login error')
        # !LM Should this support a config option?
        self.soup = BeautifulSoup(r.content,'xml')
        self.followed = self.get_watched()

    def get_watched(self):
        try:
            outlines = (self.soup
                        .find_all('outline'))
        except AttributeError:
            raise exceptions.ScrapingError()
        url_list = []
        # for o in outlines:
        #     print(type(o.get('htmlUrl')))
        for o in outlines:
            # Some series on Madokami have both translated and raw directories.
            # The regex is used here to make sure that only translated series
            # are added to the db.
            h = o.get('htmlUrl')
            # Madokami's OPML formatting is weird, and sometimes there will be
            # type:none exceptions to the rule here, so they should be checked for.
            if type(h) is str:
                match = re.search(self.url_re, h)
                if match:
                    url_list.append(h)
        return url_list