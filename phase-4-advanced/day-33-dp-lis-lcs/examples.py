# -*- coding: utf-8 -*-
"""
Day 33 - 부분 수열 DP (LIS / LCS) 예제 모음

핵심 주제:
  1) LIS - O(N^2) DP vs O(N log N) 이분 탐색 (같은 답, 다른 비용)
  2) LIS 실제 수열 복원 (부모 포인터)
  3) strictly increasing vs non-decreasing (bisect_left vs bisect_right)
  4) LCS - 2차원 DP + 실제 공통 부분 수열 복원
  5) 편집 거리 (Edit Distance) - LCS 사촌
  6) 최장 팰린드롬 부분 수열 = LCS(s, reverse(s))
  7) 부분 수열 vs 부분 배열(연속) 대비

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from bisect import bisect_left, bisect_right


# ---------------------------------------------------------------------------
# 1) LIS - O(N^2) DP
#    dp[i] = i 로 끝나는 최장 증가 부분 수열 길이,  답 = max(dp)
# ---------------------------------------------------------------------------
def lis_dp(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# ---------------------------------------------------------------------------
# 2) LIS - O(N log N) 이분 탐색
#    tails[k] = 길이 k+1 인 증가 수열들의 마지막 원소 최솟값.
#    tails 의 "길이"만 LIS 길이로 신뢰한다(내용은 실제 수열이 아님).
# ---------------------------------------------------------------------------
def lis_fast(nums):
    tails = []
    for x in nums:
        pos = bisect_left(tails, x)          # strictly increasing
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# ---------------------------------------------------------------------------
# 3) LIS 실제 수열 복원 - O(N log N) + 부모 포인터
# ---------------------------------------------------------------------------
def lis_reconstruct(nums):
    tails = []          # tails[k] = 길이 k+1 수열의 마지막 원소 (nums 인덱스)
    parent = [-1] * len(nums)
    for i, x in enumerate(nums):
        # tails 가 가리키는 값들에 대해 이분 탐색
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[tails[mid]] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo > 0:
            parent[i] = tails[lo - 1]
        if lo == len(tails):
            tails.append(i)
        else:
            tails[lo] = i
    # 마지막 원소부터 부모를 따라 역추적
    seq = []
    k = tails[-1] if tails else -1
    while k != -1:
        seq.append(nums[k])
        k = parent[k]
    seq.reverse()
    return seq


# ---------------------------------------------------------------------------
# 4) strictly vs non-decreasing - bisect 함수만 바꾼다
# ---------------------------------------------------------------------------
def lis_strict(nums):
    tails = []
    for x in nums:
        pos = bisect_left(tails, x)          # 중복 불가 (strict)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


def lis_nondecreasing(nums):
    tails = []
    for x in nums:
        pos = bisect_right(tails, x)         # 중복 허용 (<=)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# ---------------------------------------------------------------------------
# 5) LCS - 2차원 DP (길이)
# ---------------------------------------------------------------------------
def lcs(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# ---------------------------------------------------------------------------
# 6) LCS 실제 공통 부분 수열 복원 - 표를 역추적
# ---------------------------------------------------------------------------
def lcs_string(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # 역추적
    i, j, out = m, n, []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    out.reverse()
    return "".join(out)


# ---------------------------------------------------------------------------
# 7) 편집 거리 (Edit Distance)
# ---------------------------------------------------------------------------
def edit_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


# ---------------------------------------------------------------------------
# 8) 최장 팰린드롬 부분 수열 (LPS) = LCS(s, reverse(s))
# ---------------------------------------------------------------------------
def longest_palindromic_subseq(s):
    return lcs(s, s[::-1])


# ---------------------------------------------------------------------------
# 9) 부분 배열(연속) 대비 - 가장 긴 "연속" 증가 부분 배열 (DP 아님, O(N))
# ---------------------------------------------------------------------------
def longest_continuous_increasing(nums):
    if not nums:
        return 0
    best = cur = 1
    for i in range(1, len(nums)):
        cur = cur + 1 if nums[i] > nums[i - 1] else 1
        best = max(best, cur)
    return best


def main():
    print("=" * 60)
    print("Day 33 - LIS / LCS 예제")
    print("=" * 60)

    nums = [10, 9, 2, 5, 3, 7, 101, 18]

    print("\n[1] LIS - O(N^2) DP vs O(N log N) 이분 탐색")
    d = lis_dp(nums)
    f = lis_fast(nums)
    ok = "O" if d == f else "X"
    print("  nums = %s" % nums)
    print("  O(N^2)=%d  O(NlogN)=%d  [%s]  (기대값 4)" % (d, f, ok))

    print("\n[2] LIS 실제 수열 복원")
    seq = lis_reconstruct(nums)
    print("  복원된 LIS = %s (길이 %d)" % (seq, len(seq)))
    print("  * tails 길이는 정확하지만 tails 내용은 실제 수열이 아니다")

    print("\n[3] strictly increasing vs non-decreasing")
    dup = [1, 3, 3, 3, 2, 4]
    print("  nums = %s" % dup)
    print("  strict(중복불가)      = %d  (예: [1,3,4])" % lis_strict(dup))
    print("  non-decreasing(<=)    = %d  (예: [1,3,3,3,4])"
          % lis_nondecreasing(dup))

    print("\n[4] LCS - 길이와 실제 공통 부분 수열")
    a, b = "ABCBDAB", "BDCAB"
    length = lcs(a, b)
    s = lcs_string(a, b)
    print("  a=%s  b=%s" % (a, b))
    print("  LCS 길이 = %d, 한 예 = %s  (기대 길이 4)" % (length, s))

    print("\n[5] 편집 거리 (Edit Distance)")
    for x, y in [("horse", "ros"), ("intention", "execution"), ("", "abc")]:
        print("  '%s' -> '%s' : %d" % (x, y, edit_distance(x, y)))
    print("  * horse->ros=3, intention->execution=5")

    print("\n[6] 최장 팰린드롬 부분 수열 = LCS(s, reverse(s))")
    for s in ["bbbab", "cbbd", "agbdba"]:
        print("  %s -> %d" % (s, longest_palindromic_subseq(s)))
    print("  * bbbab -> 4 ('bbbb'),  cbbd -> 2 ('bb')")

    print("\n[7] 부분 수열 vs 부분 배열(연속) 대비")
    arr = [1, 3, 5, 4, 7]
    print("  arr = %s" % arr)
    print("  LIS(부분 수열)      = %d  ([1,3,5,7] 또는 [1,3,4,7])"
          % lis_dp(arr))
    print("  연속 증가(부분 배열) = %d  ([1,3,5] 만 연속)"
          % longest_continuous_increasing(arr))

    print("\n[요약] 부분 수열 DP 판별 4문(問)")
    print("  1) 연속인가? -> 연속=투포인터/슬라이딩, 건너뛰기=DP")
    print("  2) 한 수열(LIS)인가 두 수열(LCS)인가")
    print("  3) LIS 는 N 범위로 O(N^2) / O(NlogN) 택")
    print("  4) 복원 필요? -> 표/부모포인터 남기기 (공간 압축과 상충)")

    print("\n" + "=" * 60)
    print("모든 예제 실행 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
