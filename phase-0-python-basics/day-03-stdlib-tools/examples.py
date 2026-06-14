"""
Day 3 - 컴프리헨션 & 표준 라이브러리 데모 (Comprehension & Standard Library Demo)

실행 방법: python examples.py

cp949 콘솔 안전: 특수기호/이모지 미사용, 한글 및 ASCII 기호만 사용.
"""

# ─────────────────────────────────────────────
# 1. 리스트 컴프리헨션 (List Comprehension)
# ─────────────────────────────────────────────
def demo_list_comprehension():
    print("=" * 50)
    print("[1] 리스트 컴프리헨션 (List Comprehension)")
    print("=" * 50)

    # 기본: 0~9의 제곱수
    squares = [x ** 2 for x in range(10)]
    print(f"제곱수 리스트: {squares}")

    # 조건 필터링: 짝수만 선택
    evens = [x for x in range(20) if x % 2 == 0]
    print(f"짝수 리스트: {evens}")

    # 중첩(nested): 2D 행렬을 1D로 평탄화(flatten)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [val for row in matrix for val in row]
    print(f"행렬 평탄화: {flat}")

    # 일반 for + append 방식 (비교용)
    squares_old = []
    for x in range(10):
        squares_old.append(x ** 2)
    print(f"for+append 방식(동일 결과): {squares_old}")
    print()


# ─────────────────────────────────────────────
# 2. 딕셔너리/셋 컴프리헨션 (Dict/Set Comprehension)
# ─────────────────────────────────────────────
def demo_dict_set_comprehension():
    print("=" * 50)
    print("[2] 딕셔너리/셋 컴프리헨션 (Dict/Set Comprehension)")
    print("=" * 50)

    words = ["apple", "banana", "cherry", "banana"]

    # 딕셔너리 컴프리헨션: 단어 → 길이 매핑
    word_len = {w: len(w) for w in words}
    print(f"단어 길이 딕셔너리: {word_len}")

    # 키-값 뒤집기 (값이 고유한 경우만 안전)
    inv = {v: k for k, v in {"a": 1, "b": 2, "c": 3}.items()}
    print(f"키-값 반전: {inv}")

    # 셋 컴프리헨션: 고유한 단어 길이
    unique_lens = {len(w) for w in words}
    print(f"고유 길이 집합: {unique_lens}")
    print()


# ─────────────────────────────────────────────
# 3. 제너레이터 표현식 (Generator Expression)
# ─────────────────────────────────────────────
def demo_generator():
    print("=" * 50)
    print("[3] 제너레이터 표현식 (Generator Expression)")
    print("=" * 50)

    # 제너레이터: 소괄호 사용, 지연 평가(lazy evaluation)
    gen = (x ** 2 for x in range(10))
    print(f"제너레이터 객체: {gen}")  # <generator object ...>

    # next()로 하나씩 꺼냄
    print(f"첫 번째 값(next): {next(gen)}")   # 0
    print(f"두 번째 값(next): {next(gen)}")   # 1

    # 나머지를 list()로 소비
    rest = list(gen)
    print(f"나머지를 list()로: {rest}")   # [4, 9, 16, 25, 36, 49, 64, 81]

    # 메모리 절약 예시: 큰 범위의 합 (리스트 생성 없이)
    total = sum(x ** 2 for x in range(100_000))
    print(f"0~99999 제곱합 (제너레이터로): {total}")

    # 제너레이터는 한 번만 소비 가능
    gen2 = (x for x in range(3))
    print(f"첫 순회: {list(gen2)}")   # [0, 1, 2]
    print(f"두 번째 순회(소진됨): {list(gen2)}")   # []
    print()


# ─────────────────────────────────────────────
# 4. collections.deque - BFS 스케치
# ─────────────────────────────────────────────
def demo_deque_bfs():
    from collections import deque

    print("=" * 50)
    print("[4] deque + BFS (너비 우선 탐색)")
    print("=" * 50)

    # 작은 그래프 (인접 리스트)
    # 0 - 1 - 3
    # |       |
    # 2 ------+
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2],
    }

    def bfs(start):
        visited = set()
        queue = deque([start])   # deque로 큐 초기화
        visited.add(start)
        order = []

        while queue:
            node = queue.popleft()   # O(1) - 앞에서 꺼냄
            order.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)   # O(1) - 뒤에 추가
        return order

    result = bfs(0)
    print(f"BFS 탐색 순서(시작=0): {result}")

    # deque 양끝 O(1) 조작 시연
    dq = deque([1, 2, 3])
    dq.appendleft(0)
    dq.append(4)
    print(f"appendleft(0), append(4): {list(dq)}")  # [0, 1, 2, 3, 4]
    print(f"popleft(): {dq.popleft()}, 남은: {list(dq)}")   # 0, [1,2,3,4]

    # maxlen 슬라이딩 윈도우
    window = deque(maxlen=3)
    for x in range(6):
        window.append(x)
    print(f"maxlen=3, 0~5 추가 후: {list(window)}")  # [3, 4, 5]
    print()


# ─────────────────────────────────────────────
# 5. collections.Counter - 빈도 세기
# ─────────────────────────────────────────────
def demo_counter():
    from collections import Counter

    print("=" * 50)
    print("[5] Counter (빈도수 카운터)")
    print("=" * 50)

    # 문자열 빈도
    c = Counter("abracadabra")
    print(f"Counter('abracadabra'): {c}")

    # most_common(k): 상위 k개 반환
    print(f"most_common(2): {c.most_common(2)}")   # [('a', 5), ('b', 2)]

    # 없는 키 → 0 (KeyError 없음)
    print(f"c['z']: {c['z']}")   # 0

    # 리스트 빈도
    nums = [1, 2, 2, 3, 3, 3, 4]
    nc = Counter(nums)
    print(f"Counter({nums}): {nc}")

    # Counter 덧셈/뺄셈
    c1 = Counter("aab")
    c2 = Counter("abc")
    print(f"c1+c2: {c1 + c2}")   # {'a': 3, 'b': 2, 'c': 1}
    print(f"c1-c2: {c1 - c2}")   # {'a': 1}
    print()


# ─────────────────────────────────────────────
# 6. collections.defaultdict - 기본값 딕셔너리
# ─────────────────────────────────────────────
def demo_defaultdict():
    from collections import defaultdict

    print("=" * 50)
    print("[6] defaultdict (기본값 자동 생성)")
    print("=" * 50)

    # defaultdict(list): 그래프 인접 리스트 구성
    graph = defaultdict(list)
    edges = [(1, 2), (1, 3), (2, 4), (3, 4)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)   # 무방향 그래프
    print(f"그래프 인접 리스트: {dict(graph)}")

    # defaultdict(int): 단어 빈도 세기
    freq = defaultdict(int)
    for ch in "hello world":
        if ch != " ":
            freq[ch] += 1
    print(f"문자 빈도: {dict(freq)}")

    # 일반 dict와 비교: KeyError 발생 vs 자동 생성
    normal = {}
    try:
        normal["x"] += 1
    except KeyError as e:
        print(f"일반 dict: KeyError {e} 발생!")

    safe = defaultdict(int)
    safe["x"] += 1   # 에러 없음
    print(f"defaultdict: safe['x'] = {safe['x']}")
    print()


# ─────────────────────────────────────────────
# 7. heapq - 최소 힙 & 최대 힙
# ─────────────────────────────────────────────
def demo_heapq():
    import heapq

    print("=" * 50)
    print("[7] heapq (최소 힙 & 최대 힙)")
    print("=" * 50)

    # 최소 힙 (min-heap)
    h = []
    for x in [3, 1, 4, 1, 5, 9, 2, 6]:
        heapq.heappush(h, x)   # O(log n)

    print("최소 힙 순서대로 pop:")
    result = []
    while h:
        result.append(heapq.heappop(h))   # O(log n), 항상 최솟값
    print(f"  {result}")   # [1, 1, 2, 3, 4, 5, 6, 9]

    # heapify: 기존 리스트를 힙으로 변환 O(n)
    data = [3, 1, 4, 1, 5, 9]
    heapq.heapify(data)
    print(f"heapify 후 data[0](최솟값): {data[0]}")   # 1

    # 최대 힙 (max-heap) - 부호 반전 패턴
    print("\n최대 힙 (부호 반전 패턴):")
    max_h = []
    for x in [3, 1, 4, 1, 5, 9, 2, 6]:
        heapq.heappush(max_h, -x)   # 부호 반전해서 저장

    max_result = []
    while max_h:
        max_result.append(-heapq.heappop(max_h))   # 부호 다시 반전
    print(f"  최대 힙 순서대로 pop: {max_result}")   # [9, 6, 5, 4, 3, 2, 1, 1]

    # 튜플 활용: (우선순위, 값) 패턴 - 우선순위 큐(priority queue)
    print("\n우선순위 큐 (priority queue):")
    tasks = []
    heapq.heappush(tasks, (3, "저우선순위 작업"))
    heapq.heappush(tasks, (1, "고우선순위 작업"))
    heapq.heappush(tasks, (2, "중간 작업"))
    while tasks:
        priority, task = heapq.heappop(tasks)
        print(f"  우선순위 {priority}: {task}")
    print()


# ─────────────────────────────────────────────
# 8. itertools - 조합론 (Combinatorics)
# ─────────────────────────────────────────────
def demo_itertools():
    from itertools import combinations, permutations, product, accumulate
    import operator

    print("=" * 50)
    print("[8] itertools (순열, 조합, 곱, 누적)")
    print("=" * 50)

    nums = [1, 2, 3, 4]

    # combinations: 조합 (순서 무관, 중복 없음)
    combs = list(combinations(nums, 2))
    print(f"combinations([1,2,3,4], 2) - {len(combs)}가지:")
    print(f"  {combs}")

    # permutations: 순열 (순서 관련, 중복 없음)
    perms = list(permutations([1, 2, 3], 2))
    print(f"permutations([1,2,3], 2) - {len(perms)}가지:")
    print(f"  {perms}")

    # product: 데카르트 곱 (Cartesian product) - 중복 허용 순열
    prod = list(product([0, 1], repeat=3))
    print(f"product([0,1], repeat=3) - {len(prod)}가지 (3자리 이진수):")
    print(f"  {prod}")

    prod2 = list(product("AB", [1, 2]))
    print(f"product('AB', [1,2]): {prod2}")

    # accumulate: 누적 합 (prefix sum)
    data = [1, 2, 3, 4, 5]
    prefix_sum = list(accumulate(data))
    print(f"accumulate({data}): {prefix_sum}")   # [1, 3, 6, 10, 15]

    # 누적 곱
    prefix_mul = list(accumulate(data, operator.mul))
    print(f"accumulate({data}, mul): {prefix_mul}")   # [1, 2, 6, 24, 120]
    print()


# ─────────────────────────────────────────────
# 9. bisect - 이진 탐색 삽입 위치
# ─────────────────────────────────────────────
def demo_bisect():
    import bisect

    print("=" * 50)
    print("[9] bisect (정렬 리스트 이분 탐색)")
    print("=" * 50)

    a = [1, 3, 5, 7, 9]
    print(f"정렬된 리스트: {a}")

    # bisect_left: 같은 값의 왼쪽(앞) 삽입 위치
    print(f"bisect_left(a, 5):  {bisect.bisect_left(a, 5)}")    # 2
    print(f"bisect_left(a, 6):  {bisect.bisect_left(a, 6)}")    # 3
    print(f"bisect_left(a, 0):  {bisect.bisect_left(a, 0)}")    # 0

    # bisect_right: 같은 값의 오른쪽(뒤) 삽입 위치
    print(f"bisect_right(a, 5): {bisect.bisect_right(a, 5)}")   # 3
    print(f"bisect_right(a, 6): {bisect.bisect_right(a, 6)}")   # 3

    # 중복값이 있을 때 left vs right 차이 확인
    b = [1, 2, 2, 2, 3]
    print(f"\n중복 리스트: {b}")
    print(f"bisect_left(b, 2):  {bisect.bisect_left(b, 2)}")    # 1
    print(f"bisect_right(b, 2): {bisect.bisect_right(b, 2)}")   # 4
    count_2 = bisect.bisect_right(b, 2) - bisect.bisect_left(b, 2)
    print(f"2의 개수: {count_2}")   # 3

    # insort: 정렬 유지하며 삽입 (이동 O(n)이므로 대용량엔 주의)
    c = [1, 3, 5, 7]
    bisect.insort(c, 4)
    bisect.insort(c, 6)
    print(f"\ninsort 후: {c}")   # [1, 3, 4, 5, 6, 7]
    print()


# ─────────────────────────────────────────────
# 메인 실행
# ─────────────────────────────────────────────
if __name__ == "__main__":
    demo_list_comprehension()
    demo_dict_set_comprehension()
    demo_generator()
    demo_deque_bfs()
    demo_counter()
    demo_defaultdict()
    demo_heapq()
    demo_itertools()
    demo_bisect()
    print("모든 데모 완료!")
