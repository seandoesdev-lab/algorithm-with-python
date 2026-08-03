"""Day 41 - 비트마스킹 (Bitmasking & Bitmask DP) 예제 모음.

실행: PYTHONIOENCODING=cp949 python examples.py
표준 라이브러리만 사용한다. (cp949 콘솔 안전: 출력에 ASCII 기호만 사용)

구성
  1. 기본 비트 연산과 원소 조작 관용구
  2. 집합 연산 대응 (set <-> mask 교차 검증)
  3. popcount 3종과 성능 비교
  4. 부분집합 전체 열거 (itertools 교차 검증)
  5. 부분집합 합 사전계산 O(2^n)
  6. 서브마스크 열거와 3^n 검증
  7. Gosper's hack (정확히 k개 원소 부분집합)
  8. 비트 DP: 외판원 순회 TSP (순열 브루트포스 교차 검증)
  9. 비트마스크 + BFS: 모든 노드 방문 최단 보행
 10. 자리별 독립 계산: 모든 부분집합 XOR 총합
 11. 큰 정수를 비트셋으로: 부분집합 합 가능 여부
 12. 파이썬 정수의 함정 실증
"""

import random
import time
from collections import deque
from itertools import combinations, permutations


SEP = "=" * 68
SUB = "-" * 68


# ---------------------------------------------------------------------------
# 1. 기본 비트 연산과 원소 조작 관용구
# ---------------------------------------------------------------------------
def bit_test(mask, i):
    """i 번 비트를 0/1 로 정규화해 읽는다."""
    return (mask >> i) & 1


def bit_set(mask, i):
    return mask | (1 << i)


def bit_clear(mask, i):
    return mask & ~(1 << i)


def bit_toggle(mask, i):
    return mask ^ (1 << i)


def full_mask(n):
    """전체집합. (1 << n) - 1 의 괄호는 필수 (1 << n-1 은 전혀 다른 값)."""
    return (1 << n) - 1


def mask_to_set(mask, n):
    return {i for i in range(n) if mask >> i & 1}


def set_to_mask(s):
    m = 0
    for i in s:
        m |= 1 << i
    return m


def demo_basics():
    print(SEP)
    print("1. 기본 비트 연산과 원소 조작")
    print(SEP)

    a, b = 0b1100, 0b1010
    print("a = 0b1100 = %d,  b = 0b1010 = %d" % (a, b))
    print("  a & b  = %-4d (0b%s)   교집합" % (a & b, format(a & b, "04b")))
    print("  a | b  = %-4d (0b%s)   합집합" % (a | b, format(a | b, "04b")))
    print("  a ^ b  = %-4d (0b%s)   대칭차" % (a ^ b, format(a ^ b, "04b")))
    print("  ~a     = %-4d          파이썬은 음수! (~x == -x-1)" % (~a,))
    print("  a << 2 = %-4d          x * 2^2" % (a << 2,))
    print("  a >> 2 = %-4d          x // 2^2" % (a >> 2,))

    print(SUB)
    n = 5
    mask = 0b10110  # = 22, S = {1,2,4}
    print("mask = %d = 0b%s  ->  S = %s"
          % (mask, format(mask, "05b"), sorted(mask_to_set(mask, n))))
    print("  bit_test(mask, 3)   = %d   (3 은 포함 안 됨)" % bit_test(mask, 3))
    print("  bit_set(mask, 3)    = %d = 0b%s"
          % (bit_set(mask, 3), format(bit_set(mask, 3), "05b")))
    print("  bit_clear(mask, 1)  = %d = 0b%s"
          % (bit_clear(mask, 1), format(bit_clear(mask, 1), "05b")))
    print("  bit_toggle(mask, 0) = %d = 0b%s"
          % (bit_toggle(mask, 0), format(bit_toggle(mask, 0), "05b")))
    print("  full_mask(5)        = %d = 0b%s"
          % (full_mask(5), format(full_mask(5), "05b")))

    print(SUB)
    print("흔한 실수: mask & (1 << i) 의 값은 0 또는 2^i 이지 0/1 이 아니다")
    for i in range(3):
        raw = mask & (1 << i)
        norm = mask >> i & 1
        print("  i=%d  mask & (1<<i) = %-2d   (mask >> i) & 1 = %d" % (i, raw, norm))
    print("  -> 'if mask & (1<<i):' 로 쓰거나 (mask >> i) & 1 로 정규화하라")

    print(SUB)
    print("XOR 로 '짝 없는 하나' 찾기  (x ^ x = 0, x ^ 0 = x)")
    arr = [4, 1, 2, 1, 2]
    acc = 0
    for x in arr:
        acc ^= x
    print("  %s  ->  %d   (O(N) 시간, O(1) 공간)" % (arr, acc))
    assert acc == 4

    print("XOR 은 '받아올림 없는 덧셈':  a + b == (a ^ b) + ((a & b) << 1)")
    for _ in range(200):
        x, y = random.randint(0, 10 ** 6), random.randint(0, 10 ** 6)
        assert x + y == (x ^ y) + ((x & y) << 1)
    print("  무작위 200쌍 검증 OK")


# ---------------------------------------------------------------------------
# 2. 집합 연산 대응 (set <-> mask 교차 검증)
# ---------------------------------------------------------------------------
def demo_set_ops():
    print()
    print(SEP)
    print("2. 집합 연산 대응: set 결과와 비트마스크 결과가 같은지 교차 검증")
    print(SEP)

    n = 8
    random.seed(41)
    trials = 2000
    for _ in range(trials):
        A = set(random.sample(range(n), random.randint(0, n)))
        B = set(random.sample(range(n), random.randint(0, n)))
        a, b = set_to_mask(A), set_to_mask(B)
        full = full_mask(n)

        assert mask_to_set(a | b, n) == (A | B)                  # 합집합
        assert mask_to_set(a & b, n) == (A & B)                  # 교집합
        assert mask_to_set(a & ~b, n) == (A - B)                 # 차집합
        assert mask_to_set(a ^ b, n) == (A ^ B)                  # 대칭차
        assert ((a & b) == a) == (A <= B)                        # 부분집합 판정
        assert mask_to_set(full ^ a, n) == (set(range(n)) - A)   # 여집합
        assert bin(a).count("1") == len(A)                       # 원소 개수
        assert (a == 0) == (len(A) == 0)                         # 공집합

    print("무작위 %d 쌍(n=%d)에 대해 8가지 대응 전부 일치: OK" % (trials, n))

    print(SUB)
    print("표로 정리")
    rows = [
        ("A | B",    "a | b",        "합집합"),
        ("A & B",    "a & b",        "교집합"),
        ("A - B",    "a & ~b",       "차집합"),
        ("A ^ B",    "a ^ b",        "대칭차"),
        ("A <= B",   "(a & b) == a", "부분집합 판정"),
        ("len(A)",   "popcount(a)",  "원소 개수"),
        ("전체집합", "(1 << n) - 1", "n 비트 전부 1"),
        ("여집합",   "full ^ a",     "~a 는 음수라 금지"),
    ]
    print("  %-12s | %-14s | %s" % ("python set", "bitmask", "의미"))
    print("  %s" % ("-" * 58))
    for x, y, z in rows:
        print("  %-12s | %-14s | %s" % (x, y, z))


# ---------------------------------------------------------------------------
# 3. popcount 3종과 성능 비교
# ---------------------------------------------------------------------------
def popcount_naive(x):
    """비트를 하나씩 확인한다. 가장 느리다."""
    cnt = 0
    while x:
        cnt += x & 1
        x >>= 1
    return cnt


def popcount_kernighan(x):
    """Brian Kernighan: 켜진 비트 수만큼만 돈다."""
    cnt = 0
    while x:
        x &= x - 1          # 최하위 1비트 제거
        cnt += 1
    return cnt


def popcount_builtin(x):
    """파이썬 3.10+ 는 int.bit_count(). 그 이전은 bin().count('1')."""
    try:
        return x.bit_count()
    except AttributeError:
        return bin(x).count("1")


def popcount_table(n):
    """0..2^n-1 전부를 O(2^n) 에 전처리한다."""
    pc = [0] * (1 << n)
    for m in range(1, 1 << n):
        pc[m] = pc[m >> 1] + (m & 1)
    return pc


def demo_popcount():
    print()
    print(SEP)
    print("3. popcount 3종 + 전처리 테이블")
    print(SEP)

    for x in (0, 1, 7, 44, 255, 1023, 2 ** 40 - 1):
        a, b, c = popcount_naive(x), popcount_kernighan(x), popcount_builtin(x)
        assert a == b == c
        print("  x = %-14d  popcount = %-3d  (naive/kernighan/builtin 일치)" % (x, a))

    n = 12
    pc = popcount_table(n)
    for m in range(1 << n):
        assert pc[m] == popcount_builtin(m)
    print("  전처리 테이블(n=%d, %d칸) 전부 일치: OK" % (n, 1 << n))

    print(SUB)
    print("성능 비교 (0 .. 2^16-1 전부 세기)")
    limit = 1 << 16
    for name, fn in (("naive      ", popcount_naive),
                     ("kernighan  ", popcount_kernighan),
                     ("builtin    ", popcount_builtin)):
        t0 = time.perf_counter()
        total = 0
        for m in range(limit):
            total += fn(m)
        el = time.perf_counter() - t0
        print("  %s  합계 %-8d  %.4f 초" % (name, total, el))

    t0 = time.perf_counter()
    tbl = popcount_table(16)
    el = time.perf_counter() - t0
    print("  table(전처리)  합계 %-8d  %.4f 초  <- 반복 조회가 많으면 압도적"
          % (sum(tbl), el))
    print("  교훈: 루프 안에서 popcount 를 반복 계산하지 말고 전처리하라")


# ---------------------------------------------------------------------------
# 4. 부분집합 전체 열거 (itertools 교차 검증)
# ---------------------------------------------------------------------------
def all_subsets_bitmask(items):
    """for mask in range(1 << n) 한 줄로 모든 부분집합. O(2^n · n)."""
    n = len(items)
    out = []
    for mask in range(1 << n):
        out.append([items[i] for i in range(n) if mask >> i & 1])
    return out


def all_subsets_itertools(items):
    """비교용: combinations 를 크기별로 돌린다."""
    out = []
    for k in range(len(items) + 1):
        for combo in combinations(items, k):
            out.append(list(combo))
    return out


def _factorial(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def demo_enumerate():
    print()
    print(SEP)
    print("4. 부분집합 전체 열거")
    print(SEP)

    items = ["a", "b", "c"]
    subs = all_subsets_bitmask(items)
    print("items = %s   ->  2^3 = %d 개" % (items, len(subs)))
    for mask, sub in enumerate(subs):
        print("  mask=%d = 0b%s  ->  %s" % (mask, format(mask, "03b"), sub))

    print(SUB)
    items = list(range(10))
    a = sorted(tuple(sorted(s)) for s in all_subsets_bitmask(items))
    b = sorted(tuple(sorted(s)) for s in all_subsets_itertools(items))
    assert a == b
    print("n=10 에서 비트마스크 열거 == itertools.combinations 전체: OK (%d 개)" % len(a))

    print(SUB)
    print("2^n 의 크기 감각 (비트마스킹을 쓸지 말지 결정하는 유일한 근거)")
    print("  %-4s %-12s %-14s %-12s %s" % ("n", "2^n", "2^n·n^2", "3^n", "n!"))
    for n in (10, 12, 15, 16, 18, 20, 22):
        fact = "-" if n > 16 else "%.2e" % float(_factorial(n))
        print("  %-4d %-12d %-14d %-12s %s"
              % (n, 1 << n, (1 << n) * n * n, "%.2e" % float(3 ** n), fact))
    print("  파이썬 실전선: 단순 열거 n<=20~22, 비트 DP n<=16~18, 3^n n<=15")


# ---------------------------------------------------------------------------
# 5. 부분집합 합 사전계산 O(2^n)
# ---------------------------------------------------------------------------
def subset_sums_naive(nums):
    """O(2^n · n): 마스크마다 원소를 다시 다 훑는다."""
    n = len(nums)
    s = [0] * (1 << n)
    for m in range(1 << n):
        t = 0
        for i in range(n):
            if m >> i & 1:
                t += nums[i]
        s[m] = t
    return s


def subset_sums_fast(nums):
    """O(2^n): 최하위 1비트를 떼어 이전 마스크의 답을 재활용한다."""
    n = len(nums)
    s = [0] * (1 << n)
    for m in range(1, 1 << n):
        low = m & -m                    # 최하위 1비트
        i = low.bit_length() - 1        # 그 비트의 위치
        s[m] = s[m ^ low] + nums[i]
    return s


def demo_subset_sums():
    print()
    print(SEP)
    print("5. 부분집합 합 사전계산: O(2^n · n) vs O(2^n)")
    print(SEP)

    random.seed(7)
    nums = [random.randint(1, 100) for _ in range(16)]
    t0 = time.perf_counter()
    a = subset_sums_naive(nums)
    t1 = time.perf_counter()
    b = subset_sums_fast(nums)
    t2 = time.perf_counter()
    assert a == b
    print("n=16, 마스크 %d 개" % (1 << 16))
    print("  naive O(2^n·n) : %.4f 초" % (t1 - t0))
    print("  fast  O(2^n)   : %.4f 초   (약 %.1f 배 빠름)"
          % (t2 - t1, (t1 - t0) / max(t2 - t1, 1e-9)))
    print("  두 결과 일치: OK")
    print("  핵심: s[m] = s[m ^ (m & -m)] + nums[LSB위치]  <- n 을 떼어낸다")


# ---------------------------------------------------------------------------
# 6. 서브마스크 열거와 3^n 검증
# ---------------------------------------------------------------------------
def submasks(m):
    """m 의 모든 부분집합을 내림차순으로. 공집합(0)까지 반드시 포함한다."""
    out, sub = [], m
    while True:
        out.append(sub)
        if sub == 0:            # while sub: 로 쓰면 공집합을 빼먹는다!
            break
        sub = (sub - 1) & m
    return out


def demo_submasks():
    print()
    print(SEP)
    print("6. 서브마스크 열거: (sub - 1) & m")
    print(SEP)

    m = 0b1011
    subs = submasks(m)
    print("m = 0b1011 = %d  ->  서브마스크 %d 개 (2^popcount = 2^3 = 8)" % (m, len(subs)))
    print("  " + " -> ".join(format(s, "04b") for s in subs))
    assert len(subs) == 1 << popcount_builtin(m)
    assert len(set(subs)) == len(subs)                     # 중복 없음
    assert all((s & m) == s for s in subs)                 # 전부 m 의 부분집합
    assert 0 in subs                                       # 공집합 포함
    print("  중복 없음 / 전부 m 의 부분집합 / 공집합 포함: OK")

    print(SUB)
    print("모든 마스크의 모든 서브마스크 총 개수 = 3^n 검증")
    for n in range(1, 13):
        total = 0
        for mm in range(1 << n):
            total += len(submasks(mm))
        expect = 3 ** n
        assert total == expect, (n, total, expect)
        if n <= 6 or n == 12:
            print("  n=%-2d  총 %-10d  3^%-2d = %-10d  일치" % (n, total, n, expect))
    print("  이유: 각 비트가 (서브마스크에 있음 / m 에만 있음 / 둘 다 없음) 3가지")
    print("       sum over m of 2^popcount(m) = (1+2)^n = 3^n   (이항정리)")


# ---------------------------------------------------------------------------
# 7. Gosper's hack: 정확히 k개 원소 부분집합
# ---------------------------------------------------------------------------
def k_subsets_gosper(n, k):
    """popcount 가 정확히 k 인 마스크를 오름차순으로 전부 생성한다."""
    if k == 0:
        return [0]
    out = []
    x = (1 << k) - 1                        # 가장 작은 k-부분집합: 하위 k 비트
    limit = 1 << n
    while x < limit:
        out.append(x)
        c = x & -x
        r = x + c
        x = (((r ^ x) >> 2) // c) | r
    return out


def demo_gosper():
    print()
    print(SEP)
    print("7. Gosper's hack: 정확히 k개 원소인 부분집합만 열거")
    print(SEP)

    n, k = 5, 3
    masks = k_subsets_gosper(n, k)
    print("n=%d, k=%d  ->  C(5,3) = 10 개" % (n, k))
    for m in masks:
        print("  0b%s  ->  %s" % (format(m, "05b"), sorted(mask_to_set(m, n))))

    for nn in range(1, 13):
        for kk in range(0, nn + 1):
            got = sorted(sorted(mask_to_set(m, nn)) for m in k_subsets_gosper(nn, kk))
            expect = sorted(sorted(c) for c in combinations(range(nn), kk))
            assert got == expect, (nn, kk)
    print("  n=1..12, k=0..n 전부 itertools.combinations 와 일치: OK")


# ---------------------------------------------------------------------------
# 8. 비트 DP: 외판원 순회 TSP
# ---------------------------------------------------------------------------
def tsp_bitmask_dp(dist):
    """0 에서 출발해 전부 한 번씩 방문하고 0 으로 복귀. O(2^n · n^2)."""
    n = len(dist)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]     # dp[방문집합][현재위치]
    dp[1][0] = 0                                # 0번만 방문, 0에 있음
    for mask in range(1 << n):                  # 작은 마스크부터 = 위상 순서
        for last in range(n):
            cur = dp[mask][last]
            if cur == INF or not (mask >> last & 1):
                continue                        # 도달 불가 상태는 건너뛴다
            for nxt in range(n):
                if mask >> nxt & 1:
                    continue                    # 이미 방문
                nm = mask | (1 << nxt)
                cand = cur + dist[last][nxt]
                if cand < dp[nm][nxt]:
                    dp[nm][nxt] = cand
    end = (1 << n) - 1
    return min(dp[end][last] + dist[last][0] for last in range(n))


def tsp_brute_force(dist):
    """비교용 순열 완전 탐색. O(n!)."""
    n = len(dist)
    best = float("inf")
    for perm in permutations(range(1, n)):
        cost = 0
        cur = 0
        for nxt in perm:
            cost += dist[cur][nxt]
            cur = nxt
        cost += dist[cur][0]
        if cost < best:
            best = cost
    return best


def demo_tsp():
    print()
    print(SEP)
    print("8. 비트 DP: 외판원 순회 TSP  (O(n!) -> O(2^n · n^2))")
    print(SEP)

    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    got = tsp_bitmask_dp(dist)
    exp = tsp_brute_force(dist)
    print("4도시 예제 최소 비용 = %d  (브루트포스 %d 와 일치)" % (got, exp))
    assert got == exp

    print(SUB)
    print("무작위 그래프로 교차 검증 (n=4..8)")
    random.seed(41)
    for n in range(4, 9):
        for _ in range(6):
            d = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    w = random.randint(1, 50)
                    d[i][j] = d[j][i] = w
            assert tsp_bitmask_dp(d) == tsp_brute_force(d), n
        print("  n=%d  6회 전부 일치: OK" % n)

    print(SUB)
    print("n=10 속도 비교")
    n = 10
    d = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            w = random.randint(1, 50)
            d[i][j] = d[j][i] = w
    t0 = time.perf_counter()
    r1 = tsp_brute_force(d)
    t1 = time.perf_counter()
    r2 = tsp_bitmask_dp(d)
    t2 = time.perf_counter()
    assert r1 == r2
    print("  브루트포스 O(n!)      : %.4f 초  (9! = %d 순열)" % (t1 - t0, _factorial(9)))
    print("  비트 DP    O(2^n·n^2) : %.4f 초  (상태 %d 개)" % (t2 - t1, (1 << n) * n))
    print("  n 이 커질수록 격차가 폭발한다 (n=15 이면 약 18만 배)")


# ---------------------------------------------------------------------------
# 9. 비트마스크 + BFS: 모든 노드 방문 최단 보행
# ---------------------------------------------------------------------------
def shortest_path_all_nodes(graph):
    """상태 = (노드, 방문집합). 재방문 허용 최단 보행. O(2^n · n^2)."""
    n = len(graph)
    if n == 1:
        return 0
    goal = (1 << n) - 1
    dq = deque((i, 1 << i) for i in range(n))       # 시작점이 자유 -> 다중 소스
    seen = {(i, 1 << i) for i in range(n)}
    steps = 0
    while dq:
        for _ in range(len(dq)):                    # 레벨 단위 BFS
            u, mask = dq.popleft()
            if mask == goal:
                return steps
            for v in graph[u]:
                nm = mask | (1 << v)
                if (v, nm) not in seen:
                    seen.add((v, nm))
                    dq.append((v, nm))
        steps += 1
    return -1


def demo_bitmask_bfs():
    print()
    print(SEP)
    print("9. 비트마스크 + BFS: 정점을 (노드, 방문집합) 으로 확장")
    print(SEP)

    cases = [
        ([[1, 2, 3], [0], [0], [0]], 4),            # 별 모양: 중심을 여러 번 지난다
        ([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]], 4),
        ([[]], 0),                                   # 노드 1개
        ([[1], [0]], 1),
    ]
    for graph, expect in cases:
        got = shortest_path_all_nodes(graph)
        assert got == expect, (graph, got, expect)
        print("  graph=%-38s  최단 보행 = %d  OK" % (graph, got))

    print(SUB)
    n = 12
    print("상태 수 = n · 2^n.  n<=12 이면 최대 %d 개 -> 아주 여유롭다"
          % (n * (1 << n)))
    print("  평범한 visited BFS 로는 '재방문 허용'을 다룰 수 없다")
    print("  -> 방문 집합을 상태에 넣는 순간 BFS 가 그대로 최단 거리를 준다")


# ---------------------------------------------------------------------------
# 10. 자리별 독립 계산: 모든 부분집합 XOR 총합
# ---------------------------------------------------------------------------
def subset_xor_sum_brute(nums):
    """O(2^n · n): 모든 부분집합의 XOR 을 실제로 다 더한다."""
    n = len(nums)
    total = 0
    for mask in range(1 << n):
        acc = 0
        for i in range(n):
            if mask >> i & 1:
                acc ^= nums[i]
        total += acc
    return total


def subset_xor_sum_fast(nums):
    """O(n): 어떤 비트가 하나라도 켜져 있으면 부분집합의 절반에서 1."""
    acc = 0
    for x in nums:
        acc |= x
    return acc << (len(nums) - 1)


def demo_xor_sum():
    print()
    print(SEP)
    print("10. 자리별 독립 계산: 모든 부분집합 XOR 총합 (O(2^n) -> O(n))")
    print(SEP)

    print("nums=[1,3]  부분집합: [], [1], [3], [1,3]")
    print("  XOR:  0, 1, 3, 1^3=2   합 = 6")
    assert subset_xor_sum_brute([1, 3]) == 6
    assert subset_xor_sum_fast([1, 3]) == 6
    print("  브루트포스와 O(n) 공식 모두 6: OK")

    print(SUB)
    print("왜 (전체 OR) << (n-1) 인가")
    print("  어떤 비트 b 가 nums 중 하나 이상에서 1 이라고 하자.")
    print("  그 비트를 가진 원소들만 보면, 부분집합에서 '홀수 개' 뽑는 경우가 정확히 절반.")
    print("  따라서 2^n 개 부분집합 중 2^(n-1) 개에서 비트 b 가 1 이 된다.")
    print("  -> 총합 = sum over b of (2^b · 2^(n-1)) = (전체 OR) · 2^(n-1)")

    print(SUB)
    random.seed(1863)
    for _ in range(400):
        n = random.randint(1, 10)
        nums = [random.randint(0, 20) for _ in range(n)]
        assert subset_xor_sum_brute(nums) == subset_xor_sum_fast(nums), nums
    print("무작위 400 케이스(n=1..10) 교차 검증: OK")


# ---------------------------------------------------------------------------
# 11. 큰 정수를 비트셋으로: 부분집합 합 가능 여부
# ---------------------------------------------------------------------------
def reachable_sums_bitset(nums):
    """dp 를 정수 하나로 두면 갱신이 dp |= dp << w 한 줄이다."""
    dp = 1                          # 비트 0 만 켜짐 = 합 0 은 만들 수 있다
    for w in nums:
        dp |= dp << w
    return dp


def reachable_sums_set(nums):
    """비교용: set 으로 같은 계산."""
    dp = {0}
    for w in nums:
        dp |= {s + w for s in dp}
    return dp


def demo_bitset_dp():
    print()
    print(SEP)
    print("11. 큰 정수를 비트셋으로 쓰기: dp |= dp << w")
    print(SEP)

    nums = [3, 34, 4, 12, 5, 2]
    dp = reachable_sums_bitset(nums)
    ref = reachable_sums_set(nums)
    got = {i for i in range(sum(nums) + 1) if dp >> i & 1}
    assert got == ref
    print("nums = %s" % nums)
    print("  만들 수 있는 합의 개수 = %d  (set 방식과 일치: OK)" % len(got))
    print("  9 를 만들 수 있나? %s   (3+4+2)" % bool(dp >> 9 & 1))
    print("  1 을 만들 수 있나? %s" % bool(dp >> 1 & 1))

    print(SUB)
    random.seed(99)
    big = [random.randint(1, 300) for _ in range(120)]
    t0 = time.perf_counter()
    d1 = reachable_sums_bitset(big)
    t1 = time.perf_counter()
    d2 = reachable_sums_set(big)
    t2 = time.perf_counter()
    s1 = {i for i in range(sum(big) + 1) if d1 >> i & 1}
    assert s1 == d2
    print("원소 120개, 합 최대 %d" % sum(big))
    print("  큰 정수 비트셋 : %.4f 초" % (t1 - t0))
    print("  파이썬 set     : %.4f 초" % (t2 - t1))
    print("  결과 일치: OK  (비트 연산이 C 레벨에서 돌아 훨씬 빠르다)")


# ---------------------------------------------------------------------------
# 12. 파이썬 정수의 함정 실증
# ---------------------------------------------------------------------------
def demo_pitfalls():
    print()
    print(SEP)
    print("12. 파이썬 정수의 함정")
    print(SEP)

    print("(a) ~x 는 음수다:  ~x == -x - 1")
    for x in (0, 5, 22):
        print("    ~%-3d = %-4d      bin = %s" % (x, ~x, bin(~x)))
    assert ~5 == -6 and ~0 == -1
    print("    bin(-6) = '-0b110'  <- 2의 보수 표기가 아니라 부호 + 절댓값 표기")

    print(SUB)
    print("(b) 여집합은 반드시 폭을 잘라야 한다")
    n, mask = 5, 0b10110
    print("    n=%d, mask=0b%s" % (n, format(mask, "05b")))
    print("    틀림: ~mask        = %-4d  <- 음수, 인덱스로 못 쓴다" % (~mask,))
    print("    맞음: ~mask & full = %-4d = 0b%s"
          % (~mask & full_mask(n), format(~mask & full_mask(n), "05b")))
    print("    맞음: full ^ mask  = %-4d = 0b%s  <- 권장"
          % (full_mask(n) ^ mask, format(full_mask(n) ^ mask, "05b")))
    assert (~mask & full_mask(n)) == (full_mask(n) ^ mask)

    print(SUB)
    print("(c) 연산자 우선순위: 산술이 시프트보다 높다")
    n = 5
    print("    1 << n - 1   = %-4d = 0b%s   <- 의도한 값이 아니다!"
          % (1 << n - 1, format(1 << n - 1, "05b")))
    print("    (1 << n) - 1 = %-4d = 0b%s   <- 전체집합"
          % ((1 << n) - 1, format((1 << n) - 1, "05b")))
    assert (1 << n - 1) != (1 << n) - 1
    print("    x << 1 + 2   == x << 3 :  %s" % ((3 << 1 + 2) == (3 << 3)))

    print(SUB)
    print("(d) 파이썬은 & 가 == 보다 우선순위가 높다 (C/Java 와 반대)")
    a = 6
    print("    a=6:  a & 1 == 0  ->  %s   (파이썬은 (a & 1) == 0 으로 해석)"
          % (a & 1 == 0))
    print("    C/Java 라면 a & (1 == 0) 로 해석되어 버그 -> 양쪽 다 괄호를 쳐라")
    assert (a & 1 == 0) is True

    print(SUB)
    print("(e) 시프트와 마스킹")
    print("    1 << 100 도 정상 동작 (오버플로 없음): 자릿수 %d" % len(str(1 << 100)))
    print("    -1 & 0xFF = %d   (마스킹하면 원하는 폭만 볼 수 있다)" % (-1 & 0xFF))
    print("    -5 >> 1  = %d   (음수는 바닥 나눗셈: -5 // 2 = %d)" % (-5 >> 1, -5 // 2))
    assert (-1 & 0xFF) == 255 and (-5 >> 1) == -3

    print(SUB)
    print("(f) x & -x 와 x & (x-1)  (Day 40 펜윅 트리와 같은 도구)")
    for x in (44, 12, 8, 7):
        low = x & -x
        print("    x=%-3d  x & -x = %-3d (LSB, 위치 %d)   x & (x-1) = %-3d (LSB 제거)"
              % (x, low, low.bit_length() - 1, x & (x - 1)))
    assert (44 & -44) == 4 and (44 & 43) == 40


# ---------------------------------------------------------------------------
def main():
    demo_basics()
    demo_set_ops()
    demo_popcount()
    demo_enumerate()
    demo_subset_sums()
    demo_submasks()
    demo_gosper()
    demo_tsp()
    demo_bitmask_bfs()
    demo_xor_sum()
    demo_bitset_dp()
    demo_pitfalls()

    print()
    print(SEP)
    print("Day 41 예제 전체 실행 완료 (모든 assert 통과)")
    print(SEP)
    print("핵심 정리")
    print("  1) 집합을 정수로 바꾸면 집합이 배열의 첨자가 된다 -> 비트 DP")
    print("  2) 부분집합 열거는 for mask in range(1 << n) 한 줄")
    print("  3) x & -x (LSB 추출), x & (x-1) (LSB 제거) 두 관용구만 외우면 충분")
    print("  4) 서브마스크 열거는 (sub-1) & m, 공집합을 빼먹지 마라")
    print("  5) 제약에 n <= 20 이 보이면 2^n 을 먼저 계산하라")
    print("  6) 파이썬: ~x 는 음수, (1 << n) - 1 의 괄호는 필수")


if __name__ == "__main__":
    main()
