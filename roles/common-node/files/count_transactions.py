#!/usr/bin/python3

import argparse
import numpy as np
import pandas as pd
from ast import literal_eval

parser=argparse.ArgumentParser()
parser.add_argument('--path', '-p', required=True, help='Path to log file')
args=parser.parse_args()


def main():
    text_file = open(args.path, "r")
    lines = text_file.read().split('\n')

    l = []
    for row in lines[:-1]:
        #print(row)
        l.append(literal_eval(row))

    df = pd.DataFrame(l)
    result = df.groupby('block').size()
    print(result)

    return result


if __name__ == "__main__":
    main()