import asyncio
import json
import time
import math
import yaml

from common import get_address, contract_call_packer
from secp256k1 import PrivateKey
from nuls2.api.server import get_server

async def main():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
        
    pri_key = bytes.fromhex(config['source_pkey'])
    privkey = PrivateKey(pri_key, raw=True)
    pub_key = privkey.pubkey.serialize()
    address = await get_address(pub_key, config['chain_id'], config['prefix'])
    server = get_server(config['api_server'])
    
    ret = await contract_call_packer(server, address,
                                       config['contract_address'],
                                        'increaseApproval', 
                                        [[config['distribution_address'],],
                                         [str(1000000*(10**10)),]],
                                        pri_key, chain_id=config['chain_id'],
                                        asset_id=config.get('asset_id', 1))
    print(ret)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
