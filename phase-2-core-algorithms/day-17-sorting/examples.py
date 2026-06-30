# -*- coding: utf-8 -*-
"""
Day 17 - 정렬 (Sorting): 실행 가능한 예제 모음

파이썬 내장 정렬(Timsort)의 사용법과 대표 정렬 알고리즘을 직접 구현해 본다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from functools import cmp_to_key


# ---------------------------------------------------------------------------
# 1. 내장 정렬: sorted(새 리스트) vs list.sort(제자리)
# ---------------------------------------------------------------------------
def demo_builtin():
    a = [3, 1, 2]
    b = sorted(a)            # 새 리스트 반환, 원본 유지
    print("sorted(a) =", b, "/ a =", a)

    a.sort()                 # 제자리 정렬, 반환값은 None
    ret = [5, 4].sort()      # 흔한 함정: 반환은 None
    print("a.sort() 후 a =", a, "/ [5,4].sort() 반환 =", ret)


# ---------------------------------------------------------------------------
# 2. key 함수: 무엇을 기준으로 줄 세울지
# ---------------------------------------------------------------------------
def demo_key():
    words = ["banana", "kiwi", "apple"]
    print("길이순     :", sorted(words, key=len))
    print("끝글자순   :", sorted(words, key=lambda w: w[-1]))
    print("내림차순   :", sorted([3, 1, 2], reverse=True))

    # 다중 기준: x 오름차순, 같으면 y 내림차순
    pts = [(1, 2), (1, 5), (0, 9)]
    print("다중 기준  :", sorted(pts, key=lambda p: (p[0], -p[1])))


# ---------------------------------------------------------------------------
# 3. 커스텀 비교(cmp_to_key): 이어붙여 가장 큰 수
# ---------------------------------------------------------------------------
def demo_cmp():
    def cmp(x, y):
        if x + y > y + x:
            return -1        # x가 앞
        if x + y < y + x:
            return 1
        return 0

    nums = ["3", "30", "34", "5", "9"]
    largest = "".join(sorted(nums, key=cmp_to_key(cmp)))
    print("가장 큰 수 :", largest)   # 9534330


# ---------------------------------------------------------------------------
# 4. 병합 정렬 직접 구현 (O(n log n), 안정)
# ---------------------------------------------------------------------------
def merge_sort(a):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return _merge(left, right)


def _merge(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:    # <= 라서 같은 값은 왼쪽 우선(안정)
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


# ---------------------------------------------------------------------------
# 5. 삽입 정렬 직접 구현 (O(n^2), 안정, 거의 정렬된 입력에 빠름)
# ---------------------------------------------------------------------------
def insertion_sort(a):
    arr = a[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ---------------------------------------------------------------------------
# 6. 계수 정렬 직접 구현 (O(n + k), 비교 안 함, 값 범위 0..k)
# ---------------------------------------------------------------------------
def counting_sort(a, k):
    count = [0] * (k + 1)
    for x in a:
        count[x] += 1
    out = []
    for v in range(k + 1):
        out.extend([v] * count[v])
    return out


# ---------------------------------------------------------------------------
# 7. argsort 패턴: 정렬된 "원래 인덱스"
# ---------------------------------------------------------------------------
def demo_argsort():
    a = [40, 10, 30]
    order = sorted(range(len(a)), key=lambda i: a[i])
    print("argsort    :", order, "-> 값", [a[i] for i in order])


def main():
    print("=== 1. 내장 정렬 ===")
    demo_builtin()
    print()
    print("=== 2. key 함수 ===")
    demo_key()
    print()
    print("=== 3. 커스텀 비교 ===")
    demo_cmp()
    print()
    print("=== 4~6. 직접 구현 정렬 ===")
    data = [38, 27, 43, 3, 9, 82, 10]
    print("입력       :", data)
    print("병합 정렬  :", merge_sort(data))
    print("삽입 정렬  :", insertion_sort(data))
    print("계수 정렬  :", counting_sort([4, 2, 2, 0, 3, 1], 4))
    print()
    print("=== 7. argsort ===")
    demo_argsort()


if __name__ == "__main__":
    main()
