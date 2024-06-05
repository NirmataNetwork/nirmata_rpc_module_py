import unittest
import asyncio
from unittest.mock import patch, MagicMock
from nirmata_rpc_module.utils import Utils

class TestUtils(unittest.TestCase):
    @patch('nirmata_rpc_module.utils.Utils.delay', new_callable=MagicMock)
    @patch('nirmata_rpc_module.rpc_daemon.RPCDaemon.getheight')
    def test_wait_for_confirmations(self, mock_getheight, mock_delay):
        mock_getheight.side_effect = [
            {'height': 100},
            {'height': 101},
            {'height': 102},
            {'height': 103},
            {'height': 104},
            {'height': 105}
        ]
        daemon_client = MagicMock()
        daemon_client.getheight = mock_getheight

        loop = asyncio.get_event_loop()
        loop.run_until_complete(Utils.wait_for_confirmations(daemon_client, 5))

        self.assertEqual(mock_getheight.call_count, 6)
        self.assertEqual(mock_delay.call_count, 5)

    def test_delay(self):
        loop = asyncio.get_event_loop()
        start_time = loop.time()
        loop.run_until_complete(Utils.delay(1000))
        end_time = loop.time()
        self.assertAlmostEqual(end_time - start_time, 1, places=1)

if __name__ == '__main__':
    unittest.main()