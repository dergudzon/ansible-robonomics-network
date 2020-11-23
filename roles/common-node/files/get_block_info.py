from substrateinterface import SubstrateInterface, Keypair, SubstrateRequestException
from substrateinterface.utils.ss58 import ss58_encode
import json, argparse

TYPES = {
    "types": {
        "LiabilityIndex": "Vec<u8>",
        "TechnicalReport": "Vec<u8>",
        "Parameter": "Vec<u8>",
        "Record": "Vec<u8>",
        "TechnicalParam": "Vec<u8>",
        "EconomicalParam": "{}",
        "ProofParam": "MultiSignature"
    }
}


parser=argparse.ArgumentParser()
parser.add_argument('--block_hash', '-b', help='block hash')
args=parser.parse_args()

def main(block_hash=None):
        
    substrate = SubstrateInterface(
        url="ws://127.0.0.1:9944/",
        address_type=32,
        type_registry=TYPES,
    )
    result = substrate.get_runtime_block(block_hash=block_hash)

    chain_finalised_head = substrate.get_chain_finalised_head()
    result = substrate.get_runtime_block(block_hash=chain_finalised_head)
    print("%i extrinsics in block %i" % (len(result['block']['extrinsics']), result['block']['header']['number']))
    # for extrinsic in result['block']['extrinsics']:
    #     # print(extrinsic)


    #     if 'account_id' in extrinsic:
    #         signed_by_address = ss58_encode(address=extrinsic['account_id'], address_type=32)
    #     else:
    #         signed_by_address = None

    #     print('\nModule: {}\nCall: {}\nSigned by: {}'.format(
    #         extrinsic['call_module'],
    #         extrinsic['call_function'],
    #         signed_by_address
    #     ))

    #     for param in extrinsic['params']:

    #         if param['type'] == 'Address':
    #             param['value'] = ss58_encode(address=param['value'], address_type=32)

    #         if param['type'] == 'Compact<Balance>':
    #             param['value'] = '{} TXRT'.format(param['value'] / 10**12)

    #         print("Param '{}': {}".format(param['name'], param['value']))

    # print(len(result['block']['extrinsics']))
    return None


if __name__ == "__main__":
    main(block_hash=args.block_hash)