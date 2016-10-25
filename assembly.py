import sys
import getopt

class Node:
	'''
	Class the represents a node of the graph. Each node is essentially
	a fragment of DNA, containing pointers to neighbor nodes.
	'''
	def __init__(self, sequence):
		self.sequence = sequence
		self.right_nodes = []
		self.right_pointers = []
		self.left_nodes = []

	def __str__(self):
		return self.sequence

	def get_sequence(self):
		return self.sequence

	def get_right(self):
		if len(self.right_nodes) == 0:
			return None
		return self.right_nodes[0]

	def get_right_pointer(self):
		'''
		A right pointer represents when the overlap ends in a
		right neighboring node. This aids in building
		the sequence.
		'''
		if len(self.right_pointers) == 0:
			return None
		if len(self.right_pointers) > 1:
			print 'There\'s more than one way to assemble this sequence'
		return self.right_pointers[0]

	def get_left(self):
		if len(self.left_nodes) == 0:
			return None
		return self.left_nodes[0]

	def add_neighbor(self, other):
		'''
		Adds a left or right neighbor to the node, based upon the
		fact that sequences validly overlap when more than half of one of the
		sequences appears in the other sequence. In this function both
		a left matching and right matching are examined.

		Input:
			other, the other node being examined for matching to this self node

		If an other can be the left, that means the second half of the other
		appears in this node. 
		other
		  herherher

		If an other can be the right, that means it that the first half
		of the other sequence appears in this node.
		     other
		'''
		half_index = len(other.get_sequence())/2
		first_half = other.get_sequence()[:half_index]
		second_half = other.get_sequence()[half_index:]

		right_start = self.sequence.find(first_half)

		# If a match is found, assert that the overlap is all valid
		if right_start > -1:
			leftover = self.sequence[right_start + len(first_half):]
			if leftover == other.get_sequence()[half_index:half_index + len(leftover)]:
				self.right_nodes.append(other)
				self.right_pointers.append(half_index + len(leftover)) # where overlap ends in other sequence
				other.left_nodes.append(self)
		else:
			left_start = self.sequence.find(second_half) 
			if left_start > -1:
				leftover = self.sequence[:left_start]
				if leftover == other.get_sequence()[half_index - len(leftover):half_index]:
					self.left_nodes.append(other)
					other.right_nodes.append(self)
					other.right_pointers.append(half_index + len(leftover)) # where overlap ends in this sequence

def walk(nodes):
	'''
	Determines the sequence by walking down all the nodes.

	Input: nodes, processed nodes using input file
	Output: sequence, string that represents the final assembled sequence

	Because each of the inputs has a unique way of being constructed, it should be 
	straightforward to walk the graph by simply propogating 
	up the parents
	'''
	print '------------------- Walking all nodes -------------------'
	# Find the root by getting the node that does not have a parent
	sequence = ""
	pointer = 0
	current = None
	for node in nodes:
		if node.get_left() == None:
			current = node
			break

	while current != None:
		sequence += current.get_sequence()[pointer:]
		pointer = current.get_right_pointer()
		current = current.get_right()
	print '------------------- Complete -------------------'
	return sequence

def make_nodes(sequence, nodes):
	'''
	Adds the neighbors of a sequence (either right or left) and also
	creates and adds nodes.

	Input:
		sequence, a string fragment of DNA
		nodes, mutable list of all nodes
	'''

	other = Node(sequence)
	for node in nodes:
		node.add_neighbor(other)
	nodes.append(other)

def assembly(input, output):
	'''
	Function that performs the assembly of DNA fragments from input to output

	Input:
		input, filename of input file
		output, filename of intended output file
	'''
	nodes = []
	with open(input) as infile:
		next(infile)
		current = ""
		for line in infile:
			if line[0] == '>':
				make_nodes(current, nodes)
				current = ""
			else:
				current += line.strip()
		make_nodes(current, nodes)

	open(output, 'wb').write(walk(nodes))

'''
usage: assembly.py -i <inputfile> -o <outputfile>
'''
def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   
   assembly(inputfile, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

