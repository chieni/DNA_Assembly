# DNA Fragment Assembly

## General Approach
An assumption was key to my completion of the problem: that there would be one unique way of assembling the sequence (though I did add a print statement to indicate to the user for when this would not be the case). In addition, I also used the definition of overlapping as being overlapping over half of the fragment length. 

These assumptions were instrumental to the speed of the program, as an initial implementation I had done ran much more slowly (though would be more extensible). 

In general, the program is able to accept an input file, construct sequences, determining the state of overlapping sequences, and finding the ultimate ordering of sequences to produce a final assembled sequence.

## Algorithm
1) Read in the input file, constructing the full fragments (as they are broken down line by line). Once a fragment is created, instantiate a Node object. This Node contains the sequence information, and keeps track of neighboring nodes. During the creation of each Node, I iterate through the existing nodes and determine if there are any neighbors (overlapping sequences) that have already been seen. Left and right neighbors are differentiated between. That determines if the neighbors come before or after our current Node.

2) Walk through the nodes starting at the root (the node with no left neighbor). I use saved indices to determine where the overlaps occur so that the buildup of the sequence string is straightforward. Since we assume that there is one unique ordering, it is straightforward to walk down the right nodes until we reach the end of the sequence.

3) Write resultant sequence to output file.

## Usage
python assembly.py -i <input file> -o <output file>

