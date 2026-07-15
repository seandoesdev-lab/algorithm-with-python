# -*- coding: utf-8 -*-
"""
Day 27 - 백트래킹 (Backtracking): 실행 가능한 예제 모음

핵심 골격은 choose -> explore -> undo(선택 -> 재귀 -> 되돌리기)다.
표준 라이브러리만 사용한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다(한글 OK).
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from itertools import permutations as it_perm, combinations as it_comb


# ---------------------------------------------------------------------------
# 1) 부분집합 (subsets) - 포함/불포함 이진 결정. 2^n개.
# ---------------------------------------------------------------------------
def subsets(nums):
    res, path = [], []

    def dfs(i):
        if i == len(nums):
            res.append(path[:])          # 복사본 기록(참조 금지)
            return
        dfs(i + 1)                       # 원소 i 불포함
        path.append(nums[i])             # choose: 포함
        dfs(i + 1)                       # explore
        path.pop()                       # undo

    dfs(0)
    return res


# ---------------------------------------------------------------------------
# 2) 순열 (permutations) - used 배열로 중복 사용 차단. n!개.
# ---------------------------------------------------------------------------
def permutations(nums):
    res, path, used = [], [], [False] * len(nums)

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue                 # 가지치기: 이미 쓴 원소
            used[i] = True
            path.append(nums[i])         # choose
            dfs()                        # explore
            path.pop()
            used[i] = False              # undo

    dfs()
    return res


# ---------------------------------------------------------------------------
# 3) 조합 nCk (combinations) - start 인덱스로 오름차순 고정 + 가지치기.
# ---------------------------------------------------------------------------
def combinations(n, k):
    res, path = [], []

    def dfs(start):
        if len(path) == k:
            res.append(path[:])
            return
        # 가지치기: 남은 자리(k-len)를 채울 수 없는 start는 시도하지 않음
        for x in range(start, n - (k - len(path)) + 2):
            path.append(x)               # choose
            dfs(x + 1)                   # explore: x보다 큰 것만
            path.pop()                   # undo

    dfs(1)
    return res


# ---------------------------------------------------------------------------
# 4) 조합 합 (combination sum) - 같은 수 중복 사용 가능. 남은 목표로 가지치기.
# ---------------------------------------------------------------------------
def combination_sum(candidates, target):
    cand = sorted(candidates)
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(cand)):
            if cand[i] > remain:         # 정렬돼 있으니 이후 전부 초과 -> 중단
                break
            path.append(cand[i])         # choose
            dfs(i, remain - cand[i])     # explore: 같은 수 재사용 허용(i 유지)
            path.pop()                   # undo

    dfs(0, target)
    return res


# ---------------------------------------------------------------------------
# 5) N-Queens - 열/두 대각선 집합으로 O(1) 충돌 검사(가지치기).
#    대각선 인덱스: '\' 방향은 r-c 일정, '/' 방향은 r+c 일정.
# ---------------------------------------------------------------------------
def n_queens_count(n):
    cols, diag, anti = set(), set(), set()
    count = 0

    def place(r):
        nonlocal count
        if r == n:
            count += 1
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                 # 충돌 -> 가지치기
            cols.add(c); diag.add(r - c); anti.add(r + c)   # choose
            place(r + 1)                                     # explore
            cols.discard(c); diag.discard(r - c); anti.discard(r + c)  # undo

    place(0)
    return count


# ---------------------------------------------------------------------------
# 6) 유효 괄호 생성 (generate parentheses) - 열림/닫힘 개수로 가지치기.
# ---------------------------------------------------------------------------
def generate_parentheses(n):
    res = []

    def dfs(cur, open_cnt, close_cnt):
        if len(cur) == 2 * n:
            res.append(cur)
            return
        if open_cnt < n:                 # 아직 '(' 여유가 있으면
            dfs(cur + "(", open_cnt + 1, close_cnt)
        if close_cnt < open_cnt:         # 닫힘이 열림보다 적을 때만 ')'
            dfs(cur + ")", open_cnt, close_cnt + 1)

    dfs("", 0, 0)
    return res


# ---------------------------------------------------------------------------
# 데모 실행
# ---------------------------------------------------------------------------
def _demo():
    print("=== 1) 부분집합 subsets([1, 2, 3]) ===")
    subs = subsets([1, 2, 3])
    print("개수:", len(subs), "(2^3 = 8)")
    print(subs)

    print()
    print("=== 2) 순열 permutations([1, 2, 3]) ===")
    perms = permutations([1, 2, 3])
    print("개수:", len(perms), "(3! = 6)")
    print(perms)
    # itertools 결과와 동일한지 확인
    assert sorted(perms) == sorted(list(p) for p in it_perm([1, 2, 3]))
    print("itertools.permutations 결과와 일치: OK")

    print()
    print("=== 3) 조합 combinations(4, 2) ===")
    combs = combinations(4, 2)
    print("개수:", len(combs), "(4C2 = 6)")
    print(combs)
    assert sorted(combs) == sorted(list(c) for c in it_comb(range(1, 5), 2))
    print("itertools.combinations 결과와 일치: OK")

    print()
    print("=== 4) 조합 합 combination_sum([2, 3, 6, 7], 7) ===")
    cs = combination_sum([2, 3, 6, 7], 7)
    print(cs)                            # [[2, 2, 3], [7]]

    print()
    print("=== 5) N-Queens 배치 수 ===")
    for n in range(1, 9):
        print("N =", n, "-> 해의 수:", n_queens_count(n))

    print()
    print("=== 6) 유효 괄호 generate_parentheses(3) ===")
    gp = generate_parentheses(3)
    print("개수:", len(gp), "(카탈란 수 C(3) = 5)")
    print(gp)

    print()
    print("모든 예제 실행 완료 OK")


if __name__ == "__main__":
    _demo()
