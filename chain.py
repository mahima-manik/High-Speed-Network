import time
import copy

class BlockChain:
    def __init__(self, genesis):
        self.genesis = genesis
        self.last = []
        self.last.append(genesis)
        self.flist = []     
        '''for file generation'''
        self.buffer = []

    def add_block(self, prevblock, thisblock):
        thisblock.prev_block = prevblock
        found = 0           
        '''checks if present in the whole blockchain'''
        for i in self.last:
            j = copy.deepcopy(i)
            while j != None:
                if j.blockid == prevblock.blockid:
                    found = 1
                    break
                j = j.prev_block
            if found == 1:
                break

        if found == 1:       
            if prevblock in self.last:
                self.last.remove(prevblock)
            self.last.append(thisblock)
            temp = str(thisblock.blockid)+ "->"+str(prevblock.blockid)
            self.flist.append(temp)

            for b in self.buffer:
                if thisblock.blockid == b.prev_block.blockid:
                    temp = copy.deepcopy(b)
                    self.buffer.remove(b)
                    self.add_block(thisblock, temp)

        elif found == 0:
            self.buffer.append(thisblock)

    def print_blockchain(self, endblock):
        l = 0
        i = copy.deepcopy(endblock)
        #print endblock.blockid
        while i != None:
            #print i.blockid, i.num_trans, i.miningfee_list[0]
            l = l+1
            i = i.prev_block
        return l
    
    def print_longest(self):
        i = copy.deepcopy(self.find_longest_chain())
        l = 0
        #print endblock.blockid
        while i != None:
            print i.blockid, i.num_trans,
            l = l+1
            i = i.prev_block

   
    def find_longest_chain(self):
        max_len = 0
        max_last = None
        j = None
        for i in self.last:
            l = 0
            j = copy.deepcopy(i)
            while j != None:
                l = l+1
                j = j.prev_block

            if l > max_len:
                max_len = l
                max_last = i
            if l == max_len and max_last != None:         #the block generated earlier is the last block returned
                if (i.gen_time < max_last.gen_time):
                    max_len = l
                    max_last = i
        
        return max_last

#Class for the block Data structure
class Block:                        #corresponding to node
    def __init__(self, id, listoftrans, prevblock, nodeid):
        self.prev_block = prevblock    #its a block itself 
        self.blockid = id
        self.gen_time = time.time()     #time when the block was generated
        self.block_trans = listoftrans  #list of all transactions contained in the block
        self.num_trans = len(listoftrans)
        self.block_nodeid = nodeid


'''genesis = Block(5000, [], None, 1001)
my_chain = BlockChain(genesis)
block1 = Block(5001, ["mahima"], genesis, 1002)
my_chain.add_block(genesis, block1)
block2 = Block(5002, ["khush"], block1, 1003)
my_chain.add_block(block1, block2)

block4 = Block(5004, ["khush"], block1, 1002)
print "block4",my_chain.if_blockinchain(block4)
block3 = Block(5003, ["khu"], block1, 1002)
my_chain.add_block(block4, block3)
print len(my_chain.buffer)
print "block3",my_chain.if_blockinchain(block3)

my_chain.add_block(block1, block4)
print len(my_chain.buffer)
print "block4",my_chain.if_blockinchain(block4)



block5 = Block(5005, ["laddoo"], block3, 1003)
my_chain.add_block(block3, block5)
print my_chain.find_longest_chain().blockid'''
