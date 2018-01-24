
import numpy as np
import random
import math
import matplotlib.pyplot as plt

trans_id = 0

class Node:
    def __init__(self, id, btc, nature, total_nodes, num_peers):
        self.ledger = {}        #Data structure to be decided
        self.nodeid = id
        self.btc = btc          #Bitcoins initially held
        self.nature = nature    #nature = 1 then it is fast, else it is slow
        self.peers = []       
        print "Hey, I am ", id
        print "Num peers ", num_peers  
        for j in range(0, num_peers):
            a = int(1000+random.uniform(1, total_nodes+1))
            while (a in self.peers) or (a==self.nodeid):
                a = int(1000+random.uniform(1, total_nodes+1))
            self.peers.append(a)
        a = np.random.uniform(1,101,4)
        print a
        count,bins,ig = plt.hist(a,4,normed=True)
        plt.plot(bins,np.ones_like(bins),linewidth=2,color = 'r')
        plt.show()
        #print self.peers

    #Called when the node itself wants to make some transaction
    def send_trancsaction(self, amount, recv):
        global trans_id
        if amount <= self.btc:
            msg = str(trans_id)+": "+str(self.nodeid)+ " pays "+str(recv.nodeid)+" "+str(amount)+" coins"
            trans_id+=1
            recv.receive_transaction(msg)
            self.btc -= amount
        else:
            print "Transaction cannot be proceeded \n"

    #Called when the node acts as the receiver for bitcoins in the transaction
    def receive_transaction(self, msg):
        msg = msg.split()
        if (self.nodeid == int(msg[3])):    #check that the transaction is meant for itself
            sender = int(msg[1])
            self.btc += int(msg[4])
            print "Transaction successful"

#n = int(raw_input ("No. of nodes: "))
#z = int(raw_input ("Enter z (percent of past nodes): "))
n = 50
z = 50
x = z*n/100
list_fast = []
list_fast = random.sample(range(1000, 1000+int(n)), x)

all_nodes = []
for i in range(1, n+1):
    k = int(random.uniform(1, n))    #
    if 1000+i in list_fast:
        all_nodes.append(Node(1000+i, 50, 1, n, k))
    else:
        all_nodes.append(Node(1000+i, 50, 0, n, k))

