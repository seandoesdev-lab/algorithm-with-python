# -*- coding: utf-8 -*-
"""
Day 16 - 시간복잡도와 Big-O (Time Complexity & Big-O) 예제 모음

콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

import time


# ---------------------------------------------------------------------------
# 1) 같은 문제, 다른 복잡도: 중복 존재 여부  O(n^2) vs O(n)
# ---------------------------------------------------------------------------
def has_dup_slow(a):
    """O(n^2): 모든 쌍을 비교한다."""
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] == a[j]:
                return True
    return False


def has_dup_fast(a):
    """O(n): set 멤버십이 평균 O(1)."""
    seen = set()
    for x in a:
        if x in seen:
            return True
        seen.add(x)
    return False


# ---------------------------------------------------------------------------
# 2) O(log n): 이분 탐색 (정렬된 배열에서 절반씩 좁히기)
# ---------------------------------------------------------------------------
def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    steps = 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid, steps
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, steps


# ---------------------------------------------------------------------------
# 3) O(n): 최대 부분합 (Kadane) - 이중 루프 O(n^2)을 한 번 순회로
# ---------------------------------------------------------------------------
def max_subarray_slow(a):
    """O(n^2): 모든 구간의 합을 직접 계산."""
    best = a[0]
    for i in range(len(a)):
        cur = 0
        for j in range(i, len(a)):
            cur += a[j]
            if cur > best:
                best = cur
    return best


def max_subarray_fast(a):
    """O(n): 직전까지의 최선을 이어가거나 새로 시작."""
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


# ---------------------------------------------------------------------------
# 4) 숨은 복잡도 주의: 문자열 이어붙이기  O(n^2) vs O(n)
# ---------------------------------------------------------------------------
def build_bad(words):
    """O(n^2): 매 단계 새 문자열을 만든다."""
    s = ""
    for w in words:
        s = s + w
    return s


def build_good(words):
    """O(n): join은 한 번에 이어붙인다."""
    return "".join(words)


# ---------------------------------------------------------------------------
# 5) 성장 속도 체감: 같은 입력에서 O(n^2)과 O(n)의 실제 시간 차이
# ---------------------------------------------------------------------------
def measure_growth():
    print("성장 속도 비교 (중복 검사, 중복 없는 입력):")
    print("   n        slow O(n^2)      fast O(n)")
    for n in (1000, 2000, 4000):
        data = list(range(n))  # 중복 없음 -> 최악(끝까지 탐색)

        t0 = time.perf_counter()
        has_dup_slow(data)
        slow = time.perf_counter() - t0

        t0 = time.perf_counter()
        has_dup_fast(data)
        fast = time.perf_counter() - t0

        print("  {:>5}   {:>10.4f}s   {:>10.4f}s".format(n, slow, fast))
    print("  -> n이 2배가 되면 O(n^2)은 약 4배로 늘고, O(n)은 약 2배만 는다.")


def main():
    print("=== 1. 중복 존재 여부: O(n^2) vs O(n) ===")
    sample = [3, 1, 4, 1, 5, 9]
    print("  입력:", sample)
    print("  slow:", has_dup_slow(sample), " fast:", has_dup_fast(sample))
    print()

    print("=== 2. 이분 탐색 O(log n) ===")
    arr = list(range(0, 100, 2))  # 0,2,4,...,98 (정렬됨)
    idx, steps = binary_search(arr, 42)
    print("  42의 위치:", idx, " 비교 횟수:", steps, "(n=50, log2(50)~6)")
    idx, steps = binary_search(arr, 43)
    print("  43(없음):", idx, " 비교 횟수:", steps)
    print()

    print("=== 3. 최대 부분합: O(n^2) vs O(n) ===")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("  입력:", nums)
    print("  slow:", max_subarray_slow(nums), " fast:", max_subarray_fast(nums))
    print()

    print("=== 4. 문자열 이어붙이기: O(n^2) vs O(n) ===")
    words = ["a", "b", "c", "d", "e"]
    print("  bad :", build_bad(words))
    print("  good:", build_good(words))
    print()

    print("=== 5. 성장 속도 측정 ===")
    measure_growth()

    # --- 간단한 자체 검증 (assert) ---
    assert has_dup_slow([1, 2, 1]) == has_dup_fast([1, 2, 1]) is True
    assert has_dup_fast([1, 2, 3]) is False
    assert binary_search([1, 3, 5, 7], 5)[0] == 2
    assert binary_search([1, 3, 5, 7], 4)[0] == -1
    assert max_subarray_slow(nums) == max_subarray_fast(nums) == 6
    assert build_bad(words) == build_good(words) == "abcde"
    print()
    print("all checks passed: OK")


if __name__ == "__main__":
    main()
