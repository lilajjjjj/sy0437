
import os

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.ordering = self.CircularLinkedList()

    def get(self, key):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self.ordering.remove(node)
        self.ordering.append(node)
        return node.item

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.item = value
            self.ordering.remove(node)
            self.ordering.append(node)
        else:
            if self.size == self.capacity:
                lru_node = self.ordering.head.next
                del self.cache[lru_node.item]
                self.ordering.remove(lru_node)
                self.size -= 1
            new_node = self.ordering.ListNode(key, None)  # 수정된 부분
            self.cache[key] = new_node
            self.ordering.append(new_node)
            self.size += 1

    class CircularLinkedList:
        class ListNode:  # ListNode 클래스를 CircularLinkedList 내부에 정의
            def __init__(self, item, next):
                self.item = item
                self.next = next
                self.prev = None

        def __init__(self):
            self.head = self.ListNode('dummy', None)
            self.head.next = self.head
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

def calculate_hit_ratio(cache_size):
    total_requests = 0
    cache_hits = 0
    cache = LRUCache(cache_size)

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'linkbench.trc')

    with open(file_path, 'r') as file:
        for line in file:
            total_requests += 1
            request = line.strip().split()  # Assuming each line is space-separated
            if len(request) > 1:
                request_type, key = request[0], request[1]
                if request_type == 'GET':
                    if cache.get(key) != -1:
                        cache_hits += 1
                elif request_type == 'PUT':
                    value = request[2] if len(request) > 2 else None
                    cache.put(key, value)

    hit_ratio = cache_hits / total_requests
    return hit_ratio

def main():
    for cache_size in range(100, 1001, 100):
        hit_ratio = calculate_hit_ratio(cache_size)
        print(f"Cache Size: {cache_size}, Hit Ratio: {hit_ratio}")

if __name__ == "__main__":
    main()