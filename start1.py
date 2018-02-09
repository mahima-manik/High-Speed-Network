import sys
import time
import numpy as np
import random, thread, threading
import math
import matplotlib.pyplot as plt
from chain import *
trans_id = 0
i = 0
is_over = 0

#IDS are generated as 1001, 1002... 1050
class Node:
    def __init__(self, id, btc, nature, total_nodes, num_peers):
        self.ledger = []        #Data structure to be decided
        self.unspent_translist = []
        self.nodeid = id
        self.btc = btc          #Bitcoins initially held
        self.nature = nature    #nature = 1 then it is fast, else it is slow
        self.peers = []
        self.num_peers = num_peers
        self. total_nodes = total_nodes
        self.tk = 0
        self.block_rcvd = 0
        print "Hey, I am ", id,
        print "Num peers ", num_peers  
        global genesis
        self.my_chain = BlockChain(genesis)
        self.stop_simulation = 0

        #For parallel procesing
        p1 = threading.Thread(target=self.get_my_peers)
        p1.setDaemon = True
        p1.start()
        p2=threading.Thread(target=self.create_transaction) 			#thread for tcp server
       	p2.setDaemon = True
       	p2.start()
        p3=threading.Thread(target=self.create_block)
        p3.setDaemon = True
        p3.start()
        
    def get_my_peers(self):
        time.sleep(7)
        global all_nodes
        for j in range(0, self.num_peers):
            a = int(1000+random.uniform(1, self.total_nodes+1))
            while (self.check_peer(a)) or (a==self.nodeid):
                a = int(1000+random.uniform(1, self.total_nodes+1))
            
            a=a-1000
            #print "a is: ", a
            self.peers.append(all_nodes[a-1])
            if self.nodeid not in self.peers:
                self.peers.append(self)
            
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
        #self.unspent_translist.append([int(acc[0][:len(acc[0])-1]), int(acc[1]), int(acc[3]), float(acc[4])])
        recv.recv_ack(msg)

    #when the sender receives back the acknowlegement from the receiver
    def recv_ack(self, msg):
        acc = msg.split()
        self.ledger.append([int(acc[0][:len(acc[0])-1]), int(acc[1]), int(acc[3]), float(acc[4])])
        #self.unspent_translist.append([int(acc[0][:len(acc[0])-1]), int(acc[1]), int(acc[3]), float(acc[4])])
        for p in self.peers:
            p.transaction_broadcast(self.nodeid, msg)

    def transaction_broadcast(self, senderid, msg):
        acc = msg.split()
        txid = int(acc[0][:len(acc[0])-1])
        
        found = 0
        for t in self.ledger:
            if t[0] == txid:
                found = 1
                break
        
        if found != 1:    
            self.ledger.append([txid, int(acc[1]), int(acc[3]), float(acc[4])])
            #self.unspent_translist.append([int(acc[0][:len(acc[0])-1]), int(acc[1]), int(acc[3]), float(acc[4])])
            #print txid, self.nodeid, len(self.unspent_translist)
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
        time.sleep(10)
        global all_nodes
        global start_time
        while True:
            end_time = time.time()
            if end_time - start_time < 40 :     #simultion time
                x = np.random.uniform(5, 8)    #average time to generate transaction = 5
                time.sleep(x)
                recv = random.randint(0, self.num_peers-1)
                amount = 2
                self.send_transaction(amount, self.peers[recv])
            else :
                self.stop_simulation = 1            #then stop
                break

    #removing all the transactions in the new block from unspent transaction list
    def update_unspent_trans(self, target_block):
        for i in target_block.block_trans:
            if i in self.unspent_translist:
                self.unspent_translist.remove(i)

    def find_unspend(self):
        temp = self.ledger
        my_last = self.my_chain.find_longest_chain()
        while my_last != None:
            for tr in my_last.block_trans:
                if tr in self.ledger:
                    temp.remove(tr)
            my_last = my_last.prev_block

        return temp

    def create_block(self):
        time.sleep(12)
        tkr = time.time()
        first_itr = 1
        while self.stop_simulation == 0 or len(self.find_unspend()) > 0: 
            Tk = np.random.exponential(1)
            if first_itr == 1:
                w = np.random.uniform(0, 1)
                print "First itr wait: ", w
                time.sleep(w)
                first_itr = 0
            '''print self.nodeid, "Waiting for", Tk, self.block_rcvd, tkr+Tk-time.time()
            while(time.time() < tkr +Tk):
                if self.block_rcvd == 1:
                    tkr = self.tk
                    break
            '''
            flag = 0
            tkr = self.tk
            if self.block_rcvd == 1:
                #print  "Waiting for", self.nodeid, Tk + self.tk - time.time(), self.tk-tkr
                self.block_rcvd = 0
                while time.time() < Tk + self.tk:
                    if self.block_rcvd==1:
                        flag = 1
                        break
            if flag == 0:
                self.block_rcvd = 0
                
            t = len(self.find_unspend())
            #print "KITNE UPSTENT HAI",self.nodeid,len(self.find_unspend()),self.block_rcvd
            if (len(self.find_unspend()) > 0):
                if (self.block_rcvd == 0):
                    id =  random.randint(10000, 90000)      #Random block ID generated
                    final_last = self.my_chain.find_longest_chain()     #new block is added to the longest chain known till yet            
                    unspend = self.find_unspend()
                    if len(unspend)>0:
                        print "Creating block", self.nodeid, len(unspend)
                        temp = Block(id, unspend, final_last, self.nodeid)
                        self.send_broadcast_block(temp)
                        print "below"
                        if (self.block_rcvd != 1):
                            tkr = time.time()
                        print self.nodeid , "my last list len" , len(self.my_chain.last)
                    
                '''elif ((len(self.find_unspend()) > 0)):
                    #print "Block not Generated\n"
                    self.block_rcvd = 0'''
        print "Final unspent list:" , self.nodeid , self.find_unspend()
        global is_over
        is_over +=1

    def send_broadcast_block(self, target_block):
        '''if target_block.miningfee_list[0] == self.nodeid:
            self.block_rcvd = 0'''
        ffast = 0
        fslow = 0
        for i in self.peers:
            #px = threading.Thread(target=i.recv_broadcast_block, args=(target_block, self.nodeid, ))
            #px.start()

            if self.nature == 1 and i.nature == 1:
                if ffast == 0:
                    ffast = 1
                    time.sleep(latencies[self.nodeid-1001][i.nodeid-1001]+0.08)  #added m/cij value in latencies
            else:
                if fslow == 0:
                    fslow = 1
                    time.sleep(latencies[self.nodeid-1001][i.nodeid-1001]+1.6)
            i.recv_broadcast_block(target_block, self.nodeid)

    def recv_broadcast_block(self, target_block, sender_nodeid):
        
        found = 0
        l =  self.my_chain.last
        for i in l:
            j = i
            while j != None:
                if j==target_block:
                    found = 1
                    break
                j=j.prev_block
            if found==1:
                break

        if found != 1:           #if the block at the end of longest chain is the same as prev. block of the new block
            final_last = self.my_chain.find_longest_chain()
        
            if target_block.miningfee_list[0] == self.nodeid:       #if i had only generated this block
                self.my_chain.add_block(final_last, target_block)
                self.btc += 50
                
            else:
                self.my_chain.add_block(target_block.prev_block, target_block)
                self.block_rcvd = 1
            
            #if target_block.prev_block.blockid == final_last.blockid:       #if added on longest, then broadcast
                #print "received new broadcast", target_block.miningfee_list[0]
            for n in self.peers:
                if n.nodeid != sender_nodeid and n.nodeid != self.nodeid:
                    #pp = threading.Thread(target=n.send_broadcast_block, args=(target_block, ))
                    #pp.start()
                    n.send_broadcast_block(target_block)
            if target_block.miningfee_list[0] != self.nodeid:
                self.block_rcvd = 1
            self.tk = time.time()
            
            #print "Receive complete", self.nodeid

    def prune_chain(self,final_last):
        add_unspent = []
        for i in my_chain.last:
            if (i != final_last):
                add_unspent + i.block_trans
                my_chain.last.remove(i)


#n = int(raw_input ("No. of nodes: "))
#z = int(raw_input ("Enter z (percent of past nodes): "))
n = 20
z = 20
x = z*n/100
genesis = Block(5000, [], None, 0)

start_time  = time.time()
list_fast = []
list_fast = random.sample(range(1000, 1000+int(n)), x)
all_nodes = []
for i in range(1, n+1):
    k = int(random.uniform(1, n/1.5))
    if 1000+i in list_fast:
        all_nodes.append(Node(1000+i, 50, 1, n, k))
    else:
        all_nodes.append(Node(1000+i, 50, 0, n, k))



latencies = np.zeros((len(all_nodes), len(all_nodes)))
si=0
sj=0
while si < len(all_nodes):
    while sj < len(all_nodes):
        if (all_nodes[si].nature == all_nodes[sj].nature == 1):
            latencies[si][sj] = latencies[sj][si] = random.uniform(0.01, 0.5) + np.random.exponential(0.00096)
        else:
            latencies[si][sj] = latencies[sj][si] = random.uniform(0.01, 0.5) + np.random.exponential(0.0192)
        sj = sj+1
    si = si + 1

print "is_over::", is_over
while (is_over != n):
    pass

print "Total trans happened: ", len(all_nodes[0].ledger)
for i in all_nodes:
    temp = i.my_chain.find_longest_chain()
    print i.nodeid, ": ", i.my_chain.print_blockchain(temp)

#printing entire blockchain of the node
for i in all_nodes:
    print "My blockchain", i.nodeid, ": ", [ j.blockid for j in i.my_chain.last], len(i.my_chain.last)

#my_chain = BlockChain(genesis)
#block1 = Block(5001, ["mahima"], genesis)
#my_chain.add_block(genesis, block1)
#block2 = Block(5002, ["khush"], block1)
#my_chain.add_block(block1, block2)
#my_chain.print_blockchain(block2)