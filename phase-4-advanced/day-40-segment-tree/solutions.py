"""Day 40 연습문제 해설 - 세그먼트 트리·펜윅 트리 (Segment Tree & Fenwick/BIT).

실행: PYTHONIOENCODING=cp949 python solutions.py

문제 목록 (출처: 프로그래머스 / LeetCode 만)
  1. LeetCode #303  Range Sum Query - Immutable            (누적 합)
  2. LeetCode #307  Range Sum Query - Mutable              (세그트리 / BIT)
  3. LeetCode #315  Count of Smaller Numbers After Self    (BIT / 머지 소트)
  4. 프로그래머스 #64062  징검다리 건너기                   (RMQ / 덱 / 이분 탐색)
  5. LeetCode #493  Reverse Pairs                          (BIT / 머지 소트)
  6. LeetCode #732  My Calendar III                        (스위핑 / 동적 lazy)

각 문제는 플랫폼 시그니처를 그대로 쓰고, assert 로 자체 검증한다.
가능한 문제는 여러 접근을 구현해 복잡도와 실측을 비교한다.

주의(cp949 콘솔 안전): 출력 문자열에는 ASCII 기호(=, -, O, X)만 쓴다.
"""

import random
import time
from bisect import bisect_left
from collections import deque


# ==========================================================================
# 공용 자료구조
# ==========================================================================

class SegTree:
    """반복형 세그먼트 트리. 반열린 구간 [l, r). 합/min/max 등 가환 연산용."""

    def __init__(self, data, func=None, identity=0):
        self.n = len(data)
        self.f = func if func is not None else (lambda a, b: a + b)
        self.e = identity
        self.tree = [identity] * (2 * self.n)
        self.tree[self.n:] = data
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.f(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, value):
        i += self.n
        self.tree[i] = value
        i >>= 1
        while i:
            self.tree[i] = self.f(self.tree[2 * i], self.tree[2 * i + 1])
            i >>= 1

    def query(self, l, r):
        res_l = res_r = self.e
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                res_l = self.f(res_l, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                res_r = self.f(self.tree[r], res_r)
            l >>= 1
            r >>= 1
        return self.f(res_l, res_r)


class BIT:
    """펜윅 트리. 합 전용, 1-based 인덱스 강제."""

    def __init__(self, n, data=None):
        self.n = n
        self.tree = [0] * (n + 1)
        if data is not None:
            for i in range(1, n + 1):
                self.tree[i] += data[i - 1]
                parent = i + (i & -i)
                if parent <= n:
                    self.tree[parent] += self.tree[i]

    def add(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.prefix(r) - self.prefix(l - 1)


# ==========================================================================
# 1. LeetCode #303 - Range Sum Query - Immutable  (난이도: 기초)
# ==========================================================================
# 핵심: 갱신이 없다 -> 세그먼트 트리는 낭비다. 누적 합으로 질의 O(1).
#   pref[i+1] = pref[i] + nums[i]
#   sumRange(l, r) = pref[r+1] - pref[l]
# 복잡도: 전처리 O(N), 질의 O(1), 공간 O(N)
# LeetCode 클래스명은 NumArray 다.

class NumArray:
    """LeetCode #303 시그니처 그대로."""

    def __init__(self, nums):
        self.pref = [0] * (len(nums) + 1)           # pref[0]=0 이 예외 처리를 없앤다
        for i, v in enumerate(nums):
            self.pref[i + 1] = self.pref[i] + v

    def sumRange(self, left, right):
        return self.pref[right + 1] - self.pref[left]   # 닫힌 구간 -> +1


def test_303():
    print("=" * 70)
    print("1. LeetCode #303 Range Sum Query - Immutable (누적 합, 질의 O(1))")
    print("=" * 70)

    na = NumArray([-2, 0, 3, -5, 2, -1])            # 공식 예제
    assert na.sumRange(0, 2) == 1
    assert na.sumRange(2, 5) == -1
    assert na.sumRange(0, 5) == -3
    assert na.sumRange(3, 3) == -5                  # 원소 하나
    print("공식 예제 통과: sumRange(0,2)=%d, sumRange(2,5)=%d, sumRange(0,5)=%d"
          % (na.sumRange(0, 2), na.sumRange(2, 5), na.sumRange(0, 5)))

    na1 = NumArray([7])                             # 경계: 길이 1
    assert na1.sumRange(0, 0) == 7

    random.seed(303)
    for _ in range(300):                            # 브루트포스 교차 검증
        n = random.randint(1, 40)
        arr = [random.randint(-100, 100) for _ in range(n)]
        obj = NumArray(arr)
        for _ in range(20):
            l = random.randrange(n)
            r = random.randint(l, n - 1)
            assert obj.sumRange(l, r) == sum(arr[l:r + 1])
    print("무작위 300회 교차 검증 통과 -> O")
    print("교훈: 갱신이 없으면 누적 합이 정답. 세그먼트 트리를 쓰면 질의가")
    print("      O(1) -> O(log N) 으로 오히려 느려지고 코드만 길어진다.")
    print()


# ==========================================================================
# 2. LeetCode #307 - Range Sum Query - Mutable  (난이도: 중급)
# ==========================================================================
# 핵심: 갱신이 끼어든다 -> 누적 합은 갱신이 O(N) 이라 죽는다.
#       (3e4 x 3e4 = 9e8 -> TLE).  둘 다 O(log N) 으로 만들어야 한다.
# 접근 A: 반복형 세그먼트 트리   (임의 결합 연산으로 확장 가능)
# 접근 B: BIT                    (합 전용. 코드 1/3, 더 빠름)
# 함정: BIT 의 add 는 '증분'을 받는다. 문제의 update 는 '값 지정'이므로
#       현재 값을 따로 들고 있다가 delta = val - cur[i] 로 환산해야 한다.

class NumArrayMutableSeg:
    """접근 A: 세그먼트 트리. LeetCode 실제 클래스명은 NumArray."""

    def __init__(self, nums):
        self.seg = SegTree(list(nums))

    def update(self, index, val):
        self.seg.update(index, val)                 # 값 지정을 그대로 받는다

    def sumRange(self, left, right):
        return self.seg.query(left, right + 1)      # 닫힌 -> 반열린 변환 1회


class NumArrayMutableBIT:
    """접근 B: BIT. 합 문제에서는 이쪽이 더 짧고 빠르다."""

    def __init__(self, nums):
        self.cur = list(nums)                       # 현재 값을 따로 보관 (필수!)
        self.bit = BIT(len(nums), nums)

    def update(self, index, val):
        self.bit.add(index + 1, val - self.cur[index])   # 값 지정 -> 증분
        self.cur[index] = val

    def sumRange(self, left, right):
        return self.bit.range_sum(left + 1, right + 1)   # 0-based -> 1-based


def test_307():
    print("=" * 70)
    print("2. LeetCode #307 Range Sum Query - Mutable (세그트리 vs BIT)")
    print("=" * 70)

    for cls in (NumArrayMutableSeg, NumArrayMutableBIT):
        na = cls([1, 3, 5])                         # 공식 예제
        assert na.sumRange(0, 2) == 9
        na.update(1, 2)
        assert na.sumRange(0, 2) == 8
        na1 = cls([7])                              # 경계: 길이 1
        na1.update(0, -3)
        assert na1.sumRange(0, 0) == -3
    print("공식 예제 통과 (두 구현 모두): [1,3,5] -> 9, update(1,2) -> 8")

    random.seed(307)
    for _ in range(300):
        n = random.randint(1, 40)
        arr = [random.randint(-100, 100) for _ in range(n)]
        a_seg = NumArrayMutableSeg(list(arr))
        a_bit = NumArrayMutableBIT(list(arr))
        for _ in range(25):
            if random.random() < 0.4:
                i = random.randrange(n)
                v = random.randint(-100, 100)
                arr[i] = v
                a_seg.update(i, v)
                a_bit.update(i, v)
            else:
                l = random.randrange(n)
                r = random.randint(l, n - 1)
                want = sum(arr[l:r + 1])
                assert a_seg.sumRange(l, r) == want
                assert a_bit.sumRange(l, r) == want
    print("무작위 300회 x 25연산 교차 검증 통과 (세그트리 = BIT = 브루트) -> O")

    # 실측: 문제 최대 제약 근처 (N=3e4, 호출 3e4)
    n, ops = 30000, 30000
    random.seed(3070)
    base = [random.randint(-100, 100) for _ in range(n)]
    calls = []
    for _ in range(ops):
        if random.random() < 0.5:
            calls.append(('u', random.randrange(n), random.randint(-100, 100)))
        else:
            l = random.randrange(n)
            calls.append(('q', l, random.randint(l, n - 1)))

    t0 = time.perf_counter()
    obj = NumArrayMutableSeg(list(base))
    s1 = 0
    for kind, x, y in calls:
        if kind == 'u':
            obj.update(x, y)
        else:
            s1 += obj.sumRange(x, y)
    t_seg = time.perf_counter() - t0

    t0 = time.perf_counter()
    obj = NumArrayMutableBIT(list(base))
    s2 = 0
    for kind, x, y in calls:
        if kind == 'u':
            obj.update(x, y)
        else:
            s2 += obj.sumRange(x, y)
    t_bit = time.perf_counter() - t0

    assert s1 == s2
    print("실측 N=%d, 호출 %d회 (체크섬 일치)" % (n, ops))
    print("  세그먼트 트리 : %7.4f 초" % t_seg)
    print("  BIT           : %7.4f 초  <- 같은 O(log N), 상수가 작다" % t_bit)
    print("교훈: #303 과 질의는 똑같지만 update 하나 때문에 자료구조가 바뀐다.")
    print("      합만 필요하면 BIT 를 먼저 고려하라.")
    print()


# ==========================================================================
# 3. LeetCode #315 - Count of Smaller Numbers After Self  (난이도: 심화)
# ==========================================================================
# 핵심 발상 전환: 트리를 '인덱스' 위가 아니라 '값' 위에 세운다.
#   오른쪽 -> 왼쪽으로 훑으며 BIT 에 등장한 값을 표시하면
#   prefix(rank-1) = "이미 본(= 내 오른쪽) 것 중 나보다 작은 것의 개수"
# 순서가 중요: 먼저 세고(질의), 그다음 나를 등록(갱신).
#   반대로 하면 같은 값을 세어 '<' 조건이 '<=' 로 오염된다.
# 좌표 압축으로 값 범위와 무관하게 만든다 (rank 는 반드시 1-based).
# 복잡도: O(N log N) 시간, O(N) 공간

class Solution315:
    """LeetCode #315 시그니처: class Solution / def countSmaller."""

    def countSmaller(self, nums):
        """접근 A: 좌표 압축 + BIT. O(N log N). 코테 정석."""
        if not nums:
            return []
        comp = sorted(set(nums))                    # 좌표 압축
        bit = BIT(len(comp))
        out = [0] * len(nums)
        for i in range(len(nums) - 1, -1, -1):      # 오른쪽 -> 왼쪽
            rank = bisect_left(comp, nums[i]) + 1   # 1-based (0 이면 무한 루프!)
            out[i] = bit.prefix(rank - 1)           # 먼저 센다
            bit.add(rank, 1)                        # 그다음 등록한다
        return out

    def countSmaller_mergesort(self, nums):
        """접근 B: 머지 소트. 같은 O(N log N) 이지만 인덱스를 함께 옮겨야 한다."""
        n = len(nums)
        counts = [0] * n
        idx = list(range(n))                        # 값이 아니라 인덱스를 정렬한다

        def sort(lo, hi):                           # [lo, hi)
            if hi - lo <= 1:
                return
            mid = (lo + hi) // 2
            sort(lo, mid)
            sort(mid, hi)
            merged = []
            i, j = lo, mid
            moved = 0                               # 오른쪽에서 먼저 빠져나간 개수
            while i < mid and j < hi:
                if nums[idx[j]] < nums[idx[i]]:
                    merged.append(idx[j])
                    j += 1
                    moved += 1                      # 남은 왼쪽 원소들보다 작다
                else:
                    counts[idx[i]] += moved
                    merged.append(idx[i])
                    i += 1
            while i < mid:
                counts[idx[i]] += moved
                merged.append(idx[i])
                i += 1
            while j < hi:
                merged.append(idx[j])
                j += 1
            idx[lo:hi] = merged

        sort(0, n)
        return counts

    def countSmaller_brute(self, nums):
        """접근 C: 브루트포스 O(N^2). 검증용 (N=1e5 이면 TLE)."""
        n = len(nums)
        return [sum(1 for j in range(i + 1, n) if nums[j] < nums[i])
                for i in range(n)]


def test_315():
    print("=" * 70)
    print("3. LeetCode #315 Count of Smaller Numbers After Self")
    print("=" * 70)
    sol = Solution315()

    assert sol.countSmaller([5, 2, 6, 1]) == [2, 1, 1, 0]      # 공식 예제
    assert sol.countSmaller([-1]) == [0]
    assert sol.countSmaller([-1, -1]) == [0, 0]                # 같은 값 -> 0
    print("공식 예제 통과: [5,2,6,1] ->", sol.countSmaller([5, 2, 6, 1]))
    print("같은 값 경계  : [-1,-1]   ->", sol.countSmaller([-1, -1]),
          " ('<' 이므로 0. '<=' 로 오염되면 [1,0])")

    big_range = [10 ** 9, -10 ** 9, 0, 0, -5, 10 ** 9]
    print("값 범위 20억  :", sol.countSmaller(big_range),
          " (BIT 크기는 서로 다른 값 %d개뿐)" % len(set(big_range)))
    assert sol.countSmaller(big_range) == sol.countSmaller_brute(big_range)

    random.seed(315)
    for _ in range(400):                            # 세 접근 3중 교차 검증
        n = random.randint(1, 45)
        arr = [random.randint(-25, 25) for _ in range(n)]
        want = sol.countSmaller_brute(arr)
        assert sol.countSmaller(arr) == want, arr
        assert sol.countSmaller_mergesort(arr) == want, arr
    print("무작위 400회 3중 교차 검증(BIT / 머지소트 / 브루트) 통과 -> O")

    n = 100000                                      # 문제 최대 제약
    random.seed(3150)
    big = [random.randint(-10 ** 4, 10 ** 4) for _ in range(n)]
    t0 = time.perf_counter()
    r1 = sol.countSmaller(big)
    t_bit = time.perf_counter() - t0
    t0 = time.perf_counter()
    r2 = sol.countSmaller_mergesort(big)
    t_ms = time.perf_counter() - t0
    assert r1 == r2
    print("실측 N=%d (두 결과 동일). 브루트포스라면 약 %.0e 연산 -> TLE"
          % (n, n * n / 2))
    print("  BIT       : %7.4f 초" % t_bit)
    print("  머지 소트 : %7.4f 초" % t_ms)
    print("교훈: '오른쪽에서 왼쪽 + 값의 축 + 누적 개수' 3콤보를 패턴으로 외운다.")
    print()


# ==========================================================================
# 4. 프로그래머스 #64062 - 징검다리 건너기  (2019 카카오 겨울 인턴십)
# ==========================================================================
# 문제 변환이 전부다.
#   x명이 지나가면 각 디딤돌은 최대 x번 밟히므로 stones[i] < x 인 돌은
#   x번째 사람 차례에는 이미 0 이다. k칸을 넘어 뛸 수 없으니
#   "stones[i] < x 인 돌이 연속 k개" 이면 x명은 건널 수 없다.
#   그런데 "구간의 모든 돌이 x 보다 작다" == "그 구간의 최댓값 < x" 이므로
#   x 가 실패하는 조건은  min(윈도우 최댓값들) < x.
#   => 답 = 길이 k 인 모든 연속 구간의 '최댓값'들 중 '최솟값'
#      (최솟값들 중 최댓값이 아니다! 공식 예제에서는 둘 다 3 이라 구별되지 않아
#       무작위 교차 검증으로만 잡히는 함정이다)
# 접근 A: 세그먼트 트리 구간 최댓값  O(N log N)  <- 오늘 배운 도구의 직접 적용
# 접근 B: 덱 슬라이딩 윈도우         O(N)        <- 최적해
# 접근 C: 이분 탐색 + 판정           O(N log max)
# 프로그래머스 시그니처: def solution(stones, k)

def solution(stones, k):
    """접근 B(덱): O(N). 제출용 정답. 윈도우 최댓값들의 최솟값."""
    dq = deque()                                    # 값이 감소하는 인덱스 덱
    best = float('inf')
    for i, v in enumerate(stones):
        while dq and stones[dq[-1]] <= v:
            dq.pop()                                # 나보다 작으면 최댓값 후보 탈락
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                            # 윈도우를 벗어났다
        if i >= k - 1:
            window_max = stones[dq[0]]
            if window_max < best:
                best = window_max
    return best


def solution_segtree(stones, k):
    """접근 A(세그먼트 트리 구간 최댓값): O(N log N). 항등원은 -inf 여야 한다!"""
    seg = SegTree(list(stones), max, float('-inf'))
    return min(seg.query(i, i + k) for i in range(len(stones) - k + 1))


def solution_binsearch(stones, k):
    """접근 C(이분 탐색): 'x명이 가능한가?'를 O(N) 판정 + 상한 이분 탐색."""
    def can_cross(x):
        run = 0                                     # stones[i] < x 인 연속 길이
        for s in stones:
            if s < x:
                run += 1
                if run >= k:                        # k개 연속 -> 뛰어넘을 수 없다
                    return False
            else:
                run = 0
        return True

    lo, hi = 1, max(stones)                         # 최소 1명, 최대 max(stones)명
    while lo < hi:
        mid = (lo + hi + 1) // 2                    # 상한을 찾는 이분 탐색
        if can_cross(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def solution_brute(stones, k):
    """검증용 브루트포스: 윈도우 최댓값들의 최솟값."""
    return min(max(stones[i:i + k]) for i in range(len(stones) - k + 1))


def test_64062():
    print("=" * 70)
    print("4. 프로그래머스 #64062 징검다리 건너기 (2019 카카오 겨울 인턴십)")
    print("=" * 70)

    stones, k = [2, 4, 5, 3, 2, 1, 4, 2, 5, 1], 3   # 공식 예제
    assert solution(stones, k) == 3
    assert solution_segtree(stones, k) == 3
    assert solution_binsearch(stones, k) == 3
    print("공식 예제: stones =", stones, ", k =", k)
    print("  덱=%d, 세그트리=%d, 이분탐색=%d  (기대 3)"
          % (solution(stones, k), solution_segtree(stones, k),
             solution_binsearch(stones, k)))
    print("  길이 k 윈도우 최댓값들 =",
          [max(stones[i:i + k]) for i in range(len(stones) - k + 1)],
          "-> 그중 최솟값 3")
    print("  (주의: '최솟값들의 최댓값'도 이 예제에서는 우연히 3 이라 구별되지")
    print("   않는다. 올바른 식은 '최댓값들의 최솟값'이다)")

    assert solution([1], 1) == 1                    # 경계: 원소 1개
    assert solution([5, 1, 5], 3) == 5              # k = len(stones) -> max 전체
    assert solution([7, 7, 7], 1) == 7              # k = 1
    print("경계 케이스 통과: len=1 / k=len(stones) / k=1")

    random.seed(64062)
    for _ in range(400):                            # 네 접근 4중 교차 검증
        n = random.randint(1, 30)
        arr = [random.randint(1, 20) for _ in range(n)]
        kk = random.randint(1, n)
        want = solution_brute(arr, kk)
        assert solution(arr, kk) == want, (arr, kk)
        assert solution_segtree(arr, kk) == want, (arr, kk)
        assert solution_binsearch(arr, kk) == want, (arr, kk)
    print("무작위 400회 4중 교차 검증(덱 / 세그트리 / 이분 / 브루트) 통과 -> O")

    n = 200000                                      # 문제 최대 제약
    random.seed(640620)
    big = [random.randint(1, 200000000) for _ in range(n)]
    kk = 1000
    answers = []
    for name, fn in (("덱(O(N))           ", solution),
                     ("세그트리(N log N)  ", solution_segtree),
                     ("이분탐색(N log M)  ", solution_binsearch)):
        t0 = time.perf_counter()
        got = fn(big, kk)
        answers.append(got)
        print("  %s: %7.4f 초  답=%d" % (name, time.perf_counter() - t0, got))
    assert len(set(answers)) == 1
    print("실측 N=%d, k=%d - 세 접근 답 일치 -> O" % (n, kk))
    print("교훈: 세그먼트 트리로 풀 수 있어도 최적은 아니다.")
    print("      고정 길이 윈도우 min/max 는 덱이 정답이다.")
    print()


# ==========================================================================
# 5. LeetCode #493 - Reverse Pairs  (난이도: 심화)
# ==========================================================================
# #315 와 골격이 같다. 조건만 nums[j] < nums[i] -> 2*nums[j] < nums[i].
# 함정: x // 2 (정수 나눗셈)로 경계를 만들면 음수에서 틀린다.
#   안전한 방법: doubled = [2*v for v in comp] 를 미리 만들고
#               cut = bisect_left(doubled, x)  -> rank 1..cut 은 모두 2*v < x
#   doubled 가 정렬을 유지하는 이유: v 증가 -> 2v 증가 (단조).
#   bisect_left 를 쓰는 이유: 2*v == x 는 '>' 조건에 포함되지 않아야 한다.
#     (bisect_right 를 쓰면 등호를 포함해 답이 커진다)
# 복잡도: O(N log N) 시간, O(N) 공간

class Solution493:
    """LeetCode #493 시그니처: class Solution / def reversePairs."""

    def reversePairs(self, nums):
        """접근 A: 좌표 압축 + BIT. 정수 연산만 사용한다."""
        if not nums:
            return 0
        comp = sorted(set(nums))
        doubled = [2 * v for v in comp]             # 단조 증가 유지
        bit = BIT(len(comp))
        total = 0
        for i in range(len(nums) - 1, -1, -1):      # 오른쪽 -> 왼쪽
            x = nums[i]
            cut = bisect_left(doubled, x)           # doubled[cut] >= x
            total += bit.prefix(cut)                # rank 1..cut 은 모두 2*v < x
            bit.add(bisect_left(comp, x) + 1, 1)    # 나를 등록 (1-based)
        return total

    def reversePairs_mergesort(self, nums):
        """접근 B: 머지 소트 + 투 포인터. 두 절반이 정렬되어 포인터가 단조."""
        def rec(a):
            if len(a) <= 1:
                return 0, a
            mid = len(a) // 2
            c1, left = rec(a[:mid])
            c2, right = rec(a[mid:])
            count = c1 + c2
            j = 0
            for x in left:                          # left 오름차순 -> j 단조 증가
                while j < len(right) and 2 * right[j] < x:
                    j += 1
                count += j
            merged = []                             # 실제 병합
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])
            return count, merged

        return rec(list(nums))[0]

    def reversePairs_brute(self, nums):
        """검증용 브루트포스 O(N^2)."""
        n = len(nums)
        return sum(1 for i in range(n) for j in range(i + 1, n)
                   if nums[i] > 2 * nums[j])


def test_493():
    print("=" * 70)
    print("5. LeetCode #493 Reverse Pairs (역순 쌍 세기)")
    print("=" * 70)
    sol = Solution493()

    assert sol.reversePairs([1, 3, 2, 3, 1]) == 2               # 공식 예제
    assert sol.reversePairs([2, 4, 3, 5, 1]) == 3               # 공식 예제
    assert sol.reversePairs([5]) == 0
    print("공식 예제 통과: [1,3,2,3,1] -> %d, [2,4,3,5,1] -> %d"
          % (sol.reversePairs([1, 3, 2, 3, 1]),
             sol.reversePairs([2, 4, 3, 5, 1])))

    # 음수 함정: x // 2 로 경계를 만들면 여기서 틀린다
    neg = [-5, -2, -1, 3, -7]
    print("음수 케이스 :", neg)
    print("  BIT=%d, 머지소트=%d, 브루트=%d"
          % (sol.reversePairs(neg), sol.reversePairs_mergesort(neg),
             sol.reversePairs_brute(neg)))
    assert sol.reversePairs(neg) == sol.reversePairs_brute(neg)
    assert sol.reversePairs_mergesort(neg) == sol.reversePairs_brute(neg)

    # 등호 경계: 2*v == x 는 세지 않아야 한다 (bisect_left 가 그렇게 동작)
    assert sol.reversePairs([4, 2]) == 0            # 4 > 2*2 = 4 는 거짓
    assert sol.reversePairs_brute([4, 2]) == 0
    print("등호 경계  : [4,2] -> 0  (4 > 2*2 는 거짓. bisect_right 면 1 로 오답)")

    # 32비트 극단값
    ext = [2 ** 31 - 1, -2 ** 31, 0, 2 ** 31 - 1, -2 ** 31]
    assert sol.reversePairs(ext) == sol.reversePairs_brute(ext)
    print("32비트 극단값 통과:", ext, "->", sol.reversePairs(ext))

    random.seed(493)
    for _ in range(400):                            # 3중 교차 검증
        n = random.randint(1, 40)
        arr = [random.randint(-30, 30) for _ in range(n)]
        want = sol.reversePairs_brute(arr)
        assert sol.reversePairs(arr) == want, arr
        assert sol.reversePairs_mergesort(arr) == want, arr
    print("무작위 400회 3중 교차 검증(BIT / 머지소트 / 브루트) 통과 -> O")

    n = 50000                                       # 문제 최대 제약
    random.seed(4930)
    big = [random.randint(-10 ** 9, 10 ** 9) for _ in range(n)]
    t0 = time.perf_counter()
    a1 = sol.reversePairs(big)
    t_bit = time.perf_counter() - t0
    t0 = time.perf_counter()
    a2 = sol.reversePairs_mergesort(big)
    t_ms = time.perf_counter() - t0
    assert a1 == a2
    print("실측 N=%d (두 답 동일: %d)" % (n, a1))
    print("  BIT       : %7.4f 초" % t_bit)
    print("  머지 소트 : %7.4f 초" % t_ms)
    print("교훈: 부등식을 BIT 질의 '경계'로 옮기는 계산이 이 문제의 전부다.")
    print("      정수 나눗셈(x // 2) 대신 doubled 배열 + bisect_left 를 쓴다.")
    print()


# ==========================================================================
# 6. LeetCode #732 - My Calendar III  (난이도: 심화)
# ==========================================================================
# 번역: "[start, end) 의 모든 시점에 +1, 그리고 전체 최댓값을 답하라"
#       = 구간 갱신(range add) + 전체 최댓값 질의
# 접근 A: 차분 + 스위핑. 호출이 400번뿐이므로 이게 가장 단순하다.
# 접근 B: 동적(implicit) 지연 전파 세그먼트 트리. 좌표 압축 없이 0..1e9 사용.
#   여기서는 '뿌리의 최댓값'만 묻기 때문에 push_down 이 필요 없다:
#     tree[node] = max(자식들) + lazy[node]
#   서브구간을 질의해야 한다면 push_down 을 반드시 구현해야 한다.
#   최댓값 트리이므로 lazy 적용에 구간 길이를 곱하지 않는다(합 트리와 다름).

class MyCalendarThree:
    """LeetCode #732 시그니처. 접근 A: 차분 + 스위핑."""

    def __init__(self):
        self.delta = {}                             # 시각 -> 증감량

    def book(self, startTime, endTime):
        self.delta[startTime] = self.delta.get(startTime, 0) + 1
        self.delta[endTime] = self.delta.get(endTime, 0) - 1    # 반열린 구간!
        cur = best = 0
        for t in sorted(self.delta):
            cur += self.delta[t]
            if cur > best:
                best = cur
        return best


class MyCalendarThreeSeg:
    """접근 B: 동적 지연 전파 세그먼트 트리 (좌표 압축 불필요)."""

    LIMIT = 10 ** 9

    def __init__(self):
        self.tree = {}                              # node -> 서브트리 최댓값
        self.lazy = {}                              # node -> 아직 밀지 않은 +add

    def book(self, startTime, endTime):
        self._add(1, 0, self.LIMIT, startTime, endTime)
        return self.tree.get(1, 0)                  # 뿌리 = 전체 최댓값

    def _add(self, node, lo, hi, l, r):
        if r <= lo or hi <= l:                      # 완전히 벗어남
            return
        if l <= lo and hi <= r:                     # 완전 포함 -> 여기서 멈춘다
            self.tree[node] = self.tree.get(node, 0) + 1
            self.lazy[node] = self.lazy.get(node, 0) + 1   # 길이를 곱하지 않는다
            return
        mid = (lo + hi) // 2
        self._add(2 * node, lo, mid, l, r)
        self._add(2 * node + 1, mid, hi, l, r)
        # 뿌리만 조회하므로 push_down 없이 lazy 를 더해 올리면 충분하다
        self.tree[node] = (max(self.tree.get(2 * node, 0),
                               self.tree.get(2 * node + 1, 0))
                           + self.lazy.get(node, 0))


def brute_max_overlap(events):
    """검증용: 모든 시작 경계에서 겹침 수를 직접 세어 최댓값."""
    best = 0
    for p in sorted(set(s for s, _ in events)):
        cnt = sum(1 for s, e in events if s <= p < e)
        if cnt > best:
            best = cnt
    return best


def test_732():
    print("=" * 70)
    print("6. LeetCode #732 My Calendar III (구간 갱신 + 전체 최댓값)")
    print("=" * 70)

    official = [(10, 20, 1), (50, 60, 1), (10, 40, 2),
                (5, 15, 3), (5, 10, 3), (25, 55, 3)]
    for cls in (MyCalendarThree, MyCalendarThreeSeg):
        cal = cls()
        got = [cal.book(s, e) for s, e, _ in official]
        want = [w for _, _, w in official]
        assert got == want, (cls.__name__, got, want)
    print("공식 예제 통과 (두 구현 모두):", [w for _, _, w in official])

    for cls in (MyCalendarThree, MyCalendarThreeSeg):   # 반열린 구간 경계
        cal = cls()
        assert cal.book(5, 10) == 1
        assert cal.book(10, 20) == 1                    # 맞닿아도 겹치지 않는다
    print("반열린 경계  : book(5,10) 뒤 book(10,20) -> 1")
    print("               (닫힌 구간으로 착각하면 2 로 오답)")

    random.seed(732)
    for _ in range(200):                            # 3중 교차 검증
        m = random.randint(1, 18)
        events = []
        sweep = MyCalendarThree()
        seg = MyCalendarThreeSeg()
        for _ in range(m):
            s = random.randint(0, 30)
            e = random.randint(s + 1, 31)
            events.append((s, e))
            want = brute_max_overlap(events)
            assert sweep.book(s, e) == want, (events, want)
            assert seg.book(s, e) == want, (events, want)
    print("무작위 200회 3중 교차 검증(스위핑 / 동적 lazy / 브루트) 통과 -> O")

    calls = 400                                     # 문제 최대 제약
    random.seed(7320)
    plan = []
    for _ in range(calls):
        s = random.randint(0, 10 ** 9 - 2)
        plan.append((s, random.randint(s + 1, 10 ** 9)))

    t0 = time.perf_counter()
    cal = MyCalendarThree()
    last_sweep = 0
    for s, e in plan:
        last_sweep = cal.book(s, e)
    t_sweep = time.perf_counter() - t0

    t0 = time.perf_counter()
    cal = MyCalendarThreeSeg()
    last_seg = 0
    for s, e in plan:
        last_seg = cal.book(s, e)
    t_seg = time.perf_counter() - t0

    assert last_sweep == last_seg
    print("실측 호출 %d회, 시각 범위 0..1e9 (최종 답 일치: %d)"
          % (calls, last_sweep))
    print("  차분 스위핑    : %7.4f 초  (호출당 O(N log N))" % t_sweep)
    print("  동적 lazy 세그 : %7.4f 초  (호출당 O(log 1e9))" % t_seg)
    print("교훈: 제약이 작으면(호출 400회) 단순한 스위핑이 정답이다.")
    print("      호출이 10만 번으로 늘면 세그먼트 트리 쪽만 살아남는다.")
    print()


# ==========================================================================
def main():
    test_303()
    test_307()
    test_315()
    test_64062()
    test_493()
    test_732()

    print("=" * 70)
    print("전체 정리 - 오늘의 판단 기준")
    print("=" * 70)
    print("#303   갱신 없음               -> 누적 합 (질의 O(1))")
    print("#307   갱신+질의, 합           -> BIT (세그트리보다 짧고 빠름)")
    print("#315   오른쪽의 더 작은 수     -> 값의 축 + 좌표 압축 + BIT")
    print("#64062 윈도우 최댓값들의 최솟값 -> 덱 O(N) (세그트리는 O(N log N))")
    print("#493   역순 쌍                 -> #315 골격 + doubled 로 경계 계산")
    print("#732   구간 갱신 + 전체 최댓값 -> 제약 작으면 스위핑, 크면 동적 lazy")
    print()
    print("반복 실수 체크리스트")
    print("  X BIT 를 0-based 로 쓴다          -> i & -i == 0 무한 루프")
    print("  X min 트리 항등원을 0 으로 둔다   -> 모든 답이 0")
    print("  X BIT add 에 값을 그대로 넣는다   -> 증분(delta)으로 환산해야 한다")
    print("  X 2*v < x 를 x // 2 로 판정한다   -> 음수에서 틀린다")
    print("  X lazy 를 query 에서 push 안 한다 -> 옛 값을 읽는다")
    print("  X 반열린/닫힌 구간을 섞어 쓴다    -> off-by-one")
    print()
    print("모든 문제 assert 통과 -> O")


if __name__ == "__main__":
    main()
