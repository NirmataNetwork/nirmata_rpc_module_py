import unittest
import asyncio
from unittest.mock import patch, MagicMock
from nirmata_rpc_module.rpc_wallet import RPCWallet
from nirmata_rpc_module.rpc_daemon import RPCDaemon
from nirmata_rpc_module.utils import Utils
from nirmata_rpc_module.config import Config

class TestRPCWallet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = Config()
        cls.wallet_client = RPCWallet({
            'url': cls.config.wallet_address,
            'username': cls.config.wallet_username,
            'password': cls.config.wallet_password
        })
        cls.daemon_client = RPCDaemon({
            'url': cls.config.daemon_address,
            'username': cls.config.daemon_username,
            'password': cls.config.daemon_password
        })
        cls.utils = Utils()

    def test_get_balance(self):
        response = asyncio.run(self.wallet_client.get_balance())
        self.assertIn('balance', response)
        self.assertIn('unlocked_balance', response)

    def test_get_address(self):
        response = asyncio.run(self.wallet_client.get_address())
        self.assertIn('address', response)

    def test_get_wallet_info(self):
        response = asyncio.run(self.wallet_client.get_wallet_info())
        self.assertIn('address', response)
        self.assertIn('current_height', response)
        self.assertIn('is_watch_only', response)
        self.assertIn('path', response)
        self.assertIn('transfer_entries_count', response)
        self.assertIn('transfers_count', response)
        self.assertIn('utxo_distribution', response)

    def test_get_recent_txs_and_info(self):
        response = asyncio.run(self.wallet_client.get_recent_txs_and_info())
        self.assertIn('last_item_index', response)
        self.assertIn('pi', response)
        self.assertIn('total_transfers', response)
        if 'transfers' in response:
            self.assertIn('transfers', response)

    def test_transfer(self):
        opts = {
            'destinations': [{'amount': 1 * self.config.units, 'address': self.config.integrated_test_address_b}],
            'mixin': 1,
            'fee': 10000000000,
            'comment': 'woot woot'
        }
        response = asyncio.run(self.wallet_client.transfer(opts))
        self.assertIn('tx_hash', response)
        self.assertIn('tx_unsigned_hex', response)
        self.assertIn('tx_size', response)

    def test_store(self):
        response = asyncio.run(self.wallet_client.store())
        self.assertIn('wallet_file_size', response)

    def test_get_payments(self):
        opts = {'payment_id': self.config.payment_id_a}
        response = asyncio.run(self.wallet_client.get_payments(opts))
        if response:
            self.assertIn('payments', response)
            self.assertIn('payment_id', response['payments'][0])

    def test_get_bulk_payments(self):
        opts = {'payment_ids': [self.config.payment_id_a], 'min_block_height': 1}
        response = asyncio.run(self.wallet_client.get_bulk_payments(opts))
        if response:
            self.assertIn('payments', response)
            self.assertIn('payment_id', response['payments'][0])

    def test_make_integrated_address(self):
        opts = {'payment_id': self.config.payment_id_a}
        response = asyncio.run(self.wallet_client.make_integrated_address(opts))
        self.assertEqual(response['integrated_address'], self.config.integrated_test_address_a)

    def test_split_integrated_address(self):
        opts = {'integrated_address': self.config.integrated_test_address_a}
        response = asyncio.run(self.wallet_client.split_integrated_address(opts))
        self.assertEqual(response['payment_id'], self.config.payment_id_a)

    def test_sweep_below(self):
        opts = {
            'address': self.config.integrated_test_address_a,
            'mixin': 1,
            'fee': 10000000000,
            'amount': 1000000000000
        }
        try:
            response = asyncio.run(self.wallet_client.sweep_below(opts))
            self.assertIn('amount_swept', response)
            self.assertIn('amount_total', response)
            self.assertIn('outs_swept', response)
            self.assertIn('outs_total', response)
            self.assertIn('tx_hash', response)
            self.assertIn('tx_unsigned_hex', response)
        except Exception as e:
            self.assertEqual(e.code, -4)

    def test_get_restore_info(self):
        opts = {'seed_password': '123456'}
        response = asyncio.run(self.wallet_client.get_restore_info(opts))
        self.assertEqual(response['seed_phrase'], self.config.test_net_seed_a)

    def test_get_seed_phrase_info(self):
        opts = {'seed_phrase': self.config.test_net_seed_a, 'seed_password': '123456'}
        response = asyncio.run(self.wallet_client.get_seed_phrase_info(opts))
        self.assertIn('hash_sum_matched', response)
        self.assertIn('require_password', response)
        self.assertIn('syntax_correct', response)
        self.assertIn('tracking', response)

if __name__ == '__main__':
    unittest.main()