# -*- coding: utf-8 -*-

import logging

import numpy as np

from opcua import Client
from subhandler import SubHandler
from time import sleep
from IPython import embed


def main():
    logging.basicConfig(level=logging.WARN)
    client = Client("opc.tcp://WIN-B3JSS0UOON2:49320")
    try:
        client.connect()

        tag1 = client.get_node("ns=2;s=Channel1.Device1.Tag1")
        tag2 = client.get_node("ns=2;s=Simulation Examples.Functions.Ramp3")
        tag3 = client.get_node("ns=2;s=Simulation Examples.Functions.Sine1")

        tags = [tag1, tag2, tag3]

        handler = SubHandler(tags)
        sub = client.create_subscription(500, handler)

        handles = [sub.subscribe_data_change(tag1),
                   sub.subscribe_data_change(tag2),
                   sub.subscribe_data_change(tag3)]

        sleep(0.1)

        embed()

        print("")
        print("Tag1 is: ", handler.storage[0])
        print("")
        print("Tag2 is: ", handler.storage[1])
        print("")
        print("Tag3 is: ", handler.storage[2])
        print("")

        algorithm = SubHandler.extreme_value_analysis
        flags = list(map(lambda i: algorithm(np.array(i)), handler.storage))

        for i in range(len(handles)):
            if flags[i] == True:
                sub.unsubscribe(handles[i])
                print(tags[i], "is broken!")
            else:
                print(tags[i], "is OK!")

        sub.delete()

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
