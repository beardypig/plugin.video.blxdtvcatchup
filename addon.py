import urllib2
import xbmcplugin
import xbcmgui
import re
from simpleplugin import Plugin

plugin = Plugin()

USER_AGENT = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/41.0.2228.0 Safari/537.36")
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



stream_re = re.compile(r'''(?P<q>["'])(?P<stream_url>https?://.*m3u8\?.*clientKey=.*?)(?P=q)''')


@plugin.action()
def play(params):
    """
    Finds the streams from tvcatchup.com.
    """
    channel = params.get("channel") or "bbcone"
    name = params.get("name") or channel
    req = urllib2.Request("http://www.tvcatchup.com/watch/{channel}".format(channel=channel),
                          headers={"User-Agent": USER_AGENT})
    res = urllib2.urlopen(req)
    match = stream_re.search(res.read(), re.IGNORECASE | re.MULTILINE)

    if match:
        return Plugin.resolve_url(match.group("stream_url"))
    else:
        xbcmgui.Dialog().notification('Warning', 'Could not open stream for {0}!'.format(name))


@plugin.action()
def root(params):
    items = [{'label': name,
              'url': plugin.get_url(action="play", channel=channel, name=name),
              'is_playable': True,
              'thumb': 'http://new.tvcatchup.info/channel-images/{0}.png'.format(channel)}
             for name, channel in CHANNEL_LIST]
    return Plugin.create_listing(items, sort_methods=[xbmcplugin.SORT_METHOD_NONE])


if __name__ == '__main__':
    plugin.run()
