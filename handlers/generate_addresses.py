#!/usr/bin/python3


import os, argparse, sys, pathlib, time, datetime, subprocess, json
import multiprocessing as mp


parser=argparse.ArgumentParser()
parser.add_argument('--count', '-c', required=True, help='Test keys count')
parser.add_argument('--path', '-p', required=True, help='Path to save test_keys.json file')
args=parser.parse_args()


def main(path, count):
    data = { "keys": [] }
    for indx in range(count):
        # result = subprocess.run(['data/local/subkey', 'generate'], stdout=subprocess.PIPE)
        result = subprocess.run(['data/local/subkey', '-n', 'robonomics', 'generate'], stdout=subprocess.PIPE)
        r = str(result.stdout)
        seed = r.split('`')[1]
        address = r.split('SS58 Address:       ')[1][:-3]
        row = { address: seed }
        data['keys'].append(row)

    with open(path, 'w') as test_keys_file:
        json.dump(data, test_keys_file)

    return data

if __name__ == "__main__":
    main(args.path, int(args.count))
