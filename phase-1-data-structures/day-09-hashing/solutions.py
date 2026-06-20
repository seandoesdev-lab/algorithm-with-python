"""Day 9 해설 - 해시: dict / set (Hashing).

각 문제마다 접근 방식을 주석으로 먼저 설명하고,
가능하면 여러 접근(브루트포스 -> 최적화)을 함께 제시한다.
플랫폼 시그니처: LeetCode = class Solution 메서드 / 프로그래머스 = def solution(...).
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

from collections import Counter, defaultdict
from math import prod
from typing import List


# ---- 문제 1: 완주하지 못한 선수 (프로그래머스 #42576) -----------
# 동명이인이 있으므로 set 차집합은 불가(개수까지 봐야 함).
# 접근 1) Counter 뺄셈  | 시간복잡도: O(n)
def solution_42576(participant: List[str], completion: List[str]) -> str:
    # Counter(참가) - Counter(완주) => 남는 한 명(개수 0 이하 자동 제거)
    remain = Counter(participant) - Counter(completion)
    return next(iter(remain))            # 남은 단 하나의 키


# 접근 2) 정렬 후 어긋나는 지점 찾기  | 시간복잡도: O(n log n)
def solution_42576_sort(participant: List[str], completion: List[str]) -> str:
    participant.sort()
    completion.sort()
    for p, c in zip(participant, completion):
        if p != c:                       # 어긋나는 첫 지점이 미완주자
            return p
    return participant[-1]               # 끝까지 같으면 마지막이 미완주자


# ---- 문제 2: 폰켓몬 (프로그래머스 #1845) -----------------------
# N/2마리만 고를 수 있고, 종류는 set으로 센다. 둘 중 작은 값.
# 접근) set + min  | 시간복잡도: O(n)
def solution_1845(nums: List[int]) -> int:
    return min(len(nums) // 2, len(set(nums)))


# ---- 문제 3: Two Sum (LeetCode #1) ----------------------------
class Solution1:
    # 접근 1) 이중 루프(브루트포스)  | 시간복잡도: O(n^2)
    def twoSum_brute(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

    # 접근 2) 해시(보수 찾기)  | 시간복잡도: O(n)
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}                        # 값 -> 인덱스
        for i, x in enumerate(nums):
            if target - x in seen:       # 보수가 이미 있으면 정답
                return [seen[target - x], i]
            seen[x] = i
        return []


# ---- 문제 4: 전화번호 목록 (프로그래머스 #42577) --------------
# 어떤 번호가 다른 번호의 접두어이면 False.
# 접근 1) set + 접두사 검사  | 시간복잡도: O(n * L) (L=번호 길이)
def solution_42577(phone_book: List[str]) -> bool:
    book = set(phone_book)
    for number in phone_book:
        for i in range(1, len(number)):      # 자기 자신을 제외한 모든 접두사
            if number[:i] in book:           # 접두사가 다른 번호로 존재하면
                return False
    return True


# 접근 2) 정렬 후 인접 비교  | 시간복잡도: O(n log n)
def solution_42577_sort(phone_book: List[str]) -> bool:
    phone_book.sort()                        # 접두 관계는 정렬 시 인접
    for a, b in zip(phone_book, phone_book[1:]):
        if b.startswith(a):
            return False
    return True


# ---- 문제 5: 위장 (프로그래머스 #42578) -----------------------
# 종류별 (개수+1)을 곱하고, 전부 안 입는 1가지를 뺀다.
# 접근) Counter + 곱의 법칙  | 시간복잡도: O(n)
def solution_42578(clothes: List[List[str]]) -> int:
    by_type = Counter(kind for _, kind in clothes)   # 종류별 개수
    total = prod(cnt + 1 for cnt in by_type.values())
    return total - 1                         # 전부 안 입는 경우 제외


# ---- 문제 6: Group Anagrams (LeetCode #49) --------------------
class Solution49:
    # 접근 1) 정렬 문자열을 키로  | 시간복잡도: O(n * k log k) (k=단어 길이)
    def groupAnagrams_sort(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for w in strs:
            groups[tuple(sorted(w))].append(w)   # list 키 불가 -> tuple
        return list(groups.values())

    # 접근 2) 글자 개수 벡터(길이 26)를 키로  | 시간복잡도: O(n * k)
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for w in strs:
            count = [0] * 26
            for ch in w:
                count[ord(ch) - ord("a")] += 1
            groups[tuple(count)].append(w)       # 빈도 벡터를 키로(정렬 불필요)
        return list(groups.values())


# ---- 문제 7: Top K Frequent Elements (LeetCode #347) ----------
class Solution347:
    # 접근 1) Counter.most_common  | 시간복잡도: O(n log n) (most_common 내부 정렬)
    def topKFrequent_counter(self, nums: List[int], k: int) -> List[int]:
        return [val for val, _ in Counter(nums).most_common(k)]

    # 접근 2) 버킷 정렬(빈도를 인덱스로)  | 시간복잡도: O(n)
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = Counter(nums)
        buckets = [[] for _ in range(len(nums) + 1)]  # 인덱스 = 빈도
        for val, cnt in freq.items():
            buckets[cnt].append(val)
        result = []
        for cnt in range(len(buckets) - 1, 0, -1):    # 높은 빈도부터
            for val in buckets[cnt]:
                result.append(val)
                if len(result) == k:
                    return result
        return result


# ---- 문제 8: Longest Consecutive Sequence (LeetCode #128) -----
class Solution128:
    # 접근 1) 정렬  | 시간복잡도: O(n log n)
    def longestConsecutive_sort(self, nums: List[int]) -> int:
        if not nums:
            return 0
        s = sorted(set(nums))
        best = run = 1
        for prev, cur in zip(s, s[1:]):
            if cur == prev + 1:
                run += 1
                best = max(best, run)
            else:
                run = 1
        return best

    # 접근 2) set 멤버십, 시작점에서만 확장  | 시간복잡도: O(n)
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        best = 0
        for x in num_set:
            if x - 1 not in num_set:         # x가 수열의 시작점일 때만
                length = 1
                while x + length in num_set:  # 연속해서 확장
                    length += 1
                best = max(best, length)
        return best


# ---- 문제 9: 베스트앨범 (프로그래머스 #42579, 기출) ----------
# 1) 총 재생수 많은 장르 먼저, 2) 장르 내 재생수 많은 곡, 3) 같으면 인덱스 낮은 곡.
# 접근) 두 해시(장르별 합계 / 장르별 (재생수, 인덱스)) + 정렬
#       | 시간복잡도: O(n log n)
def solution_42579(genres: List[str], plays: List[int]) -> List[int]:
    total = defaultdict(int)                  # 장르 -> 총 재생수
    songs = defaultdict(list)                 # 장르 -> [(재생수, 인덱스), ...]
    for i, (g, p) in enumerate(zip(genres, plays)):
        total[g] += p
        songs[g].append((p, i))

    answer = []
    # 총 재생수 내림차순으로 장르 정렬
    for g in sorted(total, key=lambda k: -total[k]):
        # 장르 내: 재생수 내림차순, 같으면 인덱스 오름차순
        top = sorted(songs[g], key=lambda pi: (-pi[0], pi[1]))[:2]
        answer.extend(idx for _, idx in top)
    return answer


if __name__ == "__main__":
    # 문제 1
    assert solution_42576(["leo", "kiki", "eden"], ["eden", "kiki"]) == "leo"
    assert solution_42576(
        ["mislav", "stanko", "mislav", "ana"], ["stanko", "ana", "mislav"]
    ) == "mislav"
    assert solution_42576_sort(["leo", "kiki", "eden"], ["eden", "kiki"]) == "leo"
    print("[OK] 문제 1 완주하지 못한 선수")

    # 문제 2
    assert solution_1845([3, 1, 2, 3]) == 2
    assert solution_1845([3, 3, 3, 2, 2, 4]) == 3
    assert solution_1845([3, 3, 3, 2, 2, 2]) == 2
    print("[OK] 문제 2 폰켓몬")

    # 문제 3
    s1 = Solution1()
    assert s1.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s1.twoSum([3, 2, 4], 6) == [1, 2]
    assert s1.twoSum([3, 3], 6) == [0, 1]
    assert s1.twoSum_brute([2, 7, 11, 15], 9) == [0, 1]
    print("[OK] 문제 3 Two Sum")

    # 문제 4
    assert solution_42577(["119", "97674223", "1195524421"]) is False
    assert solution_42577(["123", "456", "789"]) is True
    assert solution_42577(["12", "123", "1235", "567", "88"]) is False
    assert solution_42577_sort(["119", "97674223", "1195524421"]) is False
    print("[OK] 문제 4 전화번호 목록")

    # 문제 5
    assert solution_42578(
        [["yellow_hat", "headgear"], ["blue_sunglasses", "eyewear"],
         ["green_turban", "headgear"]]
    ) == 5
    assert solution_42578(
        [["crow_mask", "face"], ["blue_sunglasses", "face"],
         ["smoky_makeup", "face"]]
    ) == 3
    print("[OK] 문제 5 위장")

    # 문제 6 (그룹 순서/내부 순서는 무관 -> 정규화 후 비교)
    def _norm(groups):
        return sorted(tuple(sorted(g)) for g in groups)
    s49 = Solution49()
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    expected49 = _norm([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
    assert _norm(s49.groupAnagrams(strs)) == expected49
    assert _norm(s49.groupAnagrams_sort(strs)) == expected49
    assert _norm(s49.groupAnagrams([""])) == [("",)]
    print("[OK] 문제 6 Group Anagrams")

    # 문제 7 (순서 무관 -> set 비교)
    s347 = Solution347()
    assert set(s347.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}
    assert set(s347.topKFrequent([1], 1)) == {1}
    assert set(s347.topKFrequent_counter([1, 1, 1, 2, 2, 3], 2)) == {1, 2}
    print("[OK] 문제 7 Top K Frequent Elements")

    # 문제 8
    s128 = Solution128()
    assert s128.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert s128.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert s128.longestConsecutive([]) == 0
    assert s128.longestConsecutive_sort([100, 4, 200, 1, 3, 2]) == 4
    print("[OK] 문제 8 Longest Consecutive Sequence")

    # 문제 9
    assert solution_42579(
        ["classic", "pop", "classic", "classic", "pop"],
        [500, 600, 150, 800, 2500]
    ) == [4, 1, 3, 0]
    print("[OK] 문제 9 베스트앨범")

    print("=== 모든 테스트 통과 ===")
