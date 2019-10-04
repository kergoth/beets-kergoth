from __future__ import division, absolute_import, print_function

from beets import plugins
from beets.autotag.hooks import AlbumInfo, TrackInfo, Distance


class MockedCandidatePlugin(plugins.BeetsPlugin):
    def __init__(self):
        super(MockedCandidatePlugin, self).__init__()
        self.config.add({
            'source_weight': 0.5,
        })

    def album_distance(self, items, album_info, mapping):
        dist = Distance()
        if hasattr(album_info, 'data_source') and album_info.data_source == 'mocked_candidate':
            dist.add('source', self.config['source_weight'].as_number())
        return dist

    def get_track(self, artist=None):
        return TrackInfo(u'A Track', u'http://foo', length=1, artist=artist or u'An Artist',
                         artist_id=1, data_source=u'mocked_candidate',
                         medium=1, medium_index=1, medium_total=3,
                         media=u'Digital Media', data_url=u'http://foo')

    def get_album(self, artist=None, album=None):
        tracks = [self.get_track(artist)]
        return AlbumInfo(album or u'An Album', u'mocked', artist or u'An Artist', u'http://foo', tracks,
                         year=2019, month=1, mediums=1,
                         day=1, country=u'XW', media=u'Digital Media',
                         data_source=u'mocked_candidate', data_url=u'http://invalid')

    def candidates(self, items, artist, album, va_likely):
        return [self.get_album(artist, album)]

    def album_for_id(self, album_id):
        if album_id == u'mocked':
            return self.get_album()

    def item_candidates(self, item, artist, album):
        return [self.get_track(artist)]

    def track_for_id(self, track_id):
        return self.get_track()
