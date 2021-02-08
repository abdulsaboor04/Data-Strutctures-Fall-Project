class FibonacciHeap:
    # internal node class
    class Node:
        def __init__(self, key):
            self.key = key               #Value of node
            self.parent =None            #Parent of node
            self.child = None          #Childeren of node
            self.left = None          #Left sibling of node
            self.right = None          #Right sibling of node
            self.degree = 0          #Degree of node
            self.mark = False          #Whether the node is marked or not

    #This function will help iteratingg through the doubly linked list
    def iterate(self, H):
        N = stop = H
        flag = False
        while True:
            if N == stop and flag is True:
                break
            elif N == stop:
                flag = True
            yield N
            N = N.right


    AllRoots =None
    minNode = None  #Always points to the minimum node
    TotalNodes = 0  #Tells the total amount of nodes in a heap


    # return min node
    def find_min(self):
        return self.minNode

    # To delete/extract the minimum node
    def extract_min(self):
        DelMin = self.minNode
        if DelMin is not None:
            if DelMin.child is not None:
                # to add the child node in the root list
                children = [i for i in self.iterate(DelMin.child)]
                for i in range(0, len(children)):
                    self.merge_with_AllRoots(children[i])
                    children[i].parent = None
            self.remove_from_AllRoots(DelMin)
            # Set the min node pointer to the new min node
            if DelMin == DelMin.right:
                self.minNode = self.AllRoots = None
            else:
                self.minNode = DelMin.right
                self.consolidate()
            self.TotalNodes -= 1
        return DelMin

    # Inserting the new node in the list in which all the roots are present
    def insert(self, key):
        newNode = self.Node(key)
        newNode.left = newNode.right = newNode
        self.merge_with_AllRoots(newNode)
        if self.minNode is None or newNode.key < self.minNode.key:
            self.minNode = newNode
        self.TotalNodes += 1

    #To change the key of any node
    def decrease_key(self, ExistingNode, newKey):
        if newKey > ExistingNode.key:
            return None
        ExistingNode.key = newKey
        nodeParent = ExistingNode.parent
        if nodeParent is not None and ExistingNode.key < nodeParent.key:
            self.cut(ExistingNode, nodeParent)
            self.cascading_cut(nodeParent)
        if ExistingNode.key < self.minNode.key:
            self.minNode = ExistingNode

    #To merge 2 heaps and make a single heap out of them
    def merge(self, H2):
        H1 = FibonacciHeap()
        H1.AllRoots, H1.minNode = self.AllRoots, self.minNode
        #While merging the heaps we ll also fix all the respective pointers
        last = H2.AllRoots.left
        H2.AllRoots.left = H1.AllRoots.left
        H1.AllRoots.left.right = H2.AllRoots
        H1.AllRoots.left = last
        H1.AllRoots.left.right = H1.AllRoots
        # update min node if needed
        if H2.minNode.key < H1.minNode.key:
            H1.minNode = H2.minNode
        # update total nodes
        H1.TotalNodes = self.TotalNodes + H2.TotalNodes
        return H1

    # if child becomes smaller than the parent it violates min heap order
    # so now we bring cut this child and bring it upto the root list
    def cut(self, ExistingNode, nodeParent):
        self.remove_from_child_list(nodeParent, ExistingNode)
        nodeParent.degree -= 1
        self.merge_with_AllRoots(ExistingNode)
        ExistingNode.parent = None
        ExistingNode.mark = False

    # Cascading cut the parent
    def cascading_cut(self, nodeParent):
        DelMin = nodeParent.parent
        if DelMin is not None:
            if nodeParent.mark is False:
                nodeParent.mark = True
            else:
                self.cut(nodeParent, DelMin)
                self.cascading_cut(DelMin)

    # To combine all the roots having same degree accordingly
    # by creating an empty array

    def consolidate(self):
        ConsoArray = [None] * self.TotalNodes
        newArr = [i for i in self.iterate(self.AllRoots)]
        for w in range(0, len(newArr)):
            ExistingNode = newArr[w]
            oldDeg = ExistingNode.degree
            while ConsoArray[oldDeg] != None:
                nodeParent = ConsoArray[oldDeg]
                if ExistingNode.key > nodeParent.key:
                    temp = ExistingNode
                    ExistingNode, nodeParent = nodeParent, temp
                self.heap_link(nodeParent, ExistingNode)
                ConsoArray[oldDeg] = None
                oldDeg += 1
            ConsoArray[oldDeg] = ExistingNode
        #Updating the min node constantlyy while iterating
        for i in range(0, len(ConsoArray)):
            if ConsoArray[i] is not None:
                if ConsoArray[i].key < self.minNode.key:
                    self.minNode = ConsoArray[i]


    def Delete(self,key):
        self.decrease_key(key,-99)
        self.extract_min()



    def heap_link(self, nodeParent, ExistingNode):
        self.remove_from_AllRoots(nodeParent)
        nodeParent.left = nodeParent.right = nodeParent
        self.merge_with_child_list(ExistingNode, nodeParent)
        ExistingNode.degree += 1
        nodeParent.parent = ExistingNode
        nodeParent.mark = False

    # To add the node in doubly linked Roots list
    def merge_with_AllRoots(self, node):
        if self.AllRoots is None:
            self.AllRoots = node
        else:
            node.right = self.AllRoots.right
            node.left = self.AllRoots
            self.AllRoots.right.left = node
            self.AllRoots.right = node

    # add a node in doubly linked child list
    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    # To delete a node from root list
    def remove_from_AllRoots(self, node):
        if node == self.AllRoots:
            self.AllRoots = node.right
        node.left.right = node.right
        node.right.left = node.left

    # To delete a node from child list
    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left

fibonacci_heap = FibonacciHeap()

fibonacci_heap.insert(7)
fibonacci_heap.insert(3)
fibonacci_heap.insert(17)
fibonacci_heap.insert(24)
fibonacci_heap.insert(8)
fibonacci_heap.insert(4)
fibonacci_heap.insert(6)
fibonacci_heap.insert(11)
fibonacci_heap.insert(9)
fibonacci_heap.insert(10)

print("Total Nodes : ",fibonacci_heap.TotalNodes)
print("Min Key : ",fibonacci_heap.find_min().key)
print("Min Key Deleted", fibonacci_heap.extract_min().key)
#fibonacci_heap.decrease_key(24, 25)
print("Min key after extracting",fibonacci_heap.find_min().key)
print("Total Nodes after deleting : ",fibonacci_heap.TotalNodes)
