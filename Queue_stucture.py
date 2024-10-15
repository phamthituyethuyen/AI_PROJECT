class Queues:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0
    def enqueue(self, value):
        if self.has_space():
            item_to_add = Node(value)
            print("Adding" +str(item_to_add.get_value()) + "to the queue")
            if self.is_empty():
                self.head = item_to_add
                self.tail = item_to_add
            else:
                print("sorry, no more room")

    def dequeue(self):
        if self.get_size() >0:
            item_to_remove = self.head
            print(str(item_to_remove.get_value()) + "is served")
            if self.get_size == 1:
                self.head = None
                self.tail = None
            else:
                self.head = self.head.get_next_node()
            self.size -=1
            return item_to_remove.get_value()
        else:
            print("No orders waiting!")
            
    def peek(self):
        if self.size > 0:
            return self.head.get_value()
        else:
            print("no oders waiting")
          

    def get_size(self):
        return self.size
    def is_empty(self):
        return self.size == 0