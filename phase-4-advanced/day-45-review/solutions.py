"""Day 45 해설 - Phase 4 심화 종합 복습 (Advanced Review)

problems.md 의 13문제를 플랫폼 시그니처로 구현하고,
가능한 곳은 두 가지 이상의 접근을 붙여 교차 검증한다.

  LeetCode     -> class Solution 안의 메서드
  프로그래머스  -> def solution(...)

실행:  PYTHONIOENCODING=cp949 python solutions.py

주의(cp949 콘솔 안전):
  print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
"""

import heapq
import random
from bisect import bisect_left, insort
from collections import deque


SEP = "=" * 62
SUB = "-" * 62
MOD = 10 ** 9 + 7


# ==========================================================================
# 1. Coin Change  (LeetCode #322)  - Day 31, 32
# ==========================================================================
class SolutionCoinChange:
    def coinChange(self, coins, amount):
        """무한 배낭 DP.  O(amount * len(coins)) 시간, O(amount) 공간.
        각 동전을 무제한으로 쓰므로 금액 축을 '정순'으로 돈다."""
        INF = float("inf")
        dp = [INF] * (amount + 1)
        dp[0] = 0
        for c in coins:
            if c > amount:
                continue
            for x in range(c, amount + 1):     # 정순 = 무한 배낭
                if dp[x - c] + 1 < dp[x]:
                    dp[x] = dp[x - c] + 1
        return -1 if dp[amount] == INF else dp[amount]

    def coinChangeBFS(self, coins, amount):
        """접근 2: 가중치 1인 최단 경로로 보고 BFS 층 탐색.
        '최소 개수' = '최소 간선 수' 라는 번역.  O(amount * len(coins))."""
        if amount == 0:
            return 0
        seen = {amount}
        frontier = [amount]
        depth = 0
        while frontier:
            depth += 1
            nxt = []
            for cur in frontier:
                for c in coins:
                    rest = cur - c
                    if rest == 0:
                        return depth
                    if rest > 0 and rest not in seen:
                        seen.add(rest)
                        nxt.append(rest)
            frontier = nxt
        return -1


# ==========================================================================
# 2. Longest Common Subsequence  (LeetCode #1143)  - Day 33
# ==========================================================================
class SolutionLCS:
    def longestCommonSubsequence(self, text1, text2):
        """1차원 롤링 DP.  O(N*M) 시간, O(min(N,M)) 공간."""
        if len(text1) < len(text2):
            text1, text2 = text2, text1        # text2 를 짧은 쪽으로
        prev = [0] * (len(text2) + 1)
        for ch in text1:
            cur = [0] * (len(text2) + 1)
            for j in range(1, len(text2) + 1):
                if ch == text2[j - 1]:
                    cur[j] = prev[j - 1] + 1
                elif cur[j - 1] >= prev[j]:
                    cur[j] = cur[j - 1]
                else:
                    cur[j] = prev[j]
            prev = cur
        return prev[-1]

    def longestCommonSubsequence2D(self, text1, text2):
        """접근 2: 교과서 2차원 DP.  O(N*M) 시간, O(N*M) 공간.
        공간을 더 쓰는 대신 역추적으로 실제 수열을 복원할 수 있다."""
        n, m = len(text1), len(text2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[n][m]


# ==========================================================================
# 3. Longest Increasing Subsequence  (LeetCode #300)  - Day 33, 18
# ==========================================================================
class SolutionLIS:
    def lengthOfLIS(self, nums):
        """O(N log N).  tails[k] = 길이 k+1 인 증가 수열의 마지막 값 최솟값."""
        tails = []
        for x in nums:
            i = bisect_left(tails, x)          # 엄격 증가 -> bisect_left
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x
        return len(tails)

    def lengthOfLISQuadratic(self, nums):
        """접근 2: O(N^2) DP. 느리지만 직관적이고 역추적이 쉽다."""
        if not nums:
            return 0
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
        return max(dp)

    def actualLIS(self, nums):
        """보너스: 실제 수열을 복원한다.
        tails 배열만으로는 못 한다 - 각 원소가 들어간 위치를 기록해야 한다."""
        if not nums:
            return []
        tails = []
        prev = [-1] * len(nums)                # 역추적 링크
        idx_at = []                            # tails[k] 를 만든 원소의 인덱스
        for i, x in enumerate(nums):
            k = bisect_left(tails, x)
            if k == len(tails):
                tails.append(x)
                idx_at.append(i)
            else:
                tails[k] = x
                idx_at[k] = i
            prev[i] = idx_at[k - 1] if k > 0 else -1
        out, cur = [], idx_at[-1]
        while cur != -1:
            out.append(nums[cur])
            cur = prev[cur]
        out.reverse()
        return out


# ==========================================================================
# 4. 배달  (프로그래머스 #12978)  - Day 34
# ==========================================================================
def solution_delivery(N, road, K):
    """플로이드-워셜.  N <= 50 이므로 O(N^3) = 125,000 으로 즉시 통과.
    코드가 가장 짧고 틀리기 어렵다."""
    INF = float("inf")
    dist = [[0 if i == j else INF for j in range(N + 1)] for i in range(N + 1)]
    for a, b, c in road:
        if c < dist[a][b]:                     # 중복 간선! 반드시 min
            dist[a][b] = c
            dist[b][a] = c
    for k in range(1, N + 1):                  # k 가 가장 바깥
        dk = dist[k]
        for i in range(1, N + 1):
            di = dist[i]
            via = di[k]
            if via == INF:
                continue
            for j in range(1, N + 1):
                if via + dk[j] < di[j]:
                    di[j] = via + dk[j]
    return sum(1 for v in range(1, N + 1) if dist[1][v] <= K)


def solution_delivery_dijkstra(N, road, K):
    """접근 2: 다익스트라.  O(E log V). 가중치가 모두 양수이므로 안전하다."""
    INF = float("inf")
    adj = [[] for _ in range(N + 1)]
    for a, b, c in road:
        adj[a].append((b, c))
        adj[b].append((a, c))                  # 양방향
    dist = [INF] * (N + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:                        # 중복 정점 건너뛰기
            continue
        for w, c in adj[v]:
            if d + c < dist[w]:
                dist[w] = d + c
                heapq.heappush(pq, (dist[w], w))
    return sum(1 for v in range(1, N + 1) if dist[v] <= K)


# ==========================================================================
# 5. Network Delay Time  (LeetCode #743)  - Day 34, 35
# ==========================================================================
class SolutionNetworkDelay:
    def networkDelayTime(self, times, n, k):
        """다익스트라.  가중치 양수 + 출발점 1개 = 실전 정답.  O(E log V)."""
        INF = float("inf")
        adj = [[] for _ in range(n + 1)]
        for u, v, w in times:
            adj[u].append((v, w))              # 방향 간선
        dist = [INF] * (n + 1)
        dist[k] = 0
        pq = [(0, k)]
        while pq:
            d, v = heapq.heappop(pq)
            if d > dist[v]:
                continue
            for w, cost in adj[v]:
                if d + cost < dist[w]:
                    dist[w] = d + cost
                    heapq.heappush(pq, (dist[w], w))
        ans = max(dist[1:])                    # 1-based: 인덱스 0 은 버린다
        return -1 if ans == INF else ans

    def networkDelayTimeBellman(self, times, n, k):
        """접근 2: 벨만-포드.  O(V*E). 음수 간선도 다룰 수 있다(여기선 없지만)."""
        INF = float("inf")
        dist = [INF] * (n + 1)
        dist[k] = 0
        for _ in range(n - 1):                 # V-1 번이면 충분하다
            updated = False
            for u, v, w in times:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break
        ans = max(dist[1:])
        return -1 if ans == INF else ans

    def networkDelayTimeFloyd(self, times, n, k):
        """접근 3: 플로이드-워셜.  O(V^3) = 10^6. n<=100 이라 통과한다."""
        INF = float("inf")
        d = [[0 if i == j else INF for j in range(n + 1)] for i in range(n + 1)]
        for u, v, w in times:
            if w < d[u][v]:
                d[u][v] = w
        for m in range(1, n + 1):              # 경유지가 가장 바깥
            dm = d[m]
            for i in range(1, n + 1):
                di = d[i]
                via = di[m]
                if via == INF:
                    continue
                for j in range(1, n + 1):
                    if via + dm[j] < di[j]:
                        di[j] = via + dm[j]
        ans = max(d[k][1:])
        return -1 if ans == INF else ans


# ==========================================================================
# 6. Number of Provinces  (LeetCode #547)  - Day 36
# ==========================================================================
class DSU:
    """경로 압축 + union by size. find 는 반복 버전(재귀 금지)."""

    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n
        self.count = n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        self.count -= 1                        # union 성공 시에만 줄인다
        return True


class SolutionProvinces:
    def findCircleNum(self, isConnected):
        """유니온파인드.  O(N^2) (인접 행렬을 훑어야 하므로)."""
        n = len(isConnected)
        dsu = DSU(n)
        for i in range(n):
            row = isConnected[i]
            for j in range(i + 1, n):          # 대칭이므로 위쪽 삼각형만
                if row[j]:
                    dsu.union(i, j)
        return dsu.count

    def findCircleNumDFS(self, isConnected):
        """접근 2: 반복 DFS.  O(N^2). 탐색을 시작한 횟수가 곧 연결 요소 개수."""
        n = len(isConnected)
        seen = [False] * n
        groups = 0
        for s in range(n):
            if seen[s]:
                continue
            groups += 1
            stack = [s]
            seen[s] = True
            while stack:
                v = stack.pop()
                row = isConnected[v]
                for w in range(n):
                    if row[w] and not seen[w]:
                        seen[w] = True
                        stack.append(w)
        return groups


# ==========================================================================
# 7. 섬 연결하기  (프로그래머스 #42861)  - Day 36, 37
# ==========================================================================
def solution_islands(n, costs):
    """크루스칼 MST.  O(E log E).
    간선을 비용순으로 보며 사이클을 만들지 않는 것만 고른다."""
    dsu = DSU(n)
    total, used = 0, 0
    for a, b, c in sorted(costs, key=lambda e: e[2]):
        if dsu.union(a, b):
            total += c
            used += 1
            if used == n - 1:                  # 조기 종료
                break
    return total


def solution_islands_prim(n, costs):
    """접근 2: 프림 MST.  O(E log V).
    0번 섬에서 시작해 가장 싼 간선을 힙으로 뽑는다."""
    if n <= 1:
        return 0
    adj = [[] for _ in range(n)]
    for a, b, c in costs:
        adj[a].append((c, b))
        adj[b].append((c, a))
    visited = [False] * n
    pq = [(0, 0)]
    total, used = 0, 0
    while pq and used < n:
        c, v = heapq.heappop(pq)
        if visited[v]:
            continue
        visited[v] = True
        total += c
        used += 1
        for nc, w in adj[v]:
            if not visited[w]:
                heapq.heappush(pq, (nc, w))
    return total


# ==========================================================================
# 8. Longest Increasing Path in a Matrix  (LeetCode #329)  - Day 38
# ==========================================================================
class SolutionLongestPath:
    def longestIncreasingPath(self, matrix):
        """위상 정렬(Kahn) 층 벗기기.  O(m*n). 재귀 0줄이라 파이썬에서 안전하다.
        '값이 커지는 방향'으로만 간선을 그으면 이 격자는 DAG 다."""
        if not matrix or not matrix[0]:
            return 0
        m, nn = len(matrix), len(matrix[0])
        outdeg = [[0] * nn for _ in range(m)]  # 더 큰 이웃의 수
        for i in range(m):
            for j in range(nn):
                v = matrix[i][j]
                cnt = 0
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < nn and matrix[ni][nj] > v:
                        cnt += 1
                outdeg[i][j] = cnt
        # 진출 차수 0 = 주변에 더 큰 값이 없는 칸 = 경로의 끝
        dq = deque((i, j) for i in range(m) for j in range(nn) if outdeg[i][j] == 0)
        depth = 0
        while dq:
            depth += 1
            for _ in range(len(dq)):           # 한 층씩 벗긴다
                i, j = dq.popleft()
                v = matrix[i][j]
                for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < nn and matrix[ni][nj] < v:
                        outdeg[ni][nj] -= 1
                        if outdeg[ni][nj] == 0:
                            dq.append((ni, nj))
        return depth

    def longestIncreasingPathMemo(self, matrix):
        """접근 2: 메모이제이션 DFS(명시적 스택).  O(m*n).
        DAG 이므로 visited 배열이 필요 없다 - 되돌아올 수 없기 때문이다."""
        if not matrix or not matrix[0]:
            return 0
        m, nn = len(matrix), len(matrix[0])
        memo = [[0] * nn for _ in range(m)]

        def compute(si, sj):
            stack = [(si, sj, False)]
            while stack:
                i, j, expanded = stack.pop()
                if memo[i][j]:
                    continue
                v = matrix[i][j]
                if expanded:
                    best = 1
                    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < m and 0 <= nj < nn and matrix[ni][nj] > v:
                            if memo[ni][nj] + 1 > best:
                                best = memo[ni][nj] + 1
                    memo[i][j] = best
                else:
                    stack.append((i, j, True))
                    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ni, nj = i + di, j + dj
                        if (0 <= ni < m and 0 <= nj < nn
                                and matrix[ni][nj] > v and not memo[ni][nj]):
                            stack.append((ni, nj, False))

        best = 0
        for i in range(m):
            for j in range(nn):
                if not memo[i][j]:
                    compute(i, j)
                if memo[i][j] > best:
                    best = memo[i][j]
        return best


# ==========================================================================
# 9. Replace Words  (LeetCode #648)  - Day 39
# ==========================================================================
END = "#"


class SolutionReplaceWords:
    def replaceWords(self, dictionary, sentence):
        """중첩 dict 트라이.  O(사전 총 길이 + 문장 총 길이).
        내려가다 처음 만난 END 가 곧 '가장 짧은 어근'이다."""
        root = {}
        for w in dictionary:
            node = root
            for ch in w:
                node = node.setdefault(ch, {})
            node[END] = True                   # 끝 표시 필수

        def shortest_root(word):
            node = root
            for i, ch in enumerate(word):
                if ch not in node:
                    return word
                node = node[ch]
                if END in node:
                    return word[:i + 1]
            return word

        return " ".join(shortest_root(w) for w in sentence.split())

    def replaceWordsSet(self, dictionary, sentence):
        """접근 2: 어근 길이가 <= 100 이므로 접두사를 잘라 set 조회.
        O(단어 수 * 어근 최대 길이). 코드가 훨씬 짧다."""
        roots = set(dictionary)
        limit = max(len(w) for w in dictionary)

        def shortest_root(word):
            for i in range(1, min(len(word), limit) + 1):
                if word[:i] in roots:
                    return word[:i]            # 짧은 것부터 보므로 첫 발견이 답
            return word

        return " ".join(shortest_root(w) for w in sentence.split())


# ==========================================================================
# 10. Create Sorted Array through Instructions  (LeetCode #1649)  - Day 40
# ==========================================================================
class BIT:
    """펜윅 트리. 1-based 필수 (i & -i 가 0 에서 무한 루프)."""

    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.t[i] += v
            i += i & -i

    def query(self, i):
        """[1, i] 합."""
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s


def _bisect_right(a, x):
    """bisect_right 를 손으로 - '같은 값' 처리를 코드에 드러내기 위해."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x:
            lo = mid + 1
        else:
            hi = mid
    return lo


class SolutionCreateSorted:
    def createSortedArray(self, instructions):
        """펜윅 + 좌표 압축.  O(N log N).
        '나보다 작은 것이 몇 개'를 세는 Phase 4 최고의 관용구."""
        vals = sorted(set(instructions))
        rank = {v: i + 1 for i, v in enumerate(vals)}   # 1-based 로 압축
        bit = BIT(len(vals))
        total = 0
        for i, x in enumerate(instructions):
            r = rank[x]
            smaller = bit.query(r - 1)         # x 미만의 개수
            greater = i - bit.query(r)         # i 개 중 x 이하를 뺀 나머지
            total += smaller if smaller < greater else greater
            bit.add(r, 1)                      # 세고 난 뒤에 넣는다
        return total % MOD

    def createSortedArrayNaive(self, instructions):
        """접근 2: bisect.insort 나이브.  O(N^2) 이지만 작은 입력에서 정답 대조용."""
        arr = []
        total = 0
        for x in instructions:
            lo = bisect_left(arr, x)           # x 미만의 개수
            hi = len(arr) - _bisect_right(arr, x)   # x 초과의 개수
            total += lo if lo < hi else hi
            insort(arr, x)
        return total % MOD


# ==========================================================================
# 11. Smallest Sufficient Team  (LeetCode #1125)  - Day 41
# ==========================================================================
class SolutionSufficientTeam:
    def smallestSufficientTeam(self, req_skills, people):
        """비트마스크 DP.  O(people * 2^skills).
        상태로 삼을 것은 '기술 집합'이지 '사람 집합'이 아니다(사람은 60명)."""
        skill_id = {s: i for i, s in enumerate(req_skills)}
        full = (1 << len(req_skills)) - 1
        dp = {0: []}
        for i, person in enumerate(people):
            pmask = 0
            for s in person:
                if s in skill_id:
                    pmask |= 1 << skill_id[s]
            if pmask == 0:
                continue
            for cur, team in list(dp.items()):  # 스냅샷! 동시 수정 금지
                nxt = cur | pmask
                if nxt == cur:                  # 보태는 게 없다
                    continue
                if nxt not in dp or len(dp[nxt]) > len(team) + 1:
                    dp[nxt] = team + [i]
        return dp[full]

    def smallestSufficientTeamCount(self, req_skills, people):
        """접근 2: 팀 크기만 dp[mask] 로 구하는 최소 버전.
        위 구현이 정말 '최소 크기'인지 대조하는 데 쓴다."""
        skill_id = {s: i for i, s in enumerate(req_skills)}
        full = (1 << len(req_skills)) - 1
        INF = float("inf")
        dp = [INF] * (full + 1)
        dp[0] = 0
        masks = []
        for person in people:
            pmask = 0
            for s in person:
                if s in skill_id:
                    pmask |= 1 << skill_id[s]
            masks.append(pmask)
        for cur in range(full + 1):
            if dp[cur] == INF:
                continue
            for pmask in masks:
                nxt = cur | pmask
                if dp[cur] + 1 < dp[nxt]:
                    dp[nxt] = dp[cur] + 1
        return dp[full]


# ==========================================================================
# 12. Longest Happy Prefix  (LeetCode #1392)  - Day 42
# ==========================================================================
class SolutionHappyPrefix:
    def longestPrefix(self, s):
        """KMP 실패 함수.  pi[-1] 이 곧 답이다.  O(N).
        '접두사이자 접미사인 최장' 이 pi 배열의 정의 그 자체다."""
        pi = [0] * len(s)
        j = 0
        for i in range(1, len(s)):
            while j and s[i] != s[j]:
                j = pi[j - 1]                  # while! if 로 쓰면 조용히 틀린다
            if s[i] == s[j]:
                j += 1
                pi[i] = j
        return s[:pi[-1]]

    def longestPrefixHash(self, s, base=131, mod=(1 << 61) - 1):
        """접근 2: 롤링 해시(라빈-카프).  O(N) 기대. 충돌 검증을 반드시 넣는다."""
        n = len(s)
        pre = suf = 0
        power = 1
        best = 0
        for k in range(1, n):                  # 길이 k 를 늘려 가며 비교
            pre = (pre * base + ord(s[k - 1])) % mod
            suf = (suf + ord(s[n - k]) * power) % mod
            power = power * base % mod
            if pre == suf and s[:k] == s[n - k:]:   # 충돌 검증 필수
                best = k
        return s[:best]


# ==========================================================================
# 13. Minimum Time to Collect All Apples in a Tree  (LeetCode #1443)
#     - Day 43, 44
# ==========================================================================
class SolutionCollectApples:
    def minTime(self, n, edges, hasApple):
        """반복 후위 순회 트리 DP.  O(N). 재귀 0줄이라 N=10^5 체인에서도 안전하다.
        핵심 관찰: 서브트리에 사과가 있으면 그 간선을 왕복(2초) 해야 한다."""
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        # BFS 로 parent 와 방문 순서를 만든다 (부모가 자식보다 앞에 온다)
        parent = [-1] * n
        visited = [False] * n
        visited[0] = True
        order = [0]
        dq = deque([0])
        while dq:
            v = dq.popleft()
            for w in adj[v]:
                if not visited[w]:
                    visited[w] = True
                    parent[w] = v
                    order.append(w)
                    dq.append(w)
        need = list(hasApple)
        total = 0
        for v in reversed(order):              # 뒤집으면 후위 순회
            if v != 0 and need[v]:             # 루트는 부모가 없으므로 제외
                need[parent[v]] = True
                total += 2
        return total

    def minTimeRecursive(self, n, edges, hasApple):
        """접근 2: 재귀 DFS.  O(N). 짧지만 깊은 트리에서 RecursionError 가 난다."""
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        def dfs(v, p):
            cost = 0
            for w in adj[v]:
                if w == p:                     # 부모로 되돌아가지 않는다
                    continue
                sub = dfs(w, v)
                if sub > 0 or hasApple[w]:
                    cost += sub + 2
            return cost

        return dfs(0, -1)


# ==========================================================================
# 테스트
# ==========================================================================
def test_1_coin_change():
    s = SolutionCoinChange()
    assert s.coinChange([1, 2, 5], 11) == 3
    assert s.coinChange([2], 3) == -1
    assert s.coinChange([1], 0) == 0
    assert s.coinChange([1], 1) == 1
    assert s.coinChange([2, 5, 10, 1], 27) == 4
    for coins, amt in [([1, 2, 5], 11), ([2], 3), ([1], 0),
                       ([186, 419, 83, 408], 6249)]:
        assert s.coinChange(coins, amt) == s.coinChangeBFS(coins, amt)
    print("1.  Coin Change (#322)                  OK  - DP / BFS 일치")


def test_2_lcs():
    s = SolutionLCS()
    assert s.longestCommonSubsequence("abcde", "ace") == 3
    assert s.longestCommonSubsequence("abc", "abc") == 3
    assert s.longestCommonSubsequence("abc", "def") == 0
    rng = random.Random(1143)
    for _ in range(200):
        a = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
        b = "".join(rng.choice("abc") for _ in range(rng.randint(0, 12)))
        assert s.longestCommonSubsequence(a, b) == s.longestCommonSubsequence2D(a, b)
    print("2.  Longest Common Subsequence (#1143)  OK  - 1D 롤링 / 2D 일치")


def test_3_lis():
    s = SolutionLIS()
    assert s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert s.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4
    assert s.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]) == 1
    rng = random.Random(300)
    for _ in range(200):
        arr = [rng.randint(-20, 20) for _ in range(rng.randint(1, 25))]
        assert s.lengthOfLIS(arr) == s.lengthOfLISQuadratic(arr)
        seq = s.actualLIS(arr)                 # 복원한 수열이 실제로 유효한가
        assert len(seq) == s.lengthOfLIS(arr)
        assert all(seq[i] < seq[i + 1] for i in range(len(seq) - 1))
    print("3.  Longest Increasing Subseq (#300)    OK  - NlogN / N^2 일치, 수열 복원 검증")


def test_4_delivery():
    road = [[1, 2, 1], [2, 3, 3], [5, 2, 2], [1, 4, 2], [5, 3, 1], [5, 4, 2]]
    assert solution_delivery(5, road, 3) == 4
    road2 = [[1, 2, 1], [1, 3, 2], [2, 3, 2], [3, 4, 3], [3, 5, 2], [3, 5, 3],
             [5, 6, 1], [1, 6, 9]]
    assert solution_delivery(6, road2, 4) == 4     # 중복 간선 [3,5,2] / [3,5,3]
    for n, r, k in [(5, road, 3), (6, road2, 4), (1, [[1, 1, 1]], 1)]:
        assert solution_delivery(n, r, k) == solution_delivery_dijkstra(n, r, k)
    print("4.  배달 (프로그래머스 #12978)          OK  - 플로이드 / 다익스트라 일치")


def test_5_network_delay():
    s = SolutionNetworkDelay()
    assert s.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert s.networkDelayTime([[1, 2, 1]], 2, 1) == 1
    assert s.networkDelayTime([[1, 2, 1]], 2, 2) == -1
    rng = random.Random(743)
    for _ in range(80):
        n = rng.randint(2, 7)
        times = []
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v and rng.random() < 0.4:
                    times.append([u, v, rng.randint(1, 10)])
        k = rng.randint(1, n)
        a = s.networkDelayTime(times, n, k)
        b = s.networkDelayTimeBellman(times, n, k)
        c = s.networkDelayTimeFloyd(times, n, k)
        assert a == b == c, (times, n, k, a, b, c)
    print("5.  Network Delay Time (#743)           OK  - 다익스트라/벨만포드/플로이드 3자 일치")


def test_6_provinces():
    s = SolutionProvinces()
    assert s.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert s.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
    assert s.findCircleNum([[1]]) == 1
    rng = random.Random(547)
    for _ in range(150):
        n = rng.randint(1, 9)
        m = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.3:
                    m[i][j] = m[j][i] = 1
        assert s.findCircleNum(m) == s.findCircleNumDFS(m)
    print("6.  Number of Provinces (#547)          OK  - 유니온파인드 / DFS 일치")


def test_7_islands():
    costs = [[0, 1, 1], [0, 2, 2], [1, 2, 5], [1, 3, 1], [2, 3, 8]]
    assert solution_islands(4, costs) == 4
    assert solution_islands(1, []) == 0            # 섬이 하나면 다리가 필요 없다
    rng = random.Random(42861)
    for _ in range(150):
        n = rng.randint(1, 8)
        edges = []
        for i in range(1, n):                      # 연결성을 보장하는 뼈대
            edges.append([rng.randint(0, i - 1), i, rng.randint(1, 100)])
        for _ in range(rng.randint(0, 6)):         # 여분 간선
            a, b = rng.randint(0, n - 1), rng.randint(0, n - 1)
            if a != b:
                edges.append([a, b, rng.randint(1, 100)])
        assert solution_islands(n, edges) == solution_islands_prim(n, edges)
    print("7.  섬 연결하기 (프로그래머스 #42861)   OK  - 크루스칼 / 프림 일치")


def test_8_longest_path():
    s = SolutionLongestPath()
    assert s.longestIncreasingPath([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
    assert s.longestIncreasingPath([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4
    assert s.longestIncreasingPath([[1]]) == 1
    rng = random.Random(329)
    for _ in range(150):
        m, nn = rng.randint(1, 5), rng.randint(1, 5)
        mat = [[rng.randint(0, 9) for _ in range(nn)] for _ in range(m)]
        assert s.longestIncreasingPath(mat) == s.longestIncreasingPathMemo(mat), mat
    print("8.  Longest Increasing Path (#329)      OK  - 위상정렬 / 메모이제이션 일치")


def test_9_replace_words():
    s = SolutionReplaceWords()
    assert (s.replaceWords(["cat", "bat", "rat"],
                           "the cattle was rattled by the battery")
            == "the cat was rat by the bat")
    assert (s.replaceWords(["a", "b", "c"], "aadsfasf absbs bbab cadsfafs")
            == "a a b c")
    # 어근 후보가 둘이면 '가장 짧은' 것을 골라야 한다 (catt 가 아니라 cat)
    assert (s.replaceWords(["catt", "cat", "bat", "rat"],
                           "the cattle was rattled by the battery")
            == "the cat was rat by the bat")
    rng = random.Random(648)
    for _ in range(150):
        dic = list({"".join(rng.choice("ab") for _ in range(rng.randint(1, 3)))
                    for _ in range(rng.randint(1, 5))})
        sent = " ".join("".join(rng.choice("ab") for _ in range(rng.randint(1, 5)))
                        for _ in range(rng.randint(1, 5)))
        assert s.replaceWords(dic, sent) == s.replaceWordsSet(dic, sent)
    print("9.  Replace Words (#648)                OK  - 트라이 / set 일치")


def test_10_create_sorted():
    s = SolutionCreateSorted()
    assert s.createSortedArray([1, 5, 6, 2]) == 1
    assert s.createSortedArray([1, 2, 3, 6, 5, 4]) == 3
    assert s.createSortedArray([1, 3, 3, 3, 2, 4, 2, 1, 2]) == 4
    # 중복 값이 많은 입력으로 '같은 값 처리'를 집중 검증한다
    rng = random.Random(1649)
    for _ in range(200):
        arr = [rng.randint(1, 8) for _ in range(rng.randint(1, 20))]
        assert s.createSortedArray(arr) == s.createSortedArrayNaive(arr), arr
    print("10. Create Sorted Array (#1649)         OK  - 펜윅 / 나이브 일치 (중복 값 포함)")


def test_11_sufficient_team():
    s = SolutionSufficientTeam()
    team = s.smallestSufficientTeam(["java", "nodejs", "reactjs"],
                                    [["java"], ["nodejs"], ["nodejs", "reactjs"]])
    assert sorted(team) == [0, 2]
    req = ["algorithms", "math", "java", "reactjs", "csharp", "aws"]
    ppl = [["algorithms", "math", "java"], ["algorithms", "math", "reactjs"],
           ["java", "csharp", "aws"], ["reactjs", "csharp"],
           ["csharp", "math"], ["aws", "java"]]
    team2 = s.smallestSufficientTeam(req, ppl)
    # 인덱스만 받고 끝내면 안 된다 - 정말 '충분한 팀'인지 검증한다
    covered = set()
    for i in team2:
        covered |= set(ppl[i])
    assert set(req) <= covered
    assert len(team2) == s.smallestSufficientTeamCount(req, ppl)   # 최소성 대조
    rng = random.Random(1125)
    checked = 0
    for _ in range(120):
        k = rng.randint(1, 6)
        req_r = ["s%d" % i for i in range(k)]
        ppl_r = [[x for x in req_r if rng.random() < 0.5]
                 for _ in range(rng.randint(1, 7))]
        all_skills = set()
        for p in ppl_r:
            all_skills |= set(p)
        if all_skills != set(req_r):           # 답이 존재하는 경우만 검사
            continue
        got = s.smallestSufficientTeam(req_r, ppl_r)
        cov = set()
        for i in got:
            cov |= set(ppl_r[i])
        assert set(req_r) <= cov
        assert len(got) == s.smallestSufficientTeamCount(req_r, ppl_r)
        checked += 1
    assert checked > 0
    print("11. Smallest Sufficient Team (#1125)    OK  - 커버 검증 + 최소성 대조 (%d 케이스)"
          % checked)


def test_12_happy_prefix():
    s = SolutionHappyPrefix()
    assert s.longestPrefix("level") == "l"
    assert s.longestPrefix("ababab") == "abab"
    assert s.longestPrefix("leetcodeleet") == "leet"
    assert s.longestPrefix("a") == ""

    def brute(t):
        for k in range(len(t) - 1, 0, -1):
            if t[:k] == t[len(t) - k:]:
                return t[:k]
        return ""

    rng = random.Random(1392)
    for _ in range(300):
        t = "".join(rng.choice("ab") for _ in range(rng.randint(1, 14)))
        expected = brute(t)
        assert s.longestPrefix(t) == expected, t
        assert s.longestPrefixHash(t) == expected, t
    print("12. Longest Happy Prefix (#1392)        OK  - KMP / 롤링해시 / 완전탐색 3자 일치")


def test_13_collect_apples():
    s = SolutionCollectApples()
    edges = [[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]]
    assert s.minTime(7, edges, [False, False, True, False, True, True, False]) == 8
    assert s.minTime(7, edges, [False, False, True, False, False, True, False]) == 6
    assert s.minTime(7, edges, [False] * 7) == 0
    assert s.minTime(1, [], [False]) == 0
    assert s.minTime(1, [], [True]) == 0       # 루트에 사과 -> 이동 불필요
    rng = random.Random(1443)
    for _ in range(200):
        n = rng.randint(1, 12)
        e = [[rng.randint(0, i - 1), i] for i in range(1, n)]
        apples = [rng.random() < 0.4 for _ in range(n)]
        assert s.minTime(n, e, apples) == s.minTimeRecursive(n, e, apples)
    # 체인 트리에서 반복 버전이 살아남는지 (재귀는 여기서 RecursionError)
    big = 20000
    chain = [[i - 1, i] for i in range(1, big)]
    apples_big = [False] * big
    apples_big[-1] = True
    assert s.minTime(big, chain, apples_big) == 2 * (big - 1)
    print("13. Collect Apples in a Tree (#1443)    OK  - 반복/재귀 일치, 체인 20,000 생존")


def test_decision_map():
    """제약 -> 도구 판정 자체 테스트. 문제를 읽고 30초 안에 해야 하는 판단."""
    cases = [
        ("#322  Coin Change     amount<=1e4", 10 ** 4, "O(N log N)", "31,32"),
        ("#1143 LCS             len<=1000", 1000, "O(N^2)", "33"),
        ("#300  LIS             N<=2500", 2500, "O(N^2)", "33,18"),
        ("#12978 배달           N<=50", 50, "O(N^3)", "34,35"),
        ("#743  Network Delay   n<=100", 100, "O(N^3)", "34,35"),
        ("#547  Provinces       n<=200", 200, "O(N^3)", "36"),
        ("#42861 섬 연결하기    n<=100", 100, "O(N^3)", "36,37"),
        ("#329  Longest Path    m*n<=40000", 40000, "O(N log N)", "38"),
        ("#648  Replace Words   len<=1e6", 10 ** 6, "O(N)", "39"),
        ("#1649 Create Sorted   N<=1e5", 10 ** 5, "O(N log N)", "40"),
        ("#1125 Team            skills<=16", 16, "O(2^N * N)", "41"),
        ("#1392 Happy Prefix    N<=1e5", 10 ** 5, "O(N log N)", "42"),
        ("#1443 Apples          n<=1e5", 10 ** 5, "O(N log N)", "43,44"),
    ]

    def allowed_for(n):
        if n <= 12:
            return "O(N!)"
        if n <= 20:
            return "O(2^N * N)"
        if n <= 400:
            return "O(N^3)"
        if n <= 5000:
            return "O(N^2)"
        if n <= 100000:
            return "O(N log N)"
        if n <= 1000000:
            return "O(N)"
        return "O(log N)"

    print("%-36s %-14s %s" % ("문제 (제약)", "허용 복잡도", "복습 Day"))
    print(SUB)
    for name, n, expected, day in cases:
        got = allowed_for(n)
        assert got == expected, (name, got, expected)
        print("%-36s %-14s Day %s" % (name, got, day))
    print(SUB)
    print("13문제 전부 '제약 -> 허용 복잡도' 판정이 일치한다")


def main():
    print(SEP)
    print("Day 45 해설 - Phase 4 심화 종합 복습 (13문제)")
    print(SEP)
    test_1_coin_change()
    test_2_lcs()
    test_3_lis()
    test_4_delivery()
    test_5_network_delay()
    test_6_provinces()
    test_7_islands()
    test_8_longest_path()
    test_9_replace_words()
    test_10_create_sorted()
    test_11_sufficient_team()
    test_12_happy_prefix()
    test_13_collect_apples()
    print()
    print(SEP)
    print("[제약 -> 도구] 판정 자체 테스트")
    print(SEP)
    test_decision_map()
    print(SEP)
    print("전체 테스트 통과 - Phase 4 (Day 31~44) 복습 완료")
    print("막힌 문제가 있었다면 해당 Day 의 problems.md 를 다시 푸세요")
    print(SEP)


if __name__ == "__main__":
    main()
