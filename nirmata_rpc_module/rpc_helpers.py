ADDRESS_LENGTH = 97
INTEGRATED_ADDRESS_LENGTH = 108
HASH_LENGTH = 64
SIGNATURE_LENGTH = 128

def is_address(value):
    return isinstance(value, str) and (len(value) == ADDRESS_LENGTH or len(value) == INTEGRATED_ADDRESS_LENGTH)

def is_ban(value):
    return (isinstance(value.get('host'), str) or isinstance(value.get('ip'), int)) and isinstance(value.get('ban'), bool) and isinstance(value.get('seconds'), int)

def is_boolean(value):
    return isinstance(value, bool)

def is_destination(value):
    return isinstance(value.get('amount'), int) and is_address(value.get('address'))

def is_contract_private_details(value):
    return (isinstance(value.get('t'), str) and isinstance(value.get('c'), str) and is_address(value.get('a_addr')) and is_address(value.get('b_addr')) and isinstance(value.get('to_pay'), int) and isinstance(value.get('a_pledge'), int) and isinstance(value.get('b_pledge'), int))

def is_offer_structure(value):
    return (isinstance(value.get('ap'), str) and isinstance(value.get('at'), str) and isinstance(value.get('cat'), str) and isinstance(value.get('cnt'), str) and isinstance(value.get('com'), str) and isinstance(value.get('do'), str) and isinstance(value.get('et'), int) and isinstance(value.get('fee'), int) and isinstance(value.get('lci'), str) and isinstance(value.get('lco'), str) and isinstance(value.get('ot'), int) and isinstance(value.get('pt'), str) and isinstance(value.get('t'), str))

def is_hash(value):
    return isinstance(value, str) and len(value) == HASH_LENGTH

def is_payment_id(value):
    return isinstance(value, str) and (len(value) == 16 or len(value) == 64)

def is_signature(value):
    return isinstance(value, str) and len(value) == SIGNATURE_LENGTH

def is_signed_key_image(value):
    return is_hash(value.get('key_image')) and is_signature(value.get('signature'))

def is_string(value):
    return isinstance(value, str)

def valid_bytes(value, length):
    return isinstance(value, str) and len(value.encode('utf-8')) <= length

class RPCHelpers:
    @staticmethod
    def check_parameter_type(opts, checks, key):
        if checks[key] == 'Address' and is_address(opts[key]):
            return True
        if checks[key] == 'ArrayOfAddresses' and isinstance(opts[key], list) and all(is_address(addr) for addr in opts[key]):
            return True
        if checks[key] == 'ArrayOfAmountAddress' and isinstance(opts[key], list):
            if not opts[key]:
                raise ValueError(f"Parameter {key} should be of type: {checks[key]}!")
            for destination in opts[key]:
                if not destination:
                    raise ValueError(f"Parameter {opts[key]} should be of type: {dict}!")
                if not is_address(destination.get('address')) or not isinstance(destination.get('amount'), int):
                    raise ValueError(f"Invalid destination in {key}!")
            return True
        if checks[key] == 'Ban' and is_ban(opts[key]):
            return True
        if checks[key] == 'ArrayOfBans' and isinstance(opts[key], list) and all(is_ban(ban) for ban in opts[key]):
            return True
        if checks[key] == 'Destination' and is_destination(opts[key]):
            return True
        if checks[key] == 'ArrayOfDestinations' and isinstance(opts[key], list) and all(is_destination(dest) for dest in opts[key]):
            return True
        if checks[key] == 'Boolean' and is_boolean(opts[key]):
            return True
        if checks[key] == 'Hash' and is_hash(opts[key]):
            return True
        if checks[key] == 'ArrayOfHashes' and isinstance(opts[key], list) and all(is_hash(h) for h in opts[key]):
            return True
        if checks[key] == 'Integer' and isinstance(opts[key], int):
            return True
        if checks[key] == 'ArrayOfIntegers' and isinstance(opts[key], list) and all(isinstance(i, int) for i in opts[key]):
            return True
        if checks[key] == 'PaymentId' and is_payment_id(opts[key]):
            return True
        if checks[key] == 'ArrayOfPaymentIds' and isinstance(opts[key], list) and all(is_payment_id(pid) for pid in opts[key]):
            return True
        if checks[key] == 'SignedKeyImage' and is_signed_key_image(opts[key]):
            return True
        if checks[key] == 'ArrayOfSignedKeyImages' and isinstance(opts[key], list) and all(is_signed_key_image(ski) for ski in opts[key]):
            return True
        if checks[key] == 'String' and is_string(opts[key]):
            return True
        if checks[key] == 'Max255Bytes' and valid_bytes(opts[key], 255):
            return True
        if checks[key] == 'ArrayOfStrings' and isinstance(opts[key], list) and all(is_string(s) for s in opts[key]):
            return True
        if checks[key] == 'ContractPrivateDetails' and is_contract_private_details(opts[key]):
            return True
        if checks[key] == 'OfferStructure' and is_offer_structure(opts[key]):
            return True
        raise ValueError(f"Parameter {key} should be of type: {checks[key]}!")

    @staticmethod
    def check_mandatory_parameters(mandatory_checks, opts):
        if not opts:
            raise ValueError(f"Missing mandatory parameter {list(mandatory_checks.keys())[0]}!")
        for key in mandatory_checks:
            if key not in opts:
                raise ValueError(f"Missing mandatory parameter {key}!")
            RPCHelpers.check_parameter_type(opts, mandatory_checks, key)
        return True

    @staticmethod
    def check_optional_parameters_type(optional_checks, opts):
        if opts and optional_checks:
            for key in optional_checks:
                if key in opts:
                    RPCHelpers.check_parameter_type(opts, optional_checks, key)
        return True

    @staticmethod
    def create_json_data(method, opts=None):
        if opts is not None:
            return {"jsonrpc": "2.0", "id": "0", "method": method, "params": opts}
        else:
            return {"jsonrpc": "2.0", "id": "0", "method": method}

    @staticmethod
    async def make_json_query(http_client, address, queue, parse_response, command, opts=None):
        return await queue.add(lambda: http_client.post(address, json=RPCHelpers.create_json_data(command, opts)).then(parse_response))

    @staticmethod
    async def make_other_query(http_client, address, queue, parse_response, command, opts=None):
        return await queue.add(lambda: http_client.post(f"{address}/{command}", json=opts).then(parse_response) if opts else http_client.post(f"{address}/{command}").then(parse_response))