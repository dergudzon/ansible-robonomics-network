#!/usr/bin/python3


import os, argparse, sys, time, datetime, subprocess, json
import multiprocessing as mp
import numpy as np
from multiprocessing import Process, current_process



parser=argparse.ArgumentParser()
# parser.add_argument('--count', '-c', type=int, default=1, help='Specify transactions count')
parser.add_argument('--test_keys_path', '-t', required=True, help='Path to test keys json file')
args=parser.parse_args()


def send_datalog(lst):
    print(current_process().name)
    for indx, key in enumerate(lst):
        for address, seed in key.items():
            # command = "robonomics io write datalog -s %s" % (seed)
            # os.system(command)
            # print(seed, indx)

            text = "0x01"
            # text = "0x516d6178673336614b68345a41547342796f427133384b454b5a6743674366657934344b68746452426477764d41"
            p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["robonomics", "io", "write", "datalog", "-s", seed], stdin=p1.stdout)
            p1.stdout.close()
            p2.communicate()


def main():
    proc_count = 4
    with open(args.test_keys_path, "r") as read_file:
        json_data = json.load(read_file)

    procs = []
    chunks = np.array_split(json_data['keys'], proc_count);

    # while True:
    for index, chunk in enumerate(chunks):
        proc = Process(target=send_datalog, args=(chunk,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


    # i = 1
    # while True:
    #     start_time = time.time()
    #     print("\nStart iteration #%i on %i seeds" % (i, len(json_data['keys'])))
    #     for indx, key in enumerate(json_data['keys']):
    #         for address, seed in key.items():
    #             # print(seed, indx)
    #             text = "%s: test datalog #%i" % (datetime.datetime.now(), indx)
    #             p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    #             p2 = subprocess.Popen(["robonomics", "io", "write", "datalog", "-s", seed], stdin=p1.stdout)
    #             p1.stdout.close()
    #             p2.communicate()
    #     print("--- %s seconds ---\n" % (time.time() - start_time))
    #     i += 1


    # for i in range(args.count):
    #     text = "%s: test datalog #%i" % (datetime.datetime.now(), i)
    #     p1 = subprocess.Popen(["echo", text], stdout=subprocess.PIPE)
    #     p2 = subprocess.Popen(["robonomics", "io", "write", "datalog", "-s", seed], stdin=p1.stdout)
    #     p1.stdout.close()
    #     p2.communicate()



        # command = "echo %s | robonomics io write datalog -s %s" % (text, seed)
        # os.system(command)


if __name__ == "__main__":
    main()
