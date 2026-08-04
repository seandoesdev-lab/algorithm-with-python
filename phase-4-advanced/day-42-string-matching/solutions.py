"""Day 42 해설 코드 - 문자열 매칭 (KMP / 라빈-카프).

실행: PYTHONIOENCODING=cp949 python solutions.py
표준 라이브러리만 사용한다. (cp949 콘솔 안전: 출력에 ASCII 기호만 사용)

문제 목록 (출처: 프로그래머스 / LeetCode 만)
  1. LeetCode #28    Find the Index of the First Occurrence in a String  (기초)
  2. LeetCode #187   Repeated DNA Sequences                              (기초)
  3. LeetCode #459   Repeated Substring Pattern                          (중급)
  4. 프로그래머스 #17683  [3차] 방금그곡                                  (기출, 2018 카카오 3차)
  5. LeetCode #214   Shortest Palindrome                                 (심화)
  6. LeetCode #1044  Longest Duplicate Substring                         (심화)

문제 설명/힌트 -> problems.md,  개념 -> concept.md
각 문제는 플랫폼 시그니처를 지키고, 가능한 한 다중 접근 + 교차 검증을 붙였다.
"""

import random

SEP = "=" * 68
SUB = "-" * 68


# ---------------------------------------------------------------------------
# 공통 도구: 실패 함수 (오늘의 핵심. #28, #459, #214 가 전부 이것을 쓴다)
# ---------------------------------------------------------------------------
def build_pi(pat):
    """pi[i] = pat[0..i] 에서 접두사이자 접미사인 최장 '진'부분문자열의 길이."""
    m = len(pat)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pat[i] != pat[k]:
            k = pi[k - 1]
        if pat[i] == pat[k]:
            k += 1
        pi[i] = k
    return pi


# ===========================================================================
# 1. LeetCode #28 - Find the Index of the First Occurrence in a String
# ===========================================================================
class Solution28:
    """세 가지 접근. 결과는 항상 같아야 한다."""

    # (A) 파이썬 정답 - CPython 의 C 구현(Two-Way)이 가장 빠르다
    def strStr(self, haystack, needle):
        return haystack.find(needle)

    # (B) 나이브 - O(N*M). 기준선이자 "왜 느린가" 를 이해하기 위한 코드
    def strStr_naive(self, haystack, needle):
        n, m = len(haystack), len(needle)
        if m == 0:
            return 0
        for i in range(n - m + 1):
            if haystack[i:i + m] == needle:
                return i
        return -1

    # (C) KMP - O(N+M). 오늘의 주인공
    def strStr_kmp(self, haystack, needle):
        n, m = len(haystack), len(needle)
        if m == 0:
            return 0
        if m > n:
            return -1
        pi = build_pi(needle)
        j = 0
        for i in range(n):                   # i 는 절대 되돌아가지 않는다
            while j > 0 and haystack[i] != needle[j]:
                j = pi[j - 1]                # 패턴만 후퇴
            if haystack[i] == needle[j]:
                j += 1
            if j == m:
                return i - m + 1
        return -1

    # (D) KMP 로 "모든" 등장 위치 (겹치는 것 포함) - 확장형
    def find_all_kmp(self, haystack, needle):
        n, m = len(haystack), len(needle)
        if m == 0:
            return [0]
        if m > n:
            return []
        pi = build_pi(needle)
        res, j = [], 0
        for i in range(n):
            while j > 0 and haystack[i] != needle[j]:
                j = pi[j - 1]
            if haystack[i] == needle[j]:
                j += 1
            if j == m:
                res.append(i - m + 1)
                j = pi[j - 1]                # 리셋이 아니라 후퇴 -> 겹치는 매치도 잡는다
        return res


def test28():
    s = Solution28()
    cases = [
        ("sadbutsad", "sad", 0),
        ("leetcode", "leeto", -1),
        ("a", "a", 0),
        ("abc", "c", 2),
        ("mississippi", "issip", 4),
        ("aaaaab", "aab", 3),
    ]
    for hay, nee, want in cases:
        assert s.strStr(hay, nee) == want, (hay, nee)
        assert s.strStr_naive(hay, nee) == want, (hay, nee)
        assert s.strStr_kmp(hay, nee) == want, (hay, nee)

    # 겹치는 매치 확인
    assert s.find_all_kmp("aaaa", "aa") == [0, 1, 2]
    assert s.find_all_kmp("ababab", "aba") == [0, 2]

    # 무작위 교차 검증: find / 나이브 / KMP 가 언제나 같은 답을 내는가
    random.seed(28)
    for _ in range(500):
        hay = "".join(random.choice("ab") for _ in range(random.randint(1, 30)))
        nee = "".join(random.choice("ab") for _ in range(random.randint(1, 5)))
        a, b, c = s.strStr(hay, nee), s.strStr_naive(hay, nee), s.strStr_kmp(hay, nee)
        assert a == b == c, (hay, nee, a, b, c)

    print("  #28    Find First Occurrence     : 통과 (O)  find/나이브/KMP 교차검증 500")


# ===========================================================================
# 2. LeetCode #187 - Repeated DNA Sequences
# ===========================================================================
class Solution187:
    """고정 길이 10. 두 가지 접근."""

    # (A) set 슬라이싱 - 길이가 고정이라 슬라이싱이 상수 비용이다. O(n)
    def findRepeatedDnaSequences(self, s):
        seen, res = set(), set()
        for i in range(len(s) - 9):          # 윈도우 개수 = n - 10 + 1
            sub = s[i:i + 10]
            if sub in seen:
                res.add(sub)
            seen.add(sub)
        return list(res)

    # (B) 2비트 인코딩 롤링 해시 - 충돌이 아예 없는 완전 해시. Day 41 의 응용
    def findRepeatedDnaSequences_bits(self, s):
        if len(s) < 10:
            return []
        code = {"A": 0, "C": 1, "G": 2, "T": 3}
        MASK = (1 << 20) - 1                 # 하위 20비트 = 10글자 (괄호 필수!)
        seen, res = set(), set()
        h = 0
        for i, c in enumerate(s):
            h = ((h << 2) | code[c]) & MASK  # 2비트 밀어넣고 잘라낸다
            if i >= 9:                       # 윈도우가 완성된 시점부터
                if h in seen:
                    res.add(s[i - 9:i + 1])
                seen.add(h)
        return list(res)


def test187():
    s = Solution187()
    cases = [
        ("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT", {"AAAAACCCCC", "CCCCCAAAAA"}),
        ("AAAAAAAAAAAAA", {"AAAAAAAAAA"}),
        ("AAAAAAAAAA", set()),               # 딱 10글자 = 한 번만 등장
        ("ACGT", set()),                     # 10글자 미만
    ]
    for text, want in cases:
        assert set(s.findRepeatedDnaSequences(text)) == want, text
        assert set(s.findRepeatedDnaSequences_bits(text)) == want, text

    # 무작위 교차 검증: 두 방법이 언제나 같은 집합을 내는가
    random.seed(187)
    for _ in range(300):
        text = "".join(random.choice("ACGT") for _ in range(random.randint(1, 60)))
        a = set(s.findRepeatedDnaSequences(text))
        b = set(s.findRepeatedDnaSequences_bits(text))
        assert a == b, (text, a, b)

    print("  #187   Repeated DNA Sequences    : 통과 (O)  set/2비트인코딩 교차검증 300")


# ===========================================================================
# 3. LeetCode #459 - Repeated Substring Pattern
# ===========================================================================
class Solution459:
    """세 가지 접근. pi 해법이 오늘의 주인공이다."""

    # (A) pi 배열의 최소 주기 - O(n). 오늘의 정석
    def repeatedSubstringPattern(self, s):
        n = len(s)
        if n < 2:
            return False
        pi = build_pi(s)
        p = n - pi[n - 1]                    # 최소 주기
        return p < n and n % p == 0          # 두 조건 모두 필요하다!

    # (B) 약수 완전 탐색 - 가장 직관적
    def repeatedSubstringPattern_divisors(self, s):
        n = len(s)
        for k in range(1, n // 2 + 1):
            if n % k == 0 and s[:k] * (n // k) == s:
                return True
        return False

    # (C) 유명한 세 줄 트릭 - 검산용
    def repeatedSubstringPattern_trick(self, s):
        return (s + s)[1:-1].find(s) != -1


def test459():
    s = Solution459()
    cases = [
        ("abab", True),
        ("aba", False),
        ("abcabcabcabc", True),
        ("a", False),
        ("aa", True),
        ("abcabca", False),                  # 주기 3 이지만 7 % 3 != 0
        ("abcd", False),
        ("aaaaaa", True),
        ("ababab", True),
    ]
    for text, want in cases:
        assert s.repeatedSubstringPattern(text) == want, (text, "pi")
        assert s.repeatedSubstringPattern_divisors(text) == want, (text, "약수")
        assert s.repeatedSubstringPattern_trick(text) == want, (text, "트릭")

    # 무작위 교차 검증: 세 방법이 언제나 일치하는가
    random.seed(459)
    for _ in range(600):
        text = "".join(random.choice("ab") for _ in range(random.randint(1, 20)))
        a = s.repeatedSubstringPattern(text)
        b = s.repeatedSubstringPattern_divisors(text)
        c = s.repeatedSubstringPattern_trick(text)
        assert a == b == c, (text, a, b, c)

    print("  #459   Repeated Substring Pattern: 통과 (O)  pi/약수/트릭 교차검증 600")


# ===========================================================================
# 4. 프로그래머스 #17683 - [3차] 방금그곡  (2018 카카오 블라인드 3차)
# ===========================================================================
def _normalize(sheet):
    """'C#' 같은 두 글자 음을 한 글자(소문자)로 정규화한다.

    이것이 이 문제의 핵심이다. 정규화하지 않으면 'C#' 의 'C' 가
    'C' 매칭에 잘못 걸려서 오답이 난다.
    소문자는 원래 음 이름(대문자)에 없으므로 충돌하지 않는다.
    """
    for sharp, low in (("C#", "c"), ("D#", "d"), ("F#", "f"),
                       ("G#", "g"), ("A#", "a")):
        sheet = sheet.replace(sharp, low)
    return sheet


def _minutes(t):
    """'12:34' -> 754 (자정 기준 분)."""
    hh, mm = t.split(":")
    return int(hh) * 60 + int(mm)


def solution(m, musicinfos):
    """프로그래머스 시그니처. 조건에 맞는 곡명, 없으면 '(None)'."""
    target = _normalize(m)
    best_title, best_play = "(None)", -1

    for info in musicinfos:
        start, end, title, sheet = info.split(",")
        play = _minutes(end) - _minutes(start)
        if play <= 0:
            continue

        norm_sheet = _normalize(sheet)
        if not norm_sheet:
            continue

        # 재생 시간만큼 반복하고 정확히 잘라낸다 (+1 로 넉넉히 만든 뒤 절단)
        played = (norm_sheet * (play // len(norm_sheet) + 1))[:play]

        # '>' 이므로 재생 시간이 같으면 먼저 입력된 곡이 유지된다
        if target in played and play > best_play:
            best_title, best_play = title, play

    return best_title


def test17683():
    cases = [
        ("ABCDEFG",
         ["12:00,12:14,HELLO,CDEFGAB", "13:00,13:05,WORLD,ABCDEF"],
         "HELLO"),
        ("CC#BCC#BCC#BCC#B",
         ["03:00,03:30,FOO,CC#B", "04:00,04:08,BAR,CC#BCC#B"],
         "FOO"),
        ("ABC",
         ["12:00,12:14,HELLO,C#DEFGAB", "13:00,13:05,WORLD,ABCDEF"],
         "WORLD"),
        # 일치하는 곡이 없는 경우
        ("XYZ", ["12:00,12:10,NONE,ABCDEF"], "(None)"),
        # 재생 시간이 같으면 먼저 입력된 곡
        ("ABC",
         ["12:00,12:05,FIRST,ABCDE", "13:00,13:05,SECOND,ABCDE"],
         "FIRST"),
        # 재생 시간이 더 긴 곡이 이긴다 (뒤에 있어도)
        ("ABC",
         ["12:00,12:05,SHORT,ABCDE", "13:00,13:20,LONG,ABCDE"],
         "LONG"),
    ]
    for m, infos, want in cases:
        got = solution(m, infos)
        assert got == want, (m, infos, got, want)

    # 정규화가 실제로 오답을 막는지 직접 확인한다 (예시 3번의 함정)
    naive_hit = "ABC" in ("C#DEFGAB" * 2)[:14]           # 정규화 없이 -> 잘못 걸린다
    smart_hit = "ABC" in (_normalize("C#DEFGAB") * 2)[:14]
    assert naive_hit is True, "정규화 없이는 잘못된 매치가 일어난다"
    assert smart_hit is False, "정규화하면 잘못된 매치가 사라진다"

    print("  #17683 방금그곡 (카카오 3차)     : 통과 (O)  C# 정규화 효과까지 검증")


# ===========================================================================
# 5. LeetCode #214 - Shortest Palindrome
# ===========================================================================
class Solution214:
    """s 앞에만 문자를 붙여 만드는 최단 팰린드롬."""

    # (A) KMP 트릭 - O(n). 오늘의 정석
    def shortestPalindrome(self, s):
        if not s:
            return ""
        # '#' 은 입력(영소문자)에 없는 문자. 반드시 넣어야 매치가 경계를 안 넘는다
        t = s + "#" + s[::-1]
        L = build_pi(t)[-1]                  # s 의 가장 긴 팰린드롬 접두사의 길이
        return s[L:][::-1] + s

    # (B) 나이브 - O(n^2). 검증용 기준선
    def shortestPalindrome_naive(self, s):
        if not s:
            return ""
        for L in range(len(s), 0, -1):
            if s[:L] == s[:L][::-1]:
                return s[L:][::-1] + s
        return s[::-1] + s                   # 도달하지 않는다 (L=1 은 항상 팰린드롬)

    # (C) 가장 긴 팰린드롬 접두사의 길이만 따로 (학습용)
    def longest_palindromic_prefix(self, s):
        if not s:
            return 0
        return build_pi(s + "#" + s[::-1])[-1]


def test214():
    s = Solution214()
    cases = [
        ("aacecaaa", "aaacecaaa"),
        ("abcd", "dcbabcd"),
        ("", ""),
        ("a", "a"),
        ("aa", "aa"),
        ("aba", "aba"),
        ("ab", "bab"),
        ("aaa", "aaa"),                      # 구분자가 없으면 여기서 깨진다
    ]
    for text, want in cases:
        assert s.shortestPalindrome(text) == want, (text, s.shortestPalindrome(text))
        assert s.shortestPalindrome_naive(text) == want, (text, "naive")

    # 결과가 실제로 팰린드롬이고 s 로 끝나는지 성질 검사
    random.seed(214)
    for _ in range(400):
        text = "".join(random.choice("ab") for _ in range(random.randint(0, 20)))
        got = s.shortestPalindrome(text)
        assert got == got[::-1], ("팰린드롬이 아니다", text, got)
        assert got.endswith(text), ("s 로 끝나지 않는다", text, got)
        assert got == s.shortestPalindrome_naive(text), ("나이브와 불일치", text)

    # 구분자를 빼면 실제로 값이 깨진다는 것을 확인한다
    bad = build_pi("aaa" + "aaa")[-1]        # 구분자 없음 -> 5 (len(s)=3 을 넘는다!)
    good = build_pi("aaa" + "#" + "aaa")[-1]
    assert bad == 5 and good == 3, (bad, good)

    print("  #214   Shortest Palindrome       : 통과 (O)  나이브 교차검증 400 + 구분자 효과")


# ===========================================================================
# 6. LeetCode #1044 - Longest Duplicate Substring
# ===========================================================================
class Solution1044:
    """이분 탐색 + 롤링 해시. 단일 해시는 저격당하므로 이중 해시를 쓴다."""

    # 서로 다른 두 (base, mod) 쌍. 튜플로 묶으면 충돌 확률이 곱해져 사실상 0
    MOD1, BASE1 = (1 << 61) - 1, 131
    MOD2, BASE2 = 1000000007, 137

    def longestDupSubstring(self, s):
        n = len(s)
        if n < 2:
            return ""
        # ord(c) - ord('a') + 1 : +1 이 없으면 'a' 가 0 이 되어
        # "a", "aa", "aaa" 의 해시가 전부 0 이 되는 치명적 버그가 생긴다
        code = [ord(c) - ord("a") + 1 for c in s]

        def check(L):
            """길이 L 짜리 중복이 있으면 그 시작 위치, 없으면 -1. O(n)."""
            p1 = pow(self.BASE1, L - 1, self.MOD1)
            p2 = pow(self.BASE2, L - 1, self.MOD2)
            h1 = h2 = 0
            for i in range(L):
                h1 = (h1 * self.BASE1 + code[i]) % self.MOD1
                h2 = (h2 * self.BASE2 + code[i]) % self.MOD2
            seen = {(h1, h2)}
            for i in range(1, n - L + 1):
                # 롤링: 앞 글자를 빼고, 한 자리 올리고, 새 글자를 더한다
                h1 = (h1 - code[i - 1] * p1) % self.MOD1
                h1 = (h1 * self.BASE1 + code[i + L - 1]) % self.MOD1
                h2 = (h2 - code[i - 1] * p2) % self.MOD2
                h2 = (h2 * self.BASE2 + code[i + L - 1]) % self.MOD2
                key = (h1, h2)
                if key in seen:
                    return i
                seen.add(key)
            return -1

        # 길이에 대한 이분 탐색 (단조성: 길이 L 이 되면 L-1 도 반드시 된다)
        lo, hi, best = 1, n - 1, ""
        while lo <= hi:
            mid = (lo + hi) // 2
            pos = check(mid)
            if pos != -1:
                best = s[pos:pos + mid]
                lo = mid + 1                 # 더 긴 것을 노린다
            else:
                hi = mid - 1
        return best

    # 나이브 - 소규모 교차 검증용 (제출하면 TLE)
    def longestDupSubstring_naive(self, s):
        n = len(s)
        for L in range(n - 1, 0, -1):
            seen = set()
            for i in range(n - L + 1):
                sub = s[i:i + L]
                if sub in seen:
                    return sub
                seen.add(sub)
        return ""


def test1044():
    s = Solution1044()
    cases = [
        ("banana", 3),                       # "ana"
        ("abcd", 0),                         # 중복 없음
        ("aa", 1),                           # "a"
        ("abcabc", 3),                       # "abc"
        ("aaaaa", 4),                        # "aaaa" (겹쳐도 된다)
    ]
    for text, want_len in cases:
        got = s.longestDupSubstring(text)
        assert len(got) == want_len, (text, got, want_len)
        if got:
            # 실제로 두 번 이상 등장하는지 확인 (겹침 허용)
            assert text.find(got, text.find(got) + 1) != -1, ("중복이 아니다", text, got)

    # 무작위 교차 검증: 나이브와 "길이" 가 같아야 한다 (답 문자열은 여러 개일 수 있다)
    random.seed(1044)
    for _ in range(200):
        text = "".join(random.choice("ab") for _ in range(random.randint(2, 24)))
        fast = s.longestDupSubstring(text)
        slow = s.longestDupSubstring_naive(text)
        assert len(fast) == len(slow), (text, fast, slow)
        if fast:
            assert text.find(fast, text.find(fast) + 1) != -1, (text, fast)

    # 세 글자 알파벳으로도 한 번 더
    for _ in range(150):
        text = "".join(random.choice("abc") for _ in range(random.randint(2, 30)))
        assert len(s.longestDupSubstring(text)) == len(s.longestDupSubstring_naive(text)), text

    print("  #1044  Longest Duplicate Substr  : 통과 (O)  나이브 교차검증 350 (이중 해시)")


# ===========================================================================
if __name__ == "__main__":
    print()
    print(SEP)
    print("Day 42 해설 - 문자열 매칭 (KMP / 라빈-카프)")
    print(SEP)
    print()

    test28()
    test187()
    test459()
    test17683()
    test214()
    test1044()

    print()
    print(SEP)
    print("문제별 핵심 한 줄")
    print(SEP)
    print("  #28    파이썬 정답은 find 한 줄. KMP 는 pi 배열을 손에 익히려고 짠다")
    print("  #187   길이가 고정이면 set 슬라이싱으로 충분. 2비트 인코딩은 충돌 없는 완전 해시")
    print("  #459   최소 주기 = n - pi[n-1].  p < n 과 n % p == 0 을 둘 다 확인")
    print("  #17683 알고리즘이 아니라 C# 정규화가 승부처. 동점은 '>' 로 먼저 입력된 곡 유지")
    print("  #214   s + '#' + rev(s) 의 pi[-1] = 가장 긴 팰린드롬 접두사 길이. 구분자 필수")
    print("  #1044  길이 이분 탐색 + 롤링 해시. 단일 해시는 저격당하니 이중 해시로")
    print()
    print(SUB)
    print("  전체 자체 테스트 통과 (O)")
    print(SUB)
    print()
