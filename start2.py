import sys
import time
import numpy as np
import random, thread, threading
from chain import *
import copy

trans_id = 0    #Transaction IDs are generated sequentially

is_over = 0     #Becomes 1 when all the threads stop

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
        
        time.sleep(5)
        global all_nodes
        
        for j in range(0, self.num_peers):
        
            a = int(1000+random.uniform(1, self.total_nodes+1))
            while (self.check_peer(a)) or (a==self.nodeid):
                a = int(1000+random.uniform(1, self.total_nodes+1))
            
            a=a-1001
            self.peers.append(all_nodes[a])
            #Adding self to the peers list
            if self not in self.peers:
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
                break
        
        if found != 1:    
            self.ledger.append([txid, int(acc[1]), int(acc[3]), float(acc[4])])
            for j in self.peers:
                if j.nodeid != senderid and j.nodeid != self.nodeid:
                    j.transaction_broadcast(self.nodeid, msg)

    #Called when the node itself wants to make some transaction
    def send_transaction(self, amount, recv):
        global trans_id, latencies
        time.sleep(latencies[self.nodeid-1001][recv.nodeid-1001])
        if amount <= self.btc:
            msg = str(trans_id) + ": " + str(self.nodeid)+ " pays "+str(recv.nodeid)+" "+str(amount)+" coins"
            trans_id+=1
            recv.receive_transaction(msg)
            self.btc -= amount
        else:
            print "Transaction cannot be proceeded \n"

    #Called when the node acts as the receiver for bitcoins in the transaction
    def receive_transaction(self, msg):
        acc = msg.split()
        if (self.nodeid == int(acc[3])):    #check that the transaction is meant for itself
            self.btc += float(acc[4])
            self.send_ack(msg)

    def create_transaction(self): 				#to make a node go offline or online with random probability
        time.sleep(7)
        global all_nodes
        global start_time
        while True:
            
            end_time = time.time()
            if end_time - start_time < 70 :     #simultion time
                x = np.random.exponential(7)    #average time to generate transaction 
                time.sleep(x)
                recv = random.randint(0, self.num_peers-1)
                
                while (self.peers[recv].nodeid == self.nodeid):
                    recv = random.randint(0, self.num_peers-1)
                
                amount = np.random.uniform(0,2)
                self.send_transaction(amount, self.peers[recv])
            
            else :
                self.stop_simulation = 1            #then stop
                break

    def find_unspend(self):
        temp = copy.copy(self.ledger)
        my_last = self.my_chain.find_longest_chain()
        while my_last != None:
            for tr in my_last.block_trans:
                if tr in temp:
                    temp.remove(tr)
            my_last = my_last.prev_block
        return temp

    def create_block(self):
        first_itr = 1
        self.tk = time.time()
        while self.stop_simulation == 0 or len(self.find_unspend()) > 0: 
            Tk = np.random.exponential(7)
            
            '''if first_itr == 1:
                w = np.random.uniform(1, 3)
                time.sleep(w)
                first_itr = 0'''
            
            if self.block_rcvd == 1:
                print  "Waiting for", self.nodeid, Tk + self.tk - time.time()
                self.block_rcvd = 0
            
                while time.time() < (Tk + self.tk):
                    if self.block_rcvd == 1:
                        break
                
            if (len(self.find_unspend()) > 0) and (self.block_rcvd == 0):
                    id =  random.randint(10000, 90000)      #Random block ID generated
                    final_last = self.my_chain.find_longest_chain()     #new block is added to the longest chain known till yet            
                    unspend = self.find_unspend()
                    print "Creating block", self.nodeid, len(unspend)
                    temp = Block(id, unspend, final_last, self.nodeid)
                    t = time.time()
                    #pp = threading.Thread(target=self.send_broadcast_block, args=(temp, )) 			#thread for tcp server
       	            #pp.setDaemon = True
                    #pp.start()
                    
                    self.send_broadcast_block(temp)
                    print self.nodeid , "Send complete after: ", time.time()-t
                    
        print "Final unspent list:" , self.nodeid , self.find_unspend()
        global is_over
        is_over +=1

    def send_broadcast_block(self, target_block):
        '''if target_block.miningfee_list[0] == self.nodeid:
            self.block_rcvd = 0'''
        ffast = 0
        fslow = 0
        for i in self.peers:
            if i.nodeid != self.nodeid:
                if self.nature == 1 and i.nature == 1:
                    if ffast == 0:
                        ffast = 1
                        time.sleep(latencies[self.nodeid-1001][i.nodeid-1001]+0.08)  #added m/cij value in latencies
                else:
                    if fslow == 0:
                        fslow = 1
                        time.sleep(latencies[self.nodeid-1001][i.nodeid-1001]+1.6)
                
                i.recv_broadcast_block(target_block, self.nodeid)
                i.tk = time.time()

    def search_trans(self, btrans, final_last):
        i = copy.deepcopy(final_last)
        while i != None:
            for tr in i.block_trans:
                if tr in btrans:
                    return False
            i = i.prev_block
        return True

    def recv_broadcast_block(self, target_block, sender_nodeid):
        found = 0
        llist =  self.my_chain.last
        final_last = self.my_chain.find_longest_chain()
        
        for i in llist:
            j = copy.deepcopy(i)
            while j != None:
                if j.blockid == target_block.blockid:         #if any of the transaction of target block is already present in longest chain, then found=1
                    found = 1
                    break
                j=j.prev_block
            if found==1:
                break

        
        if found != 1 :          #if the block at the end of longest chain is the same as prev. block of the new block
            
            '''and self.search_trans(target_block.block_trans, final_last)'''
            if target_block.miningfee_list[0] == self.nodeid:       #if i had only generated this block
                self.my_chain.add_block(target_block.prev_block, target_block)
                if target_block.prev_block.blockid == final_last.blockid:
                    self.btc += 50
                
            else:
                self.my_chain.add_block(target_block.prev_block, target_block)
                self.block_rcvd = 1
            
            #if (target_block.prev_block.blockid == final_last.blockid):
            for n in self.peers:
                if n.nodeid != sender_nodeid and n.nodeid != self.nodeid:
                    n.send_broadcast_block(target_block)
            if target_block.miningfee_list[0] != self.nodeid:
                self.block_rcvd = 1
            
            
            #print "Receive complete", self.nodeid

    def prune_chain(self,final_last):
        add_unspent = []
        for i in my_chain.last:
            if (i != final_last):
                add_unspent + i.block_trans
                my_chain.last.remove(i)


#n = int(raw_input ("No. of nodes: "))
#z = int(raw_input ("Enter z (percent of past nodes): "))
n = 10
z = 20
x = z*n/100

genesis = Block(5000, [], None, 0)

start_time  = time.time()
list_fast = []
list_fast = random.sample(range(1000, 1000+int(n)), x)
all_nodes = []
for i in range(1, n+1):
    k = int(random.uniform(3, n/1.5))
    if 1000+i in list_fast:
        all_nodes.append(Node(1000+i, 50, 1, n, k))
    else:
        all_nodes.append(Node(1000+i, 50, 0, n, k))

latencies = np.zeros((n,n))
si=0
sj=0
while si < n:
    while sj < n:
        if (all_nodes[si].nature == all_nodes[sj].nature == 1):
            latencies[si][sj] = latencies[sj][si] = random.uniform(0.01, 0.5) + np.random.exponential(0.00096)
        else:
            latencies[si][sj] = latencies[sj][si] = random.uniform(0.01, 0.5) + np.random.exponential(0.0192)
        sj = sj+1
    si = si + 1


print "is_over::", is_over
while (is_over != n):
    pass

for i in all_nodes:
    fname = "chain"+str(i.nodeid)
    fcreate = open(fname, "w+")
    for txt in i.my_chain.flist:
        fcreate.write(txt+"\n")
    fcreate.close()

print "Total trans happened: ", len(all_nodes[0].ledger)
for i in all_nodes:
    temp = i.my_chain.find_longest_chain()
    print i.nodeid, ": ", i.my_chain.print_blockchain(temp)

#printing entire blockchain of the node
for i in all_nodes:
    print "My blockchain", i.nodeid, ": ", [ j.blockid for j in i.my_chain.last], len(i.my_chain.last)



print tabulate(all_nodes.nodeid, headers=['Transaction ID', 'Sender', 'Receiver', 'Amount'])