# -*- coding: utf-8 -*-
"""
Day 12 - 힙·우선순위 큐 (Heap & Priority Queue) 예제 모음

표준 라이브러리 heapq 만 사용한다. cp949 콘솔에서도 안전하도록
print 출력에는 ASCII 기호(=, -, O, X)만 쓴다(한글은 OK).

핵심: 파이썬 heapq 는 "최소 힙(min-heap)"이다.
  - 가장 작은 값이 항상 heap[0] (peek).
  - 최대 힙이 필요하면 부호를 뒤집어(-x) 넣고 꺼낼 때 다시 뒤집는다.

실행:  PYTHONIOENCODING=cp949 python examples.py
"""

import heapq


# ---------------------------------------------------------------------------
# 1) 최소 힙 기본: push / pop / peek / heapify
# ---------------------------------------------------------------------------
def min_heap_basics():
    h = []
    for x in [5, 1, 8, 3, 2]:
        heapq.heappush(h, x)        # O(log n) 삽입
    peek = h[0]                     # O(1) 최솟값 확인 (꺼내지 않음)
    order = []
    while h:
        order.append(heapq.heappop(h))   # O(log n), 항상 최솟값부터
    return peek, order              # peek=1, order=[1,2,3,5,8] (정렬됨)


def heapify_in_place():
    data = [5, 1, 8, 3, 2]
    heapq.heapify(data)             # O(n) 으로 리스트를 제자리 힙으로
    return data[0], data            # 최솟값 1, 내부는 "정렬"이 아니라 "힙 순서"


# ---------------------------------------------------------------------------
# 2) 최대 힙: 부호를 뒤집어 흉내낸다
# ---------------------------------------------------------------------------
def max_heap_basics():
    h = []
    for x in [5, 1, 8, 3, 2]:
        heapq.heappush(h, -x)       # 음수로 저장
    largest = -h[0]                 # 꺼낼 때 다시 부호 복원
    order = []
    while h:
        order.append(-heapq.heappop(h))
    return largest, order           # largest=8, order=[8,5,3,2,1] (내림차순)


# ---------------------------------------------------------------------------
# 3) 튜플 우선순위 + 안정적 동점 처리(삽입 순서 카운터)
#    같은 우선순위일 때 "비교 불가" 객체에서 에러가 나지 않도록 카운터를 끼운다.
# ---------------------------------------------------------------------------
def priority_queue_tasks():
    pq = []
    counter = 0
    tasks = [(2, "email"), (1, "alarm"), (2, "report"), (0, "fire")]
    for priority, name in tasks:
        # (우선순위, 삽입순서, 데이터) - 우선순위 같으면 먼저 들어온 것이 먼저
        heapq.heappush(pq, (priority, counter, name))
        counter += 1
    out = []
    while pq:
        priority, _, name = heapq.heappop(pq)
        out.append((priority, name))
    return out   # [(0,'fire'), (1,'alarm'), (2,'email'), (2,'report')]


# ---------------------------------------------------------------------------
# 4) heappushpop / heapreplace: push+pop 을 한 번에 (각각 O(log n) 1회)
# ---------------------------------------------------------------------------
def push_pop_variants():
    h = [1, 3, 5]
    heapq.heapify(h)
    # heappushpop: 먼저 push 후 pop. (넣을 값이 더 작으면 그 값이 바로 나옴)
    a = heapq.heappushpop(h, 4)     # 4 push -> 최소 1 pop -> a=1
    # heapreplace: 먼저 pop 후 push. (반드시 기존 최솟값이 먼저 나옴)
    b = heapq.heapreplace(h, 0)     # 현재 최소 pop -> b, 그 뒤 0 push
    return a, b, sorted(h)


# ---------------------------------------------------------------------------
# 5) nlargest / nsmallest: 작은 k 에는 정렬보다 힙이 유리 (O(n log k))
# ---------------------------------------------------------------------------
def top_k_helpers():
    data = [7, 2, 9, 4, 1, 8, 3]
    top3 = heapq.nlargest(3, data)        # [9, 8, 7]
    bottom2 = heapq.nsmallest(2, data)    # [1, 2]
    # key 인자도 가능: 길이가 긴 단어 2개
    words = ["a", "abcd", "ab", "abc"]
    longest2 = heapq.nlargest(2, words, key=len)   # ['abcd', 'abc']
    return top3, bottom2, longest2


# ---------------------------------------------------------------------------
# 6) "K번째 큰 값" - 크기 k 짜리 최소 힙 유지 (O(n log k), 공간 O(k))
#    힙의 맨 아래(heap[0])가 "지금까지 본 k개 중 가장 작은 값" = 답 후보.
# ---------------------------------------------------------------------------
def kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:              # k개만 유지: 작은 것을 버린다
            heapq.heappop(h)
    return h[0]                     # 크기 k 힙의 최솟값 = k번째 큰 값


# ---------------------------------------------------------------------------
# 7) 여러 정렬된 리스트 병합: heapq.merge (게으른 이터레이터)
# ---------------------------------------------------------------------------
def merge_sorted_lists():
    a = [1, 4, 7]
    b = [2, 5, 8]
    c = [3, 6, 9]
    return list(heapq.merge(a, b, c))   # [1..9]


# ---------------------------------------------------------------------------
# 데모
# ---------------------------------------------------------------------------
def main():
    print("=" * 56)
    print("Day 12 - 힙·우선순위 큐 (Heap & Priority Queue) 예제")
    print("=" * 56)

    print("\n[1] 최소 힙 기본")
    peek, order = min_heap_basics()
    print("peek(최솟값) =", peek)            # 1
    print("pop 순서     =", order)           # [1, 2, 3, 5, 8]
    hpeek, harr = heapify_in_place()
    print("heapify 최솟값 =", hpeek, "/ 내부 =", harr)

    print("\n[2] 최대 힙 (부호 뒤집기)")
    largest, order = max_heap_basics()
    print("largest(최댓값) =", largest)      # 8
    print("pop 순서        =", order)        # [8, 5, 3, 2, 1]

    print("\n[3] 우선순위 큐 (튜플 + 동점 카운터)")
    print(priority_queue_tasks())

    print("\n[4] heappushpop / heapreplace")
    a, b, rest = push_pop_variants()
    print("heappushpop ->", a, "/ heapreplace ->", b, "/ 남은 힙 =", rest)

    print("\n[5] nlargest / nsmallest")
    top3, bottom2, longest2 = top_k_helpers()
    print("nlargest(3)  =", top3)            # [9, 8, 7]
    print("nsmallest(2) =", bottom2)         # [1, 2]
    print("longest2     =", longest2)        # ['abcd', 'abc']

    print("\n[6] K번째 큰 값 (크기 k 최소 힙)")
    print("kth_largest([3,2,1,5,6,4], 2) =", kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5

    print("\n[7] 정렬된 리스트 병합 (heapq.merge)")
    print(merge_sorted_lists())              # [1,2,3,4,5,6,7,8,9]

    print("\n모든 예제 실행 완료")


if __name__ == "__main__":
    main()
