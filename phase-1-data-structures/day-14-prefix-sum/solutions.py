"""
Day 14 - 누적 합 (Prefix Sum) 해설/풀이
--------------------------------------------------
실행:  PYTHONIOENCODING=cp949 python solutions.py

- LeetCode 문제는 'class Solution', 프로그래머스 문제는 'def solution' 시그니처.
- 각 문제에 assert 자체 테스트. 가능하면 한 문제에 여러 접근 + 복잡도 비교.
- 콘솔 출력은 cp949 안전 문자만(ASCII =,-,O,X). 한글 OK. 표준 라이브러리만.
"""

from itertools import accumulate
from collections import defaultdict
from typing import List


# =========================================================
# 1) LeetCode #1480 - Running Sum of 1d Array  (기초)
# =========================================================
class SolutionRunningSum:
    # 접근 A: 직접 누적 (in-place), O(n) / O(1) 추가공간
    def runningSum(self, nums: List[int]) -> List[int]:
        out = nums[:]
        for i in range(1, len(out)):
            out[i] += out[i - 1]
        return out

    # 접근 B: itertools.accumulate 한 줄, O(n)
    def runningSum_acc(self, nums: List[int]) -> List[int]:
        return list(accumulate(nums))


# =========================================================
# 2) LeetCode #303 - Range Sum Query - Immutable  (기초)
#    핵심: 생성자에서 누적합 1회(O(n)), 질의는 O(1).
# =========================================================
class NumArray:
    def __init__(self, nums: List[int]):
        # P[0]=0, P[k]=nums[0..k-1] 합. 길이 n+1.
        self.P = [0] * (len(nums) + 1)
        for i, x in enumerate(nums):
            self.P[i + 1] = self.P[i] + x

    def sumRange(self, left: int, right: int) -> int:
        return self.P[right + 1] - self.P[left]   # 양끝 포함


# =========================================================
# 3) LeetCode #724 - Find Pivot Index  (기초)
# =========================================================
class SolutionPivot:
    # 접근 A: 전체 합 - 왼쪽 누적합, O(n) / O(1)
    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        left = 0
        for i, x in enumerate(nums):
            if left == total - left - x:   # 오른쪽 합 = total - left - x
                return i
            left += x
        return -1


# =========================================================
# 4) LeetCode #560 - Subarray Sum Equals K  (중급)
#    음수 포함 가능 -> 슬라이딩 윈도우 불가, 누적합+해시맵이 정답.
# =========================================================
class SolutionSubarraySum:
    # 접근 A: 누적합 + 해시맵, O(n) / O(n)   (권장)
    def subarraySum(self, nums: List[int], k: int) -> int:
        seen = defaultdict(int)
        seen[0] = 1                      # 빈 접두부(합 0) 1회
        prefix = count = 0
        for x in nums:
            prefix += x
            count += seen[prefix - k]
            seen[prefix] += 1
        return count

    # 접근 B: 모든 구간 누적합 차이, O(n^2) (비교용, 큰 입력엔 부적합)
    def subarraySum_bruteforce(self, nums: List[int], k: int) -> int:
        P = list(accumulate(nums, initial=0))
        n = len(nums)
        count = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if P[j] - P[i] == k:
                    count += 1
        return count


# =========================================================
# 5) LeetCode #238 - Product of Array Except Self  (중급)
#    나눗셈 금지 -> 좌우 누적 곱(prefix product).
# =========================================================
class SolutionProductExceptSelf:
    # 접근 A: 좌우 누적 곱, O(n) / 출력 제외 O(1)
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n
        left = 1
        for i in range(n):
            res[i] = left
            left *= nums[i]
        right = 1
        for i in range(n - 1, -1, -1):
            res[i] *= right
            right *= nums[i]
        return res


# =========================================================
# 6) LeetCode #1248 - Count Number of Nice Subarrays  (중급)
#    홀수->1, 짝수->0 으로 치환하면 "합이 k인 구간 개수"(#560)가 된다.
# =========================================================
class SolutionNiceSubarrays:
    # 접근 A: 누적합 + 해시맵, O(n)
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        seen = defaultdict(int)
        seen[0] = 1
        prefix = count = 0
        for x in nums:
            prefix += x & 1              # 홀수면 1, 짝수면 0
            count += seen[prefix - k]
            seen[prefix] += 1
        return count


# =========================================================
# 7) LeetCode #304 - Range Sum Query 2D - Immutable  (중급)
#    2D 누적합 + 포함-배제.
# =========================================================
class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        R, C = len(matrix), len(matrix[0]) if matrix else 0
        self.P = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.P[r + 1][c + 1] = (matrix[r][c] + self.P[r][c + 1]
                                        + self.P[r + 1][c] - self.P[r][c])

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        P = self.P
        return (P[r2 + 1][c2 + 1] - P[r1][c2 + 1]
                - P[r2 + 1][c1] + P[r1][c1])


# =========================================================
# 8) 프로그래머스 #134239 - 우박수열 정적분
#    수열을 꺾은선으로 보고 구간 [a,b]의 사다리꼴 넓이를 누적합으로.
# =========================================================
def solution(k, ranges):
    # 1) 우박(콜라츠) 수열 생성: k 에서 1 이 될 때까지
    seq = [k]
    while seq[-1] != 1:
        cur = seq[-1]
        seq.append(cur // 2 if cur % 2 == 0 else cur * 3 + 1)
    n = len(seq)                          # 점 개수, 구간(사다리꼴) 개수는 n-1

    # 2) 인접 점 사이 사다리꼴 넓이(폭 1) 누적합. P[i] = 0..i-1 사다리꼴 합
    P = [0.0] * n
    for i in range(n - 1):
        P[i + 1] = P[i] + (seq[i] + seq[i + 1]) / 2

    # 3) 질의 [a, b]: 끝 인덱스는 (n-1) + b. a..end 사다리꼴 합 = P[end]-P[a]
    res = []
    for a, b in ranges:
        end = (n - 1) + b                 # b 가 0 이면 마지막 점
        if a >= end:                      # 시작점이 끝점 이상이면 불가
            res.append(-1.0)
        else:
            res.append(P[end] - P[a])
    return res


# =========================================================
# 자체 테스트
# =========================================================
def _run_tests():
    # 1) Running Sum
    s1 = SolutionRunningSum()
    assert s1.runningSum([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert s1.runningSum_acc([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert s1.runningSum([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]

    # 2) Range Sum Query (Immutable)
    na = NumArray([-2, 0, 3, -5, 2, -1])
    assert na.sumRange(0, 2) == 1
    assert na.sumRange(2, 5) == -1
    assert na.sumRange(0, 5) == -3

    # 3) Pivot Index
    s3 = SolutionPivot()
    assert s3.pivotIndex([1, 7, 3, 6, 5, 6]) == 3
    assert s3.pivotIndex([1, 2, 3]) == -1
    assert s3.pivotIndex([2, 1, -1]) == 0

    # 4) Subarray Sum Equals K (두 접근 결과 일치 확인)
    s4 = SolutionSubarraySum()
    assert s4.subarraySum([1, 1, 1], 2) == 2
    assert s4.subarraySum([1, 2, 3], 3) == 2
    assert s4.subarraySum([3, -1, -1, 1], 0) == 1
    for nums, k in ([1, 1, 1], 2), ([1, 2, 3], 3), ([3, -1, -1, 1], 0):
        assert s4.subarraySum(nums, k) == s4.subarraySum_bruteforce(nums, k)

    # 5) Product Except Self
    s5 = SolutionProductExceptSelf()
    assert s5.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert s5.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

    # 6) Nice Subarrays
    s6 = SolutionNiceSubarrays()
    assert s6.numberOfSubarrays([1, 1, 2, 1, 1], 3) == 2
    assert s6.numberOfSubarrays([2, 4, 6], 1) == 0
    assert s6.numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2) == 16

    # 7) Range Sum Query 2D
    mat = [
        [3, 0, 1, 4, 2],
        [5, 6, 3, 2, 1],
        [1, 2, 0, 1, 5],
        [4, 1, 0, 1, 7],
        [1, 0, 3, 0, 5],
    ]
    nm = NumMatrix(mat)
    assert nm.sumRegion(2, 1, 4, 3) == 8
    assert nm.sumRegion(1, 1, 2, 2) == 11
    assert nm.sumRegion(1, 2, 2, 4) == 12

    # 8) 우박수열 정적분 (k=4: 4->2->1, 사다리꼴 [3.0, 1.5], 누적 [0,3.0,4.5])
    #    end = (n-1) + b 이므로 b=0 이면 마지막 점(인덱스 2), b=-1 이면 인덱스 1.
    assert solution(4, [[0, 0]]) == [4.5]      # 0 ~ 마지막
    assert solution(4, [[0, -1]]) == [3.0]     # 0 ~ (마지막-1)
    assert solution(4, [[1, 0]]) == [1.5]      # 1 ~ 마지막
    assert solution(4, [[2, 0]]) == [-1.0]     # 시작점 == 끝점 -> 불가
    assert solution(4, [[0, 0], [0, -1], [1, 0], [2, 0]]) == [4.5, 3.0, 1.5, -1.0]

    print("OK - 모든 테스트 통과 (8개 문제)")


if __name__ == "__main__":
    _run_tests()
