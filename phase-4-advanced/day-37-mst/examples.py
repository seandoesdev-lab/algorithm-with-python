# -*- coding: utf-8 -*-
"""
Day 37 - 최소 신장 트리 (MST: Kruskal / Prim) 예제

다루는 내용:
  1) DSU (Day 36 템플릿 재사용)
  2) 크루스칼 - 간선 정렬 + 사이클 회피            O(E log E)
  3) 프림(힙)  - 트리에 가장 싸게 붙는 정점 흡수    O(E log V)
  4) 프림(배열) - 밀집/완전 그래프용                O(V^2)
  5) 최대 신장 트리 - 정렬만 뒤집기
  6) 최소 병목 경로(minimax path) - MST 가 공짜로 줌
  7) MST 유일성 판정 - 간선 하나씩 빼고 재계산
  8) 연결되지 않은 그래프 - MST 없음(최소 신장 숲)

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""

import heapq


# ===========================================================================
# 1. DSU (경로 압축 + 사이즈 합치기) - Day 36 템플릿
# ===========================================================================
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n                       # 연결 요소 수

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:        # 경로 압축
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                     # 이미 같은 그룹 -> 사이클
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True


# ===========================================================================
# 2. 크루스칼 (Kruskal) - 간선 중심
#    edges: [(a, b, w), ...]  ->  (총비용, 채택 간선 리스트)
#    연결 불가면 (None, [])
# ===========================================================================
def kruskal(n, edges):
    dsu = DSU(n)
    total, picked = 0, []
    for a, b, w in sorted(edges, key=lambda e: e[2]):   # 가중치 오름차순
        if dsu.union(a, b):                  # 사이클이 아니면 채택
            total += w
            picked.append((a, b, w))
            if len(picked) == n - 1:         # V-1 개 모이면 조기 종료
                break
    if len(picked) != n - 1:                 # 간선이 모자람 -> 연결 불가
        return None, []
    return total, picked


# ===========================================================================
# 3. 프림 (Prim) - 힙 버전, 정점 중심
#    adj[u] = [(v, w), ...]
# ===========================================================================
def prim_heap(n, adj, start=0):
    visited = [False] * n
    heap = [(0, start)]                      # (간선 비용, 정점)
    total, cnt = 0, 0
    while heap and cnt < n:
        w, u = heapq.heappop(heap)
        if visited[u]:                       # 꺼낸 직후 검사가 핵심
            continue
        visited[u] = True
        total += w
        cnt += 1
        for v, cost in adj[u]:
            if not visited[v]:
                # 넣는 값은 cost(간선 하나). 다익스트라처럼 누적하지 않는다.
                heapq.heappush(heap, (cost, v))
    return total if cnt == n else None


# ===========================================================================
# 4. 프림 (Prim) - 배열 버전 O(V^2), 밀집/완전 그래프용
#    weight[u][v] = 간선 비용 (없으면 INF)
# ===========================================================================
def prim_dense(n, weight):
    INF = float('inf')
    dist = [INF] * n                         # 트리에 붙는 최소 간선 비용
    used = [False] * n
    dist[0] = 0
    total = 0
    for _ in range(n):
        u, best = -1, INF
        for i in range(n):                   # 안 쓴 정점 중 dist 최소
            if not used[i] and dist[i] < best:
                best, u = dist[i], i
        if u == -1:                          # 남은 정점에 닿을 수 없음
            return None
        used[u] = True
        total += best
        for v in range(n):                   # u 기준으로 dist 갱신
            if not used[v] and weight[u][v] < dist[v]:
                dist[v] = weight[u][v]
    return total


# ===========================================================================
# 5. 최대 신장 트리 - 정렬 방향만 뒤집는다
# ===========================================================================
def maximum_spanning_tree(n, edges):
    dsu = DSU(n)
    total, cnt = 0, 0
    for a, b, w in sorted(edges, key=lambda e: -e[2]):  # 내림차순
        if dsu.union(a, b):
            total += w
            cnt += 1
    return total if cnt == n - 1 else None


# ===========================================================================
# 6. 최소 병목 경로 (minimax path)
#    s~t 경로들 중 "최대 간선"이 가장 작은 값.
#    크루스칼을 돌리다 s, t 가 처음 연결되는 순간의 가중치가 답.
# ===========================================================================
def bottleneck(n, edges, s, t):
    if s == t:
        return 0
    dsu = DSU(n)
    for a, b, w in sorted(edges, key=lambda e: e[2]):
        dsu.union(a, b)
        if dsu.find(s) == dsu.find(t):
            return w
    return None                              # 연결 불가


# ===========================================================================
# 7. MST 유일성 판정
#    MST 간선을 하나씩 제거하고 다시 MST 를 구해
#    같은 비용의 다른 MST 가 나오면 유일하지 않다.
# ===========================================================================
def is_mst_unique(n, edges):
    base, picked = kruskal(n, edges)
    if base is None:
        return None                          # MST 자체가 없음
    for a, b, w in picked:
        rest = [e for e in edges if e != (a, b, w)]
        alt, _ = kruskal(n, rest)
        if alt is not None and alt == base:  # 같은 비용의 대체 MST 존재
            return False
    return True


def build_adj(n, edges):
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))                # 무방향
    return adj


def build_matrix(n, edges):
    INF = float('inf')
    mat = [[INF] * n for _ in range(n)]
    for a, b, w in edges:
        if w < mat[a][b]:                    # 중복 간선은 최솟값만
            mat[a][b] = mat[b][a] = w
    return mat


# ===========================================================================
# 데모
# ===========================================================================
def main():
    print("=" * 62)
    print("Day 37 - 최소 신장 트리 (MST: Kruskal / Prim)")
    print("=" * 62)

    # 예제 그래프 (정점 0..5)
    #         4
    #    0 ------- 1
    #    |       / |
    #  3 |   1 /   | 2
    #    |   /     |
    #    2 ------- 3 ---- 4 ---- 5
    #         4      2       6
    n = 6
    edges = [
        (0, 1, 4), (0, 2, 3), (1, 2, 1),
        (1, 3, 2), (2, 3, 4), (3, 4, 2), (4, 5, 6),
    ]

    print("\n[1] 크루스칼 (간선 정렬 + 사이클 회피)")
    total, picked = kruskal(n, edges)
    print("    정렬된 간선:", sorted(edges, key=lambda e: e[2]))
    print("    MST 총비용 :", total)
    print("    채택 간선  :", picked, " (개수 =", len(picked), "= V-1)")

    print("\n[2] 프림 - 힙 버전")
    adj = build_adj(n, edges)
    print("    MST 총비용 :", prim_heap(n, adj))

    print("\n[3] 프림 - 배열 버전 O(V^2)")
    mat = build_matrix(n, edges)
    print("    MST 총비용 :", prim_dense(n, mat))

    print("\n    -> 세 방법 모두 같은 최소 비용을 낸다.")
    assert total == prim_heap(n, adj) == prim_dense(n, mat) == 14

    print("\n[4] 최대 신장 트리 (정렬만 내림차순으로)")
    print("    최대 비용  :", maximum_spanning_tree(n, edges))

    print("\n[5] 최소 병목 경로 (경로상 최대 간선의 최솟값)")
    for s, t in [(0, 4), (0, 5), (1, 3)]:
        print("    " + str(s) + " -> " + str(t) + " 병목 =",
              bottleneck(n, edges, s, t))
    print("    0->5 는 (4,5,6) 이 유일한 통로라 병목이 6 으로 커진다.")

    print("\n[6] MST 유일성 판정")
    print("    예제 그래프 MST 유일? :", is_mst_unique(n, edges))
    tri = [(0, 1, 1), (1, 2, 1), (0, 2, 1)]   # 모두 같은 가중치
    print("    삼각형(가중치 전부 1) 유일? :", is_mst_unique(3, tri),
          " -> MST 가 3 가지")
    print("    비용 자체는 항상 유일:", kruskal(3, tri)[0])

    print("\n[7] 연결되지 않은 그래프")
    broken = [(0, 1, 1), (2, 3, 1)]           # 0-1 과 2-3 이 따로 논다
    t2, p2 = kruskal(4, broken)
    print("    kruskal 결과 :", t2, "(None = MST 없음, 최소 신장 숲만 존재)")
    print("    prim  결과   :", prim_heap(4, build_adj(4, broken)))
    print("    -> 채택 간선", len(p2), "개 != V-1 =", 4 - 1, "이므로 불가 판정")

    print("\n[8] 음수 가중치도 MST 는 문제없다 (다익스트라와 다른 점)")
    neg = [(0, 1, -5), (1, 2, 3), (0, 2, 2)]
    print("    간선:", neg)
    print("    MST :", kruskal(3, neg))
    print("    -> 음수 간선은 정렬상 맨 앞이라 무조건 먼저 채택된다.")

    print("\n" + "=" * 62)
    print("정리")
    print("=" * 62)
    print("  크루스칼 : 싼 간선부터, 사이클이면 패스   O(E log E)")
    print("  프림     : 트리에 가장 싸게 붙는 정점 흡수 O(E log V) / O(V^2)")
    print("  간선 리스트 입력 -> 크루스칼, 밀집 그래프 -> 프림 배열판")
    print("  MST 는 무방향 전용. 음수 OK. MST 경로 != 최단 경로.")
    print("=" * 62)


if __name__ == "__main__":
    main()
