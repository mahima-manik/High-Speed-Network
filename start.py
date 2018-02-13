import sys
import time
import numpy as np
import random, thread, threading
from chain import *
import copy
from tabulate import tabulate

trans_id = 0    #Transaction IDs are generated sequentially

is_over = 0     #Becomes 1 when all the threads stop

#IDS are generated as 1001, 1002... 1050
class Node:
    
    def __init__(self, id, btc, nature, total_nodes, num_peers):
        self.ledger = []        #Data structure to be decided
        self.nodeid = id
        self.btc = btc          #Bitcoins initially held
        self.nature = nature    #nature = 1 then it is fast, else it is slow
        self.peers = [None for i in range(num_peers)]
        self.num_peers = num_peers
        self. total_nodes = total_nodes
        self.tk = 0             #tk time is set when some block is received
        self.block_rcvd = 0     #reflects if the block is received or not
        print "Hey, I am ", id,
        print "Num peers ", num_peers  
        global genesis
        self.my_chain = BlockChain(genesis)
        self.stop_simulation = 0    #simulation is stopped when it is set to 1
        self.check_point = genesis
        self.block_list = []

        #For parallel processing
        p1 = threading.Thread(target=self.get_my_peers)
        p1.setDaemon = True
        p1.start()
        
        p2 = threading.Thread(target=self.create_transaction)
       	p2.setDaemon = True
       	p2.start()
        
        p3 = threading.Thread(target=self.create_block)
        p3.setDaemon = True
        p3.start()

        p4 = threading.Thread(target=self.get_reward)
        p4.setDaemon = True
       	p4.start()
        
    def get_reward(self):
        while (self.peers[-1] == None):
            pass
        count = 0
        tc = self.check_point
        last_block = self.my_chain.find_longest_chain()
        temp_block = copy.copy(last_block)
        while temp_block.blockid != self.check_point.blockid:
            count += 1
            if count > 2:
                if count == 3:          
                    '''temporary block check point'''
                    tc = temp_block
                if temp_block.block_nodeid == self.nodeid:
                    self.btc += 50
            temp_block = temp_block.prev_block
        self.check_point = tc

    def get_my_peers(self):
        global all_nodes
        while (all_nodes[-1] == None):
            pass
        
        for j in range(0, self.num_peers):
        
            a = int(1000+random.uniform(1, self.total_nodes+1))
            while (self.check_peer(a)) or (a==self.nodeid):
                a = int(1000+random.uniform(1, self.total_nodes+1))
            
            a=a-1001
            self.peers[j] = all_nodes[a]
            '''Adding self to the peers list'''
            
    '''Checks if the given ID is present in the peers list of the node'''
    def check_peer(self, id):
        for i in self.peers:
            if i == None:
                return False
            if (i.nodeid == id):
                return True
        return False

    ''''Receiver of the bitcoins sends back the acknowlegement to the sender'''
    def send_ack (self, msg):
        global all_nodes
        acc = msg.split()
        '''finding the object of the sender node'''
        for n in all_nodes:
            if(n.nodeid==int(acc[1])):
                recv = n
                break
        txid = int(acc[0][:len(acc[0])-1])
        sender = int(acc[1])
        self.ledger.append([txid, sender, int(acc[3]), float(acc[4])])         #TXID, sender, receiver, amount
        recv.recv_ack(msg)

    ''''when the sender receives back the acknowlegement from the receiver'''
    def recv_ack(self, msg):
        acc = msg.split()
        self.ledger.append([int(acc[0][:len(acc[0])-1]), int(acc[1]), int(acc[3]), float(acc[4])])
        for p in self.peers:
            if p.nodeid == self.nodeid or p.nodeid == int(acc[3]):
                pass
            else:
                p.transaction_broadcast(self.nodeid, msg)

    def transaction_broadcast(self, senderid, msg):
        global latencies
        acc = msg.split()
        txid = int(acc[0][:len(acc[0])-1])
        found = 0
        for t in self.ledger:
            if t[0] == txid:
                found = 1
                break
        
        if found != 1:    
            time.sleep(latencies[self.nodeid-1001][senderid-1001])
            self.ledger.append([txid, int(acc[1]), int(acc[3]), float(acc[4])])
            for j in self.peers:
                if (j.nodeid == senderid) or (j.nodeid == self.nodeid) or j.nodeid == int(acc[1]) or j.nodeid == int(acc[3]):
                    pass
                else:
                    j.transaction_broadcast(self.nodeid, msg)

    '''Called when the node itself wants to make some transaction'''
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

    '''Called when the node acts as the receiver for bitcoins in the transaction'''
    def receive_transaction(self, msg):
        acc = msg.split()
        if (self.nodeid == int(acc[3])):    #check that the transaction is meant for itself
            self.btc += float(acc[4])
            self.send_ack(msg)
    
    def create_transaction(self): 				
        while (self.peers[-1] == None):
            pass
        time.sleep(0.5)
        global start_time
        while True:
            
            end_time = time.time()

            if end_time - start_time < 60 :     #simultion time
                x = np.random.exponential(3)    #average time to generate transaction 
                time.sleep(x)
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
        while (self.peers[-1] == None):
            pass
        first_itr = 1
        self.tk = time.time()
        while self.stop_simulation == 0 or len(self.find_unspend()) > 0: 
            Tk = np.random.exponential(4)
            
            if first_itr == 1:
                w = np.random.uniform(1, 3)
                time.sleep(w)
                first_itr = 0
            
            if self.block_rcvd == 1:
                print  "Waiting for", self.nodeid, Tk, Tk + self.tk - time.time()
                self.block_rcvd = 0
            
                while time.time() < (Tk + self.tk):
                    if self.block_rcvd == 1:
                        break
                
            if (len(self.find_unspend()) > 0) and (self.block_rcvd == 0):
                    id =  random.randint(10000, 90000)      #Random block ID generated
                    unspend = self.find_unspend()
                    final_last = self.my_chain.find_longest_chain()     #new block is added to the longest chain known till yet            
                    
                    #print "Creating block", self.nodeid, len(unspend)
                    temp = Block(id, unspend, final_last, self.nodeid)
                    temp.prev_block = final_last
                    self.my_chain.add_block(final_last, temp)
                    self.block_list.append(temp)
                    t = time.time()
                    self.send_broadcast_block(temp, self.nodeid)
                    print self.nodeid , "Send complete after: ", time.time()-t
                    
        print "Final unspent list:" , self.nodeid , self.find_unspend()
        global is_over, all_nodes
        is_over +=1
        
    def if_blockinchain(self, target_block):
        llist =  copy.deepcopy(self.my_chain.last)
        found = 0
        for b in self.my_chain.buffer:
            if b.blockid == target_block.blockid:
                found = 1
                break
        if found == 0:
            for i in llist:
                j = copy.deepcopy(i)
                while j != None:
                    if j.blockid == target_block.blockid:         #if any of the transaction of target block is already present in longest chain, then found=1
                        found = 1
                        break
                    j = j.prev_block
                if found == 1:
                    break
        
        return found

    def send_broadcast_block(self, target_block, from_nodeid):
        ffast = 0
        fslow = 0
        for i in self.peers:
            if self.nature == 1 and i.nature == 1:
                if ffast == 0:
                    ffast = 1
                    time.sleep(latencies[self.nodeid-1001][i.nodeid-1001]+0.08)  #added m/cij value in latencies
            else:
                if fslow == 0:
                    fslow = 1
                    time.sleep(latencies[self.nodeid-1001][i.nodeid-1001]+1.6)
        
            i.recv_broadcast_block(target_block, self.nodeid)
            

    def recv_broadcast_block(self,target_block,from_nodeid):
        if self.if_blockinchain(target_block) == 0:
            ffast = 0
            fslow = 0
            self.my_chain.add_block(target_block.prev_block, target_block)
            self.block_rcvd = 1
            self.tk = time.time()
            self.block_list.append(target_block)
            for i in self.peers:
                if i.nodeid == from_nodeid or target_block.block_nodeid == i.nodeid:
                    pass
                else:
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



    '''def rec_send_broadcast_block(self, target_block, from_nodeid):
        if self.if_blockinchain(target_block) == 0:
            ffast = 0
            fslow = 0
            self.my_chain.add_block(target_block.prev_block, target_block)
            self.block_rcvd = 1
            self.block_list.append(target_block)
            for i in self.peers:
                if i.nodeid == from_nodeid or target_block.block_nodeid == i.nodeid:
                    pass
                else:
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

    def recv_broadcast_block(self, target_block, sender_nodeid):
        if self.if_blockinchain(target_block) == 0:          #if the block at the end of longest chain is the same as prev. block of the new block
            self.my_chain.add_block(target_block.prev_block, target_block)
            
            if target_block not in self.block_list:
                self.block_list.append(target_block)
            
            self.block_rcvd = 1
            for i in self.peers:
                if i.nodeid == sender_nodeid or i.nodeid == target_block.block_nodeid:
                    pass
                else:
                    i.rec_send_broadcast_block(target_block, self.nodeid)'''

def verify_btc():
    global all_nodes
    check_list = [50 for i in range(len(all_nodes))]
    last_block = all_nodes[0].my_chain.find_longest_chain()
    temp_block = copy.copy(last_block)
    while temp_block.prev_block != None:
        rewardee = temp_block.block_nodeid-1001
        print "Winner", temp_block.blockid, temp_block.block_nodeid, rewardee, len(temp_block.block_trans)
        check_list[rewardee] += 50
        for tr in temp_block.block_trans:
            sender =  tr[1]-1001
            recv = tr[2]-1001
            amt = tr[3]
            check_list[sender] -= amt
            check_list[recv] += amt
        temp_block = temp_block.prev_block
    return check_list

#n = int(raw_input ("No. of nodes: "))
#z = int(raw_input ("Enter z (percent of fast nodes): "))
n = 15
z = 100
x = z*n/100

genesis = Block(5000, [], None, 0)

start_time  = time.time()
list_fast = []
list_fast = random.sample(range(1000, 1000+int(n)), x)

all_nodes = [None for i in range(n)]
for i in range(1, n+1):
    k = int(random.uniform(3, n/1.5))
    if 1000+i in list_fast:
        all_nodes[i-1] = Node(1000+i, 50, 1, n, k)
    else:
        all_nodes[i-1] = Node(1000+i, 50, 0, n, k)

latencies = np.zeros((n,n))
si=0
sj=0
while si < n:
    sj = si
    while sj < n:
        if (all_nodes[si].nature == all_nodes[sj].nature == 1):
            latencies[si][sj] = latencies[sj][si] = random.uniform(0.01, 0.5) + np.random.exponential(0.00096)
        else:
            latencies[si][sj] = latencies[sj][si]= random.uniform(0.01, 0.5) + np.random.exponential(0.0192)
        sj = sj+1
    si = si + 1

while (is_over != n):
    pass    

for i in all_nodes:
    cp = i.check_point
    last_block = copy.copy(i.my_chain.find_longest_chain())
    while last_block.blockid != cp.blockid:
        if (i.nodeid == last_block.block_nodeid):
            i.btc += 50
        last_block = last_block.prev_block
    print "\nMy peers: ", i.nodeid
    for j in i.peers:
        print j.nodeid,

for i in all_nodes:
    fname = "chain"+str(i.nodeid)
    fcreate = open(fname, "w+")
    for txt in i.my_chain.flist:
        fcreate.write(txt+"\n")
    fcreate.close()

print "Total trans happened: ", len(all_nodes[0].ledger)
'''for i in all_nodes:
    temp = i.my_chain.find_longest_chain()
    print i.nodeid, ": ", i.my_chain.print_blockchain(temp)'''

#printing entire blockchain of the node
for i in all_nodes:
    print "My blockchain", i.nodeid, ": ",i.my_chain.print_longest()

check_list = verify_btc()
nodeids = []
for j in all_nodes:
    nodeids.append([j.nodeid, j.nature, j.num_peers, j.btc, check_list[j.nodeid-1001] ,j.my_chain.print_blockchain(j.my_chain.find_longest_chain())])
print tabulate(nodeids ,headers=['Node ID', 'Nature' ,'No. of peers', "BTC", "Cal BTC" ,"Chain length"])

print "block lists"
for itr in all_nodes:
    print itr.nodeid, len(itr.block_list),len(itr.my_chain.buffer)