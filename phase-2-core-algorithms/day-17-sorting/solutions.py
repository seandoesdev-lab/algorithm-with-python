# -*- coding: utf-8 -*-
"""
Day 17 - 정렬 (Sorting): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(내장 정렬 vs 직접 구현)을 함께 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from functools import cmp_to_key


# ===========================================================================
# 1. Merge Sorted Array (LeetCode #88)
#    뒤에서부터 채우기 O(m+n) / O(1)
# ===========================================================================
class SolutionMergeSortedArray:
    def merge(self, nums1, m, nums2, n):
        """제자리 병합. 큰 값부터 nums1 끝에서 채운다."""
        i, j, k = m - 1, n - 1, m + n - 1
        while j >= 0:
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1
        return nums1


# ===========================================================================
# 2. K번째수 (프로그래머스 #42748)
#    잘라서 정렬 후 k번째
# ===========================================================================
def solution_kth(array, commands):
    """각 명령마다 i~j 슬라이스 정렬 후 k번째(1-based)."""
    answer = []
    for i, j, k in commands:
        answer.append(sorted(array[i - 1:j])[k - 1])
    return answer


# ===========================================================================
# 3. Sort an Array (LeetCode #912)
#    내장 정렬 금지 -> 병합 정렬 직접 구현 O(n log n)
# ===========================================================================
class SolutionSortArray:
    def sortArray(self, nums):
        """병합 정렬: 최악도 O(n log n) 보장, 안정."""
        if len(nums) <= 1:
            return nums
        mid = len(nums) // 2
        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        out = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        out.extend(left[i:])
        out.extend(right[j:])
        return out


# ===========================================================================
# 4. Sort Colors (LeetCode #75)
#    계수 정렬 O(n)  vs  Dutch flag 3-way 분할 O(n)/O(1) 한 번 순회
# ===========================================================================
class SolutionSortColors:
    def sortColors_count(self, nums):
        """계수 정렬: 0/1/2 개수 세고 다시 채움. O(n) 시간, 2회 순회."""
        count = [0, 0, 0]
        for x in nums:
            count[x] += 1
        idx = 0
        for v in range(3):
            for _ in range(count[v]):
                nums[idx] = v
                idx += 1
        return nums

    def sortColors(self, nums):
        """Dutch national flag: 한 번 순회 O(n), 제자리 O(1)."""
        low, mid, high = 0, 0, len(nums) - 1
        while mid <= high:
            if nums[mid] == 0:
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                mid += 1
            else:  # == 2
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
        return nums


# ===========================================================================
# 5. Merge Intervals (LeetCode #56)
#    시작점 정렬 후 병합 O(n log n)
# ===========================================================================
class SolutionMergeIntervals:
    def merge(self, intervals):
        intervals.sort(key=lambda iv: iv[0])   # 시작점 기준 정렬
        merged = []
        for start, end in intervals:
            if merged and start <= merged[-1][1]:
                # 겹침: 끝을 확장
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])
        return merged


# ===========================================================================
# 6. 가장 큰 수 (프로그래머스 #42746)
#    cmp_to_key: x+y vs y+x
# ===========================================================================
def solution_largest(numbers):
    strs = list(map(str, numbers))

    def cmp(x, y):
        if x + y > y + x:
            return -1
        if x + y < y + x:
            return 1
        return 0

    strs.sort(key=cmp_to_key(cmp))
    # 전부 0인 경우 "000" -> "0"
    return str(int("".join(strs)))


# ===========================================================================
# 7. H-Index (프로그래머스 #42747)
#    내림차순 정렬 후 citations[i] >= i+1 의 최대 i+1
# ===========================================================================
def solution_h_index(citations):
    citations.sort(reverse=True)
    h = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h = i + 1
        else:
            break
    return h


# ===========================================================================
# 8. Largest Number (LeetCode #179)
#    #42746과 동일 비교, 문자열 반환
# ===========================================================================
class SolutionLargestNumber:
    def largestNumber(self, nums):
        strs = list(map(str, nums))

        def cmp(x, y):
            if x + y > y + x:
                return -1
            if x + y < y + x:
                return 1
            return 0

        strs.sort(key=cmp_to_key(cmp))
        return str(int("".join(strs)))   # 선행 0 제거("00"->"0")


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    m = SolutionMergeSortedArray()
    assert m.merge([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]
    assert m.merge([1], 1, [], 0) == [1]
    assert m.merge([0], 0, [1], 1) == [1]

    assert solution_kth([1, 5, 2, 6, 3, 7, 4],
                        [[2, 5, 3], [4, 4, 1], [1, 7, 3]]) == [5, 6, 3]

    sa = SolutionSortArray()
    assert sa.sortArray([5, 2, 3, 1]) == [1, 2, 3, 5]
    assert sa.sortArray([5, 1, 1, 2, 0, 0]) == [0, 0, 1, 1, 2, 5]

    sc = SolutionSortColors()
    assert sc.sortColors([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]
    assert sc.sortColors([2, 0, 1]) == [0, 1, 2]
    assert sc.sortColors_count([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]

    mi = SolutionMergeIntervals()
    assert mi.merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert mi.merge([[1, 4], [4, 5]]) == [[1, 5]]

    assert solution_largest([6, 10, 2]) == "6210"
    assert solution_largest([3, 30, 34, 5, 9]) == "9534330"
    assert solution_largest([0, 0, 0]) == "0"

    assert solution_h_index([3, 0, 6, 1, 5]) == 3
    assert solution_h_index([10, 8, 5, 4, 3]) == 4
    assert solution_h_index([25, 8]) == 2

    ln = SolutionLargestNumber()
    assert ln.largestNumber([10, 2]) == "210"
    assert ln.largestNumber([3, 30, 34, 5, 9]) == "9534330"
    assert ln.largestNumber([0, 0]) == "0"

    print("Day 17 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()
