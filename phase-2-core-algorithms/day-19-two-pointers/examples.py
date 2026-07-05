# -*- coding: utf-8 -*-
"""
Day 19 - 투 포인터 (Two Pointers): 실행 가능한 예제 모음

세 가지 대표 형태를 담는다.
  (A) 양끝 수렴형(opposite ends): 정렬 배열의 양 끝에서 안으로 좁힌다.
  (B) 빠름/느림(fast & slow): 같은 방향으로 읽기/쓰기 포인터를 분리한다.
  (C) 병합형(merge): 두 정렬 구간을 각자의 포인터로 훑는다.

콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""


# ---------------------------------------------------------------------------
# (A) 양끝 수렴형 1: 정렬 배열에서 합이 target인 두 수 (1-indexed 반환)
# ---------------------------------------------------------------------------
def two_sum_sorted(a, target):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        s = a[lo] + a[hi]
        if s == target:
            return [lo + 1, hi + 1]
        if s < target:
            lo += 1               # 합이 작으니 왼쪽을 키운다
        else:
            hi -= 1               # 합이 크니 오른쪽을 줄인다
    return []


# ---------------------------------------------------------------------------
# (A) 양끝 수렴형 2: 회문(palindrome) 검사 - 영숫자만, 대소문자 무시
# ---------------------------------------------------------------------------
def is_palindrome(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        while lo < hi and not s[lo].isalnum():
            lo += 1
        while lo < hi and not s[hi].isalnum():
            hi -= 1
        if s[lo].lower() != s[hi].lower():
            return False
        lo += 1
        hi -= 1
    return True


# ---------------------------------------------------------------------------
# (A) 양끝 수렴형 3: Container With Most Water - 최대 물 넓이
#     넓이 = min(높이) * 폭. 항상 "더 낮은 쪽"을 안으로 옮긴다.
# ---------------------------------------------------------------------------
def max_area(height):
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        h = min(height[lo], height[hi])
        best = max(best, h * (hi - lo))
        if height[lo] < height[hi]:
            lo += 1               # 낮은 쪽을 옮겨야 개선 가능성이 있다
        else:
            hi -= 1
    return best


# ---------------------------------------------------------------------------
# (B) 빠름/느림: 정렬 배열 중복 제거 (in-place, O(1) 공간)
#     slow = 채울 자리, fast = 읽는 자리
# ---------------------------------------------------------------------------
def remove_duplicates(a):
    if not a:
        return 0
    slow = 0
    for fast in range(1, len(a)):
        if a[fast] != a[slow]:
            slow += 1
            a[slow] = a[fast]
    return slow + 1               # 유일 원소 개수


# ---------------------------------------------------------------------------
# (B) 빠름/느림: 0을 뒤로 밀기 (Move Zeroes) - 순서 유지 in-place
# ---------------------------------------------------------------------------
def move_zeroes(a):
    slow = 0
    for fast in range(len(a)):
        if a[fast] != 0:
            a[slow], a[fast] = a[fast], a[slow]
            slow += 1
    return a


# ---------------------------------------------------------------------------
# (C) 병합형: 정렬 배열의 제곱을 정렬 상태로 (O(n))
#     음수의 제곱이 커질 수 있으므로 양 끝에서 큰 것부터 뒤에 채운다.
# ---------------------------------------------------------------------------
def sorted_squares(a):
    n = len(a)
    res = [0] * n
    lo, hi, pos = 0, n - 1, n - 1
    while lo <= hi:
        if abs(a[lo]) > abs(a[hi]):
            res[pos] = a[lo] * a[lo]
            lo += 1
        else:
            res[pos] = a[hi] * a[hi]
            hi -= 1
        pos -= 1
    return res


# ---------------------------------------------------------------------------
# (C) 병합형: 정렬된 두 배열 합치기 (merge sort의 병합 단계)
# ---------------------------------------------------------------------------
def merge_sorted(a, b):
    i, j = 0, 0
    res = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i]); i += 1
        else:
            res.append(b[j]); j += 1
    res.extend(a[i:])             # 남은 꼬리 이어 붙이기
    res.extend(b[j:])
    return res


# ---------------------------------------------------------------------------
# 데모 출력 (ASCII only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== (A) two_sum_sorted ===")
    print("[2,7,11,15] target 18 ->", two_sum_sorted([2, 7, 11, 15], 18))
    print("[2,3,4] target 6 ->", two_sum_sorted([2, 3, 4], 6))

    print("=== (A) is_palindrome ===")
    print("A man, a plan, a canal: Panama ->",
          is_palindrome("A man, a plan, a canal: Panama"))
    print("race a car ->", is_palindrome("race a car"))

    print("=== (A) max_area ===")
    print("[1,8,6,2,5,4,8,3,7] ->", max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))

    print("=== (B) remove_duplicates ===")
    arr = [1, 1, 2, 2, 3]
    k = remove_duplicates(arr)
    print("len =", k, "front =", arr[:k])

    print("=== (B) move_zeroes ===")
    print("[0,1,0,3,12] ->", move_zeroes([0, 1, 0, 3, 12]))

    print("=== (C) sorted_squares ===")
    print("[-4,-1,0,3,10] ->", sorted_squares([-4, -1, 0, 3, 10]))

    print("=== (C) merge_sorted ===")
    print("[1,3,5]+[2,4,6] ->", merge_sorted([1, 3, 5], [2, 4, 6]))

    print("All examples ran OK")
