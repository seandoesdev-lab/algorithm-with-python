"""Day 40 - 세그먼트 트리·펜윅 트리 (Segment Tree & Fenwick/BIT) 예제 모음.

실행: PYTHONIOENCODING=cp949 python examples.py

구성
  1. 반복형 세그먼트 트리 (합/최솟값/최댓값/GCD) + 브루트포스 교차 검증
  2. 펜윅 트리(BIT): O(N) 구축, prefix/구간 합 + 교차 검증
  3. BIT 로는 왜 일반 구간 최솟값을 못 구하는가
  4. 값의 축 + 좌표 압축: 오른쪽의 더 작은 수 개수 (LeetCode #315 골격)
  5. 지연 전파(lazy propagation): 구간 +add / 구간 합 + 교차 검증
  6. 세그먼트 트리 하강(descent): 누적 합이 처음 k 이상인 위치를 O(log N)
  7. 성능 비교: 누적 합 재구축 vs 세그먼트 트리 vs BIT
  8. 고정 길이 윈도우 최댓값: 덱 O(N) vs 세그먼트 트리 O(N log N)

주의(cp949 콘솔 안전): 출력 문자열에는 ASCII 기호(=, -, O, X)만 쓴다.
"""

import random
import time
from bisect import bisect_left
from collections import deque
from math import gcd


# ==========================================================================
# 1. 반복형 세그먼트 트리 (iterative segment tree)
# ==========================================================================

class SegTree:
    """반열린 구간 [l, r) 규약. 잎을 tree[n..2n-1] 에 배치하는 반복형.

    f 는 결합법칙을 만족해야 한다. 이 반복형은 임의의 n 에 대해
    '교환법칙까지 있는' 연산(합/min/max/gcd/xor)에서 항상 옳다.
    행렬곱처럼 교환법칙이 없는 연산을 얹으려면 n 을 2의 거듭제곱으로
    패딩해야 한다(잎이 순환 이동되어 좌우 순서가 어긋날 수 있다).
    """

    def __init__(self, data, func=None, identity=0):
        self.n = len(data)
        self.f = func if func is not None else (lambda a, b: a + b)
        self.e = identity
        self.tree = [identity] * (2 * self.n)
        self.tree[self.n:] = data                       # 잎을 깐다
        for i in range(self.n - 1, 0, -1):              # 역순 1패스 -> O(N)
            self.tree[i] = self.f(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i, value):
        """A[i] = value, O(log N). 잎에서 뿌리까지 경로만 재계산."""
        i += self.n
        self.tree[i] = value
        i >>= 1
        while i:
            self.tree[i] = self.f(self.tree[2 * i], self.tree[2 * i + 1])
            i >>= 1

    def query(self, l, r):
        """f(A[l..r-1]), O(log N). l >= r 이면 항등원."""
        res_l = res_r = self.e
        l += self.n
        r += self.n
        while l < r:
            if l & 1:                                   # l 이 오른쪽 자식
                res_l = self.f(res_l, self.tree[l])
                l += 1
            if r & 1:                                   # r 이 오른쪽 자식
                r -= 1
                res_r = self.f(self.tree[r], res_r)
            l >>= 1
            r >>= 1
        return self.f(res_l, res_r)

    def get(self, i):
        return self.tree[i + self.n]


def demo_segment_tree():
    print("=" * 70)
    print("1. 반복형 세그먼트 트리: 합 / 최솟값 / 최댓값 / GCD")
    print("=" * 70)

    a = [5, 3, 7, 1, 4, 2]
    seg_sum = SegTree(a)
    seg_min = SegTree(a, min, float('inf'))
    seg_max = SegTree(a, max, float('-inf'))
    seg_gcd = SegTree([12, 18, 24, 9], gcd, 0)          # gcd 항등원은 0

    print("배열 A         :", a)
    print("내부 tree 배열 :", seg_sum.tree, "  (tree[1]=뿌리=전체 합)")
    print()
    print("query(1, 5) 합      =", seg_sum.query(1, 5), " (기대 3+7+1+4 = 15)")
    print("query(0, 6) 합      =", seg_sum.query(0, 6), " (기대 22)")
    print("query(2, 3) 합      =", seg_sum.query(2, 3), " (기대 7, 원소 하나)")
    print("query(3, 3) 합      =", seg_sum.query(3, 3), " (기대 0, 빈 구간=항등원)")
    print("query(1, 5) 최솟값  =", seg_min.query(1, 5), " (기대 1)")
    print("query(0, 3) 최댓값  =", seg_max.query(0, 3), " (기대 7)")
    print("GCD 트리 [12,18,24,9] query(0,3) =", seg_gcd.query(0, 3), "(기대 6)")
    print()

    print("update(4, 9): A[4] 를 4 -> 9 로 (경로 log N 개만 고쳐진다)")
    seg_sum.update(4, 9)
    print("  갱신 후 tree :", seg_sum.tree)
    print("  query(0, 6)  =", seg_sum.query(0, 6), " (기대 22-4+9 = 27)")
    print("  query(3, 5)  =", seg_sum.query(3, 5), " (기대 1+9 = 10)")
    print()

    print("[항등원 함정] 최솟값 트리에 항등원 0 을 쓰면?")
    bad = SegTree(a, min, 0)                            # 잘못된 항등원
    print("  잘못된 트리 query(1, 5) =", bad.query(1, 5),
          " <- 0 으로 오염됨 (정답 1)")
    print("  X 최솟값 항등원은 inf, 최댓값은 -inf, gcd 는 0, and 는 -1")
    print()


def verify_segment_tree(trials=300):
    """무작위 연산을 브루트포스와 교차 검증."""
    print("=" * 70)
    print("1-b. 세그먼트 트리 무작위 교차 검증 (브루트포스 대조)")
    print("=" * 70)
    random.seed(40)
    ok_sum = ok_min = 0
    for _ in range(trials):
        n = random.randint(1, 30)                       # 2의 거듭제곱이 아닌 n 포함
        a = [random.randint(-50, 50) for _ in range(n)]
        seg_s = SegTree(list(a))
        seg_m = SegTree(list(a), min, float('inf'))
        for _ in range(20):
            if random.random() < 0.4:                   # 갱신
                i = random.randrange(n)
                v = random.randint(-50, 50)
                a[i] = v
                seg_s.update(i, v)
                seg_m.update(i, v)
            else:                                       # 질의
                l = random.randrange(n)
                r = random.randint(l + 1, n)
                assert seg_s.query(l, r) == sum(a[l:r]), (a, l, r)
                ok_sum += 1
                assert seg_m.query(l, r) == min(a[l:r]), (a, l, r)
                ok_min += 1
    print("합 질의 %d건, 최솟값 질의 %d건 모두 일치 -> O" % (ok_sum, ok_min))
    print("  (n 이 2의 거듭제곱이 아닌 경우도 포함해 검증했다)")
    print()


# ==========================================================================
# 2. 펜윅 트리 (Fenwick tree / BIT)
# ==========================================================================

class BIT:
    """합 전용. 1-based 인덱스 강제 (i=0 이면 i & -i == 0 -> 무한 루프)."""

    def __init__(self, n, data=None):
        self.n = n
        self.tree = [0] * (n + 1)
        if data is not None:                            # O(N) 구축
            for i in range(1, n + 1):
                self.tree[i] += data[i - 1]
                parent = i + (i & -i)
                if parent <= n:
                    self.tree[parent] += self.tree[i]

    def add(self, i, delta):
        """A[i] += delta (i 는 1-based), O(log N)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i                                 # 나를 포함하는 상위 구간으로

    def prefix(self, i):
        """A[1..i] 의 합, O(log N). i=0 이면 0."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i                                 # 최하위 1비트를 떼며 왼쪽으로
        return s

    def range_sum(self, l, r):
        """A[l..r] 닫힌 구간. 뺄셈(역원)이 있어야 가능하다."""
        return self.prefix(r) - self.prefix(l - 1)


def demo_bit():
    print("=" * 70)
    print("2. 펜윅 트리(BIT): i & -i 가 전부다")
    print("=" * 70)

    print("i 와 i & -i (최하위 1비트) 대응표")
    print("  i      :", "  ".join("%2d" % i for i in range(1, 13)))
    print("  i & -i :", "  ".join("%2d" % (i & -i) for i in range(1, 13)))
    print("  -> tree[i] 는 [i-(i&-i)+1 .. i] 구간의 합을 담는다")
    print()
    print("2의 보수라서 최하위 1비트가 남는다: 12 = 0b1100")
    print("  12 & -12 =", 12 & -12, " (0b100 = 4)")
    print("  10 & -10 =", 10 & -10, " (0b10  = 2)")
    print("  16 & -16 =", 16 & -16, " (0b10000)")
    print()

    a = [5, 3, 7, 1, 4, 2, 9, 6]
    bit = BIT(len(a), a)                                # O(N) 구축
    print("배열 A (1-based) :", a)
    print("BIT 내부 tree    :", bit.tree[1:])
    print("prefix(4)        =", bit.prefix(4), " (기대 5+3+7+1 = 16)")
    print("prefix(7)        =", bit.prefix(7), " (기대 31)")
    print("range_sum(3, 6)  =", bit.range_sum(3, 6), " (기대 7+1+4+2 = 14)")
    print()
    print("add(3, +10): A[3] 을 7 -> 17 로")
    bit.add(3, 10)
    print("  range_sum(3, 6) =", bit.range_sum(3, 6), " (기대 24)")
    print("  prefix(8)       =", bit.prefix(8), " (기대 37+10 = 47)")
    print()


def verify_bit(trials=300):
    print("=" * 70)
    print("2-b. BIT 무작위 교차 검증")
    print("=" * 70)
    random.seed(4040)
    checked = 0
    for _ in range(trials):
        n = random.randint(1, 40)
        a = [random.randint(-30, 30) for _ in range(n)]
        bit = BIT(n, a)
        for _ in range(20):
            if random.random() < 0.4:
                i = random.randrange(n)
                d = random.randint(-30, 30)
                a[i] += d
                bit.add(i + 1, d)                       # 0-based -> 1-based
            else:
                l = random.randrange(n)
                r = random.randint(l, n - 1)
                assert bit.range_sum(l + 1, r + 1) == sum(a[l:r + 1])
                checked += 1
    print("구간 합 질의 %d건 모두 일치 -> O" % checked)
    print()


# ==========================================================================
# 3. BIT 로 일반 구간 최솟값을 못 구하는 이유
# ==========================================================================

def demo_bit_cannot_min():
    print("=" * 70)
    print("3. BIT 로 일반 구간 최솟값은 불가 (역원이 없다)")
    print("=" * 70)
    a = [5, 3, 7, 1, 4, 2]
    print("A =", a)
    print("prefix_min(A[1..6]) =", min(a),
          "   prefix_min(A[1..3]) =", min(a[:3]))
    print("이 둘로 min(A[4..6]) 을 복원할 수 있는가?")
    print("  실제 min(A[4..6]) =", min(a[3:]))
    print("  덧셈이라면 sum(1..6) - sum(1..3) 으로 되지만,")
    print("  max/min 에는 '뺄셈'에 해당하는 역원이 없어 복원 불가.")
    print()
    b = [1, 5, 9]
    c = [1, 6, 9]
    print("반례: prefix_min 이 모든 지점에서 완전히 같은 두 배열")
    print("  B =", b, " prefix_min 들 =", [min(b[:i + 1]) for i in range(3)])
    print("  C =", c, " prefix_min 들 =", [min(c[:i + 1]) for i in range(3)])
    print("  prefix_min 수열이 동일:",
          [min(b[:i + 1]) for i in range(3)] == [min(c[:i + 1]) for i in range(3)])
    print("  그런데 min(B[2..3]) =", min(b[1:]), " vs min(C[2..3]) =", min(c[1:]),
          " <- 다르다!")
    print("  X prefix 정보만으로는 구별 불가 -> 일반 구간 min 은 세그먼트 트리로")
    print()


# ==========================================================================
# 4. 값의 축 + 좌표 압축 (LeetCode #315 골격)
# ==========================================================================

def count_smaller_bit(nums):
    """nums[i] 오른쪽에 있는 더 작은 수의 개수. O(N log N)."""
    comp = sorted(set(nums))                            # 좌표 압축
    bit = BIT(len(comp))
    out = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):              # 오른쪽 -> 왼쪽
        rank = bisect_left(comp, nums[i]) + 1           # 1-based rank
        out[i] = bit.prefix(rank - 1)                   # 나보다 작은 것의 개수
        bit.add(rank, 1)                                # 나를 등록
    return out


def count_smaller_brute(nums):
    n = len(nums)
    return [sum(1 for j in range(i + 1, n) if nums[j] < nums[i]) for i in range(n)]


def demo_value_axis():
    print("=" * 70)
    print("4. 값의 축 + 좌표 압축: 오른쪽의 더 작은 수 개수")
    print("=" * 70)
    nums = [5, 2, 6, 1]
    comp = sorted(set(nums))
    print("nums =", nums)
    print("압축 comp =", comp, " -> rank(1-based):",
          dict((v, i + 1) for i, v in enumerate(comp)))
    print()
    print("오른쪽에서 왼쪽으로 진행하며 '이미 본 수'를 값의 축에 표시:")
    bit = BIT(len(comp))
    seen = []
    for i in range(len(nums) - 1, -1, -1):
        rank = bisect_left(comp, nums[i]) + 1
        cnt = bit.prefix(rank - 1)
        print("  i=%d x=%d(rank%d)  prefix(%d)=%d   이미 본 것=%s"
              % (i, nums[i], rank, rank - 1, cnt, sorted(seen)))
        bit.add(rank, 1)
        seen.append(nums[i])
    print()
    print("BIT   결과 :", count_smaller_bit(nums))
    print("브루트 결과:", count_smaller_brute(nums), " (기대 [2,1,1,0])")
    print()

    print("음수·중복·큰 값이 섞여도 압축으로 안전:")
    tricky = [10 ** 9, -10 ** 9, 0, 0, -5, 10 ** 9]
    print("  입력  :", tricky)
    print("  BIT   :", count_smaller_bit(tricky))
    print("  브루트:", count_smaller_brute(tricky))
    print("  (값 범위가 20억이어도 BIT 크기는 서로 다른 값의 개수 %d 뿐)"
          % len(set(tricky)))
    print()

    random.seed(315)
    for _ in range(200):
        n = random.randint(1, 40)
        arr = [random.randint(-20, 20) for _ in range(n)]
        assert count_smaller_bit(arr) == count_smaller_brute(arr), arr
    print("무작위 200회 교차 검증 통과 -> O")
    print()


# ==========================================================================
# 5. 지연 전파 (lazy propagation)
# ==========================================================================

class LazySeg:
    """구간 +add / 구간 합. 재귀형, 배열 크기 4N. 반열린 구간 [l, r)."""

    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n)

    def _build(self, a, node, lo, hi):
        if hi - lo == 1:
            self.tree[node] = a[lo]
            return
        mid = (lo + hi) // 2
        self._build(a, 2 * node, lo, mid)
        self._build(a, 2 * node + 1, mid, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def _push(self, node, lo, hi):
        """빚(lazy)을 자식에게 밀어준다. 자식을 볼 일이 생겼을 때만 호출."""
        v = self.lazy[node]
        if v == 0:
            return
        mid = (lo + hi) // 2
        for child, length in ((2 * node, mid - lo), (2 * node + 1, hi - mid)):
            self.tree[child] += v * length               # 합 트리 -> 길이를 곱한다
            self.lazy[child] += v
        self.lazy[node] = 0

    def add_range(self, l, r, v, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n
        if r <= lo or hi <= l:                          # 완전히 벗어남
            return
        if l <= lo and hi <= r:                         # 완전 포함 -> 여기서 멈춘다
            self.tree[node] += v * (hi - lo)
            self.lazy[node] += v
            return
        self._push(node, lo, hi)
        mid = (lo + hi) // 2
        self.add_range(l, r, v, 2 * node, lo, mid)
        self.add_range(l, r, v, 2 * node + 1, mid, hi)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def sum_range(self, l, r, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n
        if r <= lo or hi <= l:
            return 0                                    # 항등원
        if l <= lo and hi <= r:
            return self.tree[node]
        self._push(node, lo, hi)                        # 질의에서도 push 필수!
        mid = (lo + hi) // 2
        return (self.sum_range(l, r, 2 * node, lo, mid)
                + self.sum_range(l, r, 2 * node + 1, mid, hi))


def demo_lazy():
    print("=" * 70)
    print("5. 지연 전파: 구간 갱신도 O(log N)")
    print("=" * 70)
    a = [1, 2, 3, 4, 5, 6]
    seg = LazySeg(a)
    print("A =", a)
    print("sum_range(0, 6) =", seg.sum_range(0, 6), " (기대 21)")
    print()
    print("add_range(1, 4, +10): A[1..3] 에 각각 +10")
    seg.add_range(1, 4, 10)
    print("  sum_range(0, 6) =", seg.sum_range(0, 6), " (기대 21+30 = 51)")
    print("  sum_range(1, 4) =", seg.sum_range(1, 4), " (기대 2+3+4+30 = 39)")
    print("  sum_range(0, 2) =", seg.sum_range(0, 2), " (기대 1+12 = 13)")
    print("  sum_range(4, 6) =", seg.sum_range(4, 6), " (기대 11)")
    print()
    print("add_range(0, 6, +1) 후 개별 원소 확인:")
    seg.add_range(0, 6, 1)
    vals = [seg.sum_range(i, i + 1) for i in range(6)]
    print("  현재 A =", vals, " (기대 [2,13,14,15,6,7])")
    print()

    random.seed(732)
    checked = 0
    for _ in range(200):
        n = random.randint(1, 25)
        arr = [random.randint(-20, 20) for _ in range(n)]
        lz = LazySeg(list(arr))
        for _ in range(25):
            l = random.randrange(n)
            r = random.randint(l + 1, n)
            if random.random() < 0.5:
                v = random.randint(-15, 15)
                for i in range(l, r):
                    arr[i] += v
                lz.add_range(l, r, v)
            else:
                assert lz.sum_range(l, r) == sum(arr[l:r]), (arr, l, r)
                checked += 1
    print("무작위 구간 갱신/질의 %d건 교차 검증 통과 -> O" % checked)
    print()


# ==========================================================================
# 6. 세그먼트 트리 하강 (descent)
# ==========================================================================

def build_pow2_sum_tree(counts):
    """하강(descent)을 쓰려면 트리가 완전 이진이어야 하므로 2의 거듭제곱 패딩."""
    size = 1
    while size < len(counts):
        size <<= 1
    return SegTree(list(counts) + [0] * (size - len(counts)))


def find_kth(seg, k):
    """누적 합이 처음 k 이상이 되는 최소 인덱스. O(log N) (log^2 아님)."""
    node = 1
    while node < seg.n:
        left = 2 * node
        if seg.tree[left] >= k:
            node = left                                 # 왼쪽에 답이 있다
        else:
            k -= seg.tree[left]                         # 왼쪽을 다 쓰고 오른쪽으로
            node = left + 1
    return node - seg.n


def demo_descent():
    print("=" * 70)
    print("6. 세그먼트 트리 하강: k번째 원소를 O(log N) 에 찾기")
    print("=" * 70)
    counts = [0, 1, 0, 2, 1]        # 값 v 가 counts[v] 개 존재 (멀티셋)
    seg = build_pow2_sum_tree(counts)
    print("counts =", counts, "  (인덱스=값, 값=개수)")
    print("  -> 멀티셋 = [1, 3, 3, 4]")
    print("패딩 후 트리 잎 개수 n =", seg.n)
    for k in range(1, 5):
        print("  find_kth(%d) = 인덱스 %d" % (k, find_kth(seg, k)))
    print("  (기대: 1, 3, 3, 4)")
    print()
    print("삽입/삭제와 섞어 쓸 수 있다 -> '순서 통계 트리' 대용")
    seg.update(0, seg.get(0) + 1)                       # 값 0 을 하나 추가
    print("  값 0 추가 후 find_kth(1) =", find_kth(seg, 1), " (기대 0)")
    print()

    random.seed(6)
    trials = 0
    for _ in range(200):
        m = random.randint(1, 20)
        cnt = [random.randint(0, 3) for _ in range(m)]
        total = sum(cnt)
        if total == 0:
            continue
        flat = [v for v, c in enumerate(cnt) for _ in range(c)]
        st = build_pow2_sum_tree(cnt)
        for k in range(1, total + 1):
            assert find_kth(st, k) == flat[k - 1], (cnt, k)
        trials += 1
    print("무작위 %d회 하강 결과 교차 검증 통과 -> O" % trials)
    print()


# ==========================================================================
# 7. 성능 비교
# ==========================================================================

def make_ops(n, ops, seed):
    random.seed(seed)
    base = [random.randint(1, 100) for _ in range(n)]
    queries = []
    for _ in range(ops):
        if random.random() < 0.5:
            queries.append(('u', random.randrange(n), random.randint(1, 100)))
        else:
            l = random.randrange(n)
            queries.append(('q', l, random.randint(l + 1, n)))
    return base, queries


def demo_performance():
    print("=" * 70)
    print("7. 성능 비교: 누적 합 재구축 vs 세그먼트 트리 vs BIT")
    print("=" * 70)

    # (a) 작은 규모: 누적 합 재구축까지 포함해 비교
    n, ops = 3000, 3000
    base, queries = make_ops(n, ops, 7)

    a = list(base)                                      # 누적 합: 갱신마다 O(N)
    t0 = time.perf_counter()
    pref = [0] * (n + 1)
    for i, v in enumerate(a):
        pref[i + 1] = pref[i] + v
    checksum_pref = 0
    for kind, x, y in queries:
        if kind == 'u':
            a[x] = y
            pref = [0] * (n + 1)                        # 전체 재구축
            for i, v in enumerate(a):
                pref[i + 1] = pref[i] + v
        else:
            checksum_pref += pref[y] - pref[x]
    t_pref = time.perf_counter() - t0

    t0 = time.perf_counter()                            # 세그먼트 트리
    seg = SegTree(list(base))
    checksum_seg = 0
    for kind, x, y in queries:
        if kind == 'u':
            seg.update(x, y)
        else:
            checksum_seg += seg.query(x, y)
    t_seg = time.perf_counter() - t0

    t0 = time.perf_counter()                            # BIT (증분으로 환산)
    bit = BIT(n, base)
    cur = list(base)
    checksum_bit = 0
    for kind, x, y in queries:
        if kind == 'u':
            bit.add(x + 1, y - cur[x])                  # 값 지정 -> 증분
            cur[x] = y
        else:
            checksum_bit += bit.range_sum(x + 1, y)     # [x, y) -> [x+1, y]
    t_bit = time.perf_counter() - t0

    assert checksum_pref == checksum_seg == checksum_bit
    print("N=%d, 연산 %d회 (갱신/질의 반반). 세 방식 체크섬 일치 -> O" % (n, ops))
    print("  누적 합 재구축 : %8.4f 초   (갱신마다 O(N))" % t_pref)
    print("  세그먼트 트리  : %8.4f 초   (둘 다 O(log N))" % t_seg)
    print("  BIT            : %8.4f 초   (상수가 가장 작다)" % t_bit)
    if t_bit > 0:
        print("  -> 누적 합 대비 BIT 는 약 %.1f배 빠름" % (t_pref / t_bit))
    print()

    # (b) 큰 규모: 누적 합 재구축은 아예 돌릴 수 없다
    n, ops = 200000, 200000
    base, queries = make_ops(n, ops, 77)

    t0 = time.perf_counter()
    seg = SegTree(list(base))
    s1 = 0
    for kind, x, y in queries:
        if kind == 'u':
            seg.update(x, y)
        else:
            s1 += seg.query(x, y)
    t_seg = time.perf_counter() - t0

    t0 = time.perf_counter()
    bit = BIT(n, base)
    cur = list(base)
    s2 = 0
    for kind, x, y in queries:
        if kind == 'u':
            bit.add(x + 1, y - cur[x])
            cur[x] = y
        else:
            s2 += bit.range_sum(x + 1, y)
    t_bit = time.perf_counter() - t0

    assert s1 == s2
    print("N=%d, 연산 %d회 (누적 합 재구축이면 약 %.1e 연산 -> TLE)"
          % (n, ops, n * ops / 2))
    print("  세그먼트 트리  : %8.4f 초" % t_seg)
    print("  BIT            : %8.4f 초" % t_bit)
    print("  -> 같은 O(log N) 이지만 BIT 상수가 작아 실전에서 더 빠르다")
    print()


# ==========================================================================
# 8. 고정 길이 윈도우 최솟값: 덱 vs 세그먼트 트리
# ==========================================================================

def window_max_deque(a, k):
    """길이 k 윈도우들의 최댓값 목록. O(N)."""
    dq = deque()                                        # 값이 감소하는 인덱스 덱
    out = []
    for i, v in enumerate(a):
        while dq and a[dq[-1]] <= v:
            dq.pop()                                    # 나보다 작으면 쓸모없다
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                                # 윈도우 밖으로 나갔다
        if i >= k - 1:
            out.append(a[dq[0]])
    return out


def window_max_segtree(a, k):
    """같은 결과를 세그먼트 트리 구간 최댓값으로. O(N log N)."""
    seg = SegTree(list(a), max, float('-inf'))
    return [seg.query(i, i + k) for i in range(len(a) - k + 1)]


def demo_window_max():
    print("=" * 70)
    print("8. 고정 길이 윈도우 최댓값: 덱 O(N) vs 세그먼트 트리 O(N log N)")
    print("=" * 70)
    stones = [2, 4, 5, 3, 2, 1, 4, 2, 5, 1]
    k = 3
    print("stones =", stones, ", k =", k)
    print("  덱      :", window_max_deque(stones, k))
    print("  세그트리:", window_max_segtree(stones, k))
    print("  그중 최솟값(= 징검다리 건너기 답) =",
          min(window_max_deque(stones, k)), " (기대 3)")
    print("  근거: x명이 실패 <=> 연속 k개가 모두 x 미만")
    print("        <=> 어떤 윈도우의 최댓값 < x")
    print("        => 답 = min(윈도우 최댓값들)")
    print()

    random.seed(64062)
    for _ in range(300):
        n = random.randint(1, 40)
        arr = [random.randint(1, 50) for _ in range(n)]
        kk = random.randint(1, n)
        brute = [max(arr[i:i + kk]) for i in range(n - kk + 1)]
        assert window_max_deque(arr, kk) == brute, (arr, kk)
        assert window_max_segtree(arr, kk) == brute, (arr, kk)
    print("무작위 300회 교차 검증(덱 / 세그트리 / 브루트포스) 통과 -> O")
    print()

    n = 200000
    random.seed(8)
    big = [random.randint(1, 10 ** 8) for _ in range(n)]
    kk = 1000
    t0 = time.perf_counter()
    r1 = window_max_deque(big, kk)
    t_dq = time.perf_counter() - t0
    t0 = time.perf_counter()
    r2 = window_max_segtree(big, kk)
    t_sg = time.perf_counter() - t0
    assert r1 == r2
    print("N=%d, k=%d 실측 (두 결과 동일)" % (n, kk))
    print("  덱       : %8.4f 초  (O(N))" % t_dq)
    print("  세그트리 : %8.4f 초  (O(N log N))" % t_sg)
    print("  -> 세그먼트 트리는 만능이지만 최적은 아니다.")
    print("     고정 길이 윈도우 min/max 는 덱이 정답이다.")
    print()


def main():
    demo_segment_tree()
    verify_segment_tree()
    demo_bit()
    verify_bit()
    demo_bit_cannot_min()
    demo_value_axis()
    demo_lazy()
    demo_descent()
    demo_performance()
    demo_window_max()
    print("=" * 70)
    print("정리: 5단계 결정 트리")
    print("=" * 70)
    print("1) 갱신이 없다        -> 누적 합 / 스파스 테이블")
    print("2) 질의가 마지막에만  -> 차분 배열")
    print("3) 갱신+질의 섞임, 합 -> BIT (코드 최단, 가장 빠름)")
    print("4) min/max/gcd        -> 세그먼트 트리 (항등원 주의!)")
    print("5) 구간 전체 갱신     -> 지연 전파 (query 에서도 push 필수)")
    print("보너스) 순서/역순 쌍 세기 -> 값의 축 + 좌표 압축 + BIT")


if __name__ == "__main__":
    main()
