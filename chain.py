import time

class BlockChain:
    def __init__(self, genesis):
        self.genesis = genesis
        self.last = []
        self.last.append(genesis)

    
    def add_block(self, prevblock, thisblock):
        thisblock.prev_block = prevblock
        if prevblock in self.last: 
            self.last.remove(prevblock)
        self.last.append(thisblock)
    
    def print_blockchain(self, endblock):
        i = endblock
        while i != None:
            print i.blockid,
            i = i.prev_block
    
    def find_longest_chain(self):
        max_len = 0
        max_last = None
        for i in self.last:
            len = 0
            j = i
            while i != None:
                len = len+1
                i = i.prev_block
            if len>max_len:
                max_len = len
                max_last = j
            if len==max_len and max_last!=None:
                if (j.gen_time > max_last.gen_time):
                    max_len = len
                    max_last = j
        #print "LAST Item" , j.blockid
        return j

#Class for the block Data structure
class Block:                        #corresponding to node
    def __init__(self, id, listoftrans, prevblock):
        self.prev_block = prevblock     
        self.blockid = id
        self.gen_time = time.time()     #time when the block was generated
        self.block_trans = listoftrans  #list of all transactions contained in the block
        self.num_trans = len(listoftrans)


genesis = Block(5000, [], None)
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

print my_chain.find_longest_chain().blockid
