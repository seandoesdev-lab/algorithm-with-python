# -*- coding: utf-8 -*-
"""
Day 35 - 최단 경로: 벨만-포드 & 플로이드-워셜 예제

핵심 골격 6종:
  (1) 벨만-포드           - 단일 출발 최단 거리 + 음수 사이클 판별
  (2) 벨만-포드 (경로 복원) - parent 로 실제 최단 경로 재구성
  (3) 플로이드-워셜        - 모든 쌍(all-pairs) 최단 거리 (k 최외곽)
  (4) 플로이드-워셜 (경로 복원) - nxt 행렬로 경로 재구성
  (5) 전이 폐포(도달성)     - min/+ 대신 or/and
  (6) K-제약 벨만-포드      - 간선 K개 이하 최단 (스냅샷)

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""

INF = float("inf")


# ---------------------------------------------------------------------------
# (1) 벨만-포드 - 단일 출발 최단 거리 + 음수 사이클 판별
#     edges = [(u, v, w), ...]  (방향 그래프, 음수 w 허용)
#     반환: dist 리스트, 음수 사이클이면 None
# ---------------------------------------------------------------------------
def bellman_ford(n, edges, start):
    dist = [INF] * n
    dist[start] = 0
    for _ in range(n - 1):                      # V-1 라운드
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w           # 완화(relaxation)
                updated = True
        if not updated:                         # 조기 종료(early exit)
            break
    for u, v, w in edges:                       # +1 라운드: 또 줄면 음수 사이클
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None                         # NEGATIVE CYCLE
    return dist


# ---------------------------------------------------------------------------
# (2) 벨만-포드 경로 복원 - parent 추적
# ---------------------------------------------------------------------------
def bellman_ford_path(n, edges, start, end):
    dist = [INF] * n
    parent = [-1] * n
    dist[start] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    if dist[end] == INF:
        return INF, []
    path, cur = [], end
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    return dist[end], path[::-1]


# ---------------------------------------------------------------------------
# (3) 플로이드-워셜 - 모든 쌍 최단 거리. k 가 반드시 최외곽 루프!
# ---------------------------------------------------------------------------
def floyd_warshall(n, edges):
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)         # 중복 간선은 최솟값만
    for k in range(n):                          # 경유지 (최외곽)
        for i in range(n):
            if dist[i][k] == INF:               # 가지치기
                continue
            dik = dist[i][k]
            row_k = dist[k]
            row_i = dist[i]
            for j in range(n):
                if dik + row_k[j] < row_i[j]:
                    row_i[j] = dik + row_k[j]
    return dist


# ---------------------------------------------------------------------------
# (4) 플로이드-워셜 경로 복원 - nxt[i][j] = i에서 j로 갈 때 다음 정점
# ---------------------------------------------------------------------------
def floyd_warshall_path(n, edges):
    dist = [[INF] * n for _ in range(n)]
    nxt = [[-1] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
            nxt[u][v] = v
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    def build_path(i, j):
        if nxt[i][j] == -1:
            return []
        path = [i]
        while i != j:
            i = nxt[i][j]
            path.append(i)
        return path

    return dist, build_path


# ---------------------------------------------------------------------------
# (5) 전이 폐포(transitive closure) - 도달성. min/+ 대신 or/and
# ---------------------------------------------------------------------------
def transitive_closure(n, directed_edges):
    reach = [[False] * n for _ in range(n)]
    for u, v in directed_edges:
        reach[u][v] = True
    for k in range(n):
        for i in range(n):
            if not reach[i][k]:
                continue
            for j in range(n):
                if reach[k][j]:
                    reach[i][j] = True
    return reach


# ---------------------------------------------------------------------------
# (6) K-제약 벨만-포드 - 간선 K개 이하로 가는 최단 (스냅샷 필수)
# ---------------------------------------------------------------------------
def bellman_ford_k(n, edges, start, end, k):
    dist = [INF] * n
    dist[start] = 0
    for _ in range(k):                          # 간선 k개까지
        snap = dist[:]                          # 직전 라운드 스냅샷만 사용
        for u, v, w in edges:
            if snap[u] != INF and snap[u] + w < dist[v]:
                dist[v] = snap[u] + w
    return dist[end] if dist[end] != INF else -1


def main():
    print("=" * 60)
    print("Day 35 - Bellman-Ford & Floyd-Warshall 예제 데모")
    print("=" * 60)

    # 공통 방향 그래프 (음수 간선 포함, 사이클 없음), 4 정점
    #   0 --4--> 1
    #   0 --5--> 2
    #   1 --(-2)-> 2
    #   1 --6--> 3
    #   2 --3--> 3
    n = 4
    edges = [(0, 1, 4), (0, 2, 5), (1, 2, -2), (1, 3, 6), (2, 3, 3)]

    # (1) 벨만-포드   (0->1=4, 0->2=min(5, 4-2=2)=2, 0->3=min(4+6, 2+3)=5)
    dist = bellman_ford(n, edges, 0)
    print("[1] bellman_ford(start=0) =", dist)
    print("    기대값                = [0, 4, 2, 5]")

    # (2) 경로 복원
    cost, path = bellman_ford_path(n, edges, 0, 3)
    print("[2] 0 -> 3 최단비용 =", cost, ", 경로 =", path)
    print("    기대: 비용 5, 경로 [0, 1, 2, 3]")

    # (3) 플로이드-워셜: 벨만-포드와 0행이 일치해야 함
    fw = floyd_warshall(n, edges)
    print("[3] floyd_warshall row0 =", fw[0], " (벨만포드와 동일?",
          "O" if fw[0] == dist else "X", ")")

    # (4) 플로이드-워셜 경로 복원
    fw2, build = floyd_warshall_path(n, edges)
    print("[4] 0 -> 3 경로 =", build(0, 3), " 기대 [0, 1, 2, 3]")

    # (5) 음수 사이클 판별: 0->1->0 로 되돌아오며 음수
    #   0 --1--> 1,  1 --(-3)--> 0   => 사이클 합 -2 (음수 사이클)
    cyc_edges = [(0, 1, 1), (1, 0, -3), (1, 2, 2)]
    res = bellman_ford(3, cyc_edges, 0)
    print("[5] 음수 사이클 판별 =", "NEGATIVE CYCLE (None)" if res is None else res)

    # (6) 전이 폐포(도달성): 0->1->2 이면 0->2 도달 가능
    reach = transitive_closure(3, [(0, 1), (1, 2)])
    print("[6] 0->2 도달가능? ", "O" if reach[0][2] else "X",
          " / 2->0 도달가능?", "O" if reach[2][0] else "X", "(기대 O / X)")

    # (7) K-제약 벨만-포드: 간선 K개 이하로 0->3
    ans_k1 = bellman_ford_k(n, edges, 0, 3, 1)   # 간선 1개: 직행 없음 -> -1
    ans_k2 = bellman_ford_k(n, edges, 0, 3, 2)   # 간선 2개: 0->2->3=8 (0->1->3=10 보다 저렴)
    print("[7] K=1 (간선1개) 0->3 =", ans_k1, " 기대 -1 (직행 없음)")
    print("    K=2 (간선2개) 0->3 =", ans_k2, " 기대 8 (0->2->3)")

    print("=" * 60)
    print("데모 종료")
    print("=" * 60)


if __name__ == "__main__":
    main()
