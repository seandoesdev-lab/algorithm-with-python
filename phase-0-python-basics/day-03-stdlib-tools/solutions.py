"""
Day 3 - 연습 문제 해설 (Solutions)

실행 방법: python solutions.py

각 문제마다 복수의 접근 방식을 비교하며 왜 특정 방법이 더 좋은지 설명한다.

cp949 콘솔 안전: 특수기호/이모지 미사용, 한글 및 ASCII 기호만 사용.
"""

import heapq
from collections import Counter, defaultdict
from itertools import permutations, cycle
import math


# ===============================================================
# 문제 1 - LeetCode 1046: Last Stone Weight
# https://leetcode.com/problems/last-stone-weight/
# 난이도: Easy | 핵심: heapq max-heap (부호 반전 패턴)
# ===============================================================

class Solution1046:
    def lastStoneWeight_v1(self, stones):
        """
        접근 1 (권장): heapq max-heap -- 부호 반전 패턴
        - 시간 복잡도: O(N log N) -- N번의 heappop/heappush, 각 O(log N)
        - 공간 복잡도: O(N)

        Python heapq는 최소 힙만 지원한다.
        최대 힙을 구현하려면 값을 push할 때 부호를 반전(-x)하면 된다.
        pop 시에도 부호를 다시 반전해서 실제 값을 복원한다.
        """
        h = [-x for x in stones]   # 부호 반전: 최소 힙 -> 최대 힙처럼 동작
        heapq.heapify(h)            # O(N)

        while len(h) > 1:
            y = -heapq.heappop(h)   # 가장 무거운 돌 (부호 복원)
            x = -heapq.heappop(h)   # 두 번째로 무거운 돌
            if y > x:
                heapq.heappush(h, -(y - x))   # 차이만큼 남아서 다시 push

        return -h[0] if h else 0

    def lastStoneWeight_v2(self, stones):
        """
        접근 2 (비교용): 매번 정렬 사용
        - 시간 복잡도: O(N^2 log N) -- 매 반복마다 정렬 O(N log N)
        - 돌의 개수가 크면 비효율적 (N=100 정도면 무방)

        왜 heapq가 빠른가:
          - 정렬: 매번 전체 배열 재정렬 -> O(N log N)
          - heapq: 삽입/삭제 시 트리 경로만 비교 -> O(log N)
        """
        arr = sorted(stones)

        while len(arr) > 1:
            y = arr.pop()   # 가장 큰 값
            x = arr.pop()   # 두 번째로 큰 값
            if y > x:
                # 이진 탐색으로 삽입 위치 찾아 정렬 유지
                import bisect
                bisect.insort(arr, y - x)

        return arr[0] if arr else 0


# ===============================================================
# 문제 2 - LeetCode 347: Top K Frequent Elements
# https://leetcode.com/problems/top-k-frequent-elements/
# 난이도: Medium | 핵심: Counter + heapq.nlargest / most_common
# ===============================================================

class Solution347:
    def topKFrequent_v1(self, nums, k):
        """
        접근 1 (권장): Counter.most_common(k)
        - 시간 복잡도: O(N log k) -- 내부적으로 heapq.nlargest 사용
        - 공간 복잡도: O(N)

        Counter.most_common(k): k를 지정하면 heapq.nlargest(k, ...)를 사용해
        전체 정렬(O(N log N))보다 빠른 O(N log k) 로 상위 k개를 구한다.
        """
        cnt = Counter(nums)
        # most_common(k) -> [(원소, 빈도), ...] 형태 반환
        return [x for x, _ in cnt.most_common(k)]

    def topKFrequent_v2(self, nums, k):
        """
        접근 2: heapq.nlargest 직접 사용
        - 시간 복잡도: O(N log k)
        - most_common 내부 동작을 명시적으로 재현한 버전

        heapq.nlargest(k, iterable, key): iterable에서 key 기준 상위 k개 반환
        key=cnt.get 은 각 원소의 빈도를 기준으로 비교한다.
        """
        cnt = Counter(nums)
        return heapq.nlargest(k, cnt.keys(), key=cnt.get)

    def topKFrequent_v3(self, nums, k):
        """
        접근 3 (비교용): 전체 정렬
        - 시간 복잡도: O(N log N) -- k가 N에 비해 작을 때 v1/v2보다 느림
        - 이해하기 쉽지만 k << N 상황에서는 낭비

        Counter.items()를 빈도 내림차순으로 정렬 후 앞 k개 슬라이싱.
        """
        cnt = Counter(nums)
        sorted_items = sorted(cnt.items(), key=lambda x: -x[1])
        return [x for x, _ in sorted_items[:k]]


# ===============================================================
# 문제 3 - 프로그래머스 42840: 모의고사
# https://school.programmers.co.kr/learn/courses/30/lessons/42840
# 난이도: Level 1 | 핵심: itertools.cycle 또는 %, 리스트 컴프리헨션
# ===============================================================

def solution_mock_exam_v1(answers):
    """
    접근 1 (권장): 인덱스 나머지(%) 패턴
    - 시간 복잡도: O(N) -- N = len(answers)
    - 공간 복잡도: O(1) (패턴 배열 크기 고정)

    핵심: pattern[i % len(pattern)] 으로 패턴을 순환.
    % 연산은 인덱스를 패턴 길이 범위 내에서 돌아가게 만든다.
    """
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5],
    ]
    scores = [
        sum(1 for i, a in enumerate(answers) if a == p[i % len(p)])
        for p in patterns
    ]
    max_score = max(scores)
    return [i + 1 for i, s in enumerate(scores) if s == max_score]


def solution_mock_exam_v2(answers):
    """
    접근 2: itertools.cycle 사용
    - cycle(pattern): 패턴을 무한 반복하는 이터레이터 생성
    - zip(answers, cycle(pattern)): answers 길이만큼만 소비 (안전)
    - 시간 복잡도: O(N)

    zip은 짧은 쪽(answers)이 소진되면 자동 종료 -> cycle이 무한해도 안전하다.
    """
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5],
    ]
    scores = [
        sum(a == p for a, p in zip(answers, cycle(pat)))
        for pat in patterns
    ]
    max_score = max(scores)
    return sorted([i + 1 for i, s in enumerate(scores) if s == max_score])


# ===============================================================
# 문제 4 - 프로그래머스 42626: 더 맵게
# https://school.programmers.co.kr/learn/courses/30/lessons/42626
# 난이도: Level 2 | 핵심: heapq min-heap + 조건 반복
# ===============================================================

def solution_spicy_v1(scoville, K):
    """
    접근 1 (권장): heapq min-heap
    - 시간 복잡도: O(N log N) -- 최대 N번 pop+push, 각 O(log N)
    - 공간 복잡도: O(N)

    매 반복마다 가장 맵지 않은 두 음식을 꺼내 섞어서 다시 push.
    heapify -> O(N), 이후 연산마다 O(log N).
    """
    h = scoville[:]        # 원본 훼손 방지를 위해 복사
    heapq.heapify(h)       # 리스트를 힙으로 변환: O(N)
    count = 0

    while h[0] < K:
        if len(h) < 2:
            return -1      # 섞을 음식이 1개뿐 -> 불가능
        first = heapq.heappop(h)
        second = heapq.heappop(h)
        heapq.heappush(h, first + second * 2)
        count += 1

    return count


def solution_spicy_v2(scoville, K):
    """
    접근 2: 매번 정렬 -- 비교용 (느린 방법)
    - 시간 복잡도: O(N^2 log N) -- 매 반복 O(N log N) 정렬
    - N=100,000 이면 시간 초과 발생 -> heapq 사용이 필수

    왜 heapq가 필요한가:
      - 정렬은 전체 배열을 매번 재정렬 -> 누적 비용이 O(N^2 log N)
      - heapq는 삽입/삭제 시 log N 비교만 -> 누적 비용 O(N log N)
    """
    arr = sorted(scoville)
    count = 0

    while arr[0] < K:
        if len(arr) < 2:
            return -1
        first = arr.pop(0)    # O(N) -- 리스트 앞 요소 제거는 비쌈
        second = arr.pop(0)
        import bisect
        bisect.insort(arr, first + second * 2)
        count += 1

    return count


# ===============================================================
# 문제 5 - 프로그래머스 42579: 베스트앨범
# https://school.programmers.co.kr/learn/courses/30/lessons/42579
# 난이도: Level 3 | 핵심: defaultdict + Counter + 다중 키 정렬
# ===============================================================

def solution_best_album_v1(genres, plays):
    """
    접근 1 (권장): defaultdict + Counter + sorted
    - 시간 복잡도: O(N log N)
    - 공간 복잡도: O(N)

    3단계 처리:
      1) 장르별 총 재생수 집계 (Counter 또는 defaultdict(int))
      2) 장르별 곡 목록 구성 (defaultdict(list)) -- (재생수, 인덱스)
      3) 장르 정렬(총재생수 내림) -> 각 장르에서 최대 2곡 추출(재생수 내림, 인덱스 오름)
    """
    # 1) 장르별 총 재생수
    genre_total = defaultdict(int)
    for g, p in zip(genres, plays):
        genre_total[g] += p

    # 2) 장르별 곡 목록: (재생수, 고유번호)
    genre_songs = defaultdict(list)
    for idx, (g, p) in enumerate(zip(genres, plays)):
        genre_songs[g].append((p, idx))

    # 3) 결과 조합
    result = []
    # 총 재생수 내림차순으로 장르 순회
    for g in sorted(genre_total, key=lambda x: -genre_total[x]):
        # 재생수 내림차순, 인덱스 오름차순 정렬 후 최대 2곡
        top2 = sorted(genre_songs[g], key=lambda x: (-x[0], x[1]))[:2]
        result.extend(idx for _, idx in top2)

    return result


def solution_best_album_v2(genres, plays):
    """
    접근 2: Counter 활용 (장르 총합 집계를 Counter로)
    - 기능은 v1과 동일하지만 Counter를 명시적으로 사용하는 버전
    - Counter(dict) 는 defaultdict(int) 와 동일한 역할이지만
      most_common() 등 추가 메서드가 있어 편리

    Counter vs defaultdict(int):
      - Counter: most_common(), 연산자(+/-) 지원, 없는 키 0 반환
      - defaultdict(int): 단순 자동 기본값, 약간 더 빠름
      -> 빈도 분석 목적이면 Counter, 단순 카운트이면 defaultdict(int)
    """
    genre_total = Counter()
    for g, p in zip(genres, plays):
        genre_total[g] += p

    genre_songs = defaultdict(list)
    for idx, (g, p) in enumerate(zip(genres, plays)):
        genre_songs[g].append((p, idx))

    result = []
    for g, _ in genre_total.most_common():   # 총재생수 내림차순
        top2 = sorted(genre_songs[g], key=lambda x: (-x[0], x[1]))[:2]
        result.extend(idx for _, idx in top2)

    return result


# ===============================================================
# 메인 -- 샘플 입력으로 모든 함수 검증 (assert)
# ===============================================================

if __name__ == "__main__":

    # ── 문제 1: Last Stone Weight ─────────────────────────────
    print("=" * 55)
    print("[문제 1] LeetCode 1046: Last Stone Weight")
    print("=" * 55)

    sol1 = Solution1046()

    cases1 = [
        ([2, 7, 4, 1, 8, 1], 1),
        ([1],                 1),
        ([3, 3],              0),
        ([1, 2],              1),
    ]
    for stones, expected in cases1:
        r1 = sol1.lastStoneWeight_v1(stones[:])
        r2 = sol1.lastStoneWeight_v2(stones[:])
        print(f"stones={stones} -> v1={r1}, v2={r2}  (기댓값={expected})")
        assert r1 == expected, f"v1 실패: {r1} != {expected}"
        assert r2 == expected, f"v2 실패: {r2} != {expected}"

    print("  [성능 비교]")
    print("  v1 heapq: O(N log N) -- 권장")
    print("  v2 정렬:  O(N^2 log N) -- 비교용")
    print()

    # ── 문제 2: Top K Frequent Elements ──────────────────────
    print("=" * 55)
    print("[문제 2] LeetCode 347: Top K Frequent Elements")
    print("=" * 55)

    sol2 = Solution347()

    nums_a, k_a = [1, 1, 1, 2, 2, 3], 2
    r1 = sorted(sol2.topKFrequent_v1(nums_a, k_a))
    r2 = sorted(sol2.topKFrequent_v2(nums_a, k_a))
    r3 = sorted(sol2.topKFrequent_v3(nums_a, k_a))
    expected_a = [1, 2]
    print(f"nums={nums_a}, k={k_a}")
    print(f"  v1 most_common: {r1}  기댓값={expected_a}")
    print(f"  v2 nlargest:    {r2}  기댓값={expected_a}")
    print(f"  v3 sort:        {r3}  기댓값={expected_a}")
    assert r1 == expected_a, f"v1 실패"
    assert r2 == expected_a, f"v2 실패"
    assert r3 == expected_a, f"v3 실패"

    nums_b, k_b = [1], 1
    r1b = sol2.topKFrequent_v1(nums_b, k_b)
    assert r1b == [1]

    print()
    print("  [세 접근 비교]")
    print("  v1 most_common(k): O(N log k) -- 가장 간결, 권장")
    print("  v2 nlargest:       O(N log k) -- v1 내부 동작 명시적 재현")
    print("  v3 전체 정렬:       O(N log N) -- k << N 일 때 낭비")
    print()

    # ── 문제 3: 모의고사 ──────────────────────────────────────
    print("=" * 55)
    print("[문제 3] 프로그래머스 42840: 모의고사")
    print("=" * 55)

    cases3 = [
        ([1, 2, 3, 4, 5],  [1]),
        ([1, 3, 2, 4, 2],  [1, 2, 3]),
    ]
    for answers, expected in cases3:
        r1 = solution_mock_exam_v1(answers)
        r2 = solution_mock_exam_v2(answers)
        print(f"answers={answers}")
        print(f"  v1 (% 패턴): {r1}  기댓값={expected}")
        print(f"  v2 (cycle):  {r2}  기댓값={expected}")
        assert r1 == expected, f"v1 실패: {r1}"
        assert r2 == expected, f"v2 실패: {r2}"

    print()
    print("  [두 접근 비교]")
    print("  v1 %:     인덱스 나머지, 직관적, 코테 현장에서 많이 쓰임")
    print("  v2 cycle: itertools 활용, 파이써닉, zip과 조합시 안전")
    print("  -> 둘 다 O(N), 실전에서는 v1이 더 많이 쓰임")
    print()

    # ── 문제 4: 더 맵게 ──────────────────────────────────────
    print("=" * 55)
    print("[문제 4] 프로그래머스 42626: 더 맵게")
    print("=" * 55)

    cases4 = [
        ([1, 2, 3, 9, 10, 12], 7, 2),
        ([1, 1], 10, -1),
        ([10], 7, 0),
    ]
    for scoville, K, expected in cases4:
        r1 = solution_spicy_v1(scoville, K)
        r2 = solution_spicy_v2(scoville, K)
        print(f"scoville={scoville}, K={K}")
        print(f"  v1 heapq: {r1}  기댓값={expected}")
        print(f"  v2 정렬:  {r2}  기댓값={expected}")
        assert r1 == expected, f"v1 실패: {r1}"
        assert r2 == expected, f"v2 실패: {r2}"

    print()
    print("  [두 접근 비교]")
    print("  v1 heapq: O(N log N) -- 대용량(N=1,000,000) 처리 가능, 권장")
    print("  v2 정렬:  O(N^2 log N) -- N이 크면 시간 초과")
    print()

    # ── 문제 5: 베스트앨범 ────────────────────────────────────
    print("=" * 55)
    print("[문제 5] 프로그래머스 42579: 베스트앨범")
    print("=" * 55)

    genres5 = ["classic", "pop", "classic", "classic", "pop"]
    plays5  = [500, 600, 150, 800, 2500]
    expected5 = [4, 1, 3, 0]

    r1 = solution_best_album_v1(genres5, plays5)
    r2 = solution_best_album_v2(genres5, plays5)
    print(f"genres={genres5}")
    print(f"plays ={plays5}")
    print(f"v1 (defaultdict): {r1}  기댓값={expected5}")
    print(f"v2 (Counter):     {r2}  기댓값={expected5}")
    assert r1 == expected5, f"v1 실패: {r1}"
    assert r2 == expected5, f"v2 실패: {r2}"

    print()
    print("  [두 접근 비교]")
    print("  v1 defaultdict: 명시적 집계, 빠름")
    print("  v2 Counter:     most_common() 활용, 간결")
    print("  -> 장르별 총재생수 -> 장르 정렬 -> 각 장르 상위 2곡 패턴")
    print("  복잡도: O(N log N) (정렬 지배)")
    print()

    print("=" * 55)
    print("모든 assert 통과! 해설 실행 완료.")
    print("=" * 55)
