"""
Day 4 - 연습 문제 해설 (Solutions)

실행 방법: python solutions.py

각 문제마다 복수의 접근 방식을 비교하며 왜 특정 방법이 더 좋은지 설명한다.

cp949 콘솔 안전: 특수기호/이모지 미사용, 한글 및 ASCII 기호만 사용.
"""

import re
from collections import Counter


# ===============================================================
# 문제 1 - 프로그래머스 12918: 문자열 다루기 기본
# https://school.programmers.co.kr/learn/courses/30/lessons/12918
# 난이도: Level 1 | 핵심: len + isdigit
# ===============================================================

def solution_basic_v1(s):
    """
    접근 1 (권장): len + isdigit 한 줄
    - 시간 복잡도: O(N) -- isdigit가 전체 스캔
    - 공간 복잡도: O(1)

    길이가 4 또는 6이고 모든 문자가 숫자이면 True.
    s.isdigit()는 문자열 전체가 숫자로만 이루어졌는지 한 번에 판별한다.
    """
    return len(s) in (4, 6) and s.isdigit()


def solution_basic_v2(s):
    """
    접근 2 (비교용): 직접 순회하며 숫자 검사
    - 시간 복잡도: O(N)
    - isdigit를 안 쓰고 ord 범위로 직접 확인하는 교육용 버전

    '0'~'9'의 ord 범위(48~57)로 각 문자가 숫자인지 검사.
    실전에서는 v1이 훨씬 간결하다.
    """
    if len(s) not in (4, 6):
        return False
    for ch in s:
        if not (ord('0') <= ord(ch) <= ord('9')):
            return False
    return True


# ===============================================================
# 문제 2 - LeetCode 125: Valid Palindrome
# https://leetcode.com/problems/valid-palindrome/
# 난이도: Easy | 핵심: 영숫자 필터 + 슬라이싱/투 포인터
# ===============================================================

class Solution125:
    def isPalindrome_v1(self, s):
        """
        접근 1 (권장, 간결): 영숫자만 추출 후 슬라이싱 뒤집기 비교
        - 시간 복잡도: O(N)
        - 공간 복잡도: O(N) -- 정제된 새 리스트/문자열 생성

        isalnum()으로 영숫자만 남기고 lower()로 대소문자 통일.
        cleaned == cleaned[::-1] 로 회문 여부를 한 줄에 판별한다.
        """
        cleaned = [c.lower() for c in s if c.isalnum()]
        return cleaned == cleaned[::-1]

    def isPalindrome_v2(self, s):
        """
        접근 2 (메모리 최적): 투 포인터(two pointers)
        - 시간 복잡도: O(N)
        - 공간 복잡도: O(1) -- 추가 문자열을 만들지 않고 양끝 인덱스만 사용

        left, right를 양끝에서 좁혀오며 영숫자가 아닌 문자는 건너뛴다.
        대용량 문자열에서 추가 메모리 없이 처리할 때 유리하다.
        """
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True


# ===============================================================
# 문제 3 - LeetCode 242: Valid Anagram
# https://leetcode.com/problems/valid-anagram/
# 난이도: Easy~Medium | 핵심: Counter vs 정렬
# ===============================================================

class Solution242:
    def isAnagram_v1(self, s, t):
        """
        접근 1 (권장): Counter 빈도 비교
        - 시간 복잡도: O(N) -- 각 문자 1회 집계
        - 공간 복잡도: O(K) -- 문자 종류 수

        Counter(s) == Counter(t): 두 빈도표가 완전히 같은지 비교.
        길이가 다르면 자연히 False가 되지만, 미리 거르면 더 빠르다.
        """
        if len(s) != len(t):
            return False
        return Counter(s) == Counter(t)

    def isAnagram_v2(self, s, t):
        """
        접근 2 (비교용): 정렬 후 비교
        - 시간 복잡도: O(N log N) -- 정렬이 지배
        - 공간 복잡도: O(N)

        sorted(s) == sorted(t): 두 문자열을 정렬하면 애너그램은 동일해진다.
        직관적이지만 N이 크면 Counter(O(N))보다 느리다.
        """
        return sorted(s) == sorted(t)


# ===============================================================
# 문제 4 - 프로그래머스 17682: [1차] 다트 게임 (2018 카카오)
# https://school.programmers.co.kr/learn/courses/30/lessons/17682
# 난이도: Level 1 | 핵심: 문자열 파싱(정규식 / replace 트릭)
# ===============================================================

def solution_dart_v1(dartResult):
    """
    접근 1 (권장): 정규식으로 (점수, 보너스, 옵션) 추출
    - 시간 복잡도: O(N)
    - 공간 복잡도: O(N)

    패턴 (\\d+)([SDT])([*#]?):
      - \\d+   : 점수 (10 같은 두 자리 포함)
      - [SDT]  : 보너스 -> 1/2/3 제곱
      - [*#]?  : 옵션(있을 수도, 없을 수도)
    스타상(*)은 현재와 직전 점수를 각각 2배, 아차상(#)은 현재 점수를 음수로.
    """
    bonus = {"S": 1, "D": 2, "T": 3}
    matches = re.findall(r"(\d+)([SDT])([*#]?)", dartResult)

    scores = []
    for num, bo, opt in matches:
        score = int(num) ** bonus[bo]
        if opt == "*":
            score *= 2
            if scores:
                scores[-1] *= 2   # 직전 점수도 2배
        elif opt == "#":
            score *= -1
        scores.append(score)
    return sum(scores)


def solution_dart_v2(dartResult):
    """
    접근 2 (비교용): replace 트릭으로 '10'을 한 글자로 치환 후 직접 파싱
    - 시간 복잡도: O(N)
    - 정규식 없이 문자 단위로 순회하는 교육용 버전

    핵심 함정: 점수 10은 두 글자라 한 글자씩 보면 1과 0으로 쪼개진다.
    '10' -> 'k' 로 임시 치환해 한 글자로 만든 뒤, 'k'를 다시 10으로 해석한다.
    """
    data = dartResult.replace("10", "k")
    bonus = {"S": 1, "D": 2, "T": 3}

    scores = []
    for ch in data:
        if ch.isdigit() or ch == "k":
            num = 10 if ch == "k" else int(ch)
            scores.append(num)
        elif ch in bonus:
            scores[-1] = scores[-1] ** bonus[ch]
        elif ch == "*":
            scores[-1] *= 2
            if len(scores) >= 2:
                scores[-2] *= 2
        elif ch == "#":
            scores[-1] *= -1
    return sum(scores)


# ===============================================================
# 문제 5 - 프로그래머스 72410: 신규 아이디 추천 (2021 카카오)
# https://school.programmers.co.kr/learn/courses/30/lessons/72410
# 난이도: Level 1 (기출) | 핵심: 정규식 + 단계별 치환 파이프라인
# ===============================================================

def solution_recommend_id_v1(new_id):
    """
    접근 1 (권장): 정규식 기반 7단계 파이프라인
    - 시간 복잡도: O(N)
    - 공간 복잡도: O(N)

    각 단계의 결과를 다음 단계 입력으로 넘긴다.
      1) 소문자화          2) 허용 문자 외 제거
      3) 연속 마침표 -> 1개  4) 양끝 마침표 제거
      5) 빈 문자열 -> 'a'    6) 15자 자르고 끝 마침표 제거
      7) 2자 이하 -> 마지막 글자 반복으로 3자 채움
    """
    # 1단계: 소문자화
    s = new_id.lower()
    # 2단계: 허용 문자(소문자/숫자/._-) 외 제거
    s = re.sub(r"[^a-z0-9._-]", "", s)
    # 3단계: 연속 마침표를 하나로
    s = re.sub(r"\.{2,}", ".", s)
    # 4단계: 양끝 마침표 제거
    s = s.strip(".")
    # 5단계: 빈 문자열이면 'a'
    if s == "":
        s = "a"
    # 6단계: 15자로 자르고, 끝이 마침표면 제거
    s = s[:15].strip(".")
    # 7단계: 2자 이하이면 마지막 글자로 3자까지 채움
    if len(s) <= 2:
        s = s + s[-1] * (3 - len(s))
    return s


def solution_recommend_id_v2(new_id):
    """
    접근 2 (비교용): 정규식 없이 메서드/루프로 동일 처리
    - 시간 복잡도: O(N)
    - re 모듈 없이 같은 결과를 내는 교육용 버전

    2단계는 allowed 집합으로 필터, 3단계는 이전 문자와 비교하며 연속 마침표 제거.
    정규식이 없으면 코드가 길어지므로, 이런 문제는 v1(정규식)이 더 적합함을 보여준다.
    """
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-_.")

    # 1단계
    s = new_id.lower()
    # 2단계: 허용 문자만
    s = "".join(c for c in s if c in allowed)
    # 3단계: 연속 마침표 -> 하나
    buf = []
    for c in s:
        if c == "." and buf and buf[-1] == ".":
            continue
        buf.append(c)
    s = "".join(buf)
    # 4단계
    s = s.strip(".")
    # 5단계
    if s == "":
        s = "a"
    # 6단계
    s = s[:15].strip(".")
    # 7단계
    while len(s) <= 2:
        s = s + s[-1]
    return s


# ===============================================================
# 메인 -- 샘플 입력으로 모든 함수 검증 (assert)
# ===============================================================

if __name__ == "__main__":

    # -- 문제 1: 문자열 다루기 기본 --------------------------------
    print("=" * 55)
    print("[문제 1] 프로그래머스 12918: 문자열 다루기 기본")
    print("=" * 55)

    cases1 = [
        ("a234", False),
        ("1234", True),
        ("123456", True),
        ("12345", False),   # 길이 5 -> False
        ("12a4", False),
    ]
    for s, expected in cases1:
        r1 = solution_basic_v1(s)
        r2 = solution_basic_v2(s)
        print(f"s='{s}' -> v1={r1}, v2={r2}  (기댓값={expected})")
        assert r1 == expected, f"v1 실패: {s}"
        assert r2 == expected, f"v2 실패: {s}"
    print()

    # -- 문제 2: Valid Palindrome --------------------------------
    print("=" * 55)
    print("[문제 2] LeetCode 125: Valid Palindrome")
    print("=" * 55)

    sol125 = Solution125()
    cases2 = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),       # 영숫자 없음 -> 빈 문자열 -> 회문
        ("0P", False),     # '0' vs 'p'
        ("level", True),
    ]
    for s, expected in cases2:
        r1 = sol125.isPalindrome_v1(s)
        r2 = sol125.isPalindrome_v2(s)
        print(f"s='{s}' -> v1={r1}, v2={r2}  (기댓값={expected})")
        assert r1 == expected, f"v1 실패: {s}"
        assert r2 == expected, f"v2 실패: {s}"
    print("  v1 슬라이싱: O(N) 시간, O(N) 공간 -- 간결")
    print("  v2 투포인터: O(N) 시간, O(1) 공간 -- 메모리 절약")
    print()

    # -- 문제 3: Valid Anagram -----------------------------------
    print("=" * 55)
    print("[문제 3] LeetCode 242: Valid Anagram")
    print("=" * 55)

    sol242 = Solution242()
    cases3 = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("a", "ab", False),
        ("listen", "silent", True),
    ]
    for s, t, expected in cases3:
        r1 = sol242.isAnagram_v1(s, t)
        r2 = sol242.isAnagram_v2(s, t)
        print(f"s='{s}', t='{t}' -> v1={r1}, v2={r2}  (기댓값={expected})")
        assert r1 == expected, f"v1 실패: {s},{t}"
        assert r2 == expected, f"v2 실패: {s},{t}"
    print("  v1 Counter: O(N)       -- 권장")
    print("  v2 정렬:    O(N log N)  -- 직관적이나 느림")
    print()

    # -- 문제 4: 다트 게임 ----------------------------------------
    print("=" * 55)
    print("[문제 4] 프로그래머스 17682: [1차] 다트 게임")
    print("=" * 55)

    cases4 = [
        ("1S2D*3T", 37),
        ("1D2S#10S", 9),
        ("1D2S0T", 3),
        ("1S*2T*3S", 23),
        ("1D#2S*3S", 5),
        ("1T2D3D#", -4),
        ("1D2S3T*", 59),
    ]
    for dart, expected in cases4:
        r1 = solution_dart_v1(dart)
        r2 = solution_dart_v2(dart)
        print(f"dart='{dart}' -> v1={r1}, v2={r2}  (기댓값={expected})")
        assert r1 == expected, f"v1 실패: {dart} -> {r1}"
        assert r2 == expected, f"v2 실패: {dart} -> {r2}"
    print("  v1 정규식:     (점수,보너스,옵션) 한 번에 추출 -- 권장")
    print("  v2 replace트릭: '10'->'k' 치환 후 문자 단위 파싱")
    print()

    # -- 문제 5: 신규 아이디 추천 ----------------------------------
    print("=" * 55)
    print("[문제 5] 프로그래머스 72410: 신규 아이디 추천")
    print("=" * 55)

    cases5 = [
        ("...!@BaT#*..y.abcdefghijklm", "bat.y.abcdefghi"),
        ("z-+.^.", "z--"),
        ("=.=", "aaa"),
        ("123_.def", "123_.def"),
        ("abcdefghijklmn.p", "abcdefghijklmn"),
    ]
    for new_id, expected in cases5:
        r1 = solution_recommend_id_v1(new_id)
        r2 = solution_recommend_id_v2(new_id)
        print(f"id='{new_id}'")
        print(f"  v1={r1}, v2={r2}  (기댓값={expected})")
        assert r1 == expected, f"v1 실패: {new_id} -> {r1}"
        assert r2 == expected, f"v2 실패: {new_id} -> {r2}"
    print("  v1 정규식:     단계별 sub/strip 파이프라인 -- 권장")
    print("  v2 메서드/루프: 정규식 없이 동일 처리 (코드 길어짐)")
    print()

    print("=" * 55)
    print("모든 assert 통과! 해설 실행 완료.")
    print("=" * 55)
