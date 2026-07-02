# -*- coding: utf-8 -*-
"""
Day 18 - 이분 탐색 (Binary Search): 실행 가능한 예제 모음

정렬된 배열에서 O(log n)으로 값을 찾는 이분 탐색과,
"조건을 만족하는 경계"를 찾는 결정 문제형(parametric) 이분 탐색을 다룬다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

import bisect


# ---------------------------------------------------------------------------
# 1. 표준 이분 탐색 (값의 정확한 위치 찾기), 닫힌 구간 [lo, hi]
#    핵심: mid = (lo + hi) // 2 로 반씩 줄인다. 못 찾으면 -1.
# ---------------------------------------------------------------------------
def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:                 # 구간이 비지 않는 동안
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1            # 오른쪽 절반
        else:
            hi = mid - 1            # 왼쪽 절반
    return -1


# ---------------------------------------------------------------------------
# 2. lower_bound / upper_bound 직접 구현, 반열린 구간 [lo, hi)
#    lower_bound: target 이상이 처음 나오는 위치
#    upper_bound: target 초과가 처음 나오는 위치
# ---------------------------------------------------------------------------
def lower_bound(a, target):
    lo, hi = 0, len(a)             # hi는 "범위 밖"을 가리킴
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid                # 조건 만족 -> 경계를 왼쪽으로
    return lo


def upper_bound(a, target):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------------------
# 3. 표준 라이브러리 bisect: 직접 구현할 필요 없다
#    bisect_left  == lower_bound, bisect_right == upper_bound
# ---------------------------------------------------------------------------
def demo_bisect():
    a = [1, 2, 2, 2, 5, 7]
    print("배열           :", a)
    print("bisect_left(2) :", bisect.bisect_left(a, 2))    # 1
    print("bisect_right(2):", bisect.bisect_right(a, 2))   # 4
    print("2의 개수       :", bisect.bisect_right(a, 2) - bisect.bisect_left(a, 2))

    # insort: 정렬을 유지하며 삽입 O(n) (탐색은 O(log n), 이동이 O(n))
    b = [1, 3, 5]
    bisect.insort(b, 4)
    print("insort 후      :", b)                            # [1, 3, 4, 5]

    # 존재 여부 확인: bisect_left 위치의 값이 target인지 본다
    def contains(arr, x):
        i = bisect.bisect_left(arr, x)
        return i < len(arr) and arr[i] == x
    print("contains(a, 5) :", contains(a, 5), "/ contains(a, 6):", contains(a, 6))


# ---------------------------------------------------------------------------
# 4. 결정 문제형(parametric) 이분 탐색: "정답 자체"를 이분 탐색
#    조건 pred(x)가 특정 경계를 기준으로 F..F,T..T 로 단조(monotonic)면
#    가장 작은 T(또는 가장 큰 T)를 log 번 만에 찾는다.
#    예) 제곱근: x*x <= n 을 만족하는 가장 큰 x (정수 sqrt)
# ---------------------------------------------------------------------------
def isqrt_by_search(n):
    lo, hi = 0, n                   # 답 후보 범위 [0, n]
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n:          # 조건 만족 -> 더 크게 시도
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


# ---------------------------------------------------------------------------
# 5. 실수(부동소수) 이분 탐색: 반복 횟수로 종료 (정밀도 함정 회피)
#    예) 어떤 수의 제곱근을 소수점까지
# ---------------------------------------------------------------------------
def sqrt_float(n, iterations=100):
    lo, hi = 0.0, max(1.0, n)
    for _ in range(iterations):     # while hi-lo>eps 대신 고정 반복이 안전
        mid = (lo + hi) / 2
        if mid * mid < n:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    print("=== 1. 표준 이분 탐색 ===")
    a = [1, 3, 5, 7, 9, 11]
    print("배열:", a)
    print("search(7)  ->", binary_search(a, 7), "(인덱스 3)")
    print("search(8)  ->", binary_search(a, 8), "(없음 -1)")
    print()

    print("=== 2. lower/upper bound 직접 구현 ===")
    b = [1, 2, 2, 2, 5, 7]
    print("배열:", b)
    print("lower_bound(2) =", lower_bound(b, 2), "/ upper_bound(2) =", upper_bound(b, 2))
    print()

    print("=== 3. 표준 라이브러리 bisect ===")
    demo_bisect()
    print()

    print("=== 4. 결정 문제형: 정수 제곱근 ===")
    for n in [0, 1, 8, 16, 26, 100]:
        print("isqrt(", n, ") =", isqrt_by_search(n))
    print()

    print("=== 5. 실수 이분 탐색: 제곱근 ===")
    print("sqrt(2)  ~", round(sqrt_float(2), 6))
    print("sqrt(10) ~", round(sqrt_float(10), 6))


if __name__ == "__main__":
    main()
