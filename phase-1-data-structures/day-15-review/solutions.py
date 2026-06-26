"""
Day 15 - 자료구조 종합 복습 (Data Structures Review) 해설/풀이
--------------------------------------------------
실행:  PYTHONIOENCODING=cp949 python solutions.py

- LeetCode 문제는 'class Solution', 프로그래머스 문제는 'def solution' 시그니처.
- 각 문제에 assert 자체 테스트. 가능하면 한 문제에 여러 접근 + 복잡도 비교.
- 콘솔 출력은 cp949 안전 문자만(ASCII =,-,O,X). 한글 OK. 표준 라이브러리만.

Phase 1 전 범위를 섞은 복습 세트: 스택 / 큐 / 해시 / 연결 리스트 / 트리 / 힙.
"""

from collections import deque, Counter, defaultdict
from typing import List, Optional
import heapq
import math


# =========================================================
# 1) LeetCode #20 - Valid Parentheses  (기초, 스택)
# =========================================================
class SolutionValidParen:
    # 접근 A: 스택 - 여는 괄호는 push, 닫는 괄호는 짝 검사, O(n) / O(n)
    def isValid(self, s: str) -> bool:
        pair = {')': '(', ']': '[', '}': '{'}
        stack = []
        for ch in s:
            if ch in '([{':
                stack.append(ch)
            elif not stack or stack.pop() != pair[ch]:
                return False
        return not stack


# =========================================================
# 2) LeetCode #232 - Implement Queue using Stacks  (기초)
#    두 스택(in/out)으로 FIFO 구현. 분할 상환(amortized) O(1).
# =========================================================
class MyQueue:
    def __init__(self):
        self.in_st = []      # push 받는 스택
        self.out_st = []     # pop/peek 내보내는 스택

    def push(self, x: int) -> None:
        self.in_st.append(x)

    def _move(self):
        if not self.out_st:                 # out 이 비면 in 을 뒤집어 옮긴다
            while self.in_st:
                self.out_st.append(self.in_st.pop())

    def pop(self) -> int:
        self._move()
        return self.out_st.pop()

    def peek(self) -> int:
        self._move()
        return self.out_st[-1]

    def empty(self) -> bool:
        return not self.in_st and not self.out_st


# =========================================================
# 3) LeetCode #1 - Two Sum  (기초, 해시)
# =========================================================
class SolutionTwoSum:
    # 접근 A: 해시맵 한 번 순회, O(n) / O(n)   (권장)
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []

    # 접근 B: 이중 루프, O(n^2) / O(1) (비교용 - 큰 입력엔 부적합)
    def twoSum_bruteforce(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


# =========================================================
# 4) LeetCode #206 - Reverse Linked List  (기초, 연결 리스트)
# =========================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionReverseList:
    # 접근 A: 반복(iterative), O(n) / O(1)   (권장)
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        while head:
            nxt = head.next      # 끊기 전에 다음 노드 보관
            head.next = prev
            prev = head
            head = nxt
        return prev

    # 접근 B: 재귀, O(n) / O(n) 스택 (개념 정리용)
    def reverseList_rec(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        new_head = self.reverseList_rec(head.next)
        head.next.next = head
        head.next = None
        return new_head


# =========================================================
# 5) LeetCode #104 - Maximum Depth of Binary Tree  (기초, 트리)
# =========================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class SolutionMaxDepth:
    # 접근 A: 재귀 DFS, O(n) / O(h) (h=트리 높이)
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

    # 접근 B: 큐 BFS 레벨 카운트, O(n) / O(n)
    def maxDepth_bfs(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        depth = 0
        q = deque([root])
        while q:
            depth += 1
            for _ in range(len(q)):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return depth


# =========================================================
# 6) LeetCode #739 - Daily Temperatures  (중급, 단조 스택)
# =========================================================
class SolutionDailyTemps:
    # 접근 A: 단조 감소 스택(인덱스 보관), O(n) / O(n)   (권장)
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        ans = [0] * len(temperatures)
        stack = []
        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                ans[j] = i - j
            stack.append(i)
        return ans

    # 접근 B: 이중 루프, O(n^2) (비교용)
    def dailyTemperatures_bruteforce(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if temperatures[j] > temperatures[i]:
                    ans[i] = j - i
                    break
        return ans


# =========================================================
# 7) LeetCode #347 - Top K Frequent Elements  (중급, 해시+힙)
# =========================================================
class SolutionTopK:
    # 접근 A: Counter + 크기 K 힙(nlargest), O(n log k) / O(n)   (권장)
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        return [v for v, _ in heapq.nlargest(k, freq.items(),
                                             key=lambda kv: kv[1])]

    # 접근 B: 버킷 정렬(빈도를 인덱스로), O(n) / O(n)
    def topKFrequent_bucket(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]   # 빈도 -> 값 목록
        for v, c in freq.items():
            buckets[c].append(v)
        res = []
        for c in range(len(buckets) - 1, 0, -1):       # 높은 빈도부터
            for v in buckets[c]:
                res.append(v)
                if len(res) == k:
                    return res
        return res


# =========================================================
# 8) LeetCode #703 - Kth Largest Element in a Stream  (기초, 크기 K 힙)
#    핵심: 크기 K 최소 힙을 유지하면 힙의 최솟값이 곧 K번째 큰 값.
# =========================================================
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


# =========================================================
# 9) 프로그래머스 #42586 - 기능개발  (중급, 큐)
#    앞 작업이 끝나야 함께 배포. 누적 진도로 완료일을 구하고 큐처럼 처리.
# =========================================================
def solution_42586(progresses, speeds):
    # 각 작업의 완료까지 걸리는 '일수' (올림)
    days = [math.ceil((100 - p) / s) for p, s in zip(progresses, speeds)]
    answer = []
    cur = days[0]            # 현재 배포 묶음의 기준(최대) 완료일
    count = 0
    for d in days:
        if d <= cur:         # 기준일 안에 끝나면 같은 배포에 합류
            count += 1
        else:                # 더 늦게 끝나면 이전 묶음을 배포하고 새 기준
            answer.append(count)
            cur = d
            count = 1
    answer.append(count)
    return answer


# =========================================================
# 10) 프로그래머스 #42579 - 베스트앨범  (중급, 해시+정렬)
#     장르별 총 재생수로 장르 순서를 정하고, 장르 내 (재생수, 인덱스)로 2곡.
# =========================================================
def solution_42579(genres, plays):
    total = defaultdict(int)                 # 장르 -> 총 재생수
    songs = defaultdict(list)                # 장르 -> [(재생수, 인덱스)]
    for i, (g, p) in enumerate(zip(genres, plays)):
        total[g] += p
        songs[g].append((p, i))

    answer = []
    # 장르: 총 재생수 내림차순
    for g in sorted(total, key=lambda x: -total[x]):
        # 장르 내: 재생수 내림차순, 같으면 인덱스 오름차순 -> 최대 2곡
        picked = sorted(songs[g], key=lambda t: (-t[0], t[1]))[:2]
        answer.extend(i for _, i in picked)
    return answer


# =========================================================
# 헬퍼: 리스트 <-> 연결 리스트
# =========================================================
def _build(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def _to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# =========================================================
# 자체 테스트
# =========================================================
def _run_tests():
    # 1) Valid Parentheses
    s1 = SolutionValidParen()
    assert s1.isValid("()[]{}") is True
    assert s1.isValid("(]") is False
    assert s1.isValid("([)]") is False
    assert s1.isValid("{[]}") is True

    # 2) Implement Queue using Stacks
    q = MyQueue()
    q.push(1); q.push(2)
    assert q.peek() == 1
    assert q.pop() == 1
    q.push(3)
    assert q.pop() == 2
    assert q.pop() == 3
    assert q.empty() is True

    # 3) Two Sum (두 접근 일치 확인)
    s3 = SolutionTwoSum()
    assert s3.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s3.twoSum([3, 2, 4], 6) == [1, 2]
    for nums, t in ([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6):
        assert s3.twoSum(nums, t) == s3.twoSum_bruteforce(nums, t)

    # 4) Reverse Linked List (두 접근 일치 확인)
    s4 = SolutionReverseList()
    assert _to_list(s4.reverseList(_build([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert _to_list(s4.reverseList_rec(_build([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert _to_list(s4.reverseList(_build([]))) == []

    # 5) Maximum Depth of Binary Tree (두 접근 일치 확인)
    s5 = SolutionMaxDepth()
    root = TreeNode(3, TreeNode(9),
                    TreeNode(20, TreeNode(15), TreeNode(7)))
    assert s5.maxDepth(root) == 3
    assert s5.maxDepth_bfs(root) == 3
    assert s5.maxDepth(None) == 0

    # 6) Daily Temperatures (두 접근 일치 확인)
    s6 = SolutionDailyTemps()
    assert s6.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == \
        [1, 1, 4, 2, 1, 1, 0, 0]
    assert s6.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    for t in ([73, 74, 75, 71, 69, 72, 76, 73], [30, 60, 90], [90, 60, 30]):
        assert s6.dailyTemperatures(t) == s6.dailyTemperatures_bruteforce(t)

    # 7) Top K Frequent (두 접근 결과 집합 일치)
    s7 = SolutionTopK()
    assert sorted(s7.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert s7.topKFrequent([1], 1) == [1]
    for nums, k in ([1, 1, 1, 2, 2, 3], 2), ([4, 4, 5, 5, 5, 6], 2):
        assert sorted(s7.topKFrequent(nums, k)) == \
            sorted(s7.topKFrequent_bucket(nums, k))

    # 8) Kth Largest in a Stream
    kl = KthLargest(3, [4, 5, 8, 2])
    assert kl.add(3) == 4
    assert kl.add(5) == 5
    assert kl.add(10) == 5
    assert kl.add(9) == 8
    assert kl.add(4) == 8

    # 9) 기능개발
    assert solution_42586([93, 30, 55], [1, 30, 5]) == [2, 1]
    assert solution_42586([95, 90, 99, 99, 80, 99], [1, 1, 1, 1, 1, 1]) == [1, 3, 2]

    # 10) 베스트앨범
    assert solution_42579(
        ["classic", "pop", "classic", "classic", "pop"],
        [500, 600, 150, 800, 2500]) == [4, 1, 3, 0]

    print("OK - 모든 테스트 통과 (10개 문제)")


if __name__ == "__main__":
    _run_tests()
