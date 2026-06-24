# -*- coding: utf-8 -*-
"""
Day 13 - 해시맵 응용 (Hashmap Patterns) 문제 해설

- LeetCode 문제는 `class Solution` 시그니처를 따른다.
- 프로그래머스 문제는 `def solution(...)` 시그니처를 따른다.
- 가능한 경우 다중 접근(해시 / 정렬 / 누적합 등)을 보여주고 맨 아래 assert 로 자체 검증.
- cp949 콘솔 안전: print 출력에는 ASCII 기호(=, -, O, X)만 사용(한글은 OK).

실행:  PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import Counter, defaultdict, OrderedDict
from itertools import combinations
import random


# ===========================================================================
# 1) LeetCode #560 - Subarray Sum Equals K  (누적합 + 해시맵)
#    prefix[j] - prefix[i] == k  <=>  prefix[i] == prefix[j] - k
# ===========================================================================
class SolutionSubarraySum:
    # 접근: 누적합의 등장 횟수를 dict 로 누적하며 즉시 카운트. O(n) / O(n)
    def subarraySum(self, nums, k):
        count = 0
        prefix = 0
        seen = defaultdict(int)
        seen[0] = 1                  # 빈 접두부(합 0)를 1번 본 것으로 시작
        for x in nums:
            prefix += x
            count += seen[prefix - k]
            seen[prefix] += 1
        return count


# ===========================================================================
# 2) LeetCode #523 - Continuous Subarray Sum  (누적합 + 나머지 해시맵)
#    합이 k 의 배수 <=> 두 누적합의 나머지(mod k)가 같다.
#    길이 2 이상 조건 -> "나머지를 처음 본 인덱스"를 저장해 거리 검사.
# ===========================================================================
class SolutionContinuousSum:
    def checkSubarraySum(self, nums, k):
        prefix = 0
        first_idx = {0: -1}          # 나머지 -> 처음 등장한 인덱스
        for i, x in enumerate(nums):
            prefix += x
            r = prefix % k
            if r in first_idx:
                if i - first_idx[r] >= 2:   # 길이 2 이상
                    return True
            else:
                first_idx[r] = i     # 처음 본 나머지만 기록(가장 이른 위치 유지)
        return False


# ===========================================================================
# 3) LeetCode #454 - 4Sum II  (보수 찾기를 두 그룹으로 분할)
#    네 배열을 2+2 로 쪼개 한쪽 합의 빈도를 dict 에 모으고,
#    다른 쪽 합의 보수(-합)를 조회. O(n^2).
# ===========================================================================
class Solution4SumII:
    def fourSumCount(self, a, b, c, d):
        ab = Counter(x + y for x in a for y in b)   # 합 -> 횟수
        total = 0
        for x in c:
            for y in d:
                total += ab[-(x + y)]               # 보수 합의 개수만큼 더함
        return total


# ===========================================================================
# 4) LeetCode #205 - Isomorphic Strings  (양방향 매핑)
# ===========================================================================
class SolutionIsomorphic:
    # 접근 A: 두 dict 로 양방향 1:1 대응 검증
    def isIsomorphic(self, s, t):
        if len(s) != len(t):
            return False
        st, ts = {}, {}
        for a, b in zip(s, t):
            if st.setdefault(a, b) != b:
                return False
            if ts.setdefault(b, a) != a:
                return False
        return True

    # 접근 B: "처음 등장 위치 패턴"이 같은가
    def isIsomorphicB(self, s, t):
        return [s.index(c) for c in s] == [t.index(c) for c in t]


# ===========================================================================
# 5) LeetCode #290 - Word Pattern  (양방향 매핑, 토큰 단위)
# ===========================================================================
class SolutionWordPattern:
    def wordPattern(self, pattern, s):
        words = s.split()
        if len(pattern) != len(words):
            return False
        p2w, w2p = {}, {}
        for c, w in zip(pattern, words):
            if p2w.setdefault(c, w) != w:
                return False
            if w2p.setdefault(w, c) != c:
                return False
        return True


# ===========================================================================
# 6) LeetCode #380 - Insert Delete GetRandom O(1)  (dict + 리스트 설계)
#    삭제는 "마지막 원소와 swap 후 pop" 으로 O(1) 유지.
# ===========================================================================
class RandomizedSet:
    def __init__(self):
        self.vals = []
        self.pos = {}                # 값 -> vals 인덱스

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i = self.pos[val]
        last = self.vals[-1]
        self.vals[i] = last
        self.pos[last] = i
        self.vals.pop()
        del self.pos[val]
        return True

    def getRandom(self):
        return random.choice(self.vals)


# ===========================================================================
# 7) LeetCode #146 - LRU Cache  (해시맵 + 순서 유지)
#    OrderedDict - move_to_end 로 최근 사용 갱신, popitem(last=False)로 추방.
# ===========================================================================
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()      # key -> value, 순서 = 사용 이력

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)     # 방금 사용 -> 맨 뒤(최신)로
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)   # 가장 오래된(맨 앞) 항목 추방


# ===========================================================================
# 8) 프로그래머스 #42888 - 오픈채팅방  (uid -> 닉네임 매핑)
#    Enter/Change 로 최종 닉네임 dict 를 확정한 뒤, 로그를 재생성.
# ===========================================================================
def solution_chat(record):
    name = {}                        # uid -> 최종 닉네임
    events = []                      # (uid, 메시지)
    for line in record:
        parts = line.split()
        cmd, uid = parts[0], parts[1]
        if cmd in ("Enter", "Change"):
            name[uid] = parts[2]
        if cmd == "Enter":
            events.append((uid, "님이 들어왔습니다."))
        elif cmd == "Leave":
            events.append((uid, "님이 나갔습니다."))
    return [name[uid] + msg for uid, msg in events]


# ===========================================================================
# 9) 프로그래머스 #92334 - 신고 결과 받기  (다중 해시: 집합 + 카운터)
# ===========================================================================
def solution_report(id_list, report, k):
    reported_by = defaultdict(set)   # 피신고자 -> 신고한 사람 집합(중복 제거)
    for line in set(report):         # 같은 (신고자,피신고자)는 1회로
        reporter, reported = line.split()
        reported_by[reported].add(reporter)

    # 정지될 사람: k번 이상 신고당한 사람
    banned = {u for u, s in reported_by.items() if len(s) >= k}
    # 각 사람이 "신고한 사람 중 정지된 수" = 받을 메일 수
    mail = defaultdict(int)
    for reported, reporters in reported_by.items():
        if reported in banned:
            for r in reporters:
                mail[r] += 1
    return [mail[u] for u in id_list]


# ===========================================================================
# 10) 프로그래머스 #72411 - 메뉴 리뉴얼  (조합 + Counter)
#     각 손님 주문에서 길이 c 조합을 모두 세고, 최다 빈도(2 이상)만 채택.
# ===========================================================================
def solution_menu(orders, course):
    answer = []
    for c in course:
        counter = Counter()
        for order in orders:
            for combo in combinations(sorted(order), c):
                counter[combo] += 1
        if not counter:
            continue
        best = max(counter.values())
        if best >= 2:                # 2명 이상이 함께 주문한 것만
            answer += ["".join(combo) for combo, n in counter.items()
                       if n == best]
    return sorted(answer)


# ===========================================================================
# 자체 검증
# ===========================================================================
def main():
    print("=" * 56)
    print("Day 13 - 해시맵 응용 solutions 자체 검증")
    print("=" * 56)

    # 1) Subarray Sum Equals K
    s1 = SolutionSubarraySum()
    assert s1.subarraySum([1, 1, 1], 2) == 2
    assert s1.subarraySum([1, 2, 3], 3) == 2
    assert s1.subarraySum([1, -1, 0], 0) == 3
    print("[1] Subarray Sum Equals K (#560)   : OK")

    # 2) Continuous Subarray Sum
    s2 = SolutionContinuousSum()
    assert s2.checkSubarraySum([23, 2, 4, 6, 7], 6) is True
    assert s2.checkSubarraySum([23, 2, 6, 4, 7], 13) is False
    assert s2.checkSubarraySum([0, 0], 1) is True
    print("[2] Continuous Subarray Sum (#523) : OK")

    # 3) 4Sum II
    s3 = Solution4SumII()
    assert s3.fourSumCount([1, 2], [-2, -1], [-1, 2], [0, 2]) == 2
    assert s3.fourSumCount([0], [0], [0], [0]) == 1
    print("[3] 4Sum II (#454)                 : OK")

    # 4) Isomorphic Strings
    s4 = SolutionIsomorphic()
    assert s4.isIsomorphic("egg", "add") is True
    assert s4.isIsomorphic("foo", "bar") is False
    assert s4.isIsomorphic("paper", "title") is True
    assert s4.isIsomorphicB("badc", "baba") is False
    print("[4] Isomorphic Strings (#205)      : OK")

    # 5) Word Pattern
    s5 = SolutionWordPattern()
    assert s5.wordPattern("abba", "dog cat cat dog") is True
    assert s5.wordPattern("abba", "dog cat cat fish") is False
    assert s5.wordPattern("aaaa", "dog cat cat dog") is False
    print("[5] Word Pattern (#290)            : OK")

    # 6) RandomizedSet
    rs = RandomizedSet()
    assert rs.insert(1) is True
    assert rs.remove(2) is False
    assert rs.insert(2) is True
    assert rs.remove(1) is True
    assert rs.insert(2) is False
    assert rs.getRandom() == 2
    print("[6] Insert Delete GetRandom (#380) : OK")

    # 7) LRU Cache
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1           # 1 사용 -> 최신
    lru.put(3, 3)                    # 용량 초과 -> 가장 오래된 2 추방
    assert lru.get(2) == -1
    lru.put(4, 4)                    # 1 추방
    assert lru.get(1) == -1
    assert lru.get(3) == 3
    assert lru.get(4) == 4
    print("[7] LRU Cache (#146)               : OK")

    # 8) 오픈채팅방
    rec = ["Enter uid1234 Muzi", "Enter uid4567 Prodo",
           "Leave uid1234", "Enter uid1234 Prodo", "Change uid4567 Ryan"]
    assert solution_chat(rec) == [
        "Prodo님이 들어왔습니다.",
        "Ryan님이 들어왔습니다.",
        "Prodo님이 나갔습니다.",
        "Prodo님이 들어왔습니다.",
    ]
    print("[8] 오픈채팅방 (#42888)            : OK")

    # 9) 신고 결과 받기
    assert solution_report(
        ["muzi", "frodo", "apeach", "neo"],
        ["muzi frodo", "apeach frodo", "frodo neo", "muzi neo", "apeach muzi"],
        2) == [2, 1, 1, 0]
    assert solution_report(
        ["con", "ryan"],
        ["ryan con", "ryan con", "ryan con", "ryan con"],
        3) == [0, 0]
    print("[9] 신고 결과 받기 (#92334)        : OK")

    # 10) 메뉴 리뉴얼
    got = solution_menu(
        ["ABCFG", "AC", "CDE", "ACDE", "BCFG", "ACDEH"], [2, 3, 4])
    assert got == ["AC", "ACDE", "BCFG", "CDE"]
    got2 = solution_menu(
        ["ABCDE", "AB", "CD", "ADE", "XYZ", "XYZ", "ACD"], [2, 3, 5])
    assert got2 == ["ACD", "AD", "ADE", "CD", "XYZ"]
    print("[10] 메뉴 리뉴얼 (#72411)          : OK")

    print("\n모든 solutions 검증 통과")


if __name__ == "__main__":
    main()
