# -*- coding: utf-8 -*-
"""
Day 36 - 서로소 집합 (Union-Find / Disjoint Set) 해설

플랫폼 시그니처 유지:
  - LeetCode  : class Solution 의 메서드
  - 프로그래머스 : def solution(...)
각 문제에 assert 자체 테스트 포함. 가능한 곳은 다중 접근(Union-Find vs DFS) + 비교.

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import defaultdict


# ===========================================================================
# 공용 DSU (경로 압축 + 사이즈 합치기)
# ===========================================================================
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n                      # 연결 요소 수

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:       # 경로 압축
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                    # 이미 같은 그룹 -> 사이클
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True


# ===========================================================================
# 1. Number of Provinces (LeetCode #547) - 연결 요소 개수
#    접근 A: Union-Find.  접근 B: DFS.
#    시간 O(n^2 * alpha) / O(n^2).
# ===========================================================================
class SolutionProvinces:
    def findCircleNum(self, isConnected):
        n = len(isConnected)
        dsu = DSU(n)
        for i in range(n):
            for j in range(i + 1, n):           # 상삼각만
                if isConnected[i][j] == 1:
                    dsu.union(i, j)
        return dsu.count

    def findCircleNum_dfs(self, isConnected):
        n = len(isConnected)
        seen = [False] * n

        def dfs(u):
            for v in range(n):
                if isConnected[u][v] == 1 and not seen[v]:
                    seen[v] = True
                    dfs(v)

        cnt = 0
        for i in range(n):
            if not seen[i]:
                seen[i] = True
                dfs(i)
                cnt += 1
        return cnt


# ===========================================================================
# 2. 네트워크 (프로그래머스 #43162) - 연결 요소 개수
#    computers[i][j] == 1 이면 union. 답은 서로 다른 root 수.
# ===========================================================================
def solution(n, computers):
    dsu = DSU(n)
    for i in range(n):
        for j in range(i + 1, n):
            if computers[i][j] == 1:
                dsu.union(i, j)
    return dsu.count


# ===========================================================================
# 3. Redundant Connection (LeetCode #684) - 무방향 사이클 판별
#    union 이 처음 실패하는 간선이 정답(가장 뒤 간선).
#    시간 O(n * alpha).
# ===========================================================================
class SolutionRedundant:
    def findRedundantConnection(self, edges):
        n = len(edges)                          # 노드 1..n
        dsu = DSU(n + 1)
        for a, b in edges:
            if not dsu.union(a, b):             # 이미 연결됨 -> 이 간선이 여분
                return [a, b]
        return []


# ===========================================================================
# 4. Satisfiability of Equality Equations (LeetCode #990)
#    등식(==) 먼저 union, 부등식(!=)에서 같은 그룹이면 모순.
#    시간 O(len(equations) * alpha).
# ===========================================================================
class SolutionEquations:
    def equationsPossible(self, equations):
        dsu = DSU(26)
        for eq in equations:                    # 1-pass: == 먼저
            if eq[1] == '=':
                a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
                dsu.union(a, b)
        for eq in equations:                    # 2-pass: != 검사
            if eq[1] == '!':
                a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
                if dsu.find(a) == dsu.find(b):
                    return False
        return True


# ===========================================================================
# 5. Number of Operations to Make Network Connected (LeetCode #1319)
#    간선이 n-1 개 미만이면 -1. 아니면 답 = 컴포넌트 수 - 1.
#    시간 O((n + E) * alpha).
# ===========================================================================
class SolutionConnect:
    def makeConnected(self, n, connections):
        if len(connections) < n - 1:            # 케이블 부족 -> 불가능
            return -1
        dsu = DSU(n)
        for a, b in connections:
            dsu.union(a, b)
        return dsu.count - 1                     # 컴포넌트 c개 -> c-1 번 이동


# ===========================================================================
# 6. Accounts Merge (LeetCode #721) - 문자열 dict 인덱싱 + 그룹핑
#    접근 A: Union-Find (계정 인덱스를 union).
#    접근 B: 이메일 그래프 DFS.
# ===========================================================================
class SolutionAccounts:
    def accountsMerge(self, accounts):
        dsu = DSU(len(accounts))
        email_owner = {}                        # 이메일 -> 최초 계정 인덱스
        for i, acc in enumerate(accounts):
            for email in acc[1:]:
                if email in email_owner:
                    dsu.union(i, email_owner[email])   # 같은 사람
                else:
                    email_owner[email] = i
        # root 별로 이메일 모으기
        groups = defaultdict(set)
        for email, owner in email_owner.items():
            groups[dsu.find(owner)].add(email)
        res = []
        for root, emails in groups.items():
            name = accounts[root][0]
            res.append([name] + sorted(emails))
        return res

    def accountsMerge_dfs(self, accounts):
        graph = defaultdict(set)                # 이메일 그래프
        email_name = {}
        for acc in accounts:
            first = acc[1]
            for email in acc[1:]:
                graph[first].add(email)
                graph[email].add(first)
                email_name[email] = acc[0]
        seen, res = set(), []
        for email in email_name:
            if email in seen:
                continue
            stack, comp = [email], []
            seen.add(email)
            while stack:                        # DFS 로 연결된 이메일 수집
                cur = stack.pop()
                comp.append(cur)
                for nxt in graph[cur]:
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            res.append([email_name[email]] + sorted(comp))
        return res


def _norm(list_of_accounts):
    # 계정 리스트 비교용 정규화(순서 무관)
    return sorted([[acc[0]] + sorted(acc[1:]) for acc in list_of_accounts])


def run_tests():
    print("=" * 60)
    print("Day 36 - Union-Find (Disjoint Set) 해설 self-test")
    print("=" * 60)

    # 1. Number of Provinces - 두 접근 동일
    pr = SolutionProvinces()
    cases1 = [
        ([[1, 1, 0], [1, 1, 0], [0, 0, 1]], 2),
        ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1),
    ]
    for mat, exp in cases1:
        assert pr.findCircleNum(mat) == exp
        assert pr.findCircleNum_dfs(mat) == exp
    print("[1] Number of Provinces (UF == DFS)     OK")

    # 2. 네트워크 (프로그래머스)
    assert solution(3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert solution(3, [[1, 1, 0], [1, 1, 1], [0, 1, 1]]) == 1
    print("[2] 네트워크 (연결 요소)                OK")

    # 3. Redundant Connection
    rd = SolutionRedundant()
    assert rd.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert rd.findRedundantConnection(
        [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    print("[3] Redundant Connection (사이클)       OK")

    # 4. Satisfiability of Equality Equations
    eq = SolutionEquations()
    assert eq.equationsPossible(["a==b", "b!=a"]) is False
    assert eq.equationsPossible(["b==a", "a==b"]) is True
    assert eq.equationsPossible(["a==b", "b==c", "a==c"]) is True
    assert eq.equationsPossible(["a==b", "b!=c", "c==a"]) is False
    assert eq.equationsPossible(["c==c", "b==d", "x!=z"]) is True
    print("[4] Satisfiability of Equations         OK")

    # 5. Number of Operations to Make Network Connected
    cn = SolutionConnect()
    assert cn.makeConnected(4, [[0, 1], [0, 2], [1, 2]]) == 1
    assert cn.makeConnected(
        6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]) == 2
    assert cn.makeConnected(6, [[0, 1], [0, 2], [0, 3], [1, 2]]) == -1
    assert cn.makeConnected(5, [[0, 1], [0, 2], [3, 4], [2, 3]]) == 0
    print("[5] Make Network Connected (컴포넌트-1)  OK")

    # 6. Accounts Merge - 두 접근 동일
    ac = SolutionAccounts()
    accounts = [
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ]
    expected = [
        ["John", "john00@mail.com", "john_newyork@mail.com",
         "johnsmith@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ]
    assert _norm(ac.accountsMerge(accounts)) == _norm(expected)
    assert _norm(ac.accountsMerge_dfs(accounts)) == _norm(expected)
    print("[6] Accounts Merge (UF == DFS)          OK")

    print("=" * 60)
    print("모든 테스트 통과 (All tests passed)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
