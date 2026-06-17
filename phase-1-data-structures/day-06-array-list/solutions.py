"""Day 6 해설 — 배열과 동적 리스트 (Array & List).

각 문제마다 접근 방식을 주석으로 먼저 설명하고,
가능하면 여러 접근(브루트포스 -> 최적화)을 함께 제시한다.
플랫폼 시그니처: LeetCode = class Solution 메서드 / 프로그래머스 = def solution(...).
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

from collections import deque
from itertools import accumulate, combinations
from typing import List


# ---- 문제 1: 배열의 평균값 (프로그래머스 #120817) -----------------
# 원소의 평균값을 반환. 한 번 훑어 합을 구하면 O(n).
def solution_120817(numbers: List[int]) -> float:
    return sum(numbers) / len(numbers)


# ---- 문제 2: Running Sum of 1d Array (LeetCode #1480) -------------
# runningSum[i] = nums[0] + ... + nums[i]
class Solution1480:
    # 접근 1) 직전 누적값에 더해 가며 새 리스트 작성  | 시간복잡도: O(n)
    def runningSum_loop(self, nums: List[int]) -> List[int]:
        out = []
        total = 0
        for x in nums:
            total += x
            out.append(total)
        return out

    # 접근 2) itertools.accumulate 로 한 줄  | 시간복잡도: O(n)
    def runningSum_itertools(self, nums: List[int]) -> List[int]:
        return list(accumulate(nums))

    # 접근 3) 제자리(in-place) 갱신, 추가 공간 O(1)  | 시간복잡도: O(n)
    def runningSum_inplace(self, nums: List[int]) -> List[int]:
        for i in range(1, len(nums)):
            nums[i] += nums[i - 1]
        return nums


# ---- 문제 3: 배열 회전시키기 (프로그래머스 #120844) ---------------
# direction 방향("left"/"right")으로 한 칸 회전.
# 접근 1) 슬라이싱  | 시간복잡도: O(n), 공간 O(n)
def solution_120844_slice(numbers: List[int], direction: str) -> List[int]:
    if direction == "right":
        return numbers[-1:] + numbers[:-1]   # 마지막을 앞으로
    return numbers[1:] + numbers[:1]         # 첫 원소를 뒤로 (left)


# 접근 2) deque.rotate 활용  | 시간복잡도: O(n)
def solution_120844_deque(numbers: List[int], direction: str) -> List[int]:
    dq = deque(numbers)
    dq.rotate(1 if direction == "right" else -1)   # +1=오른쪽, -1=왼쪽
    return list(dq)


# ---- 문제 4: 두 개 뽑아서 더하기 (프로그래머스 #68644) ------------
# 서로 다른 두 인덱스의 합을 중복 없이 오름차순으로.
# 접근 1) 이중 루프 + set  | 시간복잡도: O(n^2)
def solution_68644_loop(numbers: List[int]) -> List[int]:
    sums = set()
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            sums.add(numbers[i] + numbers[j])
    return sorted(sums)


# 접근 2) combinations 로 간결하게  | 시간복잡도: O(n^2)
def solution_68644_comb(numbers: List[int]) -> List[int]:
    return sorted({a + b for a, b in combinations(numbers, 2)})


# ---- 문제 5: Rotate Array (LeetCode #189) ------------------------
# 배열을 오른쪽으로 k칸 회전. 가능하면 제자리(in-place).
class Solution189:
    # 접근 1) 슬라이싱 대입  | 시간복잡도: O(n), 공간 O(n)
    def rotate_slice(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n                       # k가 n보다 클 수 있으니 정규화
        if k:
            nums[:] = nums[-k:] + nums[:-k]

    # 접근 2) 3번 뒤집기 트릭  | 시간복잡도: O(n), 공간 O(1)
    def rotate_reverse(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n

        def rev(lo: int, hi: int) -> None:
            while lo < hi:
                nums[lo], nums[hi] = nums[hi], nums[lo]
                lo += 1
                hi -= 1

        rev(0, n - 1)        # 전체 뒤집기
        rev(0, k - 1)        # 앞 k개 뒤집기
        rev(k, n - 1)        # 나머지 뒤집기


# ---- 문제 6: Product of Array Except Self (LeetCode #238) --------
# answer[i] = 자기 자신을 뺀 나머지 모든 원소의 곱. 나눗셈 금지.
class Solution238:
    # 접근) prefix(왼쪽 누적 곱) -> suffix(오른쪽 누적 곱)  | O(n), 추가 공간 O(1)
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [1] * n
        # 1단계: answer[i] = nums[0..i-1] 의 곱 (왼쪽 누적)
        prefix = 1
        for i in range(n):
            answer[i] = prefix
            prefix *= nums[i]
        # 2단계: 오른쪽 누적 곱을 곱해 합친다
        suffix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= suffix
            suffix *= nums[i]
        return answer


if __name__ == "__main__":
    # 문제 1
    assert solution_120817([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 5.5
    assert solution_120817([89]) == 89.0
    print("[OK] 문제 1 배열의 평균값")

    # 문제 2
    s1480 = Solution1480()
    assert s1480.runningSum_loop([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert s1480.runningSum_itertools([1, 1, 1, 1, 1]) == [1, 2, 3, 4, 5]
    assert s1480.runningSum_inplace([3, 1, 2, 10, 1]) == [3, 4, 6, 16, 17]
    print("[OK] 문제 2 Running Sum of 1d Array")

    # 문제 3
    for fn in (solution_120844_slice, solution_120844_deque):
        assert fn([1, 2, 3], "right") == [3, 1, 2]
        assert fn([1, 2, 3], "left") == [2, 3, 1]
        assert fn([4, 455, 6, 4, -1, 45, 6], "left") == [455, 6, 4, -1, 45, 6, 4]
    print("[OK] 문제 3 배열 회전시키기")

    # 문제 4
    for fn in (solution_68644_loop, solution_68644_comb):
        assert fn([2, 1, 3, 4, 1]) == [2, 3, 4, 5, 6, 7]
        assert fn([5, 0, 2, 7]) == [2, 5, 7, 9, 12]
    print("[OK] 문제 4 두 개 뽑아서 더하기")

    # 문제 5
    s189 = Solution189()
    a = [1, 2, 3, 4, 5, 6, 7]
    s189.rotate_slice(a, 3)
    assert a == [5, 6, 7, 1, 2, 3, 4]
    b = [1, 2, 3, 4, 5, 6, 7]
    s189.rotate_reverse(b, 3)
    assert b == [5, 6, 7, 1, 2, 3, 4]
    c = [-1, -100, 3, 99]
    s189.rotate_reverse(c, 2)
    assert c == [3, 99, -1, -100]
    print("[OK] 문제 5 Rotate Array")

    # 문제 6
    s238 = Solution238()
    assert s238.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert s238.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    print("[OK] 문제 6 Product of Array Except Self")

    print("=== 모든 테스트 통과 ===")
