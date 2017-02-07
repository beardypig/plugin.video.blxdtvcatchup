from urllib import quote

from xbmcswift2 import Plugin

CHANNEL_LIST = {
    ("BBC One", "bbcone"),
    ("BBC Two", "bbctwo"),
    ("ITV", "itv"),
    ("Channel 4", "channel4"),
    ("Channel 5", "five"),
    ("BBC News", "bbcnews"),
    ("CBBC", "cbbc"),
    ("CBeeBies", "cbeebies"),
    ("BBC Four", "bbcfour"),
    ("MillenniumTV", "millenniumtv"),
    ("Quest", "quest"),
    ("VIVA", "viva"),
    ("BBC Parliament", "bbcparliament"),
    ("RT", "rt"),
    ("BBC Red Button", "bbcredbutton"),
    ("Sail TV", "sailtv"),
    ("Community Channel", "communitychannel"),
    ("S4C", "s4c"),
    ("BBC Alba", "bbcalba"),
    ("TV Warehouse", "tvwarehouse"),
    ("QVC", "qvc"),
    ("QVC Beauty", "qvcbeauty"),
    ("QVC Style", "qvcstyle"),
    ("QVC Extra", "qvcextra"),
    ("Al Jazeera", "aljazeera"),
    ("CCTV News", "cctvnews"),
    ("Ideal World", "idealworld"),
    ("Ideal Extra", "idealextra"),
    ("Create and Craft", "createandcraft"),
    ("Craft Extra", "craftextra"),
}

plugin = Plugin()


@plugin.route('/')
def index():
    items = [{'label': name,
              'path': "plugin://plugin.video.streamlink/play?url={0}".format(
                  quote("http://tvcatchup.com/watch/{0}".format(shortname))
              ),
              'is_playable': True,
              'thumbnail': 'http://new.tvcatchup.info/channel-images/{0}.png'.format(shortname)}
             for name, shortname in CHANNEL_LIST]
    return plugin.finish(items, sort_methods=[])


if __name__ == '__main__':
    plugin.run()
