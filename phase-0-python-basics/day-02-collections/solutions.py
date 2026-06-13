# -*- coding: utf-8 -*-
"""Day 02 해설 -- 자료형과 컬렉션 (Types & Collections).

각 문제마다 접근 방식을 주석으로 먼저 설명하고,
가능하면 여러 접근을 함께 제시한다.
실행: python solutions.py
"""

from collections import Counter

# ── 문제 1: Two Sum (LeetCode #1) ──────────────────────────────────────────
#
# 문제: 정수 배열 nums와 target이 주어질 때, 합이 target인 두 인덱스를 반환.
#
# 접근 A) dict 한 번 순회(one-pass)  |  시간복잡도: O(N), 공간복잡도: O(N)
#   - 순회하면서 "target - nums[i]"가 이미 seen dict에 있으면 정답 인덱스 반환
#   - 없으면 {nums[i]: i} 기록 후 계속
#   - 가장 빠른 방법: 탐색과 기록을 한 번의 순회로 동시 처리
#
# 접근 B) 이중 반복문(brute force)  |  시간복잡도: O(N^2), 공간복잡도: O(1)
#   - 모든 (i, j) 쌍에서 nums[i] + nums[j] == target 확인
#   - 코드는 단순하지만 N=10^4 에서 최대 10^8 연산 → 실제 제출 시 느릴 수 있음


class Solution1:
    """LeetCode #1 Two Sum."""

    def twoSum_dict(self, nums: list, target: int) -> list:
        """접근 A: dict 한 번 순회 - O(N)."""
        # seen: {값: 인덱스} 해시 테이블
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:          # O(1) 조회
                return [seen[complement], i]
            seen[num] = i                   # 아직 짝이 없으면 기록
        return []  # 정상적으로는 도달하지 않음 (답 유일 보장)

    def twoSum_brute(self, nums: list, target: int) -> list:
        """접근 B: 이중 반복문 - O(N^2). 개념 확인용."""
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


# ── 문제 2: Contains Duplicate (LeetCode #217) ─────────────────────────────
#
# 문제: 정수 배열 nums에서 같은 값이 두 번 이상 나타나면 True, 아니면 False.
#
# 접근 A) set 변환 길이 비교  |  시간복잡도: O(N), 공간복잡도: O(N)
#   - set(nums)은 중복 제거 → len이 줄었으면 중복 존재
#   - 가장 간결한 파이썬 관용구
#
# 접근 B) set 순회 조기 종료  |  시간복잡도: O(N) 최악, 공간복잡도: O(N)
#   - seen set에 이미 있으면 바로 True 반환
#   - 중복이 앞쪽에 있을수록 빠름
#
# 접근 C) 정렬 후 인접 비교  |  시간복잡도: O(N log N), 공간복잡도: O(1) 추가
#   - 정렬하면 중복 원소가 인접 → nums[i] == nums[i+1] 확인
#   - set 사용이 불가한 제약 조건이나 공간 절약이 필요할 때 활용


class Solution2:
    """LeetCode #217 Contains Duplicate."""

    def containsDuplicate_set_len(self, nums: list) -> bool:
        """접근 A: set 변환 길이 비교 - O(N)."""
        # set은 중복 원소를 하나만 보관 → 길이 차이 = 중복 존재 여부
        return len(nums) != len(set(nums))

    def containsDuplicate_set_early(self, nums: list) -> bool:
        """접근 B: set 순회 조기 종료 - O(N) 최악, 중복이 앞쪽이면 빠름."""
        seen = set()
        for num in nums:
            if num in seen:     # O(1) 해시 조회
                return True
            seen.add(num)
        return False

    def containsDuplicate_sort(self, nums: list) -> bool:
        """접근 C: 정렬 후 인접 비교 - O(N log N), 추가 공간 O(1)."""
        sorted_nums = sorted(nums)  # 원본 보존을 위해 sorted() 사용
        for i in range(len(sorted_nums) - 1):
            if sorted_nums[i] == sorted_nums[i + 1]:
                return True
        return False


# ── 문제 3: 전화번호 목록 (프로그래머스 해시 Lv.2) ──────────────────────────
#
# 문제: 전화번호 목록에서 한 번호가 다른 번호의 접두어(prefix)인지 확인.
#       접두어 관계가 하나라도 있으면 False, 없으면 True.
#
# 접근 A) set + 접두어 직접 확인  |  시간복잡도: O(N * L^2), 공간복잡도: O(N)
#   - 모든 번호를 set에 저장
#   - 각 번호의 모든 접두어(길이 1 ~ len-1)가 set에 있는지 O(1) 조회
#   - L = 번호 최대 길이(최대 20), N = 번호 수 → L이 작아 실용적
#
# 접근 B) 정렬 후 인접 비교  |  시간복잡도: O(N log N + N*L), 공간복잡도: O(N)
#   - 사전 순 정렬하면 접두어 관계인 번호들이 인접
#   - phone_list[i+1].startswith(phone_list[i]) 만 확인
#   - 정렬 비용이 있지만 코드가 단순하고 이해하기 쉬움


def solution_phonebook_set(phone_list: list) -> bool:
    """접근 A: set + 접두어 확인 - O(N * L^2)."""
    # 모든 번호를 set에 저장 - O(N)
    phone_set = set(phone_list)

    for phone in phone_list:
        # 길이 1부터 len-1까지 잘라낸 접두어가 set에 있는지 확인
        for length in range(1, len(phone)):
            prefix = phone[:length]
            if prefix in phone_set:  # O(1) 해시 조회
                return False
    return True


def solution_phonebook_sort(phone_list: list) -> bool:
    """접근 B: 정렬 후 인접 비교 - O(N log N)."""
    # 사전순 정렬: "119"와 "11999224" 같은 접두어 쌍이 인접하게 됨
    sorted_phones = sorted(phone_list)

    for i in range(len(sorted_phones) - 1):
        # 정렬 후 인접한 번호끼리만 비교하면 충분
        if sorted_phones[i + 1].startswith(sorted_phones[i]):
            return False
    return True


# ── 문제 4: 완주하지 못한 선수 (프로그래머스 해시 Lv.1) ─────────────────────
#
# 문제: 참가자 목록과 완주자 목록이 주어질 때, 완주하지 못한 한 명을 찾아라.
#       동명이인이 있으므로 단순 set 비교 불가.
#
# 접근 A) dict 빈도 카운팅  |  시간복잡도: O(N)
#   - 참가자를 dict에 +1 카운팅
#   - 완주자로 -1 차감
#   - 값이 1 이상인 키가 미완주자
#
# 접근 B) Counter 차집합  |  시간복잡도: O(N)
#   - Counter(participant) - Counter(completion) 한 줄로 해결
#   - 내부적으로 접근 A와 동일, Counter 관용구 연습에 좋음
#
# 접근 C) 정렬 비교  |  시간복잡도: O(N log N)
#   - 두 리스트를 정렬 후 나란히 비교
#   - 다른 첫 번째 위치가 미완주자 (또는 마지막 참가자)


def solve_marathon_dict(participant: list, completion: list) -> str:
    """접근 A: dict 빈도 카운팅 - O(N)."""
    count = {}
    for name in participant:
        count[name] = count.get(name, 0) + 1   # 참가자 +1
    for name in completion:
        count[name] -= 1                        # 완주자 -1

    for name, cnt in count.items():
        if cnt > 0:
            return name
    return ""   # 정상적으로는 도달하지 않음


def solve_marathon_counter(participant: list, completion: list) -> str:
    """접근 B: collections.Counter 차집합 - O(N)."""
    # Counter 차집합: 양수인 원소만 남음
    diff = Counter(participant) - Counter(completion)
    # diff에 남은 유일한 원소가 미완주자
    return list(diff.keys())[0]


def solve_marathon_sort(participant: list, completion: list) -> str:
    """접근 C: 정렬 비교 - O(N log N). dict 없이도 풀 수 있음을 보여주는 방법."""
    p = sorted(participant)
    c = sorted(completion)
    for a, b in zip(p, c):
        if a != b:
            return a
    # 모든 쌍이 일치하면 마지막 참가자가 미완주자
    return p[-1]


# ── 데모 실행 ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol1 = Solution1()
    print("=" * 60)
    print("문제 1: Two Sum (LeetCode #1)")
    print("=" * 60)
    cases1 = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
    ]
    for nums, target, expected in cases1:
        r_dict = sol1.twoSum_dict(nums[:], target)
        r_brute = sol1.twoSum_brute(nums[:], target)
        status = "O" if r_dict == expected and r_brute == expected else "X"
        print(f"  {status} nums={nums}, target={target}")
        print(f"    dict={r_dict}, brute={r_brute}  (예상: {expected})")
        assert r_dict == expected, f"dict 풀이 오류: {r_dict}"
        assert r_brute == expected, f"brute 풀이 오류: {r_brute}"
    print("  -> 모든 케이스 정답!\n")

    sol2 = Solution2()
    print("=" * 60)
    print("문제 2: Contains Duplicate (LeetCode #217)")
    print("=" * 60)
    cases2 = [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True),
    ]
    for nums, expected in cases2:
        r_a = sol2.containsDuplicate_set_len(nums)
        r_b = sol2.containsDuplicate_set_early(nums)
        r_c = sol2.containsDuplicate_sort(nums)
        status = "O" if r_a == r_b == r_c == expected else "X"
        print(f"  {status} nums={nums}")
        print(f"    set_len={r_a}, set_early={r_b}, sort={r_c}  (예상: {expected})")
        assert r_a == expected, f"set_len 풀이 오류"
        assert r_b == expected, f"set_early 풀이 오류"
        assert r_c == expected, f"sort 풀이 오류"
    print("  -> 모든 케이스 정답!\n")

    print("=" * 60)
    print("문제 3: 전화번호 목록 (프로그래머스 Lv.2)")
    print("=" * 60)
    cases3 = [
        (["119", "97674223", "1195524421"], False),  # 119가 1195524421의 접두어
        (["123", "456", "789"], True),               # 접두어 관계 없음
        (["12", "123", "1235", "567", "88"], False), # 12가 123의 접두어
    ]
    for phone_list, expected in cases3:
        r_set = solution_phonebook_set(phone_list[:])
        r_sort = solution_phonebook_sort(phone_list[:])
        status = "O" if r_set == r_sort == expected else "X"
        print(f"  {status} phone_list={phone_list}")
        print(f"    set={r_set}, sort={r_sort}  (예상: {expected})")
        assert r_set == expected, f"set 풀이 오류: {r_set}"
        assert r_sort == expected, f"sort 풀이 오류: {r_sort}"
    print("  -> 모든 케이스 정답!\n")

    print("=" * 60)
    print("문제 4: 완주하지 못한 선수 (프로그래머스 Lv.1)")
    print("=" * 60)
    cases4 = [
        (["leo", "kiki", "eden"], ["eden", "kiki"], "leo"),
        (["marina", "josipa", "nikola", "vinko", "filipa"],
         ["josipa", "filipa", "marina", "nikola"], "vinko"),
        (["mislav", "stanko", "mislav", "ana"],
         ["stanko", "ana", "mislav"], "mislav"),  # 동명이인 케이스
    ]
    for participant, completion, expected_ans in cases4:
        r_dict = solve_marathon_dict(participant[:], completion[:])
        r_counter = solve_marathon_counter(participant[:], completion[:])
        r_sort = solve_marathon_sort(participant[:], completion[:])
        status = "O" if r_dict == r_counter == r_sort == expected_ans else "X"
        print(f"  {status} participant={participant}")
        print(f"    dict={r_dict}, Counter={r_counter}, sort={r_sort}  (예상: {expected_ans})")
        assert r_dict == expected_ans, f"dict 풀이 오류: {r_dict} != {expected_ans}"
        assert r_counter == expected_ans, f"Counter 풀이 오류"
        assert r_sort == expected_ans, f"sort 풀이 오류"
    print("  -> 모든 케이스 정답!\n")

    print("모든 문제 해설 실행 완료!")
