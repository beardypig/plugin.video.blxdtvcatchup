import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import urllib2
import xbmcgui
import re

from retrying import retry
from simpleplugin import Plugin

plugin = Plugin()
_ = plugin.initialize_gettext()
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


@retry(stop_max_attempt_number=10, wait_exponential_multiplier=500, wait_exponential_max=5000)
def urlget(url, **kwargs):
    timeout = kwargs.pop("timeout", 10.0)
    req = urllib2.Request(url, **kwargs)
    res = urllib2.urlopen(req, timeout=timeout)
    return res.read()


@plugin.action()
def play(params):
    """
    Finds the streams from tvcatchup.com.
    """
    channel = params.get("channel") or "bbcone"
    name = params.get("name") or channel

    try:
        data = urlget("http://www.tvcatchup.com/watch/{channel}".format(channel=channel),
                      headers={"User-Agent": USER_AGENT})

        match = stream_re.search(data, re.IGNORECASE | re.MULTILINE)

        if match:
            return Plugin.resolve_url(match.group("stream_url"))
        else:
            plugin.log_error("Failed to open stream {0} (Could not find stream URL)".format(channel))
    except Exception as err:
        plugin.log_error("Failed to open stream {0} ({1})".format(channel, err))

    xbmcgui.Dialog().notification(_('Warning'), _('Could not open stream for {0}!').format(name))
    return Plugin.resolve_url(succeeded=False)


@plugin.action()
def root(params):
    items = [{'label': name,
              'url': plugin.get_url(action="play", channel=channel, name=name),
              'is_playable': True,
              'thumb': 'http://new.tvcatchup.info/channel-images/{0}.png'.format(channel)}
             for name, channel in CHANNEL_LIST]
    return Plugin.create_listing(items, sort_methods=[])


if __name__ == '__main__':
    plugin.run()
