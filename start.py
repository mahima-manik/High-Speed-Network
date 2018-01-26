import time
import numpy as np
import random, thread, threading
import math
import matplotlib.pyplot as plt
trans_id = 0

class BlockChain:
    def __init__(self, genesis):
        self.genesis = genesis

#Class for the block Data structure
class Block:                        #corresponding to node
    def __init__(self, id, listoftrans, prevblock):
        self.prev_block = prevblock
        self.blockid = id
        self.gen_time = time.time()     #time when the block was generated
        self.block_trans = listoftrans  #list of all transactions contained in the block
        self.num_trans = len(listoftrans)

#IDS are generated as 1001, 1002... 1050
class Node:
    def __init__(self, id, btc, nature, total_nodes, num_peers):
        self.ledger = []        #Data structure to be decided
        self.nodeid = id
        self.btc = btc          #Bitcoins initially held
        self.nature = nature    #nature = 1 then it is fast, else it is slow
        self.peers = [] 
        self.num_peers = num_peers
        self. total_nodes = total_nodes
        print "Hey, I am ", id
        print "Num peers ", num_peers  
        global genesis
        self.my_chain = BlockChain(genesis)

        p1 = threading.Thread(target=self.get_my_peers)
        p1.setDaemon = True
        p1.start()
        p2=threading.Thread(target=self.create_transaction) 			#thread for tcp server
       	p2.setDaemon = True
       	p2.start()
        
    def get_my_peers(self):
        time.sleep(5)
        global all_nodes
        for j in range(0, self.num_peers):
            a = int(1000+random.uniform(1, self.total_nodes+1))
            while (self.check_peer(a)) or (a==self.nodeid):
                a = int(1000+random.uniform(1, self.total_nodes+1))
            
            a=a-1000
            #print "a is: ", a
            self.peers.append(all_nodes[a-1])
            

    def check_peer(self, id):
        for i in self.peers:
            if (i.nodeid == id):
                return True
        return False


    #Receiver of the bitcoins sends back the acknowlegement to the sender
    def send_ack (self, msg):
        global all_nodes
        acc = msg.split()
        #finding the object of the sender node
        for n in all_nodes:
            if(n.nodeid==int(acc[1])):
                recv = n
                break
        self.ledger.append([int(acc[0][:len(acc[0])-1]), int(acc[1]), int(acc[3]), float(acc[4])])         #TXID, sender, receiver, amount
        recv.recv_ack(msg)

    #when the sender receives back the acknowlegement from the receiver
    def recv_ack(self, msg):
        acc = msg.split()
        self.ledger.append([int(acc[0][:len(acc[0])-1]), int(acc[1]), int(acc[3]), float(acc[4])])
        for p in self.peers:
            p.transaction_broadcast(self.nodeid, msg)

    def transaction_broadcast(self, senderid, msg):
        acc = msg.split()
        txid = int(acc[0][:len(acc[0])-1])
        
        found = 0
        for t in self.ledger:
            if t[0] == txid:
                found = 1
            
        if found != 1:    
            print txid, self.nodeid, acc[1], acc[3]
            self.ledger.append([txid, int(acc[1]), int(acc[3]), float(acc[4])])
            for j in self.peers:
                if j.nodeid != senderid:
                    j.transaction_broadcast(self.nodeid, msg)

    #Called when the node itself wants to make some transaction
    def send_transaction(self, amount, recv):
        global trans_id, latencies
        time.sleep(latencies[self.nodeid-1001][recv.nodeid-1001])
        if amount <= self.btc:
            msg = str(trans_id)+": "+str(self.nodeid)+ " pays "+str(recv.nodeid)+" "+str(amount)+" coins"
            trans_id+=1
            recv.receive_transaction(msg)
            self.btc -= amount
        else:
            print "Transaction cannot be proceeded \n"

    #Called when the node acts as the receiver for bitcoins in the transaction
    def receive_transaction(self, msg):
        acc = msg.split()
        
        if (self.nodeid == int(acc[3])):    #check that the transaction is meant for itself
            self.btc += int(acc[4])
            self.send_ack(msg)

    def create_transaction(self): 				#to make a node go offline or online with random probability
        time.sleep(11)
        global all_nodes
        while True:
            x = np.random.exponential(5)    #average time to generate transaction = 5
            time.sleep(x)
            recv = random.randint(0, self.num_peers-1)
            amount = 2
            self.send_transaction(amount, self.peers[recv])             #
            

#n = int(raw_input ("No. of nodes: "))
#z = int(raw_input ("Enter z (percent of past nodes): "))
n = 5
z = 50
x = z*n/100

genesis = Block(5000, [], None)

list_fast = []
list_fast = random.sample(range(1000, 1000+int(n)), x)
all_nodes = []
for i in range(1, n+1):
    k = int(random.uniform(1, n))    #
    if 1000+i in list_fast:
        all_nodes.append(Node(1000+i, 50, 1, n, k))
    else:
        all_nodes.append(Node(1000+i, 50, 0, n, k))

latencies = np.zeros((len(all_nodes), len(all_nodes)))
si=0
sj=0
i=0
while si < len(all_nodes):
    while sj < len(all_nodes):
        if (all_nodes[si].nature == all_nodes[sj].nature == 1):
            latencies[si][sj] = latencies[sj][si] = random.uniform(0.01, 0.5) + np.random.exponential(0.00096)
        else:
            latencies[si][sj] = latencies[sj][si] = random.uniform(0.01, 0.5) + np.random.exponential(0.0192)
        sj = sj+1
        i=i+1
        print i
    si = si + 1