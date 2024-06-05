import requests
from pqueue import PQueue
import rpc_helpers

def parse_daemon_response(res):
    if res.status_code == 200:
        data = res.json()
        if 'error' in data:
            error = Exception('HTTP Error!')
            error.code = data['error']['code']
            error.message = data['error']['message']
            raise error
        if 'result' in data:
            json = data['result']
        else:
            json = data
        if json.get('status') == 'OK' or json:
            return json
        else:
            error = Exception('RPC Error!')
            error.code = json['error']['code']
            error.message = json['error']['message']
            raise error
    else:
        error = Exception('HTTP Error!')
        error.code = res.status_code
        error.message = res.text
        raise error

class RPCDaemon:
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

    async def get_block_count(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'getblockcount')

    async def on_get_block_hash(self, opts):
        rpc_helpers.check_mandatory_parameters({'height': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'on_getblockhash', [opts['height']])

    async def get_block_header_by_hash(self, opts):
        rpc_helpers.check_mandatory_parameters({'hash': 'Hash'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'getblockheaderbyhash', opts)

    async def get_block_header_by_height(self, opts):
        rpc_helpers.check_mandatory_parameters({'height': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'getblockheaderbyheight', opts)

    async def get_alias_details(self, opts):
        rpc_helpers.check_mandatory_parameters({'alias': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_alias_details', opts)

    async def get_alias_by_address(self, opts):
        rpc_helpers.check_mandatory_parameters({'address': 'Address'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_alias_by_address', opts['address'])

    async def get_alias_reward(self, opts):
        rpc_helpers.check_mandatory_parameters({'alias': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_alias_reward', opts)

    async def get_blocks_details(self, opts):
        rpc_helpers.check_mandatory_parameters({'height_start': 'Integer', 'count': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_blocks_details', opts)

    async def get_tx_details(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_hash': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_tx_details', opts)

    async def search_by_id(self, opts):
        rpc_helpers.check_mandatory_parameters({'id': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'search_by_id', opts)

    async def get_block_template(self, opts):
        fields = {'wallet_address': 'Address'}
        if opts.get('pos_block'):
            fields.update({'pos_block': 'Boolean', 'stakeholder_address': 'String'})
        rpc_helpers.check_mandatory_parameters(fields, opts)
        rpc_helpers.check_optional_parameters_type({'extra_text': 'Max255Bytes'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'getblocktemplate', opts)

    async def get_info(self, opts):
        rpc_helpers.check_mandatory_parameters({'flags': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'getinfo')

    async def get_out_info(self, opts):
        rpc_helpers.check_mandatory_parameters({'amount': 'Integer', 'i': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_out_info', opts)

    async def get_multisig_info(self, opts):
        rpc_helpers.check_mandatory_parameters({'ms_id': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_multisig_info', opts)

    async def get_all_alias_details(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_all_alias_details')

    async def get_aliases(self, opts):
        rpc_helpers.check_mandatory_parameters({'offset': 'Integer', 'count': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_aliases', opts)

    async def get_pool_txs_details(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_pool_txs_details')

    async def get_pool_txs_brief_details(self, opts):
        rpc_helpers.check_mandatory_parameters({'ids': 'ArrayOfStrings'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_pool_txs_brief_details', opts)

    async def get_all_pool_tx_list(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_all_pool_tx_list')

    async def get_main_block_details(self, opts):
        rpc_helpers.check_mandatory_parameters({'id': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_main_block_details', opts)

    async def get_alt_block_details(self, opts):
        rpc_helpers.check_mandatory_parameters({'id': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_alt_block_details', opts)

    async def get_alt_blocks_details(self, opts):
        rpc_helpers.check_mandatory_parameters({'offset': 'Integer', 'count': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_alt_blocks_details', opts)

    async def reset_transaction_pool(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'reset_transaction_pool')

    async def get_current_core_tx_expiration_median(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'get_current_core_tx_expiration_median')

    async def marketplace_global_get_offers_ex(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'marketplace_global_get_offers_ex')

    async def getheight(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address.replace('json_rpc', 'getheight'), self.queue, parse_daemon_response)

    async def gettransactions(self, opts):
        rpc_helpers.check_mandatory_parameters({'txs_hashes': 'ArrayOfStrings'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address.replace('json_rpc', 'gettransactions'), self.queue, parse_daemon_response, None, opts)

    async def sendrawtransaction(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_as_text': 'String'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address.replace('json_rpc', 'sendrawtransaction'), self.queue, parse_daemon_response, None, opts)

    async def force_relay(self, opts):
        rpc_helpers.check_mandatory_parameters({'tx_as_hex': 'ArrayOfStrings'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address.replace('json_rpc', 'force_relay'), self.queue, parse_daemon_response, None, opts)

    async def start_mining(self, opts):
        rpc_helpers.check_mandatory_parameters({'miner_address': 'Address', 'thread_count': 'Integer'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address.replace('json_rpc', 'start_mining'), self.queue, parse_daemon_response, None, opts)

    async def stop_mining(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address.replace('json_rpc', 'stop_mining'), self.queue, parse_daemon_response, None)

    async def get_info_legacy(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address.replace('json_rpc', 'getinfo'), self.queue, parse_daemon_response, None)

    async def get_last_block_header(self):
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'getlastblockheader')

    async def submit_block(self, opts):
        rpc_helpers.check_mandatory_parameters({'blobs': 'ArrayOfStrings'}, opts)
        return await rpc_helpers.make_json_query(self.http_client, self.json_address, self.queue, parse_daemon_response, 'submitblock', opts['blobs'])