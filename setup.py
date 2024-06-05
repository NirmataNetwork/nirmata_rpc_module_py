from setuptools import setup, find_packages

setup(
    name='nirmata-rpc',
    version='0.1.0',
    description='Python library to interact with Nirmata RPC Daemon and RPC Wallet',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='NwiZ',
    author_email='nwiznirmata@gmail.com',
    url='https://github.com/NirmataNetwork/nirmata_rpc_module_py',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'pytest',
        'pytest-asyncio',
        'requests',
        'pqueue',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'generate-docs=nirmata-rpc.generate_docs:main',
            'test-wallet-market-place=nirmata-rpc.test_wallet_market_place:main',
            'test-wallet-account=nirmata-rpc.test_wallet_account:main',
            'test-wallet-atomics=nirmata-rpc.test_wallet_atomics:main',
            'test-wallet-cold-signing=nirmata-rpc.test_wallet_cold_signing:main',
            'test-wallet-contracts=nirmata-rpc.test_wallet_contracts:main',
        ],
    },
)