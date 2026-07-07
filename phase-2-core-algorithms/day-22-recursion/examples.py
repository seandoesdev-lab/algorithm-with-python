# -*- coding: utf-8 -*-
"""
Day 22 - 재귀와 분할정복 (Recursion & Divide-Conquer): 핵심 개념 예제 모음

재귀의 3요소(기저 조건 / 입력 축소 / 자기 호출)와,
분할정복 골격(Divide -> Conquer -> Combine)을 예제로 보여준다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

import sys
from functools import lru_cache


# ---------------------------------------------------------------------------
# 1) 기본 재귀: 팩토리얼
#    기저 조건 n<=1 -> 1, 재귀 단계 n * factorial(n-1). 입력이 매번 1씩 줄어든다.
# ---------------------------------------------------------------------------
def factorial(n):
    if n <= 1:                       # 기저 조건
        return 1
    return n * factorial(n - 1)      # 재귀 단계


# ---------------------------------------------------------------------------
# 2) 나이브 재귀 vs 메모이제이션: 피보나치
#    나이브는 같은 값을 지수적으로 재계산(O(2^n)), 메모는 각 n 1회(O(n)).
# ---------------------------------------------------------------------------
def fib_naive(n):
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@lru_cache(maxsize=None)
def fib_memo(n):
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


# ---------------------------------------------------------------------------
# 3) 하노이의 탑 (Tower of Hanoi)
#    n-1개를 보조 기둥으로 옮기고, 가장 큰 원반을 목적지로, 다시 n-1개를 올린다.
#    이동 횟수는 2^n - 1.
# ---------------------------------------------------------------------------
def hanoi(n, src, dst, via, moves):
    if n == 0:                       # 기저 조건: 옮길 원반 없음
        return
    hanoi(n - 1, src, via, dst, moves)   # (1) 위 n-1개를 보조로
    moves.append((src, dst))             # (2) 가장 큰 원반을 목적지로
    hanoi(n - 1, via, dst, src, moves)   # (3) 보조의 n-1개를 목적지로


# ---------------------------------------------------------------------------
# 4) 분할정복: 병합 정렬 (Merge Sort)
#    Divide(반으로) -> Conquer(각 반 재귀 정렬) -> Combine(두 정렬본 병합).
# ---------------------------------------------------------------------------
def merge_sort(arr):
    if len(arr) <= 1:                # 기저 조건
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])     # Divide + Conquer
    right = merge_sort(arr[mid:])
    return _merge(left, right)       # Combine


def _merge(a, b):
    merged, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            merged.append(a[i]); i += 1
        else:
            merged.append(b[j]); j += 1
    merged.extend(a[i:])
    merged.extend(b[j:])
    return merged


# ---------------------------------------------------------------------------
# 5) 분할정복: 빠른 거듭제곱 x^n (Fast Power), O(log n)
#    x^n = (x^(n/2))^2, 홀수면 x 한 번 더 곱한다.
# ---------------------------------------------------------------------------
def fast_pow(x, n):
    if n == 0:                       # 기저 조건
        return 1
    half = fast_pow(x, n // 2)
    if n % 2 == 0:
        return half * half
    return half * half * x


# ---------------------------------------------------------------------------
# 6) 재귀 -> 반복 변환 예: 리스트 합
#    깊은 입력에서 스택 오버플로를 피하려면 반복문이 안전하다.
# ---------------------------------------------------------------------------
def list_sum_recursive(arr, i=0):
    if i == len(arr):                # 기저 조건
        return 0
    return arr[i] + list_sum_recursive(arr, i + 1)


def list_sum_iterative(arr):
    total = 0
    for x in arr:
        total += x
    return total


def _demo():
    print("1) factorial(5):", factorial(5))                    # 120

    print("2) fib_naive(20):", fib_naive(20))                  # 6765
    print("2) fib_memo(50):", fib_memo(50))                    # 12586269025

    moves = []
    hanoi(3, "A", "C", "B", moves)
    print("3) hanoi(3) move count:", len(moves), "(expect 7)")
    print("3) hanoi(3) moves:", moves)

    data = [5, 2, 8, 1, 9, 3, 7, 4]
    print("4) merge_sort:", merge_sort(data))                  # 1..9 sorted

    print("5) fast_pow(2, 10):", fast_pow(2, 10))              # 1024
    print("5) fast_pow(3, 5):", fast_pow(3, 5))                # 243

    nums = list(range(1, 101))
    print("6) list_sum recursive vs iterative:",
          list_sum_recursive(nums), "vs", list_sum_iterative(nums))  # 5050 5050

    print("info) default recursion limit:", sys.getrecursionlimit())


if __name__ == "__main__":
    _demo()
