class LRUCache:
    class ListNode:
        def __init__(self, newItem, nextNode:'ListNode'):
            self.item = newItem
            self.next = nextNode
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.ordering = self.CircularLinkedList()  # CircularLinkedList를 사용하여 순서를 유지한다.

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.ordering.remove(node)  # 기존의 remove 메서드를 사용하여 해당 노드를 삭제한다.
        self.ordering.append(node)  # append 메서드를 사용하여 해당 노드를 끝으로 이동시킨다.
        return node.item

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.item = value
            self.ordering.remove(node)  # 기존의 remove 메서드를 사용하여 해당 노드를 삭제한다.
            self.ordering.append(node)  # append 메서드를 사용하여 해당 노드를 끝으로 이동시킨다.
        else:
            if self.size == self.capacity:
                lru_node = self.ordering.head.next  # CircularLinkedList의 첫 번째 노드를 가져온다.
                del self.cache[lru_node.item]
                self.ordering.remove(lru_node)  # CircularLinkedList에서 첫 번째 노드를 삭제한다.
                self.size -= 1
            new_node = self.ListNode(key, None)
            self.cache[key] = new_node
            self.ordering.append(new_node)  # 새로운 노드를 CircularLinkedList에 추가한다.
            self.size += 1

    class CircularLinkedList:
        def __init__(self):
            self.head = self.ListNode('dummy', None)
            self.head.next = self.head  # CircularLinkedList의 특성을 갖기 위해 머리 노드의 다음을 자기 자신으로 지정한다.
            self.head.prev = self.head
            self.numItems = 0

        def append(self, newNode):
            newNode.next = self.head
            newNode.prev = self.head.prev
            self.head.prev.next = newNode
            self.head.prev = newNode
            self.numItems += 1

        def remove(self, node):
            node.prev.next = node.next
            node.next.prev = node.prev
            node.prev = None
            node.next = None
            self.numItems -= 1