import unittest
import asyncio
from unittest.mock import patch, MagicMock
from nirmata_rpc_module.rpc_daemon import RPCDaemon
from nirmata_rpc_module.config import Config

class TestRPCDaemon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.daemon_client = RPCDaemon({
            'url': cls.config.daemon_address,
            'username': cls.config.daemon_username,
            'password': cls.config.daemon_password
        })

    def test_get_block_count(self):
        response = asyncio.run(self.daemon_client.get_block_count())
        self.assertIn('status', response)
        self.assertIn('count', response)
        self.assertGreater(response['count'], 0)

    def test_on_get_block_hash(self):
        opts = {'height': self.config.block_height}
        response = asyncio.run(self.daemon_client.on_get_block_hash(opts))
        self.assertEqual(response, self.config.block_hash)

    def test_get_block_header_by_hash(self):
        opts = {'hash': self.config.block_hash}
        response = asyncio.run(self.daemon_client.get_block_header_by_hash(opts))
        self.assertIn('block_header', response)
        self.assertIn('height', response['block_header'])
        self.assertEqual(response['block_header']['height'], self.config.block_height)

    def test_get_block_header_by_height(self):
        opts = {'height': self.config.block_height}
        response = asyncio.run(self.daemon_client.get_block_header_by_height(opts))
        self.assertIn('block_header', response)
        self.assertIn('hash', response['block_header'])
        self.assertEqual(response['block_header']['hash'], self.config.block_hash)

    def test_get_alias_details(self):
        opts = {'alias': self.config.alias}
        response = asyncio.run(self.daemon_client.get_alias_details(opts))
        self.assertIn('alias_details', response)
        self.assertIn('address', response['alias_details'])

    def test_get_alias_by_address(self):
        opts = {'address': self.config.stagenet_wallet_address}
        response = asyncio.run(self.daemon_client.get_alias_by_address(opts))
        self.assertIn('alias_info', response)
        self.assertIn('alias', response['alias_info'])

    def test_get_alias_reward(self):
        opts = {'alias': self.config.alias}
        response = asyncio.run(self.daemon_client.get_alias_reward(opts))
        self.assertIn('reward', response)
        self.assertEqual(response['reward'], self.config.alias_fee)

    def test_get_blocks_details(self):
        opts = {'height_start': 100, 'count': 1}
        response = asyncio.run(self.daemon_client.get_blocks_details(opts))
        self.assertIn('blocks', response)

    def test_get_tx_details(self):
        opts = {'tx_hash': self.config.txids[0]}
        response = asyncio.run(self.daemon_client.get_tx_details(opts))
        self.assertIn('tx_info', response)

    def test_search_by_id(self):
        opts = {'id': self.config.txids[0]}
        response = asyncio.run(self.daemon_client.search_by_id(opts))
        self.assertIn('status', response)
        self.assertEqual(response['status'], 'OK')
        self.assertIn('types_found', response)
        self.assertIn('tx', response['types_found'])

    def test_get_block_template(self):
        opts = {'wallet_address': self.config.stagenet_wallet_address, 'extra_text': 'foobar'}
        response = asyncio.run(self.daemon_client.get_block_template(opts))
        self.assertIn('status', response)
        self.assertEqual(response['status'], 'OK')

    def test_get_info(self):
        opts = {'flags': 4294967295}
        response = asyncio.run(self.daemon_client.get_info(opts))
        self.assertIn('alias_count', response)

    def test_get_out_info(self):
        opts = {'amount': 1000000000, 'i': 2}
        response = asyncio.run(self.daemon_client.get_out_info(opts))
        self.assertIn('out_no', response)
        self.assertIn('tx_id', response)

    def test_get_multisig_info(self):
        opts = {'ms_id': '5698B701F989214770C2CFF71166408C13D97E907AA4654781DC05E6994E59A5'}
        response = asyncio.run(self.daemon_client.get_multisig_info(opts))
        self.assertIn('out_no', response)
        self.assertIn('tx_id', response)

    def test_get_all_alias_details(self):
        response = asyncio.run(self.daemon_client.get_all_alias_details())
        self.assertIn('aliases', response)
        self.assertIn('status', response)

    def test_get_aliases(self):
        opts = {'offset': 0, 'count': 2}
        response = asyncio.run(self.daemon_client.get_aliases(opts))
        self.assertIn('aliases', response)
        self.assertIn('status', response)

    def test_get_pool_txs_details(self):
        response = asyncio.run(self.daemon_client.get_pool_txs_details())
        self.assertIn('status', response)

    def test_get_pool_txs_brief_details(self):
        opts = {'ids': ['c99c2f9a53e4bab5d08f9820ee555d62059e0e9bf799fbe07a6137aac607f4e8']}
        response = asyncio.run(self.daemon_client.get_pool_txs_brief_details(opts))
        self.assertIn('status', response)

    def test_get_all_pool_tx_list(self):
        response = asyncio.run(self.daemon_client.get_all_pool_tx_list())
        self.assertIn('status', response)

    def test_get_main_block_details(self):
        opts = {'id': '5698B701F989214770C2CFF71166408C13D97E907AA4654781DC05E6994E59A5'}
        response = asyncio.run(self.daemon_client.get_main_block_details(opts))
        self.assertIn('block_details', response)
        self.assertIn('status', response)

    def test_get_alt_block_details(self):
        opts = {'id': '5698B701F989214770C2CFF71166408C13D97E907AA4654781DC05E6994E59A5'}
        with self.assertRaises(Exception) as context:
            asyncio.run(self.daemon_client.get_alt_block_details(opts))
        self.assertEqual(context.exception.code, -14)

    def test_get_alt_blocks_details(self):
        opts = {'offset': 0, 'count': 2}
        response = asyncio.run(self.daemon_client.get_alt_blocks_details(opts))
        self.assertIn('status', response)

    def test_reset_transaction_pool(self):
        response = asyncio.run(self.daemon_client.reset_transaction_pool())
        self.assertIn('status', response)
        self.assertEqual(response['status'], 'OK')

    def test_get_current_core_tx_expiration_median(self):
        response = asyncio.run(self.daemon_client.get_current_core_tx_expiration_median())
        self.assertIn('status', response)
        self.assertEqual(response['status'], 'OK')

    def test_marketplace_global_get_offers_ex(self):
        response = asyncio.run(self.daemon_client.marketplace_global_get_offers_ex())
        self.assertIn('status', response)
        self.assertEqual(response['status'], 'OK')

    def test_getheight(self):
        response = asyncio.run(self.daemon_client.getheight())
        self.assertIn('height', response)
        self.assertIn('status', response)

    def test_gettransactions(self):
        opts = {'txs_hashes': ['809f9656da9d0681ed6ae3c51d544834962750cc46d4c175ed32531c2fa293af']}
        response = asyncio.run(self.daemon_client.gettransactions(opts))
        self.assertIn('status', response)

    def test_sendrawtransaction(self):
        opts = {'tx_as_text': '809f9656da9d0681ed6ae3c51d544834962750cc46d4c175ed32531c2fa293af'}
        response = asyncio.run(self.daemon_client.sendrawtransaction(opts))
        self.assertIn('status', response)

    def test_force_relay(self):
        opts = {'tx_as_hex': ['809f9656da9d0681ed6ae3c51d544834962750cc46d4c175ed32531c2fa293af']}
        response = asyncio.run(self.daemon_client.force_relay(opts))
        self.assertIn('status', response)

    def test_start_mining(self):
        opts = {'miner_address': self.config.stagenet_wallet_address, 'thread_count': 1}
        response = asyncio.run(self.daemon_client.start_mining(opts))
        self.assertIn('status', response)

    def test_stop_mining(self):
        response = asyncio.run(self.daemon_client.stop_mining())
        self.assertIn('status', response)

    def test_get_info_legacy(self):
        response = asyncio.run(self.daemon_client.get_info_legacy())
        self.assertIn('alias_count', response)
        self.assertIn('alt_blocks_count', response)
        self.assertIn('block_reward', response)
        self.assertIn('current_blocks_median', response)
        self.assertIn('current_max_allowed_block_size', response)
        self.assertIn('current_network_hashrate_350', response)
        self.assertIn('current_network_hashrate_50', response)
        self.assertIn('daemon_network_state', response)
        self.assertIn('default_fee', response)
        self.assertIn('expiration_median_timestamp', response)
        self.assertIn('grey_peerlist_size', response)
        self.assertIn('height', response)
        self.assertIn('incoming_connections_count', response)
        self.assertIn('last_block_hash', response)
        self.assertIn('last_block_size', response)
        self.assertIn('last_block_timestamp', response)
        self.assertIn('last_block_total_reward', response)
        self.assertIn('last_pos_timestamp', response)
        self.assertIn('last_pow_timestamp', response)
        self.assertIn('max_net_seen_height', response)
        self.assertIn('mi', response)
        self.assertIn('minimum_fee', response)
        self.assertIn('net_time_delta_median', response)
        self.assertIn('offers_count', response)
        self.assertIn('outgoing_connections_count', response)
        self.assertIn('outs_stat', response)
        self.assertIn('performance_data', response)
        self.assertIn('pos_allowed', response)
        self.assertIn('pos_block_ts_shift_vs_actual', response)
        self.assertIn('pos_diff_total_coins_rate', response)
        self.assertIn('pos_difficulty', response)
        self.assertIn('pos_sequence_factor', response)
        self.assertIn('pow_difficulty', response)
        self.assertIn('pow_sequence_factor', response)
        self.assertIn('seconds_for_10_blocks', response)
        self.assertIn('seconds_for_30_blocks', response)
        self.assertIn('status', response)
        self.assertIn('synchronization_start_height', response)
        self.assertIn('synchronized_connections_count', response)
        self.assertIn('total_coins', response)
        self.assertIn('transactions_cnt_per_day', response)
        self.assertIn('transactions_volume_per_day', response)
        self.assertIn('tx_count', response)
        self.assertIn('tx_count_in_last_block', response)
        self.assertIn('tx_pool_performance_data', response)
        self.assertIn('tx_pool_size', response)
        self.assertIn('white_peerlist_size', response)

    def test_get_last_block_header(self):
        response = asyncio.run(self.daemon_client.get_last_block_header())
        self.assertIn('block_header', response)
        self.assertIn('depth', response['block_header'])
        self.assertIn('difficulty', response['block_header'])
        self.assertIn('hash', response['block_header'])
        self.assertIn('height', response['block_header'])
        self.assertIn('major_version', response['block_header'])
        self.assertIn('minor_version', response['block_header'])
        self.assertIn('nonce', response['block_header'])
        self.assertIn('orphan_status', response['block_header'])
        self.assertIn('prev_hash', response['block_header'])
        self.assertIn('reward', response['block_header'])
        self.assertIn('timestamp', response['block_header'])

    def test_submit_block(self):
        opts = {'blobs': ['0707e6bdfedc053771512f1bc27c62731ae9e8f2443db64ce742f4e57f5cf8d393de28551e441a0000000002fb830a01ffbf830a018cfe88bee283060274c0aae2ef5730e680308d9c00b6da59187ad0352efe3c71d36eeeb28782f29f2501bd56b952c3ddc3e350c2631d3a5086cac172c56893831228b17de296ff4669de020200000000']}
        with self.assertRaises(Exception) as context:
            asyncio.run(self.daemon_client.submit_block(opts))
        self.assertEqual(context.exception.code, -6)

if __name__ == '__main__':
    unittest.main()