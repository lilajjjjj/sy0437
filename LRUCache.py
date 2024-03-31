class ListNode:
    def __init__(self, newItem, nextNode=None):
        self.item = newItem
        self.next = nextNode

class CircularLinkedList:
    def __init__(self):
        self.head = ListNode('dummy')
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

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.ordering = CircularLinkedList()  # CircularLinkedList를 사용하여 순서를 유지한다.

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
            new_node = ListNode(key, None)
            self.cache[key] = new_node
            self.ordering.append(new_node)
            self.size += 1

def calculate_hit_ratio(cache_size):
    cache = LRUCache(cache_size)
    total_requests = 0
    cache_hits = 0
    with open('/lru_sim/linkbench.trc/to/linkbench.trc') as file:  # 실제 파일 경로로 수정해야 합니다.
        for line in file:
            total_requests += 1
            key = line.strip()  # Assuming each line is a key
            if cache.get(key) != -1:
                cache_hits += 1
            else:
                cache.put(key, 1)  # Value doesn't matter for hit ratio calculation
    hit_ratio = cache_hits / total_requests if total_requests > 0 else 0
    return hit_ratio

def main():
    for cache_size in range(100, 1001, 100):
        hit_ratio = calculate_hit_ratio(cache_size)
        print(f"Cache Size: {cache_size}, Hit Ratio: {hit_ratio}")

if __name__ == "__main__":
    main()
