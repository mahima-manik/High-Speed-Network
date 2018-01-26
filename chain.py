import time

class BlockChain:
    def __init__(self, genesis):
        self.genesis = genesis
        self.last =  genesis

    
    def add_block(self, prevblock, thisblock):
        thisblock.prev_block = prevblock
        self.last = thisblock
    
    def print_blockchain(self, last):
        i = last
        while i != None:
            print i.blockid
            i = i.prev_block

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

my_chain.print_blockchain(block2)
