"""Day 45 - Phase 4 심화 종합 복습 (Advanced Review) 예제 모음

Day 31~44 에서 배운 심화 알고리즘 14종의 "암기용 최소 템플릿"을 한 파일에 모았다.
각 템플릿은 실전에서 그대로 꺼내 쓸 수 있는 골격이며,
마지막에 "제약 -> 도구" 판정 표와 교차 검증(나이브 대조), 함정 확인을 붙였다.

실행:  PYTHONIOENCODING=cp949 python examples.py

주의(cp949 콘솔 안전):
  print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
  한글은 안전하지만 이모지/특수기호는 .md 에만 쓴다.
"""

import heapq
from bisect import bisect_left
from collections import deque


SEP = "=" * 62
SUB = "-" * 62


# ==========================================================================
# Day 31. 동적 계획법 입문 - 상태 / 전이 / 순서
# ==========================================================================
def fib_dp(n):
    """dp[i] = dp[i-1] + dp[i-2].  O(N) 시간, O(1) 공간."""
    if n < 2:
        return n
    prev, cur = 0, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur


# ==========================================================================
# Day 32. 배낭 문제 - 0/1 은 역순, 무한은 정순
# ==========================================================================
def knapsack_01(weights, values, cap):
    """각 물건을 최대 1번.  무게 축을 반드시 역순으로 돈다."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):        # 역순! 정순이면 물건을 재사용한다
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[cap]


def knapsack_unbounded(weights, values, cap):
    """각 물건을 무제한.  무게 축을 정순으로 돈다."""
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(w, cap + 1):            # 정순! 재사용이 허용된다
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[cap]


# ==========================================================================
# Day 33. 부분 수열 DP - LIS 두 가지, LCS
# ==========================================================================
def lis_quadratic(a):
    """O(N^2). 느리지만 역추적(실제 수열 복원)이 쉽다."""
    n = len(a)
    if n == 0:
        return 0
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[j] < a[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
    return max(dp)


def lis_nlogn(a):
    """O(N log N). tails 는 '길이 k 인 LIS 의 마지막 값 최솟값'이지 답 수열이 아니다."""
    tails = []
    for x in a:
        i = bisect_left(tails, x)              # 엄격 증가 -> bisect_left
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def lcs(s, t):
    """O(N*M) 시간, O(min(N,M)) 공간 (1차원 롤링)."""
    if len(s) < len(t):
        s, t = t, s                            # t 를 짧은 쪽으로
    prev = [0] * (len(t) + 1)
    for ch in s:
        cur = [0] * (len(t) + 1)
        for j, cj in enumerate(t, 1):
            if ch == cj:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = cur[j - 1] if cur[j - 1] >= prev[j] else prev[j]
        prev = cur
    return prev[-1]


# ==========================================================================
# Day 34. 다익스트라 - 가중치 >= 0
# ==========================================================================
def dijkstra(n, adj, src):
    """adj[v] = [(이웃, 비용), ...].  O(E log V)."""
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    parent = [-1] * n                          # 경로 복원용
    pq = [(0, src)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:                        # 필수! 힙에 같은 정점이 여러 번 들어온다
            continue
        for w, cost in adj[v]:
            nd = d + cost
            if nd < dist[w]:
                dist[w] = nd
                parent[w] = v
                heapq.heappush(pq, (nd, w))
    return dist, parent


def restore_path(parent, dst):
    """추적 배열로 경로 복원. '값만 구하는 코드는 절반짜리'."""
    path = []
    while dst != -1:
        path.append(dst)
        dst = parent[dst]
    path.reverse()
    return path


# ==========================================================================
# Day 35. 벨만-포드 / 플로이드-워셜 - 음수 간선을 다룬다
# ==========================================================================
def bellman_ford(n, edges, src):
    """edges = [(a, b, cost), ...].  O(V*E).
    반환: (dist, 음수사이클_존재여부)"""
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for i in range(n):                         # V 번 돈다. V 번째 갱신 = 음수 사이클
        updated = False
        for a, b, c in edges:
            if dist[a] != INF and dist[a] + c < dist[b]:
                dist[b] = dist[a] + c
                updated = True
        if not updated:
            return dist, False
        if i == n - 1:                         # V 번째에도 갱신되면 음수 사이클
            return dist, True
    return dist, False


def floyd_warshall(n, dist):
    """dist: n x n 인접 행렬(자기 자신 0, 없으면 INF).  O(V^3).
    k 루프가 반드시 가장 바깥이어야 한다 - 순서를 바꾸면 조용히 틀린다."""
    INF = float("inf")
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            via = di[k]
            if via == INF:
                continue                       # 가지치기(상수 절감)
            for j in range(n):
                if via + dk[j] < di[j]:
                    di[j] = via + dk[j]
    return dist


# ==========================================================================
# Day 36. 서로소 집합 (유니온파인드) - 반복 버전
# ==========================================================================
class DSU:
    """경로 압축 + union by size. 사실상 O(1).
    find 를 재귀로 짜면 깊이 10^5 에서 죽는다 - 반드시 while 로."""

    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n
        self.count = n                         # 연결 요소 개수

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]      # 경로 압축
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                       # 이미 같은 집합 -> 이 간선은 사이클
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        self.count -= 1
        return True


# ==========================================================================
# Day 37. 최소 신장 트리 - 크루스칼 / 프림
# ==========================================================================
def kruskal(n, edges):
    """edges = [(cost, a, b), ...].  O(E log E).  연결 불가면 -1."""
    dsu = DSU(n)
    total, used = 0, 0
    for cost, a, b in sorted(edges):
        if dsu.union(a, b):
            total += cost
            used += 1
            if used == n - 1:                  # 조기 종료
                break
    return total if used == n - 1 else -1


def prim(n, adj):
    """adj[v] = [(이웃, 비용), ...].  O(E log V).  밀집 그래프에 유리."""
    visited = [False] * n
    pq = [(0, 0)]
    total, used = 0, 0
    while pq and used < n:
        cost, v = heapq.heappop(pq)
        if visited[v]:
            continue
        visited[v] = True
        total += cost
        used += 1
        for w, c in adj[v]:
            if not visited[w]:
                heapq.heappush(pq, (c, w))
    return total if used == n else -1


# ==========================================================================
# Day 38. 위상 정렬 (Kahn) - 순서이자 사이클 탐지기
# ==========================================================================
def topo_sort(n, graph, indeg):
    """graph[v] = [다음 노드들].  결과 길이가 n 보다 작으면 사이클이 있다."""
    dq = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while dq:
        v = dq.popleft()
        order.append(v)
        for w in graph[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                dq.append(w)
    return order if len(order) == n else []


def longest_path_dag(n, graph, indeg):
    """DAG 위 최장 경로(노드 수). 위상 순서대로 dp 를 전파한다."""
    order = topo_sort(n, graph, indeg[:])
    if not order:
        return -1                              # 사이클
    dp = [1] * n
    for v in order:
        for w in graph[v]:
            if dp[v] + 1 > dp[w]:
                dp[w] = dp[v] + 1
    return max(dp)


# ==========================================================================
# Day 39. 트라이 - 중첩 dict 가 클래스보다 빠르다
# ==========================================================================
END = "#"                                      # 단어 끝 표시. 없으면 최다 버그


def trie_build(words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node[END] = True                       # 반드시 끝을 표시한다
    return root


def trie_search(root, word):
    node = root
    for ch in word:
        if ch not in node:
            return False
        node = node[ch]
    return END in node                         # 접두사만으로는 True 가 아니다


def trie_shortest_root(root, word):
    """word 의 접두사 중 사전에 있는 가장 짧은 것. 없으면 word 그대로."""
    node = root
    for i, ch in enumerate(word):
        if ch not in node:
            return word
        node = node[ch]
        if END in node:
            return word[:i + 1]
    return word


# ==========================================================================
# Day 40. 펜윅 트리 (BIT) / 세그먼트 트리
# ==========================================================================
class BIT:
    """구간 합 + 점 갱신을 O(log N).
    '뺄 수 있는' 연산에만 쓴다. min/max 는 세그먼트 트리가 필요하다."""

    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)                 # 인덱스 0 은 쓰지 않는다 (1-based 필수)

    def add(self, i, v):
        while i <= self.n:                     # i 는 1-based
            self.t[i] += v
            i += i & -i

    def query(self, i):
        """[1, i] 구간 합."""
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.query(r) - self.query(l - 1)


class SegTreeMin:
    """구간 최솟값 + 점 갱신. min 은 뺄 수 없으므로 펜윅으로는 못 한다."""

    def __init__(self, a):
        self.n = len(a)
        self.t = [float("inf")] * (4 * self.n)  # 4N 이 항상 안전하다
        self._build(a, 1, 0, self.n - 1)

    def _build(self, a, node, lo, hi):
        if lo == hi:
            self.t[node] = a[lo]
            return
        mid = (lo + hi) // 2
        self._build(a, node * 2, lo, mid)
        self._build(a, node * 2 + 1, mid + 1, hi)
        self.t[node] = min(self.t[node * 2], self.t[node * 2 + 1])

    def update(self, i, v, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        if lo == hi:
            self.t[node] = v
            return
        mid = (lo + hi) // 2
        if i <= mid:
            self.update(i, v, node * 2, lo, mid)
        else:
            self.update(i, v, node * 2 + 1, mid + 1, hi)
        self.t[node] = min(self.t[node * 2], self.t[node * 2 + 1])

    def query(self, l, r, node=1, lo=0, hi=None):
        if hi is None:
            hi = self.n - 1
        if r < lo or hi < l:
            return float("inf")
        if l <= lo and hi <= r:
            return self.t[node]
        mid = (lo + hi) // 2
        return min(self.query(l, r, node * 2, lo, mid),
                   self.query(l, r, node * 2 + 1, mid + 1, hi))


# ==========================================================================
# Day 41. 비트마스킹 - N <= 20 의 신호
# ==========================================================================
def subsets_bitmask(items):
    """2^N 개의 부분집합을 전부 열거한다."""
    n = len(items)
    out = []
    for mask in range(1 << n):
        cur = [items[i] for i in range(n) if (mask >> i) & 1]   # 괄호 필수
        out.append(cur)
    return out


def tsp_bitmask(dist):
    """외판원 순회 최소 비용(0 에서 출발해 전부 돌고 0 으로).  O(2^N * N^2)."""
    n = len(dist)
    FULL = (1 << n) - 1
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                               # 0번만 방문한 상태
    for mask in range(1 << n):
        row = dp[mask]
        for v in range(n):
            if row[v] == INF or not (mask >> v) & 1:
                continue
            base = row[v]
            for w in range(n):
                if (mask >> w) & 1:
                    continue                   # 이미 방문
                nm = mask | (1 << w)
                nd = base + dist[v][w]
                if nd < dp[nm][w]:
                    dp[nm][w] = nd
    return min(dp[FULL][v] + dist[v][0] for v in range(n))


# ==========================================================================
# Day 42. 문자열 매칭 - KMP 실패 함수 / 라빈-카프
# ==========================================================================
def build_pi(p):
    """실패 함수(부분 일치 테이블). pi[i] = p[:i+1] 의 '접두사이자 접미사' 최장 길이."""
    pi = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j and p[i] != p[j]:
            j = pi[j - 1]                      # while 이어야 한다. if 면 틀린다
        if p[i] == p[j]:
            j += 1
            pi[i] = j
    return pi


def kmp_find_all(text, pat):
    """pat 이 등장하는 모든 시작 인덱스.  O(N+M) 보장."""
    if not pat:
        return []
    pi = build_pi(pat)
    res, j = [], 0
    for i, ch in enumerate(text):
        while j and ch != pat[j]:
            j = pi[j - 1]
        if ch == pat[j]:
            j += 1
            if j == len(pat):
                res.append(i - j + 1)
                j = pi[j - 1]                  # 겹치는 등장도 찾기 위해 되감는다
    return res


def rabin_karp_find(text, pat, base=131, mod=(1 << 61) - 1):
    """롤링 해시. 해시가 같아도 반드시 실제 문자열을 비교해야 한다."""
    n, m = len(text), len(pat)
    if m == 0 or m > n:
        return -1
    high = pow(base, m - 1, mod)
    hp = ht = 0
    for i in range(m):
        hp = (hp * base + ord(pat[i])) % mod
        ht = (ht * base + ord(text[i])) % mod
    for i in range(n - m + 1):
        if hp == ht and text[i:i + m] == pat:  # 충돌 검증 필수
            return i
        if i < n - m:
            ht = ((ht - ord(text[i]) * high) * base + ord(text[i + m])) % mod
    return -1


# ==========================================================================
# Day 43. LCA - 희소 배열(이진 리프팅). 전처리 O(N log N), 질의 O(log N)
# ==========================================================================
class LCA:
    def __init__(self, n, adj, root=0):
        self.n = n
        self.LOG = max(1, n.bit_length())
        self.depth = [0] * n
        self.up = [[-1] * n for _ in range(self.LOG)]
        # 재귀 없이 BFS 로 parent/depth 를 만든다
        visited = [False] * n
        visited[root] = True
        dq = deque([root])
        order = [root]
        while dq:
            v = dq.popleft()
            for w in adj[v]:
                if not visited[w]:
                    visited[w] = True
                    self.up[0][w] = v
                    self.depth[w] = self.depth[v] + 1
                    order.append(w)
                    dq.append(w)
        self.order = order
        for k in range(1, self.LOG):
            upk, upk1 = self.up[k], self.up[k - 1]
            for v in range(n):
                mid = upk1[v]
                upk[v] = upk1[mid] if mid != -1 else -1

    def query(self, a, b):
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        diff = self.depth[a] - self.depth[b]
        for k in range(self.LOG):              # 깊이를 먼저 맞춘다
            if (diff >> k) & 1:
                a = self.up[k][a]
        if a == b:
            return a
        for k in range(self.LOG - 1, -1, -1):  # 함께 올라간다
            if self.up[k][a] != self.up[k][b]:
                a, b = self.up[k][a], self.up[k][b]
        return self.up[0][a]

    def distance(self, a, b):
        return self.depth[a] + self.depth[b] - 2 * self.depth[self.query(a, b)]


# ==========================================================================
# Day 44. 트리 DP - BFS 순서를 뒤집으면 후위 순회 (재귀 0줄)
# ==========================================================================
def root_tree(adj, root=0):
    """무향 트리에 루트를 정해 parent / depth / BFS 순서를 만든다."""
    n = len(adj)
    parent, depth = [-1] * n, [0] * n
    visited = [False] * n
    visited[root] = True
    order = [root]
    dq = deque([root])
    while dq:
        v = dq.popleft()
        for w in adj[v]:
            if not visited[w]:
                visited[w] = True
                parent[w] = v
                depth[w] = depth[v] + 1
                order.append(w)
                dq.append(w)
    return parent, depth, order


def subtree_sizes(adj, root=0):
    """서브트리 크기. reversed(order) 안에서 자식은 이미 계산되어 있다."""
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    size = [1] * n
    for v in reversed(order):
        p = parent[v]
        if p != -1:
            size[p] += size[v]
    return size


def tree_diameter(adj, root=0):
    """지름(간선 수). 올려보내는 값(한 갈래)과 정답(두 갈래)이 다르다."""
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    down = [0] * n
    best = 0
    for v in reversed(order):
        top1 = top2 = 0
        for w in adj[v]:
            if w == parent[v]:
                continue
            d = down[w] + 1
            if d > top1:
                top1, top2 = d, top1
            elif d > top2:
                top2 = d
        down[v] = top1                         # 부모에게는 한 갈래만
        if top1 + top2 > best:
            best = top1 + top2                 # 정답에는 두 갈래
    return best


def min_height_roots(n, edges):
    """최소 높이 루트 - 잎을 층층이 깎는다. 답은 항상 1개 또는 2개."""
    if n == 1:
        return [0]
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    leaves = [v for v in range(n) if len(adj[v]) == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        nxt = []
        for v in leaves:
            w = adj[v].pop()
            adj[w].discard(v)
            if len(adj[w]) == 1:
                nxt.append(w)
        leaves = nxt
    return sorted(leaves)


# ==========================================================================
# 교차 검증용 나이브 구현
# ==========================================================================
def dijkstra_naive(n, adj, src):
    """힙 없는 O(V^2) 다익스트라. 작은 그래프에서 정답 대조용."""
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    done = [False] * n
    for _ in range(n):
        v, best = -1, INF
        for i in range(n):
            if not done[i] and dist[i] < best:
                v, best = i, dist[i]
        if v == -1:
            break
        done[v] = True
        for w, c in adj[v]:
            if dist[v] + c < dist[w]:
                dist[w] = dist[v] + c
    return dist


def lcs_naive(s, t):
    """2차원 DP. 롤링 버전과 대조한다."""
    dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
    for i, a in enumerate(s, 1):
        for j, b in enumerate(t, 1):
            if a == b:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


# ==========================================================================
# 제약 -> 도구 판정 표
# ==========================================================================
def pick_tool(n):
    """N 만 보고 허용 복잡도와 열리는 도구를 답한다. 실전 30초 판단의 자동화."""
    if n <= 12:
        return "O(N!)", "순열 완전 탐색 (Day 24)"
    if n <= 20:
        return "O(2^N * N)", "비트마스크 DP, 부분집합 열거 (Day 41)"
    if n <= 400:
        return "O(N^3)", "플로이드-워셜, 3중 루프 DP (Day 35)"
    if n <= 5000:
        return "O(N^2)", "LCS, LIS O(N^2), 벨만-포드 (Day 33, 35)"
    if n <= 100000:
        return "O(N log N)", "정렬, 다익스트라, MST, LIS 이분 (Day 34, 37, 33)"
    if n <= 1000000:
        return "O(N)", "KMP, 유니온파인드, 펜윅, 트라이 (Day 42, 36, 40, 39)"
    return "O(log N)", "이분 탐색, 거듭제곱, 수학 (Day 18, 05)"


# ==========================================================================
# 데모
# ==========================================================================
def demo_dp():
    print(SEP)
    print("[Day 31~33] DP 계열 - 상태/전이/순서")
    print(SEP)
    print("피보나치 fib(30)      =", fib_dp(30))

    weights, values, cap = [2, 3], [3, 4], 6
    print("0/1 배낭 (역순 갱신)  =", knapsack_01(weights, values, cap),
          "(정답 7: 무게2+무게3 을 하나씩)")
    print("무한 배낭 (정순 갱신) =", knapsack_unbounded(weights, values, cap),
          "(정답 9: 무게2 짜리를 3개)")
    print("같은 입력인데 답이 다르다 -> 루프 방향 하나가 문제를 바꾼다")
    print(SUB)

    a = [10, 9, 2, 5, 3, 7, 101, 18]
    print("LIS 대상 배열         =", a)
    print("LIS  O(N^2)           =", lis_quadratic(a))
    print("LIS  O(N log N)       =", lis_nlogn(a))
    print("두 방법 일치          =", "O" if lis_quadratic(a) == lis_nlogn(a) else "X")
    print(SUB)

    s, t = "abcde", "ace"
    print("LCS('abcde','ace')    =", lcs(s, t), "(롤링 1차원)")
    print("LCS 나이브 2차원      =", lcs_naive(s, t))
    print("두 방법 일치          =", "O" if lcs(s, t) == lcs_naive(s, t) else "X")
    print()


def demo_shortest_path():
    print(SEP)
    print("[Day 34~35] 최단 경로 3형제")
    print(SEP)
    n = 5
    edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]
    adj = [[] for _ in range(n)]
    for a, b, c in edges:
        adj[a].append((b, c))

    dist, parent = dijkstra(n, adj, 0)
    print("다익스트라 dist       =", dist)
    print("0 -> 4 경로 복원      =", restore_path(parent, 4))
    naive = dijkstra_naive(n, adj, 0)
    print("나이브 O(V^2) 대조    =", naive)
    print("두 방법 일치          =", "O" if dist == naive else "X")
    print(SUB)

    bf_dist, neg = bellman_ford(n, edges, 0)
    print("벨만-포드 dist        =", bf_dist)
    print("음수 사이클 존재      =", "O" if neg else "X")
    print("다익스트라와 일치     =", "O" if bf_dist == dist else "X")
    print(SUB)

    neg_edges = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]
    _, has_neg = bellman_ford(3, neg_edges, 0)
    print("음수 사이클 그래프 탐지 =", "O (탐지 성공)" if has_neg else "X")
    print(SUB)

    INF = float("inf")
    mat = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, c in edges:
        if c < mat[a][b]:
            mat[a][b] = c
    floyd_warshall(n, mat)
    print("플로이드 0행(모든 쌍) =", mat[0])
    print("다익스트라와 일치     =", "O" if mat[0] == dist else "X")
    print()


def demo_connectivity():
    print(SEP)
    print("[Day 36~38] 연결성과 순서 - 유니온파인드 / MST / 위상 정렬")
    print(SEP)
    dsu = DSU(6)
    for a, b in [(0, 1), (1, 2), (3, 4)]:
        dsu.union(a, b)
    print("연결 요소 개수        =", dsu.count, "(정답 3: {0,1,2} {3,4} {5})")
    print("0 과 2 는 같은 그룹   =", "O" if dsu.find(0) == dsu.find(2) else "X")
    print("0 과 5 는 같은 그룹   =", "O" if dsu.find(0) == dsu.find(5) else "X")
    print(SUB)

    n = 4
    mst_edges = [(1, 0, 1), (2, 1, 2), (3, 0, 2), (4, 2, 3), (5, 0, 3)]
    adj = [[] for _ in range(n)]
    for c, a, b in mst_edges:
        adj[a].append((b, c))
        adj[b].append((a, c))
    k = kruskal(n, mst_edges)
    p = prim(n, adj)
    print("크루스칼 MST 비용     =", k)
    print("프림     MST 비용     =", p)
    print("두 방법 일치          =", "O" if k == p else "X")
    print(SUB)

    # 0 -> 1 -> 3, 0 -> 2 -> 3
    graph = [[1, 2], [3], [3], []]
    indeg = [0, 1, 1, 2]
    order = topo_sort(4, graph, indeg[:])
    print("위상 정렬 결과        =", order)
    print("DAG 최장 경로(노드수) =", longest_path_dag(4, graph, indeg))
    print(SUB)

    cyc_graph = [[1], [2], [0]]
    cyc_indeg = [1, 1, 1]
    print("사이클 그래프 판정    =",
          "사이클 있음" if not topo_sort(3, cyc_graph, cyc_indeg) else "DAG")
    print()


def demo_structures():
    print(SEP)
    print("[Day 39~41] 자료구조 심화 - 트라이 / 펜윅 / 세그먼트 / 비트마스크")
    print(SEP)
    root = trie_build(["cat", "cattle", "bat", "rat"])
    print("트라이 검색 'cat'     =", "O" if trie_search(root, "cat") else "X")
    print("트라이 검색 'ca'      =", "O" if trie_search(root, "ca") else "X",
          "(접두사만으로는 X 여야 한다)")
    print("가장 짧은 어근 'cattle' =", trie_shortest_root(root, "cattle"))
    print("사전에 없는 'dog'       =", trie_shortest_root(root, "dog"))
    print(SUB)

    a = [1, 3, 5, 7, 9, 11]
    bit = BIT(len(a))
    for i, v in enumerate(a, 1):
        bit.add(i, v)
    print("펜윅 [1..3] 합        =", bit.range_sum(1, 3), "(정답 9)")
    bit.add(2, 10)                             # a[1] 을 3 -> 13 으로
    print("a[1] += 10 후 [1..3]  =", bit.range_sum(1, 3), "(정답 19)")
    print("나이브 대조           =", 1 + 13 + 5)
    print(SUB)

    seg = SegTreeMin([5, 2, 8, 1, 9])
    print("세그먼트 min[0..2]    =", seg.query(0, 2), "(정답 2)")
    seg.update(1, 100)
    print("a[1]=100 후 min[0..2] =", seg.query(0, 2), "(정답 5)")
    print("min 은 뺄 수 없어서 펜윅으로는 못 한다")
    print(SUB)

    subs = subsets_bitmask(["a", "b", "c"])
    print("부분집합 개수 (2^3)   =", len(subs))
    print("부분집합 목록         =", ["".join(s) if s else "{}" for s in subs])
    print(SUB)

    tsp = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    print("TSP 최소 순회 비용    =", tsp_bitmask(tsp), "(정답 80)")
    print()


def demo_string_and_tree():
    print(SEP)
    print("[Day 42~44] 문자열 매칭과 트리")
    print(SEP)
    text, pat = "ababcabcabababd", "ababd"
    print("KMP pi('ababd')       =", build_pi(pat))
    print("KMP 등장 위치         =", kmp_find_all(text, pat))
    print("내장 find 대조        =", text.find(pat))
    print("라빈-카프 대조        =", rabin_karp_find(text, pat))
    print(SUB)

    # 실패 함수 자체가 답이 되는 유형: 접두사이자 접미사인 최장
    for s in ["level", "ababab", "abcd", "aaaa"]:
        pi = build_pi(s)
        print("가장 긴 접두사=접미사 '%s' -> '%s'" % (s, s[:pi[-1]]))
    print(SUB)

    #        0
    #      /   \
    #     1     2
    #    / \     \
    #   3   4     5
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    n = 6
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    lca = LCA(n, adj, 0)
    print("LCA(3, 4)             =", lca.query(3, 4), "(정답 1)")
    print("LCA(3, 5)             =", lca.query(3, 5), "(정답 0)")
    print("거리(3, 5)            =", lca.distance(3, 5), "(정답 4)")
    print(SUB)

    print("서브트리 크기         =", subtree_sizes(adj, 0), "(정답 [6,3,2,1,1,1])")
    print("트리 지름(간선 수)    =", tree_diameter(adj, 0), "(정답 4: 3-1-0-2-5)")
    print("최소 높이 루트        =", min_height_roots(n, edges))
    print()


def demo_decision_map():
    print(SEP)
    print("[Day 45] 제약 -> 도구 판정표 - 문제를 읽고 30초 안에 하는 판단")
    print(SEP)
    print("%-12s %-16s %s" % ("N", "허용 복잡도", "열리는 도구"))
    print(SUB)
    for n in [10, 18, 300, 3000, 50000, 500000, 10 ** 9]:
        allowed, tool = pick_tool(n)
        print("%-12s %-16s %s" % ("{:,}".format(n), allowed, tool))
    print(SUB)
    print("판단 순서:")
    print("  1) 제약을 읽어 허용 복잡도를 정한다")
    print("  2) 문제의 구조 신호로 도구를 하나 고른다")
    print("     (선후관계=위상정렬 / 연결성=유니온파인드 / 접두사=트라이 ...)")
    print("  3) 전제를 확인한다 (음수 간선? 갱신이 있나? 사이클이 있나?)")
    print("  4) 복잡도에 최댓값을 대입해 1e7 을 넘는지 검산한다")
    print()


def demo_pitfalls():
    print(SEP)
    print("[함정 확인] 자주 틀리는 지점을 코드로 확인한다")
    print(SEP)

    # 함정 1: 0/1 배낭을 정순으로 돌면 물건을 재사용한다
    cap = 9
    wrong = [0] * (cap + 1)
    for c in range(3, cap + 1):                # 정순 = 무한 배낭이 되어 버린다
        if wrong[c - 3] + 4 > wrong[c]:
            wrong[c] = wrong[c - 3] + 4
    print("0/1 배낭인데 정순으로 = %d (틀림. 무게3 물건을 3번 썼다)" % wrong[cap])
    print("역순으로 제대로       = %d (맞음. 1번만)" % knapsack_01([3], [4], cap))
    print(SUB)

    # 함정 2: KMP 되감기를 if 로 하면 틀린다
    def build_pi_wrong(p):
        pi = [0] * len(p)
        j = 0
        for i in range(1, len(p)):
            if j and p[i] != p[j]:             # while 이어야 한다
                j = pi[j - 1]
            if p[i] == p[j]:
                j += 1
                pi[i] = j
        return pi

    probe = "aabaaacaa"                        # 인덱스 6 에서 두 번 되감아야 한다
    right = build_pi(probe)
    wrong_pi = build_pi_wrong(probe)
    print("KMP pi 정상(while)    =", right)
    print("KMP pi 잘못(if)       =", wrong_pi)
    print("두 결과가 다른가      =",
          "O (if 로 짜면 틀린다)" if right != wrong_pi
          else "X (이 입력에서는 우연히 같다)")
    print(SUB)

    # 함정 3: 트라이에 단어 끝 표시가 없으면 접두사를 단어로 착각한다
    root = trie_build(["apple"])
    print("사전=['apple'], 'app' 검색 =", "O" if trie_search(root, "app") else "X",
          "(끝 표시가 있으므로 X 가 맞다)")
    print(SUB)

    # 함정 4: 다익스트라를 음수 간선에 쓰면 틀린다
    #   교과서형(visited 로 확정하는) 다익스트라를 써야 실패가 드러난다.
    #   위쪽 dijkstra() 는 확정 없이 계속 재완화하는 lazy 버전이라
    #   음수 사이클만 없으면 우연히 수렴한다 - 이것도 알아 둘 만한 사실이다.
    def dijkstra_visited(n, adj, src):
        INF = float("inf")
        dist = [INF] * n
        dist[src] = 0
        visited = [False] * n
        pq = [(0, src)]
        while pq:
            d, v = heapq.heappop(pq)
            if visited[v]:
                continue
            visited[v] = True                  # 한 번 꺼내면 확정 - 음수에서 깨진다
            for w, cost in adj[v]:
                if not visited[w] and d + cost < dist[w]:
                    dist[w] = d + cost
                    heapq.heappush(pq, (dist[w], w))
        return dist

    n = 3
    adj = [[(2, 1), (1, 5)], [(2, -10)], []]   # 0->2:1, 0->1:5, 1->2:-10
    d_bad = dijkstra_visited(n, adj, 0)
    d_lazy, _ = dijkstra(n, adj, 0)
    neg_edges = [(0, 2, 1), (0, 1, 5), (1, 2, -10)]
    d_bf, _ = bellman_ford(n, neg_edges, 0)
    print("정답(벨만-포드)              =", d_bf, "  0->1->2 = 5-10 = -5")
    print("다익스트라(visited 확정형)   =", d_bad)
    print("  틀렸는가            =", "O (2번 정점을 1 로 확정해 버렸다)"
          if d_bad != d_bf else "X")
    print("다익스트라(lazy 재완화형)    =", d_lazy)
    print("  이쪽은 맞는가       =", "O (음수 사이클이 없으면 우연히 수렴한다)"
          if d_lazy == d_bf else "X")
    print("  -> 그래도 음수 간선에는 쓰지 마라. 최악에 지수 시간이 되고,")
    print("     음수 사이클이 있으면 무한 루프에 빠진다")
    print()


def main():
    demo_dp()
    demo_shortest_path()
    demo_connectivity()
    demo_structures()
    demo_string_and_tree()
    demo_decision_map()
    demo_pitfalls()
    print(SEP)
    print("Day 45 예제 실행 완료 - Phase 4 도구 14종 + 판정표 + 함정 확인")
    print(SEP)


if __name__ == "__main__":
    main()
