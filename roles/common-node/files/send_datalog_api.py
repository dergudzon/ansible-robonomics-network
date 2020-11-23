from substrateinterface import SubstrateInterface, Keypair, SubstrateRequestException
from substrateinterface.utils.ss58 import ss58_encode
import json, time, argparse
from multiprocessing import Process

TYPES = {
    "types": 
    # {
    #     "LiabilityIndex": "Vec<u8>",
    #     "TechnicalReport": "Vec<u8>",
    #     "Parameter": "Vec<u8>",
    #     "Record": "Vec<u8>",
    #     "TechnicalParam": "Vec<u8>",
    #     "EconomicalParam": "{}",
    #     "ProofParam": "MultiSignature"
    # }

    {
        "Record": "Vec<u8>",
        "TechnicalParam": "Vec<u8>",
        "TechnicalReport": "Vec<u8>",
        "EconomicalParam": "{}",
        "ProofParam": "MultiSignature",
        "LiabilityIndex": "u64"
    }
}


parser=argparse.ArgumentParser()
parser.add_argument('--path', '-p', required=True, help='block hash')
parser.add_argument('--wait_for_inclusion', '-w', help='block hash')
parser.add_argument('--nonce', '-n', help='block hash')
args=parser.parse_args()


def transaction_submitter():
    pass


def main(path, wait_for_inclusion=False, nonce=0):
    with open(path) as json_file:
        test_adresses = json.load(json_file)

    custom_type_registry = load_type_registry_file("types.json")
    print(custom_type_registry)
    substrate = SubstrateInterface(
        url="ws://127.0.0.1:9944/",
        address_type=32,
        type_registry=TYPES,
        type_registry_preset='robonomics'
    )



    # substrate = SubstrateInterface(
    #     url="ws://127.0.0.1:9944/",
    #     address_type=32,
    #     type_registry=TYPES,
    # )

    # Set block_hash to None for chaintip
    # block_hash = None


    # Retrieve extrinsics in block
    # result = substrate.get_runtime_block(block_hash=block_hash)

    # for extrinsic in result['block']['extrinsics']:

    #     if 'account_id' in extrinsic:
    #         signed_by_address = ss58_encode(address=extrinsic['account_id'], address_type=2)
    #     else:
    #         signed_by_address = None

    #     print('\nModule: {}\nCall: {}\nSigned by: {}'.format(
    #         extrinsic['call_module'],
    #         extrinsic['call_function'],
    #         signed_by_address
    #     ))

    #     for param in extrinsic['params']:

    #         if param['type'] == 'Address':
    #             param['value'] = ss58_encode(address=param['value'], address_type=2)

    #         if param['type'] == 'Compact<Balance>':
    #             param['value'] = '{} DOT'.format(param['value'] / 10**12)

    #         print("Param '{}': {}".format(param['name'], param['value']))

    # Storage call examples
    # print("\n\nCurrent Account info: {} DOT".format(
    #     substrate.get_runtime_state(
    #         module='System',
    #         storage_function='Account',
    #         params=['4GmqwyTi37bbwgWHiamoi7uCnebxuhj9Mmo2rCcjPgjF4Nag']
    #     ).get('result')
    # ))

    # print("Balance @ {}: {} DOT".format(
    #     block_hash,
    #     substrate.get_runtime_state(
    #         module='Balances',
    #         storage_function='FreeBalance',
    #         params=['4GmqwyTi37bbwgWHiamoi7uCnebxuhj9Mmo2rCcjPgjF4Nag'],
    #         block_hash=block_hash
    #     ).get('result')
    # ))
    nonce = int(nonce)
    while True:
        for indx, row in enumerate(test_adresses['keys']):
            for address, mnemonic in row.items():
                # Create, sign and submit extrinsic example
                # mnemonic = Keypair.generate_mnemonic()
                # mnemonic = "pave small hub weapon jewel dream net canvas mirror nurse delay they"
                keypair = Keypair.create_from_mnemonic(mnemonic, 32)

            # nonce = substrate.get_account_nonce(address)
            # nonce = substrate.get_account_nonce(address)
            print("Nonce: ", nonce)
            # keypair = Keypair(
            #     ss58_address='4GQJvwgJwZ1U8j776kmawm5wccE9ZSRFCuH1GnxyCEuGWqL4', 
            #     public_key='0xba3f1ff4f7894070afc1dc88551f47c3d76e4b9a2847fbd045c571b998623c62',
            #     address_type=32
            # )

            # keypair = Keypair.create_from_private_key(
            #     '0x24dcd65948fe301e27eab1456df0c60ea6884f7eef9eb4e55b329a1a785eb43f', 
            #     public_key='0xba3f1ff4f7894070afc1dc88551f47c3d76e4b9a2847fbd045c571b998623c62', 
            #     ss58_address='4GQJvwgJwZ1U8j776kmawm5wccE9ZSRFCuH1GnxyCEuGWqL4', 
            #     address_type=32
            # )

            print("Created address: {}".format(keypair.ss58_address))
            nonce = substrate.get_account_nonce(keypair.ss58_address)
            print(nonce)
            call = substrate.compose_call(
                'Datalog',
                'record',
                call_params={
                    'record': '0x516d6178673336614b68345a41547342796f427133384b454b5a6743674366657934344b68746452426477764d41',
                }
            )
            
            # call = substrate.compose_call(
            #     call_module='Launch',
            #     call_function='launch',
            #     call_params={
            #         # 'date': '0x01',
            #         'Parameter': False,
            #     }
            # )

            # call = substrate.compose_call(
            #     call_module='Balances',
            #     call_function='transfer',
            #     call_params={
            #         'dest': '4Ca9DE2ghDH4jQofEpRAhnQpdFejgVi3zVvkAo2QwsXFJvWA',
            #         'value': 5 * 10**3
            #     }
            # )
            print('create extrinsic')
            extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair, nonce=nonce)
            # extrinsic = substrate.create_unsigned_extrinsic(call=call)

            try:
                print('try to send')
                result = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=wait_for_inclusion)

                print('Extrinsic "{}" included in block "{}"'.format(
                    result['extrinsic_hash'], result.get('block_hash')
                ))

                print(result)

            except SubstrateRequestException as e:
                print("Failed to send: {}".format(e))

        nonce += 1


if __name__ == "__main__":
    start_time = time.time()
    wait_for_inclusion = True if args.wait_for_inclusion=="yes" else False
    main(args.path, wait_for_inclusion=wait_for_inclusion, nonce=args.nonce)
    print("--- %s seconds ---" % (time.time() - start_time))