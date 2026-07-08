# -*- coding: utf-8 -*-
"""
Day 23 - 알고리즘 기초 복습 (Core Algorithms Review): 예제 모음

Phase 2의 7개 기법을 한 파일에서 다시 훑는다:
  이분 탐색 / 정답 이분 탐색 / 투 포인터 / 슬라이딩 윈도우 / 정렬+그리디 / 분할정복.
표준 라이브러리만 사용한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

import bisect


# ---------------------------------------------------------------------------
# 1) 이분 탐색 (Binary Search): 정렬된 배열에서 target 위치 (없으면 -1)
#    전제: 배열이 정렬돼 있어야 한다. 매 단계 후보 구간을 절반으로. O(log n).
# ---------------------------------------------------------------------------
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1        # 오른쪽 절반으로
        else:
            hi = mid - 1        # 왼쪽 절반으로
    return -1


# ---------------------------------------------------------------------------
# 2) 정답 이분 탐색 (Parametric Search): feasible(K)가 단조일 때 최소 K.
#    값이 아니라 "답의 범위"를 이분 탐색한다.
# ---------------------------------------------------------------------------
def min_feasible_k(lo, hi, feasible):
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid            # 더 작아질 수 있나?
        else:
            lo = mid + 1        # 더 커야 한다
    return lo


# ---------------------------------------------------------------------------
# 3) 투 포인터 (Two Pointers): 정렬된 배열에서 합이 target인 두 값(1-indexed).
#    양 끝에서 좁혀 O(n).
# ---------------------------------------------------------------------------
def two_sum_sorted(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1             # 합을 키운다
        else:
            hi -= 1             # 합을 줄인다
    return []


# ---------------------------------------------------------------------------
# 4) 슬라이딩 윈도우 (Sliding Window): 중복 없는 가장 긴 부분 문자열 길이.
#    창의 상태(문자 -> 마지막 위치)를 O(1)로 갱신. O(n).
# ---------------------------------------------------------------------------
def longest_unique(s):
    seen = {}
    start = best = 0
    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1        # 창의 왼쪽을 당긴다
        seen[ch] = i
        best = max(best, i - start + 1)
    return best


# ---------------------------------------------------------------------------
# 5) 정렬 + 그리디 (Sort + Greedy): 겹치는 구간 병합 (Merge Intervals).
#    시작점 기준 정렬 후, 앞에서부터 겹치면 확장.
# ---------------------------------------------------------------------------
def merge_intervals(intervals):
    intervals = sorted(intervals)
    merged = []
    for s, e in intervals:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)   # 겹치면 확장
        else:
            merged.append([s, e])
    return merged


# ---------------------------------------------------------------------------
# 6) 분할정복 (Divide & Conquer): 병합 정렬. 반으로 나눠 각각 정렬 후 병합.
#    T(n) = 2T(n/2) + O(n) -> O(n log n).
# ---------------------------------------------------------------------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):     # 투 포인터로 병합
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


# ---------------------------------------------------------------------------
# 7) 표준 라이브러리 bisect: 손으로 짠 이분 탐색을 대체.
# ---------------------------------------------------------------------------
def bisect_demo():
    arr = [1, 3, 5, 7, 9]
    return {
        "insert_pos_for_5": bisect.bisect_left(arr, 5),     # 2
        "insert_pos_after_5": bisect.bisect_right(arr, 5),  # 3
        "insert_pos_for_6": bisect.bisect_left(arr, 6),     # 3
    }


def main():
    print("=== 1) Binary Search ===")
    nums = [1, 3, 5, 7, 9, 11]
    print("array:", nums)
    print("index of 7:", binary_search(nums, 7))       # 3
    print("index of 8:", binary_search(nums, 8))       # -1

    print()
    print("=== 2) Parametric Search (min feasible K) ===")
    # 예: x*x >= 50 을 만족하는 최소 정수 x (1..100)
    k = min_feasible_k(1, 100, lambda x: x * x >= 50)
    print("smallest x with x*x >= 50:", k)             # 8 (8*8=64)

    print()
    print("=== 3) Two Pointers (Two Sum II, sorted) ===")
    sorted_nums = [2, 7, 11, 15]
    print("array:", sorted_nums, "target: 9")
    print("1-indexed pair:", two_sum_sorted(sorted_nums, 9))   # [1, 2]

    print()
    print("=== 4) Sliding Window (longest unique substring) ===")
    for text in ["abcabcbb", "bbbbb", "pwwkew"]:
        print("input:", text, "-> length:", longest_unique(text))

    print()
    print("=== 5) Sort + Greedy (merge intervals) ===")
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print("input:", intervals)
    print("merged:", merge_intervals(intervals))       # [[1,6],[8,10],[15,18]]

    print()
    print("=== 6) Divide & Conquer (merge sort) ===")
    data = [5, 2, 8, 1, 9, 3, 7]
    print("input:", data)
    print("sorted:", merge_sort(data))                 # [1,2,3,5,7,8,9]

    print()
    print("=== 7) bisect (standard library) ===")
    for key, value in bisect_demo().items():
        print(key, "->", value)

    print()
    print("All Day 23 examples ran OK")


if __name__ == "__main__":
    main()
