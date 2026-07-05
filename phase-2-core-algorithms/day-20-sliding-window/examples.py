# -*- coding: utf-8 -*-
"""
Day 20 - 슬라이딩 윈도우 (Sliding Window): 예제 코드

세 가지 창 형태를 실행 가능한 형태로 정리한다.
  (A) 고정 크기 창 (fixed window)  - 초기 합 후 한 칸씩 밀기
  (B) 가변 크기 창 (variable)      - 확장(expand) / 수축(shrink) 골격
  (C) 가변 창 + 해시               - 중복 없는 최장 부분 문자열
  (D) 고정 창 + 문자 카운트         - 아나그램 시작 인덱스 모두 찾기
  (E) 단조 덱                      - 창 최댓값 O(n)

콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다. (한글 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from collections import deque


# ---------------------------------------------------------------------------
# (A) 고정 크기 창 - 길이 k 부분 배열의 최대 합/평균
#     초기 창 합을 한 번만 구하고, 한 칸 밀 때 +새원소 -옛원소로 O(1) 갱신.
# ---------------------------------------------------------------------------
def max_sum_fixed(a, k):
    if k > len(a):
        return None
    window = sum(a[:k])       # 초기 창 (한 번만 전체 합산)
    best = window
    for right in range(k, len(a)):
        window += a[right] - a[right - k]   # 새 원소 추가, k칸 전 원소 제거
        if window > best:
            best = window
    return best


def max_average_fixed(a, k):
    return max_sum_fixed(a, k) / k


# ---------------------------------------------------------------------------
# (B) 가변 크기 창 - 합이 target 이상인 최소 길이 (양수 배열 전제)
#     오른쪽으로 확장, 조건을 만족하면 왼쪽을 최대한 조인다.
# ---------------------------------------------------------------------------
def min_subarray_len(target, nums):
    left = 0
    total = 0
    best = len(nums) + 1                # 불가능을 뜻하는 큰 값
    for right in range(len(nums)):
        total += nums[right]            # 확장(expand)
        while total >= target:          # 유효하면 수축(shrink)
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0


# ---------------------------------------------------------------------------
# (C) 가변 창 + 해시 - 중복 없는 최장 부분 문자열 길이
#     각 문자의 마지막 위치를 기억하고, 중복을 만나면 left를 점프시킨다.
#     주의: left는 절대 되돌아가면 안 되므로 max(...)로 갱신.
# ---------------------------------------------------------------------------
def longest_unique(s):
    last = {}                           # 문자 -> 마지막 등장 인덱스
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last and last[c] >= left:
            left = last[c] + 1          # 중복을 창 밖으로 밀어냄
        last[c] = right
        best = max(best, right - left + 1)
    return best


# ---------------------------------------------------------------------------
# (D) 고정 창 + 문자 카운트 - 문자열 s에서 p의 아나그램 시작 인덱스 모두 찾기
#     창 길이 = len(p) 로 고정. 창 안 문자 개수 == p 문자 개수 이면 아나그램.
# ---------------------------------------------------------------------------
def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    need = {}
    for c in p:
        need[c] = need.get(c, 0) + 1
    window = {}
    res = []
    k = len(p)
    for right, c in enumerate(s):
        window[c] = window.get(c, 0) + 1        # 새 문자 추가
        if right >= k:                          # 창을 벗어난 왼쪽 문자 제거
            left_c = s[right - k]
            window[left_c] -= 1
            if window[left_c] == 0:
                del window[left_c]
        if window == need:                      # 창 길이가 k일 때만 일치 가능
            res.append(right - k + 1)
    return res


# ---------------------------------------------------------------------------
# (E) 창 최댓값 - 단조 덱(monotonic deque)으로 O(n)
#     덱에는 "인덱스"를 값이 단조 감소하도록 저장한다.
#     맨 앞(deque[0])이 항상 현재 창의 최댓값 인덱스.
# ---------------------------------------------------------------------------
def max_sliding_window(nums, k):
    dq = deque()            # 인덱스 저장 (대응 값이 단조 감소)
    res = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:     # 새 값보다 작은 뒤쪽은 쓸모 없다
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                  # 창을 벗어난 앞쪽 제거
            dq.popleft()
        if i >= k - 1:                      # 첫 완전한 창부터 기록
            res.append(nums[dq[0]])
    return res


def _demo():
    arr = [1, 12, -5, -6, 50, 3]
    print("고정 창 최대 합 (k=4):", max_sum_fixed(arr, 4))          # 51
    print("고정 창 최대 평균 (k=4):", max_average_fixed(arr, 4))    # 12.75

    print("최소 길이 (target=7):", min_subarray_len(7, [2, 3, 1, 2, 4, 3]))  # 2
    print("최소 길이 (불가능):", min_subarray_len(100, [1, 2, 3]))           # 0

    print("중복 없는 최장 abcabcbb:", longest_unique("abcabcbb"))   # 3
    print("중복 없는 최장 bbbbb:", longest_unique("bbbbb"))         # 1
    print("중복 없는 최장 pwwkew:", longest_unique("pwwkew"))       # 3

    print("아나그램 인덱스 cbaebabacd/abc:", find_anagrams("cbaebabacd", "abc"))  # [0, 6]
    print("아나그램 인덱스 abab/ab:", find_anagrams("abab", "ab"))                # [0, 1, 2]

    print("창 최댓값 [1,3,-1,-3,5,3,6,7] k=3:",
          max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))       # [3,3,5,5,6,7]

    print("Day 20 examples: OK")


if __name__ == "__main__":
    _demo()
