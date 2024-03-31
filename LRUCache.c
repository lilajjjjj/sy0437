#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//이중 연결 리스트의 노드를 나타내는 구조체
typedef struct ListNode {
    char* key;
    int value;
    struct ListNode* prev;
    struct ListNode* next;
} ListNode;

//LRUCache 구조체
typedef struct {
    int capacity;
    int size;
    ListNode* head;
    ListNode* tail;
    // 해시 테이블을 사용하여 빠른 키 조회를 위한 배열
    ListNode** table;
} LRUCache;

//새로운 노드를 생성하는 함수
ListNode* createNode(char* key, int value) {
    ListNode* node = (ListNode*)malloc(sizeof(ListNode));
    node->key = strdup(key);
    node->value = value;
    node->prev = NULL;
    node->next = NULL;
    return node;
}

//새로운 LRUCache를 생성하는 함수
LRUCache* createLRUCache(int capacity) {
    LRUCache* cache = (LRUCache*)malloc(sizeof(LRUCache));
    cache->capacity = capacity;
    cache->size = 0;
    cache->head = NULL;
    cache->tail = NULL;
    cache->table = (ListNode**)calloc(capacity, sizeof(ListNode*));
    return cache;
}

//LRUCache에서 키에 해당하는 값을 가져오는 함수
int get(LRUCache* cache, char* key) {
    ListNode* node = cache->table[*key % cache->capacity];
    while (node != NULL) {
        if (strcmp(node->key, key) == 0) {
            // 값을 찾으면 해당 값을 반환하고, 노드를 최신으로 업데이트
            if (node != cache->head) {
                node->prev->next = node->next;
                if (node != cache->tail) {
                    node->next->prev = node->prev;
                } else {
                    cache->tail = node->prev;
                }
                node->next = cache->head;
                node->prev = NULL;
                cache->head->prev = node;
                cache->head = node;
            }
            return node->value;
        }
        node = node->next;
    }
    return -1; // 키를 찾지 못한 경우 -1 반환
}

//LRUCache에 키-값 쌍을 추가하는 함수
void put(LRUCache* cache, char* key, int value) {
    ListNode* node = cache->table[*key % cache->capacity];
    while (node != NULL) {
        if (strcmp(node->key, key) == 0) {
            // 이미 존재하는 키인 경우 값만 업데이트하고 노드를 최신으로 업데이트
            node->value = value;
            if (node != cache->head) {
                node->prev->next = node->next;
                if (node != cache->tail) {
                    node->next->prev = node->prev;
                } else {
                    cache->tail = node->prev;
                }
                node->next = cache->head;
                node->prev = NULL;
                cache->head->prev = node;
                cache->head = node;
            }
            return;
        }
        node = node->next;
    }

    // 키가 존재하지 않는 경우 새로운 노드를 생성하여 추가
    ListNode* newNode = createNode(key, value);
    newNode->next = cache->head;
    if (cache->head != NULL) {
        cache->head->prev = newNode;
    }
    cache->head = newNode;
    if (cache->tail == NULL) {
        cache->tail = newNode;
    }
    cache->table[*key % cache->capacity] = newNode;

    // 캐시 크기가 capacity를 초과하는 경우 가장 오래된 노드를 제거
    if (cache->size == cache->capacity) {
        ListNode* tail = cache->tail;
        cache->tail = tail->prev;
        if (cache->tail != NULL) {
            cache->tail->next = NULL;
        }
        cache->table[*tail->key % cache->capacity] = NULL;
        free(tail->key);
        free(tail);
    } else {
        cache->size++;
    }
}

// LRUCache를 삭제하는 함수
void destroyLRUCache(LRUCache* cache) {
    while (cache->head != NULL) {
        ListNode* tmp = cache->head;
        cache->head = cache->head->next;
        free(tmp->key);
        free(tmp);
    }
    free(cache->table);
    free(cache);
}

int main() {
    // 캐시 크기를 100에서 1000까지 변화시키면서 테스트
    for (int capacity = 100; capacity <= 1000; capacity += 100) {
        LRUCache* cache = createLRUCache(capacity);

        // linkbench.trc 파일을 읽고 테스트 데이터 생성
        FILE* file = fopen("linkbench.trc", "r");
        if (file == NULL) {
            fprintf(stderr, "Error: Unable to open file\n");
            return 1;
        }

        int hits = 0;
        int requests = 0;
        char key[100];
        while (fscanf(file, "%s", key) != EOF) {
            if (get(cache, key) != -1) {
                hits++;
            } else {
                put(cache, key, 1);
            }
            requests++;
        }
        fclose(file);

        // 히트 비율 출력
        double hit_ratio = (double)hits / requests * 100;
        printf("Cache size: %d, Hit ratio: %.2f%%\n", capacity, hit_ratio);

        // LRUCache 삭제
        destroyLRUCache(cache);
    }

    return 0;
}