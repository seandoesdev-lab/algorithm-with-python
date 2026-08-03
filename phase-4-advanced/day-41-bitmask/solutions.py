"""Day 41 해설 코드 - 비트마스킹 (Bitmasking & Bitmask DP).

실행: PYTHONIOENCODING=cp949 python solutions.py
표준 라이브러리만 사용한다. (cp949 콘솔 안전: 출력에 ASCII 기호만 사용)

문제 목록 (출처: 프로그래머스 / LeetCode 만)
  1. LeetCode #78    Subsets                            (기초)
  2. LeetCode #1863  Sum of All Subset XOR Totals       (기초)
  3. LeetCode #338   Counting Bits                      (중급)
  4. 프로그래머스 #64064  불량 사용자                     (기출, 2019 카카오 겨울 인턴십)
  5. LeetCode #847   Shortest Path Visiting All Nodes   (심화)
  6. LeetCode #698   Partition to K Equal Sum Subsets   (심화)

문제 설명/힌트 -> problems.md,  개념 -> concept.md
각 문제는 플랫폼 시그니처를 지키고, 가능한 한 다중 접근 + 교차 검증을 붙였다.
"""

import random
import time
from collections import deque
from itertools import combinations, permutations


SEP = "=" * 68
SUB = "-" * 68


def popcount(x):
    """파이썬 3.10+ 는 int.bit_count(), 그 이전은 bin().count('1')."""
    try:
        return x.bit_count()
    except AttributeError:
        return bin(x).count("1")


# ===========================================================================
# 1. LeetCode #78 - Subsets
# ===========================================================================
class Solution78:
    """세 가지 접근. 결과는 모두 동일한 멱집합(power set)이다."""

    # (A) 비트마스크 열거 - 오늘의 정석. 재귀가 없다.
    def subsets(self, nums):
        n = len(nums)
        out = []
        for mask in range(1 << n):                 # 0 .. 2^n - 1 = 모든 부분집합
            out.append([nums[i] for i in range(n) if mask >> i & 1])
        return out

    # (B) 백트래킹 - Day 27 의 표준형
    def subsets_backtrack(self, nums):
        n = len(nums)
        out = []
        path = []

        def dfs(start):
            out.append(list(path))                 # path 를 복사해서 담는다 (중요!)
            for i in range(start, n):
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return out

    # (C) 누적 확장(cascading) - 가장 짧다
    def subsets_cascade(self, nums):
        out = [[]]
        for x in nums:
            out += [sub + [x] for sub in out]      # 오른쪽 out 은 이 시점의 스냅샷
        return out


def _norm(subsets):
    """비교용 정규화: 각 부분집합을 정렬하고 전체를 정렬한다."""
    return sorted(tuple(sorted(s)) for s in subsets)


def test_78():
    print(SEP)
    print("1. LeetCode #78 - Subsets  (부분집합 열거)")
    print(SEP)

    s = Solution78()
    nums = [1, 2, 3]
    got = s.subsets(nums)
    print("nums = %s  ->  2^3 = %d 개" % (nums, len(got)))
    for mask, sub in enumerate(got):
        print("  mask=%d = 0b%s  ->  %s" % (mask, format(mask, "03b"), sub))
    assert _norm(got) == _norm([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])

    print(SUB)
    print("세 접근 교차 검증 (n=1..10, 무작위 값)")
    random.seed(78)
    for n in range(1, 11):
        arr = random.sample(range(-10, 11), n)     # 원소는 서로 다르다
        a = _norm(s.subsets(arr))
        b = _norm(s.subsets_backtrack(arr))
        c = _norm(s.subsets_cascade(arr))
        assert a == b == c, n
        assert len(a) == 1 << n
    print("  비트마스크 == 백트래킹 == 누적확장, 개수도 2^n: OK")

    print(SUB)
    print("접근 비교")
    print("  (A) 비트마스크 : for mask in range(1 << n)  -> 재귀 없음, 상태 관리 없음")
    print("  (B) 백트래킹   : 가지치기를 얹을 수 있다 (부분집합 합 제한 등)")
    print("  (C) 누적 확장  : 세 줄. 다만 원소 추가 순서에 결과 순서가 묶인다")
    print("  세 방법 모두 O(2^n · n) - 출력 크기 자체가 그만큼이라 더 빠를 수 없다")


# ===========================================================================
# 2. LeetCode #1863 - Sum of All Subset XOR Totals
# ===========================================================================
class Solution1863:
    # (A) 브루트포스: 부분집합을 전부 만들어 XOR 을 더한다. O(2^n · n)
    def subsetXORSum_brute(self, nums):
        n = len(nums)
        total = 0
        for mask in range(1 << n):
            acc = 0
            for i in range(n):
                if mask >> i & 1:
                    acc ^= nums[i]
            total += acc
        return total

    # (B) 자리별 독립 계산: O(n)  <- 오늘의 핵심 발상
    def subsetXORSum(self, nums):
        """어떤 비트가 하나라도 켜져 있으면 부분집합의 정확히 절반에서 1이 된다."""
        acc = 0
        for x in nums:
            acc |= x                              # 전체 OR
        return acc << (len(nums) - 1)             # x 2^(n-1)

    # (C) 비트 자리를 명시적으로 세는 버전 (유도 과정을 코드로 남긴 것)
    def subsetXORSum_perbit(self, nums):
        n = len(nums)
        total = 0
        width = max(nums).bit_length() if nums else 0
        for b in range(width):
            k = sum(1 for x in nums if x >> b & 1)    # 그 비트를 가진 원소 수
            if k == 0:
                continue                              # 0 번
            total += (1 << b) * (1 << (n - 1))        # 항상 2^(n-1) 번 (k 와 무관!)
        return total


def test_1863():
    print()
    print(SEP)
    print("2. LeetCode #1863 - Sum of All Subset XOR Totals")
    print(SEP)

    s = Solution1863()
    for nums, expect in (([1, 3], 6), ([5, 1, 6], 28), ([3, 4, 5, 6, 7, 8], 480)):
        a = s.subsetXORSum_brute(nums)
        b = s.subsetXORSum(nums)
        c = s.subsetXORSum_perbit(nums)
        assert a == b == c == expect, (nums, a, b, c, expect)
        acc = 0
        for x in nums:
            acc |= x
        print("  nums=%-22s  답 %-4d   (전체 OR = %d) << (n-1 = %d)"
              % (nums, expect, acc, len(nums) - 1))

    print(SUB)
    print("유도 (nums=[1,3] 로 확인)")
    print("  부분집합 XOR:  [] -> 0,  [1] -> 1,  [3] -> 3,  [1,3] -> 2      합 6")
    print("  비트 0 (값 1): 원소 1, 3 둘 다 가짐 (k=2)")
    print("                 k=2 중 홀수 개 뽑기 = 2^(k-1) = 2 가지")
    print("                 나머지 n-k=0 개 자유 = 2^0 = 1 가지  ->  2 x 1 = 2 = 2^(n-1)")
    print("  비트 1 (값 2): 원소 3 만 가짐 (k=1)")
    print("                 2^(k-1)=1, 2^(n-k)=2  ->  1 x 2 = 2 = 2^(n-1)")
    print("  -> k 가 무엇이든 2^(n-1). 합 = (1 + 2) x 2 = 6.  (전체 OR=3) << 1 = 6")

    print(SUB)
    print("무작위 교차 검증 (브루트포스 vs O(n) 공식)")
    random.seed(1863)
    for _ in range(600):
        n = random.randint(1, 11)
        nums = [random.randint(1, 20) for _ in range(n)]
        assert (s.subsetXORSum_brute(nums)
                == s.subsetXORSum(nums)
                == s.subsetXORSum_perbit(nums)), nums
    print("  600 케이스(n=1..11) 전부 일치: OK")
    print("  경계: n=1 이면 << 0 이라 답이 nums[0] 이다  ->  %d" % s.subsetXORSum([7]))
    assert s.subsetXORSum([7]) == 7


# ===========================================================================
# 3. LeetCode #338 - Counting Bits
# ===========================================================================
class Solution338:
    # (A) 내장 함수: 가장 짧고 파이썬에서 가장 빠르다
    def countBits(self, n):
        return [popcount(i) for i in range(n + 1)]

    # (B) DP - 마지막 비트를 뗀다:  dp[i] = dp[i >> 1] + (i & 1)
    def countBits_shift(self, n):
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
        return dp

    # (C) DP - 최하위 1비트를 뗀다:  dp[i] = dp[i & (i-1)] + 1
    def countBits_lowbit(self, n):
        dp = [0] * (n + 1)
        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1
        return dp

    # (D) 2의 거듭제곱 블록: 앞 블록을 복사하며 1을 더한다
    def countBits_block(self, n):
        dp = [0] * (n + 1)
        power = 1                                  # i 이하의 가장 큰 2의 거듭제곱
        for i in range(1, n + 1):
            if i == power * 2:
                power *= 2
            dp[i] = dp[i - power] + 1
        return dp


def test_338():
    print()
    print(SEP)
    print("3. LeetCode #338 - Counting Bits")
    print(SEP)

    s = Solution338()
    assert s.countBits(2) == [0, 1, 1]
    assert s.countBits(5) == [0, 1, 1, 2, 1, 2]
    assert s.countBits(0) == [0]                   # 경계: n=0 이면 [0]
    print("  n=2  -> %s" % s.countBits(2))
    print("  n=5  -> %s" % s.countBits(5))
    print("  n=0  -> %s   (경계)" % s.countBits(0))

    print(SUB)
    print("네 구현이 n=0..2000 에서 전부 일치하는지")
    for n in range(0, 2001):
        a = s.countBits(n)
        assert a == s.countBits_shift(n)
        assert a == s.countBits_lowbit(n)
        assert a == s.countBits_block(n)
    print("  builtin == shift == lowbit == block: OK")

    print(SUB)
    print("두 점화식은 '값을 쪼개는 서로 다른 방법'이다")
    for i in (5, 6, 7, 12):
        print("  i=%-3d = 0b%-6s  |  i>>1 = %-3d (+%d)  |  i&(i-1) = %-3d (+1)"
              % (i, format(i, "b"), i >> 1, i & 1, i & (i - 1)))

    print(SUB)
    print("성능 비교 (n = 10^5)")
    n = 10 ** 5
    for name, fn in (("builtin  ", s.countBits),
                     ("shift DP ", s.countBits_shift),
                     ("lowbit DP", s.countBits_lowbit),
                     ("block DP ", s.countBits_block)):
        t0 = time.perf_counter()
        fn(n)
        print("  %s : %.4f 초" % (name, time.perf_counter() - t0))
    print("  교훈: 이론상 O(1) 전이라도 파이썬 상수(C 구현 내장 함수)를 못 이길 수 있다")


# ===========================================================================
# 4. 프로그래머스 #64064 - 불량 사용자 (2019 카카오 개발자 겨울 인턴십)
# ===========================================================================
def _match(uid, pattern):
    """'*' 하나 = 문자 하나. 길이가 다르면 무조건 불일치 (최다 오답 지점)."""
    if len(uid) != len(pattern):
        return False
    return all(p == "*" or p == c for c, p in zip(uid, pattern))


def solution(user_id, banned_id):
    """프로그래머스 시그니처. 백트래킹 + 마스크로 '순서 무관 중복 제거'."""
    n = len(user_id)
    # 1단계: 각 banned_id 에 매칭되는 user_id 인덱스 목록
    candidates = [[u for u in range(n) if _match(user_id[u], pat)] for pat in banned_id]

    # 2단계: 서로 다른 사용자를 하나씩 배정하고, 결과 집합을 마스크로 모은다
    results = set()

    def dfs(idx, used_mask):
        if idx == len(banned_id):
            results.add(used_mask)              # 정수 하나 = 집합 하나 -> 중복 자동 제거
            return
        for u in candidates[idx]:
            if used_mask >> u & 1:              # 이미 쓴 사용자
                continue
            dfs(idx + 1, used_mask | (1 << u))  # 새 정수를 넘기므로 되돌리기가 없다

    dfs(0, 0)
    return len(results)


def solution_frozenset(user_id, banned_id):
    """비교용: frozenset 으로 중복 제거 (같은 답, 해싱이 더 비싸다)."""
    n = len(user_id)
    candidates = [[u for u in range(n) if _match(user_id[u], pat)] for pat in banned_id]
    results = set()
    chosen = []

    def dfs(idx):
        if idx == len(banned_id):
            results.add(frozenset(chosen))
            return
        for u in candidates[idx]:
            if u in chosen:
                continue
            chosen.append(u)
            dfs(idx + 1)
            chosen.pop()                        # 되돌리기가 필요하다

    dfs(0)
    return len(results)


def solution_enumerate(user_id, banned_id):
    """비교용: 크기 B 인 부분집합을 전부 만들고 유효한 배정이 있는지 판정."""
    n, b = len(user_id), len(banned_id)
    ok = [[_match(user_id[u], pat) for u in range(n)] for pat in banned_id]
    count = 0
    for combo in combinations(range(n), b):
        # combo 의 사용자들을 banned_id 에 1:1 배정할 수 있는가 (B <= 8 이라 순열 탐색)
        found = False
        for perm in permutations(combo):
            if all(ok[i][perm[i]] for i in range(b)):
                found = True
                break
        if found:
            count += 1
    return count


def test_64064():
    print()
    print(SEP)
    print("4. 프로그래머스 #64064 - 불량 사용자 (2019 카카오 겨울 인턴십)")
    print(SEP)

    cases = [
        (["frodo", "fradi", "crodo", "abc123", "frodoc"], ["*rodo", "*rodo", "******"], 2),
        (["frodo", "fradi", "crodo", "abc123", "frodoc"], ["fr*d*", "abc1**"], 2),
        (["frodo", "fradi", "crodo", "abc123", "frodoc"],
         ["fr*d*", "*rodo", "******", "******"], 3),
    ]
    for user_id, banned_id, expect in cases:
        got = solution(user_id, banned_id)
        assert got == expect, (banned_id, got, expect)
        assert solution_frozenset(user_id, banned_id) == expect
        assert solution_enumerate(user_id, banned_id) == expect
        print("  banned_id=%-42s  ->  %d  OK" % (banned_id, got))

    print(SUB)
    print("길이 비교가 왜 필수인가 ('*' 는 정확히 한 글자)")
    print("  _match('frodo',  '*rodo')  = %s   (5글자 vs 5글자)" % _match("frodo", "*rodo"))
    print("  _match('frodoc', '*rodo')  = %s   (6글자 vs 5글자 -> 불일치!)"
          % _match("frodoc", "*rodo"))
    print("  _match('frodoc', '******') = %s   (6글자 vs 6글자)" % _match("frodoc", "******"))
    assert _match("frodo", "*rodo") and not _match("frodoc", "*rodo")

    print(SUB)
    print("마스크가 중복을 어떻게 제거하는가 (예제 1: ['*rodo','*rodo','******'])")
    user_id = ["frodo", "fradi", "crodo", "abc123", "frodoc"]
    banned_id = ["*rodo", "*rodo", "******"]
    n = len(user_id)
    cand = [[u for u in range(n) if _match(user_id[u], p)] for p in banned_id]
    for i, c in enumerate(cand):
        print("  banned_id[%d]=%-8s  후보 = %s" % (i, banned_id[i], [user_id[u] for u in c]))

    seen = set()
    stats = {"paths": 0}

    def dfs(idx, mask):
        if idx == len(banned_id):
            stats["paths"] += 1
            seen.add(mask)
            return
        for u in cand[idx]:
            if mask >> u & 1:
                continue
            dfs(idx + 1, mask | (1 << u))

    dfs(0, 0)
    print("  재귀가 도달한 경로 수 = %d  (순서까지 구분한 개수)" % stats["paths"])
    print("  서로 다른 마스크 수   = %d  <- 이게 답 (순서 무관)" % len(seen))
    for m in sorted(seen):
        print("      0b%s -> %s" % (format(m, "05b"),
                                    [user_id[i] for i in range(n) if m >> i & 1]))
    assert stats["paths"] == 4 and len(seen) == 2

    print(SUB)
    print("세 접근 무작위 교차 검증")
    random.seed(64064)
    alphabet = "abcdef123"
    for _ in range(300):
        nu = random.randint(1, 6)
        users = []
        while len(users) < nu:
            length = random.randint(4, 6)
            uid = "".join(random.choice(alphabet) for _ in range(length))
            if uid not in users:
                users.append(uid)
        nb = random.randint(1, nu)
        bans = []
        for _ in range(nb):
            base = random.choice(users)
            pat = list(base)
            stars = random.sample(range(len(pat)), random.randint(1, len(pat)))
            for p in stars:
                pat[p] = "*"
            bans.append("".join(pat))
        a = solution(users, bans)
        b = solution_frozenset(users, bans)
        c = solution_enumerate(users, bans)
        assert a == b == c, (users, bans, a, b, c)
    print("  마스크 / frozenset / 열거후판정  300 케이스 전부 일치: OK")
    print("  마스크가 나은 점: 정수 해시가 싸고, 상태 전달이 O(1), 되돌리기가 필요 없다")


# ===========================================================================
# 5. LeetCode #847 - Shortest Path Visiting All Nodes
# ===========================================================================
class Solution847:
    # (A) 비트마스크 + BFS: 상태 = (노드, 방문집합).  O(2^n · n^2)
    def shortestPathLength(self, graph):
        n = len(graph)
        goal = (1 << n) - 1
        dq = deque((i, 1 << i) for i in range(n))        # 시작점 자유 -> 다중 소스
        seen = {(i, 1 << i) for i in range(n)}
        steps = 0
        while dq:
            for _ in range(len(dq)):                     # 레벨 단위
                u, mask = dq.popleft()
                if mask == goal:                         # 꺼낼 때 검사 -> n=1 도 0 이 나온다
                    return steps
                for v in graph[u]:
                    nm = mask | (1 << v)
                    if (v, nm) not in seen:
                        seen.add((v, nm))
                        dq.append((v, nm))
            steps += 1
        return -1

    # (B) 교차 검증용: 전체 쌍 최단거리(BFS) + 순열 완전 탐색. O(n! · n), n 이 작을 때만
    def shortestPathLength_brute(self, graph):
        n = len(graph)
        if n == 1:
            return 0
        dist = [self._bfs(graph, s) for s in range(n)]    # dist[s][t]
        best = float("inf")
        for perm in permutations(range(n)):               # 노드를 방문하는 순서
            cost = 0
            for a, b in zip(perm, perm[1:]):
                cost += dist[a][b]
            if cost < best:
                best = cost
        return best

    @staticmethod
    def _bfs(graph, src):
        n = len(graph)
        d = [-1] * n
        d[src] = 0
        dq = deque([src])
        while dq:
            u = dq.popleft()
            for v in graph[u]:
                if d[v] == -1:
                    d[v] = d[u] + 1
                    dq.append(v)
        return d


def test_847():
    print()
    print(SEP)
    print("5. LeetCode #847 - Shortest Path Visiting All Nodes")
    print(SEP)

    s = Solution847()
    cases = [
        ([[1, 2, 3], [0], [0], [0]], 4),
        ([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]], 4),
        ([[]], 0),                                        # 경계: n=1
        ([[1], [0]], 1),
        ([[1, 2], [0, 2], [0, 1]], 2),                    # 삼각형
    ]
    for graph, expect in cases:
        got = s.shortestPathLength(graph)
        assert got == expect, (graph, got, expect)
        assert s.shortestPathLength_brute(graph) == expect
        print("  graph=%-38s  ->  %d  OK" % (graph, got))

    print(SUB)
    print("왜 평범한 BFS 로는 안 되는가 (graph=[[1,2,3],[0],[0],[0]])")
    print("  최적 경로 예: 1 -> 0 -> 2 -> 0 -> 3   (노드 0 을 세 번 지난다)")
    print("  visited[node] 를 쓰면 0 을 재방문할 수 없어 답에 도달하지 못한다")
    print("  -> 상태를 (노드, 방문집합) 으로 확장하면 재방문이 자연히 허용되고")
    print("     상태 수가 n · 2^n 으로 유한하므로 종료도 보장된다")

    print(SUB)
    print("상태 추적 (graph=[[1],[0]], n=2)")
    graph = [[1], [0]]
    n = 2
    goal = (1 << n) - 1
    dq = deque((i, 1 << i) for i in range(n))
    seen = {(i, 1 << i) for i in range(n)}
    steps = 0
    done = None
    while dq and done is None:
        print("  steps=%d  큐=%s" % (steps, [(u, format(m, "02b")) for u, m in dq]))
        for _ in range(len(dq)):
            u, mask = dq.popleft()
            if mask == goal:
                done = steps
                break
            for v in graph[u]:
                nm = mask | (1 << v)
                if (v, nm) not in seen:
                    seen.add((v, nm))
                    dq.append((v, nm))
        if done is None:
            steps += 1
    print("  goal=0b%s 에 처음 도달한 거리 = %d" % (format(goal, "02b"), done))
    assert done == 1

    print(SUB)
    print("무작위 연결 그래프 교차 검증 (BFS 비트마스크 vs 순열 브루트포스)")
    random.seed(847)
    for n in range(1, 8):
        for _ in range(25):
            # 랜덤 트리로 연결성 보장 후 간선 몇 개 추가
            g = [[] for _ in range(n)]
            for v in range(1, n):
                u = random.randint(0, v - 1)
                g[u].append(v)
                g[v].append(u)
            if n >= 2:
                for _ in range(random.randint(0, n)):
                    a, b = random.sample(range(n), 2)
                    if b not in g[a]:
                        g[a].append(b)
                        g[b].append(a)
            assert s.shortestPathLength(g) == s.shortestPathLength_brute(g), g
        print("  n=%d  25회 전부 일치: OK" % n)

    print(SUB)
    n = 12
    print("제약 n<=12 -> 상태 수 최대 n · 2^n = %d 개. 아주 여유롭다" % (n * (1 << n)))


# ===========================================================================
# 6. LeetCode #698 - Partition to K Equal Sum Subsets
# ===========================================================================
class Solution698:
    # (A) 비트 DP: 상태 = "쓴 원소 집합" 하나.  O(2^n · n)
    def canPartitionKSubsets(self, nums, k):
        total = sum(nums)
        if total % k:
            return False
        target = total // k
        if max(nums) > target:
            return False

        nums = sorted(nums)                        # 오름차순: break 가지치기용
        n = len(nums)
        dp = [False] * (1 << n)
        dp[0] = True
        used = [0] * (1 << n)                      # used[mask] = mask 의 원소 합

        for mask in range(1 << n):                 # 작은 마스크부터 = 위상 순서
            if not dp[mask]:
                continue
            room = used[mask] % target             # 현재 바구니에 담긴 양
            for j in range(n):
                if mask >> j & 1:
                    continue
                if room + nums[j] > target:
                    break                          # 오름차순이므로 뒤는 다 더 크다
                nxt = mask | (1 << j)
                if not dp[nxt]:
                    dp[nxt] = True
                    used[nxt] = used[mask] + nums[j]
        return dp[(1 << n) - 1]

    # (B) 가지치기 백트래킹: 최악은 지수지만 실전에서 매우 빠르다
    def canPartitionKSubsets_backtrack(self, nums, k):
        total = sum(nums)
        if total % k:
            return False
        target = total // k
        nums = sorted(nums, reverse=True)          # 내림차순: 큰 것 먼저 배치
        if nums[0] > target:
            return False
        n = len(nums)
        buckets = [0] * k

        def dfs(i):
            if i == n:
                return True                        # 모든 원소를 배치했다
            x = nums[i]
            tried = set()
            for j in range(k):
                if buckets[j] in tried:            # 같은 담긴 양의 바구니는 한 번만
                    continue
                if buckets[j] + x > target:
                    continue
                tried.add(buckets[j])
                buckets[j] += x
                if dfs(i + 1):
                    return True
                buckets[j] -= x
                if buckets[j] == 0:
                    break                          # 빈 바구니에 넣어 실패 -> 더 볼 필요 없다
            return False

        return dfs(0)

    # (C) 교차 검증용 브루트포스: 원소마다 k개 바구니를 모두 시도. O(k^n)
    def canPartitionKSubsets_brute(self, nums, k):
        total = sum(nums)
        if total % k:
            return False
        target = total // k
        n = len(nums)
        buckets = [0] * k

        def dfs(i):
            if i == n:
                return all(b == target for b in buckets)
            for j in range(k):
                if buckets[j] + nums[i] <= target:
                    buckets[j] += nums[i]
                    if dfs(i + 1):
                        return True
                    buckets[j] -= nums[i]
            return False

        return dfs(0)


def test_698():
    print()
    print(SEP)
    print("6. LeetCode #698 - Partition to K Equal Sum Subsets")
    print(SEP)

    s = Solution698()
    cases = [
        ([4, 3, 2, 3, 5, 2, 1], 4, True),
        ([1, 2, 3, 4], 3, False),
        ([1, 1, 1, 1], 4, True),                   # k = len(nums)
        ([2, 2, 2, 2, 3, 4, 5], 4, False),
        ([10], 1, True),                           # k = 1 은 항상 True
        ([1, 1], 2, True),
        ([3, 3, 10, 2, 3], 3, False),
    ]
    for nums, k, expect in cases:
        a = s.canPartitionKSubsets(nums, k)
        b = s.canPartitionKSubsets_backtrack(nums, k)
        c = s.canPartitionKSubsets_brute(nums, k)
        assert a == b == c == expect, (nums, k, a, b, c, expect)
        print("  nums=%-24s k=%d  ->  %-5s  OK" % (nums, k, expect))

    print(SUB)
    print("핵심 발상: 'k개 바구니' 상태를 지우고 '쓴 원소 집합' 하나만 남긴다")
    nums = [4, 3, 2, 3, 5, 2, 1]
    target = sum(nums) // 4
    print("  nums=%s, k=4  ->  target = %d" % (nums, target))
    srt = sorted(nums)
    print("  정렬 후 = %s" % srt)
    for mask in (0b0000001, 0b0000011, 0b0001111):
        chosen = [srt[i] for i in range(len(srt)) if mask >> i & 1]
        tot = sum(chosen)
        print("    mask=0b%s  원소=%-12s  합=%-3d  합%%target=%d  <- 현재 바구니에 담긴 양"
              % (format(mask, "07b"), chosen, tot, tot % target))
    print("  'k' 가 상태에서 사라진다 -> dp[mask] 1차원으로 충분하다")

    print(SUB)
    print("무작위 교차 검증 (비트 DP vs 가지치기 백트래킹 vs 브루트포스)")
    random.seed(698)
    checked = 0
    for _ in range(500):
        n = random.randint(1, 9)
        k = random.randint(1, n)
        nums = [random.randint(1, 8) for _ in range(n)]
        a = s.canPartitionKSubsets(nums, k)
        b = s.canPartitionKSubsets_backtrack(nums, k)
        c = s.canPartitionKSubsets_brute(nums, k)
        assert a == b == c, (nums, k, a, b, c)
        checked += 1
    print("  %d 케이스(n=1..9) 전부 일치: OK" % checked)

    print(SUB)
    print("성능 비교 (n=16 어려운 케이스: 값이 비슷하고 k 가 중간)")
    random.seed(1)
    hard = []
    for _ in range(6):
        nums = [random.randint(10, 20) for _ in range(16)]
        k = 4
        if sum(nums) % k:
            nums[0] += k - sum(nums) % k          # 나누어떨어지게 만들어 탐색이 깊어지게
        hard.append((nums, k))

    t0 = time.perf_counter()
    r1 = [s.canPartitionKSubsets(nums, k) for nums, k in hard]
    t1 = time.perf_counter()
    r2 = [s.canPartitionKSubsets_backtrack(nums, k) for nums, k in hard]
    t2 = time.perf_counter()
    assert r1 == r2
    print("  비트 DP   O(2^n · n) : %.4f 초   결과 %s" % (t1 - t0, r1))
    print("  백트래킹  (가지치기)  : %.4f 초   결과 %s" % (t2 - t1, r2))
    print("  교훈: 지수 복잡도끼리는 상수와 가지치기가 승부를 가른다")
    print("       최악 복잡도만 보고 '비트 DP 가 항상 낫다'고 단정하지 마라")


# ===========================================================================
def main():
    test_78()
    test_1863()
    test_338()
    test_64064()
    test_847()
    test_698()

    print()
    print(SEP)
    print("Day 41 해설 전체 실행 완료 (모든 assert 통과)")
    print(SEP)
    print("오늘의 판단 기준")
    print("  - 부분집합 전부 확인, n <= 20   -> for mask in range(1 << n)        (#78)")
    print("  - 답이 비트 자리별로 분해됨     -> 자리별 계산으로 O(n)             (#1863)")
    print("  - 값을 비트로 쪼개는 DP         -> dp[i>>1]+(i&1) / dp[i&(i-1)]+1   (#338)")
    print("  - 순서 무관 조합의 개수         -> 마스크를 set 에 넣어 중복 제거    (#64064)")
    print("  - 재방문 허용 최단 경로         -> (노드, 방문집합) BFS             (#847)")
    print("  - 순열 같지만 '집합'만 중요      -> 비트 DP (상태 압축)              (#698)")
    print("  - n > 25                        -> 비트마스킹 포기, 다른 알고리즘")
    print()
    print("파이썬 주의: (1 << n) - 1 의 괄호 필수, ~x 는 음수, mask & (1<<i) 는 0/1 아님")


if __name__ == "__main__":
    main()
