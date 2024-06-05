import requests
from pqueue import PQueue
import rpc_helpers

def parse_wallet_response(res):
    if res.status_code == 200:
        data = res.json()
        if 'error' in data:
            error = Exception('HTTP Error!')
            error.code = data['error']['code']
            error.message = data['error']['message']
            raise error
        if 'result' in data:
            return data['result']
        else:
            error = Exception('RPC Error!')
            error.code = data['error']['code']
            error.message = data['error']['message']
            raise error
    else:
        error = Exception('HTTP Error!')
        error.code = res.status_code
        error.message = res.text
        raise error

class RPCWallet:
    def __init__(self, config):
        self.queue = PQueue(concurrency=1)
        self.http_client = requests.Session()
        self.http_client.headers.update({'Content-Type': 'application/json'})
        self.json_address = f"{config['url']}/json_rpc"
        self.config = config

    def reset_nonces(self):
        return self.http_client.reset_nonces()

    def ssl_reject_unauthorized(self, value):
        self.http_client.verify = value
        return value

    async def get_address(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'getaddress')

    async def get_wallet_info(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'get_wallet_info')

    async def get_recent_txs_and_info(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'get_recent_txs_and_info')

    async def get_balance(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'getbalance')

    async def get_bulk_payments(self, opts):
        rpc_helpers.check_mandatory_parameters({
            'payment_ids': 'ArrayOfPaymentIds',
            'min_block_height': 'Integer'
        }, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'get_bulk_payments', opts)

    async def get_payments(self, opts):
        rpc_helpers.check_mandatory_parameters({'payment_id': 'PaymentId'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'get_payments', opts)

    async def get_mining_history(self, opts):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'get_mining_history', opts)

    async def make_integrated_address(self, opts):
        rpc_helpers.check_optional_parameters_type({'payment_id': 'PaymentId'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'make_integrated_address', opts)

    async def sign_transfer(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_unsigned_hex': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'sign_transfer', opts)

    async def split_integrated_address(self, opts):
        rpc_helpers.check_mandatory_parameters({'integrated_address': 'Address'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'split_integrated_address', opts)

    async def store(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'store')

    async def submit_transfer(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_signed_hex': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'submit_transfer', opts)

    async def get_restore_info(self, opts):
        rpc_helpers.check_mandatory_parameters({'seed_password': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'get_restore_info', opts)

    async def get_seed_phrase_info(self, opts):
        rpc_helpers.check_mandatory_parameters({'seed_password': 'String', 'seed_phrase': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'get_seed_phrase_info', opts)

    async def sweep_below(self, opts):
        rpc_helpers.check_mandatory_parameters({
            'mixin': 'Integer',
            'address': 'Address',
            'fee': 'Integer',
            'amount': 'Integer'
        }, opts)
        rpc_helpers.check_optional_parameters_type({'payment_id_hex': 'PaymentId'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'sweep_below', opts)

    async def search_for_transactions(self, opts):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'search_for_transactions', opts)

    async def transfer(self, opts):
        rpc_helpers.check_mandatory_parameters({
            'destinations': 'ArrayOfAmountAddress',
            'mixin': 'Integer',
            'fee': 'Integer'
        }, opts)
        rpc_helpers.check_optional_parameters_type({
            'payment_id': 'PaymentId',
            'comment': 'String',
            'push_payer': 'Boolean',
            'hide_receiver': 'Boolean',
            'service_entries_permanent': 'Boolean'
        }, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'transfer', opts)

    async def contracts_send_proposal(self, opts):
        rpc_helpers.check_mandatory_parameters({'details': 'ContractPrivateDetails'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'contracts_send_proposal', opts)

    async def contracts_accept_proposal(self, opts):
        rpc_helpers.check_mandatory_parameters({'contract_id': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'contracts_accept_proposal', opts)

    async def contracts_get_all(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'contracts_get_all')

    async def contracts_release(self, opts):
        rpc_helpers.check_mandatory_parameters({'contract_id': 'String', 'release_type': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'contracts_release', opts)

    async def contracts_request_cancel(self, opts):
        rpc_helpers.check_mandatory_parameters({
            'contract_id': 'String',
            'expiration_period': 'Integer',
            'fee': 'Integer'
        }, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'contracts_request_cancel', opts)

    async def contracts_accept_cancel(self, opts):
        rpc_helpers.check_mandatory_parameters({'contract_id': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'contracts_accept_cancel', opts)

    async def marketplace_get_offers_ex(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'marketplace_get_offers_ex')

    async def marketplace_push_offer(self, opts):
        rpc_helpers.check_mandatory_parameters({'od': 'OfferStructure'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'marketplace_push_offer', opts)

    async def marketplace_push_update_offer(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_id': 'String', 'od': 'OfferStructure'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'marketplace_push_update_offer', opts)

    async def marketplace_cancel_offer(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_id': 'String', 'fee': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'marketplace_cancel_offer', opts)

    async def atomics_create_htlc_proposal(self, opts):
        rpc_helpers.check_mandatory_parameters({
            'amount': 'Integer',
            'counterparty_address': 'String',
            'lock_blocks_count': 'Integer'
        }, opts)
        rpc_helpers.check_optional_parameters_type({'htlc_hash': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'atomics_create_htlc_proposal', opts)

    async def atomics_get_list_of_active_htlc(self, opts):
        rpc_helpers.check_mandatory_parameters({'income_redeem_only': 'Boolean'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'atomics_get_list_of_active_htlc', opts)

    async def atomics_redeem_htlc(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_id': 'String', 'origin_secret_as_hex': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'atomics_redeem_htlc', opts)

    async def atomics_check_htlc_redeemed(self, opts):
        rpc_helpers.check_mandatory_parameters({'htlc_tx_id': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_wallet_response, 'atomics_check_htlc_redeemed', opts)