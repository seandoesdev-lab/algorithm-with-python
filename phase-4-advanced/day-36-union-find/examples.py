# -*- coding: utf-8 -*-
"""
Day 36 - 서로소 집합 (Union-Find / Disjoint Set) 예제

핵심 골격 6종:
  (1) 순수 Union-Find      - 최적화 없는 기본형 (개념 확인용)
  (2) 표준 DSU 클래스       - 경로 압축 + 사이즈 합치기 (코테 템플릿)
  (3) 연결 요소 개수        - union 후 서로 다른 root 수
  (4) 무방향 사이클 판별     - union 실패(이미 같은 그룹) == 사이클
  (5) 문자열 원소 DSU        - dict 로 "이름 -> 정수 인덱스" 매핑
  (6) 격자(grid) 셀 union    - (r,c) 를 r*W+c 로 1차원화

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""


# ---------------------------------------------------------------------------
# (1) 순수 Union-Find (최적화 없음) - 개념 확인용
#     parent 배열만. 최악의 경우 find 가 O(N) 이 될 수 있다.
# ---------------------------------------------------------------------------
def find_naive(parent, x):
    while parent[x] != x:          # root 에 닿을 때까지 부모를 타고 올라감
        x = parent[x]
    return x


def union_naive(parent, a, b):
    ra, rb = find_naive(parent, a), find_naive(parent, b)
    if ra != rb:
        parent[ra] = rb           # 한 root 를 다른 root 밑에 붙임


# ---------------------------------------------------------------------------
# (2) 표준 DSU - 경로 압축(path compression) + 사이즈 합치기(union by size)
#     한 연산이 사실상 O(alpha(N)) = 거의 O(1).
# ---------------------------------------------------------------------------
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))    # 각자 자기 자신이 root
        self.size = [1] * n             # 각 그룹의 원소 수
        self.count = n                  # 연결 요소(그룹) 개수

    def find(self, x):                  # 경로 압축 (반복 버전 - 재귀 깊이 안전)
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:   # 지나온 노드를 root 로 직결
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                # 이미 같은 그룹 -> 합칠 것 없음(사이클)
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra             # ra 가 항상 더 큰 쪽
        self.parent[rb] = ra            # 작은 rb 를 큰 ra 밑에
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def group_size(self, x):
        return self.size[self.find(x)]


# ---------------------------------------------------------------------------
# (3) 연결 요소 개수 - 두 가지 방법이 같은 답
# ---------------------------------------------------------------------------
def count_components(n, edges):
    dsu = DSU(n)
    for a, b in edges:
        dsu.union(a, b)
    by_count = dsu.count                        # union 성공마다 감소시킨 값
    by_roots = sum(1 for i in range(n)          # 서로 다른 root 수
                   if dsu.find(i) == i)
    assert by_count == by_roots
    return by_count


# ---------------------------------------------------------------------------
# (4) 무방향 그래프 사이클 판별 - union 이 False 면 사이클
# ---------------------------------------------------------------------------
def has_cycle(n, edges):
    dsu = DSU(n)
    for a, b in edges:
        if not dsu.union(a, b):                 # 이미 같은 그룹인데 또 이음
            return True
    return False


# ---------------------------------------------------------------------------
# (5) 문자열 원소 DSU - dict 로 인덱싱
# ---------------------------------------------------------------------------
def union_strings(pairs):
    idx = {}

    def get_id(name):
        if name not in idx:
            idx[name] = len(idx)
        return idx[name]

    for a, b in pairs:                          # 먼저 모든 이름에 번호 부여
        get_id(a)
        get_id(b)
    dsu = DSU(len(idx))
    for a, b in pairs:
        dsu.union(idx[a], idx[b])
    # 이름 -> 대표 이름
    id_to_name = {v: k for k, v in idx.items()}
    return {name: id_to_name[dsu.find(i)] for name, i in idx.items()}


# ---------------------------------------------------------------------------
# (6) 격자 union - 1(땅) 셀들을 상하좌우로 union -> 섬 개수
# ---------------------------------------------------------------------------
def count_islands(grid):
    if not grid or not grid[0]:
        return 0, 0
    H, W = len(grid), len(grid[0])
    dsu = DSU(H * W)
    land = 0
    for r in range(H):
        for c in range(W):
            if grid[r][c] != 1:
                continue
            land += 1
            if r + 1 < H and grid[r + 1][c] == 1:   # 아래
                dsu.union(r * W + c, (r + 1) * W + c)
            if c + 1 < W and grid[r][c + 1] == 1:   # 오른쪽
                dsu.union(r * W + c, r * W + c + 1)
    # 땅 셀들의 서로 다른 root 수 = 섬 개수
    roots = {dsu.find(r * W + c)
             for r in range(H) for c in range(W) if grid[r][c] == 1}
    return len(roots), land


def main():
    print("=" * 60)
    print("Day 36 - Union-Find (Disjoint Set) 예제 데모")
    print("=" * 60)

    # (1) 순수 Union-Find
    parent = list(range(5))
    union_naive(parent, 0, 1)
    union_naive(parent, 2, 3)
    union_naive(parent, 1, 3)
    same = find_naive(parent, 0) == find_naive(parent, 3)
    print("[1] naive: 0 과 3 같은 그룹? ", "O" if same else "X", "(기대 O)")
    print("    4 와 0 같은 그룹? ",
          "O" if find_naive(parent, 4) == find_naive(parent, 0) else "X",
          "(기대 X)")

    # (2) 표준 DSU
    dsu = DSU(6)
    dsu.union(0, 1)
    dsu.union(1, 2)
    dsu.union(3, 4)
    print("[2] DSU: connected(0,2) =", "O" if dsu.connected(0, 2) else "X",
          " / connected(0,3) =", "O" if dsu.connected(0, 3) else "X")
    print("    group_size(0) =", dsu.group_size(0), " (기대 3: 0,1,2)")
    print("    남은 그룹 수 count =", dsu.count, " (기대 3: [0,1,2][3,4][5])")

    # (3) 연결 요소 개수
    n, edges = 5, [(0, 1), (1, 2), (3, 4)]
    print("[3] 연결 요소 개수 =", count_components(n, edges),
          " (기대 2: [0,1,2][3,4])")

    # (4) 사이클 판별
    print("[4] 사이클 [(0,1),(1,2),(2,0)] =",
          "O" if has_cycle(3, [(0, 1), (1, 2), (2, 0)]) else "X",
          "(기대 O)")
    print("    사이클 [(0,1),(1,2)]       =",
          "O" if has_cycle(3, [(0, 1), (1, 2)]) else "X",
          "(기대 X)")

    # (5) 문자열 DSU
    groups = union_strings([("a", "b"), ("b", "c"), ("x", "y")])
    same_abc = groups["a"] == groups["c"]
    same_ax = groups["a"] == groups["x"]
    print("[5] str: a 와 c 같은 그룹? ", "O" if same_abc else "X",
          " / a 와 x 같은 그룹? ", "O" if same_ax else "X",
          "(기대 O / X)")

    # (6) 격자 섬 개수
    grid = [
        [1, 1, 0, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 1],
    ]
    islands, land = count_islands(grid)
    print("[6] 섬 개수 =", islands, " (기대 2) / 땅 셀 수 =", land)

    print("=" * 60)
    print("데모 종료")
    print("=" * 60)


if __name__ == "__main__":
    main()
