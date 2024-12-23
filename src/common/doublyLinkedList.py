class LLNode:
    def __init__(self, data, linked_list):
        self.data = data
        self.prev = None
        self.next = None
        self.linked_list = linked_list

    def insertAfter(self, data):
        new_node = LLNode(data, self.linked_list)
        new_node.next = self.next
        new_node.prev = self
        self.next = new_node
        return new_node

    def insertBefore(self, data):
        new_node = LLNode(data, self.linked_list)
        new_node.prev = self.prev
        new_node.next = self
        self.prev = new_node
        return new_node


class DoublyLinkedList:
    def __init__(self, starting_values = None):
        self.head = None
        self.tail = None
        self._current = None  # For iteration

        if starting_values is not None:
            for value in starting_values:
                self.append(value)

    def append(self, data):
        new_node = LLNode(data, self)
        if self.head is None:  # If the list is empty
            self.head = self.tail = new_node
        else:  # Add to the end
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        return new_node

    def prepend(self, data):
        new_node = LLNode(data, self)
        if self.head is None:  # If the list is empty
            self.head = self.tail = new_node
        else:  # Add to the start
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        return new_node

    def delete(self, data):
        current = self.head
        while current:  # Traverse to find the node to delete
            if current.data == data:
                if current.prev:  # Node is not the head
                    current.prev.next = current.next
                else:  # Node is the head
                    self.head = current.next
                
                if current.next:  # Node is not the tail
                    current.next.prev = current.prev
                else:  # Node is the tail
                    self.tail = current.prev

                return True  # Data found and deleted
            current = current.next
        return False  # Data not found

    # Iterator methods
    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        data = self._current
        self._current = self._current.next
        return data
    
    # Length
    def __len__(self):
        count = 0
        for val in self:
            count += 1
        return count