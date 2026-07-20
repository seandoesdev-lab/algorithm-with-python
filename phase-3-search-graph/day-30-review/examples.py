# -*- coding: utf-8 -*-
"""
Day 30 - 개념 집중기 종합 복습 (Final Review) 예제 모음

개념 집중기(Phase 0~3)에서 배운 무기들을 "세 개의 질문"으로 묶어 실행한다.
  (1) 자료구조 선택   - 무엇을 저장하고 어떻게 꺼내는가?
  (2) 알고리즘 기법   - 이미 정렬/단조인가, 답을 어떻게 좁히는가?
  (3) 탐색 선택       - 상태 공간을 어떻게 훑는가? (완전탐색/DFS/BFS/백트래킹)

cp949 콘솔 안전: print 문자열은 ASCII 기호(=,-,O,X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from collections import deque, Counter
import heapq


# ---------------------------------------------------------------------------
# (1) 자료구조: 해시로 O(n^2)를 O(n)으로 (Two Sum)
# ---------------------------------------------------------------------------
def two_sum(nums, target):
    """정렬 안 된 배열에서 합이 target인 두 인덱스. 해시로 O(1) 조회 -> 전체 O(n)."""
    seen = {}                              # 값 -> 인덱스
    for i, x in enumerate(nums):
        if target - x in seen:             # 이미 본 값 중에 짝이 있나 (O(1))
            return [seen[target - x], i]
        seen[x] = i
    return []


# ---------------------------------------------------------------------------
# (2) 자료구조: 스택으로 괄호 짝 맞추기 (LIFO)
# ---------------------------------------------------------------------------
def valid_parentheses(s):
    """가장 최근에 열린 괄호가 가장 먼저 닫혀야 한다 -> 스택."""
    pair = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        else:
            if not stack or stack.pop() != pair[ch]:
                return False
    return not stack                       # 남은 게 없어야 완전한 짝


# ---------------------------------------------------------------------------
# (3) 기법: 이분 탐색 (정렬된 배열에서 값 위치)
# ---------------------------------------------------------------------------
def binary_search(nums, target):
    """정렬됨이 전제. 매 단계 후보를 절반으로 -> O(log n)."""
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1                   # 오른쪽 절반
        else:
            hi = mid - 1                   # 왼쪽 절반
    return -1


# ---------------------------------------------------------------------------
# (4) 기법: 정렬 + 그리디 (구간 병합)
# ---------------------------------------------------------------------------
def merge_intervals(intervals):
    """시작점 정렬 후 앞에서부터 겹치면 확장 -> O(n log n)."""
    intervals = sorted(intervals)
    merged = []
    for s, e in intervals:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged


# ---------------------------------------------------------------------------
# (5) 결합: dict 집계 + heap으로 상위 K (Top K Frequent)
# ---------------------------------------------------------------------------
def top_k_frequent(nums, k):
    """빈도 집계는 해시 O(n), 상위 K 추출은 힙 nlargest O(n log k)."""
    freq = Counter(nums)
    top = heapq.nlargest(k, freq.items(), key=lambda kv: kv[1])
    return [x for x, _ in top]


# ---------------------------------------------------------------------------
# (6) 탐색: DFS로 그리드 섬 개수 세기 (완전 탐색 + 깊이 우선)
# ---------------------------------------------------------------------------
def num_islands(grid):
    """각 칸을 훑다가 땅(1)을 만나면 DFS로 그 섬 전체를 0으로 지운다."""
    if not grid:
        return 0
    R, C = len(grid), len(grid[0])
    g = [row[:] for row in grid]           # 원본 보존을 위해 복사

    def sink(r, c):
        if r < 0 or r >= R or c < 0 or c >= C or g[r][c] == 0:
            return
        g[r][c] = 0                        # 방문 표시 = 물로 만들기
        sink(r + 1, c); sink(r - 1, c)
        sink(r, c + 1); sink(r, c - 1)

    count = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] == 1:
                count += 1
                sink(r, c)
    return count


# ---------------------------------------------------------------------------
# (7) 탐색: BFS로 무가중치 최단 거리 (그리드)
# ---------------------------------------------------------------------------
def bfs_shortest(grid, start, goal):
    """큐로 가까운 칸부터 확장 -> 목표를 처음 만나는 순간이 최단."""
    R, C = len(grid), len(grid[0])
    q = deque([(start, 0)])
    seen = {start}
    while q:
        (r, c), d = q.popleft()
        if (r, c) == goal:
            return d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append(((nr, nc), d + 1))
    return -1


# ---------------------------------------------------------------------------
# (8) 완전 탐색/DFS: 부호 조합으로 target 만들기 (타겟 넘버 골격)
# ---------------------------------------------------------------------------
def count_targets(numbers, target):
    """각 수에 +/- 를 붙이는 2^n 조합을 DFS로 모두 시도. N<=20이라 허용."""
    def dfs(i, total):
        if i == len(numbers):
            return 1 if total == target else 0
        return dfs(i + 1, total + numbers[i]) + dfs(i + 1, total - numbers[i])
    return dfs(0, 0)


# ---------------------------------------------------------------------------
# (9) 탐색: 그래프 연결 요소 수 세기 (네트워크 골격, DFS)
# ---------------------------------------------------------------------------
def count_networks(n, computers):
    """인접 행렬에서 방문 안 한 노드를 만날 때마다 DFS로 컴포넌트 하나를 소진."""
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        for v in range(n):
            if computers[u][v] == 1 and not visited[v]:
                dfs(v)

    groups = 0
    for i in range(n):
        if not visited[i]:
            groups += 1                    # 새 연결 요소 시작
            dfs(i)
    return groups


def main():
    print("=== Day 30 개념 집중기 종합 복습 예제 ===")

    print("\n[1] 자료구조/해시 - Two Sum")
    print("  two_sum([2,7,11,15], 9) =", two_sum([2, 7, 11, 15], 9))
    print("  two_sum([3,2,4], 6)     =", two_sum([3, 2, 4], 6))

    print("\n[2] 자료구조/스택 - Valid Parentheses")
    print("  '()[]{}' ->", valid_parentheses("()[]{}"))
    print("  '(]'     ->", valid_parentheses("(]"))

    print("\n[3] 기법/이분 탐색 - Binary Search")
    print("  index of 9 in [-1,0,3,5,9,12] =", binary_search([-1, 0, 3, 5, 9, 12], 9))
    print("  index of 2 (없음)             =", binary_search([-1, 0, 3, 5, 9, 12], 2))

    print("\n[4] 기법/정렬+그리디 - Merge Intervals")
    print("  merge [[1,3],[2,6],[8,10],[15,18]] =",
          merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))

    print("\n[5] 결합/해시+힙 - Top K Frequent")
    print("  top 2 of [1,1,1,2,2,3] =", sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)))

    print("\n[6] 탐색/DFS - Number of Islands")
    grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1],
    ]
    print("  섬 개수 =", num_islands(grid))

    print("\n[7] 탐색/BFS - 무가중치 최단 거리")
    maze = [
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
    ]
    print("  (0,0)->(3,3) 최단 =", bfs_shortest(maze, (0, 0), (3, 3)))

    print("\n[8] 완전탐색/DFS - 타겟 넘버")
    print("  count_targets([1,1,1,1,1], 3) =", count_targets([1, 1, 1, 1, 1], 3))

    print("\n[9] 탐색/그래프 - 네트워크(연결 요소 수)")
    comps = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
    ]
    print("  네트워크 개수 =", count_networks(3, comps))

    print("\n=== 모든 예제 실행 완료 (OK) ===")


if __name__ == "__main__":
    main()
