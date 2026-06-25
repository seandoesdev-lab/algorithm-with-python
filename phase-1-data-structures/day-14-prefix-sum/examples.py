"""
Day 14 - 누적 합 (Prefix Sum) 예제 모음
--------------------------------------------------
실행:  PYTHONIOENCODING=cp949 python examples.py

콘솔 출력 문자열은 cp949 안전 문자만 사용한다(ASCII =,-,O,X). 한글은 OK.
표준 라이브러리만 사용한다.
"""

from itertools import accumulate
from collections import defaultdict


# 1) 표준 누적합 배열 (1-indexed, 맨 앞에 0): 구간 합을 O(1)에 답한다.
def build_prefix(A):
    """P[0]=0, P[k]=A[0]+...+A[k-1]. 길이 n+1."""
    P = [0] * (len(A) + 1)
    for i, x in enumerate(A):
        P[i + 1] = P[i] + x
    return P


def range_sum(P, i, j):
    """원본 A의 구간 A[i..j] (양끝 포함) 합 = P[j+1] - P[i]."""
    return P[j + 1] - P[i]


def build_prefix_pythonic(A):
    """파이썬다운 한 줄 버전. accumulate(initial=0) 은 3.8+."""
    return list(accumulate(A, initial=0))


# 2) 합이 K 인 "연속 구간 개수": 누적합 + 해시맵으로 O(n).
def subarray_sum_count(nums, K):
    seen = defaultdict(int)
    seen[0] = 1                      # 빈 접두부(합 0)를 1번 본 것으로 둔다.
    prefix = count = 0
    for x in nums:
        prefix += x
        count += seen[prefix - K]    # 과거 누적합 중 (prefix-K)가 몇 번이었나?
        seen[prefix] += 1
    return count


# 3) 자기 자신을 제외한 곱(prefix product): 나눗셈 없이 O(n).
def product_except_self(nums):
    n = len(nums)
    res = [1] * n
    left = 1
    for i in range(n):               # res[i] = 왼쪽 모든 원소의 곱
        res[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):   # 오른쪽 누적 곱을 곱해 합성
        res[i] *= right
        right *= nums[i]
    return res


# 4) 2D 누적합: 직사각형 합을 O(1)에 (포함-배제).
def build_prefix_2d(M):
    R, C = len(M), len(M[0])
    P = [[0] * (C + 1) for _ in range(R + 1)]
    for r in range(R):
        for c in range(C):
            P[r + 1][c + 1] = M[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
    return P


def region_sum_2d(P, r1, c1, r2, c2):
    """좌상단 (r1,c1) ~ 우하단 (r2,c2) 직사각형 합 (양끝 포함)."""
    return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]


# 5) 차분 배열(difference array): 구간 갱신 O(1), 마지막에 누적합으로 복원.
def apply_range_updates(n, updates):
    """updates: (l, r, v) 목록. 구간 [l, r] (양끝 포함)에 v를 더한다."""
    D = [0] * (n + 1)
    for l, r, v in updates:
        D[l] += v
        D[r + 1] -= v
    return list(accumulate(D))[:n]


def demo():
    print("=== 1) 1D 누적합 / 구간 합 ===")
    A = [3, 1, 4, 1, 5]
    P = build_prefix(A)
    print("A =", A)
    print("P =", P, "(길이 n+1, P[0]=0)")
    print("sum A[1..3] =", range_sum(P, 1, 3), "(기대 6)")
    print("sum A[0..4] =", range_sum(P, 0, 4), "(기대 14)")
    print("accumulate 버전 P =", build_prefix_pythonic(A))

    print()
    print("=== 2) 합이 K 인 연속 구간 개수 ===")
    print("nums=[1,1,1], K=2 ->", subarray_sum_count([1, 1, 1], 2), "(기대 2)")
    print("nums=[1,2,3], K=3 ->", subarray_sum_count([1, 2, 3], 3), "(기대 2)")
    print("음수 포함 [3,-1,-1,1], K=0 ->",
          subarray_sum_count([3, -1, -1, 1], 0), "(기대 1)")

    print()
    print("=== 3) 자기 자신 제외 곱 ===")
    print("[1,2,3,4] ->", product_except_self([1, 2, 3, 4]), "(기대 [24,12,8,6])")
    print("0 포함 [0,4,0] ->", product_except_self([0, 4, 0]), "(기대 [0,0,0])")

    print()
    print("=== 4) 2D 누적합 직사각형 합 ===")
    M = [
        [3, 0, 1, 4],
        [5, 6, 3, 2],
        [1, 2, 0, 1],
    ]
    P2 = build_prefix_2d(M)
    # (1,1)~(2,3) = 6+3+2 + 2+0+1 = 14
    print("region (1,1)~(2,3) =", region_sum_2d(P2, 1, 1, 2, 3), "(기대 14)")
    # 전체 합
    print("region (0,0)~(2,3) =", region_sum_2d(P2, 0, 0, 2, 3), "(기대 28)")

    print()
    print("=== 5) 차분 배열 구간 갱신 ===")
    # 길이 5, [1,3]에 +2, [0,2]에 +1 -> [1,3,3,2,0]
    updates = [(1, 3, 2), (0, 2, 1)]
    print("updates", updates, "->", apply_range_updates(5, updates),
          "(기대 [1,3,3,2,0])")


if __name__ == "__main__":
    demo()
