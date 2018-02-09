import time

class BlockChain:
    def __init__(self, genesis):
        self.genesis = genesis
        self.last = []
        self.last.append(genesis)
        self.chains = [[(genesis.blockid, genesis.prev_block)]]
    
    def add_block(self, prevblock, thisblock):
        thisblock.prev_block = prevblock
        flag = 0
        for c in self.chains:       #if the previous block is at the end of some chain
            if (c[len(c)-1] == prevblock):
                c.append(prevblock)
                flag = 1

        if flag != 1:
            for c in self.chains:
                if prevblock in c:
                    temp = c[0:c.index(prevblock)]
                    temp.append(thisblock.blockid)
                    self.chains.append(temp)
               
        if prevblock in self.last:
            self.last.remove(prevblock)
        self.last.append(thisblock)
    
    def print_blockchain(self, endblock):
        l = 0
        i = endblock
        print endblock.blockid
        while i != None:
            print i.blockid,
            l = l+1
            i = i.prev_block
        print "\n"
        print "LENGTH OF LON CHAIN",l
    
    def find_longest_chain(self):
        max_len = 0
        max_last = None
        j = None
        for i in self.last:
            len = 0
            j = i
            while i != None:
                len = len+1
                i = i.prev_block
            if len>max_len:
                max_len = len
                max_last = j
            if len==max_len and max_last!=None:         #the block generated earlier is the last block returned
                if (j.gen_time < max_last.gen_time):
                    max_len = len
                    max_last = j
        #print "LAST Item" , j.blockid
        #return j    #mahima check this once
        return max_last

#Class for the block Data structure
class Block:                        #corresponding to node
    def __init__(self, id, listoftrans, prevblock, nodeid):
        self.prev_block = prevblock     
        self.blockid = id
        self.gen_time = time.time()     #time when the block was generated
        self.block_trans = listoftrans  #list of all transactions contained in the block
        self.num_trans = len(listoftrans)
        self.miningfee_list = [nodeid, self.blockid, 50]
        self.visit_flag = 0 #used in pruning the chain


'''genesis = Block(5000, [], None)
my_chain = BlockChain(genesis)
block1 = Block(5001, ["mahima"], genesis)
my_chain.add_block(genesis, block1)
block2 = Block(5002, ["khush"], block1)
my_chain.add_block(block1, block2)

block3 = Block(5003, ["khush"], block1)
my_chain.add_block(block1, block3)


block4 = Block(5004, ["laddoo"], block3)
my_chain.add_block(block3, block4)

my_chain.print_blockchain(block2)
print "\n"
my_chain.print_blockchain(block4)

print my_chain.find_longest_chain().blockid'''
