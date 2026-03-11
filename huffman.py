import heapq  # Import heapq for priority queue implementation
from collections import Counter  # Import Counter for counting frequencies

class HuffmanNode:
    """
    Node class for Huffman tree
    
    Each node stores a character, its frequency, and references to left/right children.
    The __lt__ method allows nodes to be compared by frequency in the heap.
    """
    
    def __init__(self, char, freq):
        """
        Initialize a Huffman tree node
        
        Args:
            char: Character stored in node (None for internal nodes)
            freq: Frequency of character (or sum for internal nodes)
        """
        self.char = char  # Character (None for internal nodes)
        self.freq = freq  # Frequency count
        self.left = None  # Left child (initialized as None)
        self.right = None  # Right child (initialized as None)
    
    def __lt__(self, other):
        """
        Less than comparison for heap queue
        Allows nodes to be compared by frequency
        """
        return self.freq < other.freq  # Compare based on frequency

def huffman_coding(text):
    """
    Compress text using Huffman coding
    
    Args:
        text: Input string to compress
    
    Returns:
        tuple: (encoded_text, codes_dict, tree_root)
    """
    # Step 1: Count frequency of each character
    # Counter creates a dictionary with character frequencies
    frequency = Counter(text)
    
    # Step 2: Create a priority queue (min-heap) of leaf nodes
    heap = []  # Initialize empty heap
    
    # Create a node for each character and push to heap
    for char, freq in frequency.items():
        node = HuffmanNode(char, freq)  # Create leaf node
        heapq.heappush(heap, node)  # Push to heap (ordered by freq)
    
    # Step 3: Build Huffman tree by merging nodes
    # Continue until only one node remains (the root)
    while len(heap) > 1:
        # Pop two nodes with smallest frequencies
        left = heapq.heappop(heap)  # Smallest frequency
        right = heapq.heappop(heap)  # Second smallest
        
        # Create internal node with combined frequency
        # Internal nodes have char = None
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left  # Set left child
        merged.right = right  # Set right child
        
        # Push merged node back to heap
        heapq.heappush(heap, merged)
    
    # Step 4: Generate Huffman codes by traversing the tree
    codes = {}  # Dictionary to store character -> code mapping
    
    def generate_codes(node, code=""):
        """
        Recursively traverse Huffman tree to generate codes
        
        Args:
            node: Current node in traversal
            code: Current code string built so far
        """
        if node is None:  # Base case: empty node
            return
        
        if node.char is not None:  # Leaf node found
            codes[node.char] = code  # Store the code
            return
        
        # Recursively traverse left (add '0') and right (add '1')
        generate_codes(node.left, code + "0")
        generate_codes(node.right, code + "1")
    
    # Get root of Huffman tree (last node in heap)
    root = heap[0] if heap else None
    
    # Generate codes starting from root with empty code
    if root:
        generate_codes(root)
    
    # Step 5: Encode the original text
    encoded = ""  # Initialize empty encoded string
    for char in text:  # Loop through each character
        encoded += codes[char]  # Append its code
    
    return encoded, codes, root  # Return results

def decode(encoded, root):
    """
    Decode Huffman encoded text back to original
    
    Args:
        encoded: Encoded binary string
        root: Root of Huffman tree
    
    Returns:
        str: Decoded original text
    """
    decoded = ""  # Initialize empty decoded string
    current = root  # Start at root
    
    # Traverse the encoded string bit by bit
    for bit in encoded:
        if bit == "0":  # If bit is 0, go left
            current = current.left
        else:  # If bit is 1, go right
            current = current.right
        
        # If we reached a leaf node
        if current.char is not None:
            decoded += current.char  # Add character to result
            current = root  # Go back to root for next character
    
    return decoded  # Return decoded text

# Example usage
if __name__ == "__main__":
    text = "hello world"  # Input text
    
    # Encode the text
    encoded, codes, tree = huffman_coding(text)
    
    # Decode back to verify
    decoded = decode(encoded, tree)
    
    # Print results
    print(f"Original text: '{text}'")
    print("\nHuffman Codes:")
    for char, code in sorted(codes.items()):
        print(f"  '{char}': {code}")
    print(f"\nEncoded: {encoded}")
    print(f"Decoded: '{decoded}'")
    print(f"\nOriginal bits: {len(text) * 8}")
    print(f"Compressed bits: {len(encoded)}")
    print(f"Compression ratio: {len(encoded)/(8*len(text))*100:.1f}%")
