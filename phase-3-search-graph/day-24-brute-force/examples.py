# -*- coding: utf-8 -*-
"""
Day 24 - 완전 탐색 (Brute Force / Exhaustive Search): 핵심 개념 예제 모음

완전 탐색의 4대 형태(중첩 반복 / 부분집합 / 순열 / 조합)를
재귀와 itertools 두 가지로 보여준다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from itertools import permutations, combinations, product


# ---------------------------------------------------------------------------
# 1) 중첩 반복(nested loop) 완전 탐색: 두 수의 합이 target인 쌍 (Two Sum)
#    모든 (i, j) 쌍을 전수조사. O(n^2).
# ---------------------------------------------------------------------------
def two_sum_brute(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):        # i < j 인 모든 쌍
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# ---------------------------------------------------------------------------
# 2) 부분집합(subset): 재귀로 모든 부분집합 생성. 2^n 가지.
#    각 원소에 대해 "빼고" 가지 / "넣고" 가지로 분기한다.
# ---------------------------------------------------------------------------
def all_subsets(nums):
    res = []

    def go(i, chosen):
        if i == len(nums):               # 기저 조건: 모든 원소 결정 끝
            res.append(chosen[:])        # 현재 후보 확정(리스트 복사)
            return
        go(i + 1, chosen)                # i번째 빼고
        chosen.append(nums[i])
        go(i + 1, chosen)                # i번째 넣고
        chosen.pop()                     # 되돌리기(undo) - 상태 오염 방지

    go(0, [])
    return res


# ---------------------------------------------------------------------------
# 3) 부분집합: 비트마스크(bitmask)로. 재귀 없이 반복문만으로.
#    0 .. 2^n - 1 각 정수의 i번째 비트가 nums[i] 포함 여부.
# ---------------------------------------------------------------------------
def all_subsets_bitmask(nums):
    n = len(nums)
    res = []
    for mask in range(1 << n):           # 1 << n == 2^n
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        res.append(subset)
    return res


# ---------------------------------------------------------------------------
# 4) 순열(permutation): 재귀로 모든 순서 나열. n! 가지.
#    아직 안 쓴 원소를 하나씩 골라 자리에 놓는다.
# ---------------------------------------------------------------------------
def all_permutations_recursive(nums):
    res = []
    used = [False] * len(nums)
    cur = []

    def go():
        if len(cur) == len(nums):
            res.append(cur[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            cur.append(nums[i])
            go()
            cur.pop()                    # 되돌리기
            used[i] = False

    go()
    return res


# ---------------------------------------------------------------------------
# 5) itertools 로 순열 / 조합을 한 줄에.
# ---------------------------------------------------------------------------
def all_permutations(nums):
    return [list(p) for p in permutations(nums)]


def all_combinations(nums, r):
    return [list(c) for c in combinations(nums, r)]


# ---------------------------------------------------------------------------
# 6) product: 여러 축의 곱집합(중첩 반복의 일반형).
#    자물쇠 '00'..'11' 처럼 각 자리를 독립적으로 전수.
# ---------------------------------------------------------------------------
def all_codes(digits, length):
    return ["".join(p) for p in product(digits, repeat=length)]


# ---------------------------------------------------------------------------
# 7) 응용: 부분집합 중 합이 target인 것의 개수 (완전 탐색으로 세기)
# ---------------------------------------------------------------------------
def count_subsets_with_sum(nums, target):
    count = 0
    for mask in range(1 << len(nums)):
        total = sum(nums[i] for i in range(len(nums)) if mask & (1 << i))
        if total == target:
            count += 1
    return count


def _factorial(n):
    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def _demo():
    print("1) two_sum_brute([2,7,11,15], 9):", two_sum_brute([2, 7, 11, 15], 9))  # [0, 1]

    subs = all_subsets([1, 2, 3])
    print("2) all_subsets([1,2,3]) count:", len(subs), "(expect 8)")
    print("2) all_subsets([1,2,3]):", subs)

    print("3) bitmask subsets count:", len(all_subsets_bitmask([1, 2, 3])))  # 8

    perms = all_permutations_recursive([1, 2, 3])
    print("4) recursive permutations count:", len(perms), "(expect 6)")

    print("5) itertools permutations count:", len(all_permutations([1, 2, 3])))  # 6
    print("5) combinations 4C2:", all_combinations([1, 2, 3, 4], 2))         # 6개

    print("6) 2-digit codes from '01':", all_codes("01", 2))  # ['00','01','10','11']

    print("7) subsets of [1,2,3,4,5] summing to 5:",
          count_subsets_with_sum([1, 2, 3, 4, 5], 5))  # {5},{1,4},{2,3} -> 3

    # 경우의 수 감각: 형태별 폭발성
    print("info) 2^20 =", 1 << 20, "/ 10! =", _factorial(10))


if __name__ == "__main__":
    _demo()
