## THE MODULE IS UNDER DEVELOPMENT AND NOT READY FOR USE YET

Nirmata RPC Daemon and RPC Wallet Python Library
Python library to interact with RPC Daemon and RPC Wallet.\
All requests are queued. Most functions are async.
The library supports HTTP, HTTPS, and digest authentication.
Digest authentication is activated as soon as a username and a password are supplied during object creation.
Once initialized, simply use the query functions.
## Installation
```pip install nirmata-rpc```
## RPCDaemon without Digest Authentication
```python
from nirmata_rpc_module.rpc_daemon import RPCDaemon

daemon_client = RPCDaemon({
    'url': 'http://127.0.0.1:11232'
})
# When using a self-signed certificate with HTTPS, you need to set the function ssl_reject_unauthorized to False.
daemon_client.ssl_reject_unauthorized(False)
```
## RPCDaemon with Digest Authentication
```python
from nirmata_rpc_module.rpc_daemon import RPCDaemon

daemon_client = RPCDaemon({
    'url': 'http://127.0.0.1:11232',
    'username': 'user',
    'password': 'pass'
})
# When using a self-signed certificate with HTTPS, you need to set the function ssl_reject_unauthorized to False.
daemon_client.ssl_reject_unauthorized(False)
```
## RPCWallet without Digest Authentication
```python
from nirmata_rpc_module.rpc_wallet import RPCWallet

wallet_client = RPCWallet({
    'url': 'http://127.0.0.1:11222'
})
# When using a self-signed certificate with HTTPS, you need to set the function ssl_reject_unauthorized to False.
wallet_client.ssl_reject_unauthorized(False)
```
## RPCWallet with Digest Authentication
```python
from nirmata_rpc_module.rpc_wallet import RPCWallet

wallet_client = RPCWallet({
    'url': 'http://127.0.0.1:11222',
    'username': 'user',
    'password': 'pass'
})
# When using a self-signed certificate with HTTPS, you need to set the function ssl_reject_unauthorized to False.
wallet_client.ssl_reject_unauthorized(False)
```
## Generate Documentation
```
make docs
```
## Run Unit Tests
```
pytest
```
## MarketPlace Tests

NOTE: tests can take several minutes to complete while block confirmations occur
1. Use Console to restore a testnet wallet from seed
```./simplewallet --restore-wallet nwiz.test --password 123456 ```

2. When instructed, provide the following seed phrase
```screen -S regularwallet ./simplewallet --wallet-file nwiz.test --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 22002 --daemon-address 0.0.0.0:22022```

3. When instructed, provide the following password for the secured seed
```pytest tests/test_wallet_market_place.py```

4. Use Console to execute the following command to open a normal wallet as a service with screen
```screen -S regularwallet ./simplewallet --wallet-file nwiz.test --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 22002 --daemon-address 0.0.0.0:22022```

5. Run the market-place tests
```pytest tests/test_wallet_market_place.py```

## Wallet Tests

1. Use Console to restore a testnet wallet from seed
```./simplewallet --restore-wallet nwiz.test --password 123456 ```

2. Use Console to execute the following command to open a normal wallet as a service with screen
```screen -S regularwallet ./simplewallet --wallet-file nwiz.test --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 22002 --daemon-address 0.0.0.0:22022```

3. Run the wallet tests
```pytest tests/test_wallet_account.py```

## Atomics Tests

NOTE: tests require two wallets and can take several minutes to complete while block confirmations occur
1. Use Console to restore a testnet wallet from seed
```./simplewallet --restore-wallet nwiz.test --password 123456 ```

2. When instructed, provide the following seed phrase
```coffee rest stand said leg muse defense wild about mighty horse melt really hum sharp seek honest brush depress beyond hundred silly confusion inhale birthday frozen```

3. When instructed, provide the following password for the secured seed
```123456```

4. Use Console to execute the following command to open a normal wallet as a service with screen
```screen -S regularwallet ./simplewallet --wallet-file nwiz.test --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 22002 --daemon-address 0.0.0.0:22022```

5. Use Console to restore a testnet wallet from seed
```./simplewallet --restore-wallet nwiz.test --password 123456 ```

6. When instructed, provide the following seed phrase
```obviously essence rise wow appear glove veil gain beneath ask suddenly manage thunder near sympathy respect pants led lucky pie rant water deeply mean shift somebody```

7. When instructed, provide the following password for the secured seed
```123456```

8. Use Console to execute the following command to open a normal wallet as a service with screen
```screen -S otherwallet ./simplewallet --wallet-file nwiz.other --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 12234 --daemon-address 0.0.0.0:22022```

9. Run the atomic tests
```pytest tests/test_wallet_atomics.py``

## Cold Signing Tests

1. Use Console to restore a testnet wallet from seed
```./simplewallet --restore-wallet nwiz.test --password 123456 ```

2. When instructed, provide the following seed phrase
```coffee rest stand said leg muse defense wild about mighty horse melt really hum sharp seek honest brush depress beyond hundred silly confusion inhale birthday frozen```

3. When instructed, provide the following password for the secured seed
```123456```

4. Use Simplewallet console to execute the following to save a watch-only wallet
```save_watch_only nwiz.watch 123456```

5. Use Console to execute the following command to open a watch-only wallet as a service with screen
```screen -S watchwallet ./simplewallet --wallet-file nwiz.watch --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 12235 --daemon-address 0.0.0.0:22022```

6. Use Console to execute the following command to open a normal wallet as a service with screen
```screen -S regularwallet ./simplewallet --wallet-file nwiz.test --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 22002 --daemon-address 0.0.0.0:22022```

7. Run the cold-signing tests
```pytest tests/test_wallet_cold_signing.py```

## Contract Tests

***NOTE: tests require two wallets and can take several minutes to complete while block confirmations occur***

1. Use Console to restore a testnet wallet from seed
```./simplewallet --restore-wallet nwiz.test --password 123456```

2. When instructed, provide the following seed phrase
```coffee rest stand said leg muse defense wild about mighty horse melt really hum sharp seek honest brush depress beyond hundred silly confusion inhale birthday frozen```

3. When instructed, provide the following password for the secured seed
```123456```

4. Use Console to execute the following command to open a normal wallet as a service with screen
```screen -S regularwallet ./simplewallet --wallet-file nwiz.test --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 22002 --daemon-address 0.0.0.0:22022```

5. Use Console to restore a testnet wallet from seed
```./simplewallet --restore-wallet nwiz.test --password 123456```

6. When instructed, provide the following seed phrase
```obviously essence rise wow appear glove veil gain beneath ask suddenly manage thunder near sympathy respect pants led lucky pie rant water deeply mean shift somebody```

7. When instructed, provide the following password for the secured seed
```123456```

8. Use Console to execute the following command to open a normal wallet as a service with screen
```screen -S otherwallet ./simplewallet --wallet-file nwiz.other --password 123456 --rpc-bind-ip 0.0.0.0 --rpc-bind-port 12234 --daemon-address 0.0.0.0:22022```

9. Run the contract tests
```pytest tests/test_wallet_contract.py```

