# -*- coding: utf-8 -*-
"""
Day 30 - 개념 집중기 종합 복습 (Final Review) 해설

각 문제를 "세 개의 질문"(자료구조 / 기법 / 탐색)으로 분해하고,
가능한 경우 다중 접근을 복잡도와 함께 비교한다.
플랫폼 시그니처 유지: LeetCode -> class Solution / 프로그래머스 -> def solution.

cp949 콘솔 안전: print 문자열은 ASCII 기호(=,-,O,X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import deque, Counter, defaultdict
import heapq


# ===========================================================================
# 1. Valid Anagram (LeetCode #242) - 해시 vs 정렬
# ===========================================================================
class SolutionAnagram:
    def isAnagram_hash(self, s: str, t: str) -> bool:
        # 접근 1) Counter 비교: O(n) 시간, O(k) 공간(문자 종류)
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)

    def isAnagram_sort(self, s: str, t: str) -> bool:
        # 접근 2) 정렬 비교: O(n log n) 시간
        return sorted(s) == sorted(t)


# ===========================================================================
# 2. Two Sum (LeetCode #1) - 해시 O(1) 조회 vs 브루트포스
# ===========================================================================
class SolutionTwoSum:
    def twoSum_hash(self, nums, target):
        # 접근 1) 해시: 이미 본 값을 O(1)에 조회 -> 전체 O(n)
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []

    def twoSum_brute(self, nums, target):
        # 접근 2) 브루트포스: O(n^2) (기준선)
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


# ===========================================================================
# 3. Valid Parentheses (LeetCode #20) - 스택
# ===========================================================================
class SolutionParen:
    def isValid(self, s: str) -> bool:
        pair = {')': '(', ']': '[', '}': '{'}
        stack = []
        for ch in s:
            if ch in '([{':
                stack.append(ch)
            elif not stack or stack.pop() != pair[ch]:
                return False
        return not stack


# ===========================================================================
# 4. Binary Search (LeetCode #704) - 손코딩 vs bisect
# ===========================================================================
class SolutionBSearch:
    def search_manual(self, nums, target):
        # 접근 1) 직접 이분 탐색: O(log n)
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    def search_bisect(self, nums, target):
        # 접근 2) 표준 라이브러리 bisect: off-by-one 버그 감소
        import bisect
        i = bisect.bisect_left(nums, target)
        return i if i < len(nums) and nums[i] == target else -1


# ===========================================================================
# 5. Number of Islands (LeetCode #200) - DFS vs BFS
# ===========================================================================
class SolutionIslands:
    def numIslands_dfs(self, grid):
        # 접근 1) DFS: 방문 칸을 '0'으로 덮어써 visited 대체. O(R*C)
        if not grid:
            return 0
        g = [row[:] for row in grid]
        R, C = len(g), len(g[0])

        def sink(r, c):
            if r < 0 or r >= R or c < 0 or c >= C or g[r][c] != '1':
                return
            g[r][c] = '0'
            sink(r + 1, c); sink(r - 1, c)
            sink(r, c + 1); sink(r, c - 1)

        count = 0
        for r in range(R):
            for c in range(C):
                if g[r][c] == '1':
                    count += 1
                    sink(r, c)
        return count

    def numIslands_bfs(self, grid):
        # 접근 2) BFS: 큐로 확장 -> 깊은 그리드에서 재귀 한계 회피. O(R*C)
        if not grid:
            return 0
        g = [row[:] for row in grid]
        R, C = len(g), len(g[0])
        count = 0
        for sr in range(R):
            for sc in range(C):
                if g[sr][sc] == '1':
                    count += 1
                    g[sr][sc] = '0'
                    q = deque([(sr, sc)])
                    while q:
                        r, c = q.popleft()
                        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] == '1':
                                g[nr][nc] = '0'
                                q.append((nr, nc))
        return count


# ===========================================================================
# 6. Merge Intervals (LeetCode #56) - 정렬 + 그리디
# ===========================================================================
class SolutionMerge:
    def merge(self, intervals):
        # 시작점 정렬 후 앞에서부터 겹치면 확장. O(n log n)
        intervals = sorted(intervals)
        out = []
        for s, e in intervals:
            if out and s <= out[-1][1]:
                out[-1][1] = max(out[-1][1], e)
            else:
                out.append([s, e])
        return out


# ===========================================================================
# 7. Top K Frequent Elements (LeetCode #347) - 힙 vs 버킷 정렬
# ===========================================================================
class SolutionTopK:
    def topKFrequent_heap(self, nums, k):
        # 접근 1) 해시 집계 + 힙: O(n log k)
        freq = Counter(nums)
        return [x for x, _ in heapq.nlargest(k, freq.items(), key=lambda kv: kv[1])]

    def topKFrequent_bucket(self, nums, k):
        # 접근 2) 버킷 정렬: 빈도를 인덱스로 -> O(n)
        freq = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]
        for x, c in freq.items():
            buckets[c].append(x)
        res = []
        for c in range(len(buckets) - 1, 0, -1):
            for x in buckets[c]:
                res.append(x)
                if len(res) == k:
                    return res
        return res


# ===========================================================================
# 8. Course Schedule (LeetCode #207) - 위상 정렬(BFS, Kahn)
# ===========================================================================
class SolutionCourse:
    def canFinish(self, numCourses, prerequisites):
        # 진입차수 0부터 큐로 제거 -> 제거 수가 전체면 사이클 없음(DAG). O(V+E)
        indeg = [0] * numCourses
        adj = defaultdict(list)
        for a, b in prerequisites:          # b -> a (b가 a의 선수과목)
            adj[b].append(a)
            indeg[a] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        done = 0
        while q:
            u = q.popleft()
            done += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return done == numCourses


# ===========================================================================
# 9. 타겟 넘버 (프로그래머스 #43165) - DFS 완전 탐색
#    프로그래머스 시그니처: def solution(numbers, target)
# ===========================================================================
def solution_target(numbers, target):
    # 각 수에 +/- 를 붙이는 2^n 조합을 DFS로 모두 시도. n<=20이라 허용
    def dfs(i, total):
        if i == len(numbers):
            return 1 if total == target else 0
        return dfs(i + 1, total + numbers[i]) + dfs(i + 1, total - numbers[i])
    return dfs(0, 0)


# ===========================================================================
# 10. 네트워크 (프로그래머스 #43162) - 연결 요소 세기 (DFS / Union-Find)
#     프로그래머스 시그니처: def solution(n, computers)
# ===========================================================================
def solution_network(n, computers):
    # 접근 1) DFS: 방문 안 한 노드에서 시작할 때마다 컴포넌트 +1. O(n^2)
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        for v in range(n):
            if computers[u][v] == 1 and not visited[v]:
                dfs(v)

    groups = 0
    for i in range(n):
        if not visited[i]:
            groups += 1
            dfs(i)
    return groups


def solution_network_union(n, computers):
    # 접근 2) Union-Find: 연결을 합치고 남은 대표원소 수 = 네트워크 수
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # 경로 압축
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i in range(n):
        for j in range(i + 1, n):
            if computers[i][j] == 1:
                union(i, j)
    return len({find(i) for i in range(n)})


# ===========================================================================
# 자체 테스트
# ===========================================================================
def _run_tests():
    # 1. Valid Anagram
    a = SolutionAnagram()
    for f in (a.isAnagram_hash, a.isAnagram_sort):
        assert f("anagram", "nagaram") is True
        assert f("rat", "car") is False
        assert f("a", "ab") is False

    # 2. Two Sum
    ts = SolutionTwoSum()
    for f in (ts.twoSum_hash, ts.twoSum_brute):
        assert f([2, 7, 11, 15], 9) == [0, 1]
        assert f([3, 2, 4], 6) == [1, 2]
        assert f([3, 3], 6) == [0, 1]

    # 3. Valid Parentheses
    p = SolutionParen()
    assert p.isValid("()[]{}") is True
    assert p.isValid("(]") is False
    assert p.isValid("([)]") is False
    assert p.isValid("{[]}") is True

    # 4. Binary Search
    bs = SolutionBSearch()
    arr = [-1, 0, 3, 5, 9, 12]
    for f in (bs.search_manual, bs.search_bisect):
        assert f(arr, 9) == 4
        assert f(arr, 2) == -1
        assert f(arr, -1) == 0

    # 5. Number of Islands
    isl = SolutionIslands()
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert isl.numIslands_dfs(grid) == 3
    assert isl.numIslands_bfs(grid) == 3
    assert isl.numIslands_dfs([["1", "1", "1"], ["1", "1", "1"]]) == 1

    # 6. Merge Intervals
    mg = SolutionMerge()
    assert mg.merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert mg.merge([[1, 4], [4, 5]]) == [[1, 5]]

    # 7. Top K Frequent
    tk = SolutionTopK()
    for f in (tk.topKFrequent_heap, tk.topKFrequent_bucket):
        assert sorted(f([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
        assert f([1], 1) == [1]

    # 8. Course Schedule
    cs = SolutionCourse()
    assert cs.canFinish(2, [[1, 0]]) is True
    assert cs.canFinish(2, [[1, 0], [0, 1]]) is False
    assert cs.canFinish(4, [[1, 0], [2, 1], [3, 2]]) is True

    # 9. 타겟 넘버
    assert solution_target([1, 1, 1, 1, 1], 3) == 5
    assert solution_target([4, 1, 2, 1], 4) == 2

    # 10. 네트워크
    for f in (solution_network, solution_network_union):
        assert f(3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
        assert f(3, [[1, 1, 0], [1, 1, 1], [0, 1, 1]]) == 1

    print("All tests passed (OK)")


if __name__ == "__main__":
    _run_tests()

    print("\n=== Day 30 대표 실행 결과 ===")
    print("Two Sum([2,7,11,15], 9) =", SolutionTwoSum().twoSum_hash([2, 7, 11, 15], 9))
    print("Islands(DFS) =", SolutionIslands().numIslands_dfs(
        [["1", "1", "0"], ["0", "1", "0"], ["0", "0", "1"]]))
    print("타겟 넘버([1,1,1,1,1], 3) =", solution_target([1, 1, 1, 1, 1], 3))
    print("네트워크(DFS) =", solution_network(3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]]))
    print("네트워크(Union-Find) =", solution_network_union(3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]]))
