import pytest
import unittest
import sys
import os.path
# force the lib directory in to the python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from mock import patch
from tvcatchup import TVCatchup, TVCatchupBlocked

online = pytest.mark.skipif(
    not pytest.config.getoption("--online"),
    reason="online test"
)



class TestTVCatchup(unittest.TestCase):
    def test_region_lookup(self):
        # default to London
        self.assertEqual(1, TVCatchup.lookup_region("invalid_name"))
        self.assertEqual(1, TVCatchup.lookup_region("Greater London"))
        self.assertEqual(43, TVCatchup.lookup_region("Northumberland"))

    def test_create(self):
        tvcu = TVCatchup(region=1)
        self.assertEqual(1, tvcu.region)

    @patch('tvcatchup.TVCatchup.api_call')
    def test_channels(self, api_call):
        tvcu = TVCatchup()
        tvcu.channels()
        api_call.assert_called_with("appcache")

    @patch('tvcatchup.TVCatchup.api_call')
    def test_stream(self, api_call):
        api_call.return_value = {"stream": "http://tvcatchup.com/example",
                                 "blocked": False}
        tvcu = TVCatchup()
        tvcu.stream(1)
        api_call.assert_called_with("stream/1")

    @patch('tvcatchup.TVCatchup.api_call')
    def test_stream_blocked(self, api_call):
        api_call.return_value = {"blocked": True,
                                 "blocked_message": "blocked"}
        tvcu = TVCatchup()
        self.assertRaises(TVCatchupBlocked, tvcu.stream, 1)
        api_call.assert_called_with("stream/1")

    @online
    def test_channels_online(self):
        tvcu = TVCatchup()
        channels = tvcu.channels()
        self.assertNotEqual(0, len(channels))

    @online
    def test_streams_online(self):
        tvcu = TVCatchup()
        channels = tvcu.channels()
        self.assertNotEqual(0, len(channels))
        channel_id = channels[0]["id"]
        stream = tvcu.stream(channel_id)
        self.assertIsNotNone(stream)
