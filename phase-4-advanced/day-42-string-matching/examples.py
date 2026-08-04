"""Day 42 예제 코드 - 문자열 매칭 (KMP / 라빈-카프).

실행: PYTHONIOENCODING=cp949 python examples.py
표준 라이브러리만 사용한다. (cp949 콘솔 안전: 출력에 ASCII 기호만 사용)

구성
  1. 나이브 탐색                 - O(N*M) 기준선
  2. 실패 함수(prefix function)  - KMP 의 심장, O(M)
  3. KMP 탐색                    - O(N+M), 겹치는 매치까지
  4. pi 배열의 응용              - 최소 주기, 반복 판정, 모든 경계(border)
  5. 라빈-카프                   - 롤링 해시로 평균 O(N+M)
  6. 접두사 해시 클래스          - 임의 구간 비교를 O(1) 로
  7. Z 알고리즘                  - KMP 의 사촌
  8. 다중 패턴 매칭              - 라빈-카프가 KMP 를 이기는 지점
  9. 실측 비교                   - 파이썬 KMP vs str.find

개념 -> concept.md,  연습문제 -> problems.md,  해설 -> solutions.py
"""

import random
import time

SEP = "=" * 68
SUB = "-" * 68

# 롤링 해시 기본 파라미터.
# 2^61-1 은 메르센 소수. 파이썬은 큰 정수를 공짜로 다루므로 10^9+7 을 고집할 이유가 없다.
MOD = (1 << 61) - 1
BASE = 131


# ===========================================================================
# 1. 나이브 탐색 - O(N*M) 기준선이자 검증용 정답
# ===========================================================================
def naive_search(text, pat):
    """모든 시작 위치에서 통째로 비교. 느리지만 확실하다."""
    n, m = len(text), len(pat)
    if m == 0:
        return [0]
    return [i for i in range(n - m + 1) if text[i:i + m] == pat]


# ===========================================================================
# 2. 실패 함수 (prefix function / failure function / LPS)
# ===========================================================================
def build_pi(pat):
    """pi[i] = pat[0..i] 에서 접두사이면서 접미사인 최장 '진'부분문자열의 길이.

    진부분문자열이므로 자기 자신은 제외한다 -> pi[0] 은 항상 0.
    시간 O(m): k 는 for 문에서 최대 m 번 증가하고 while 은 감소만 하므로
               while 의 총 반복 횟수도 m 을 넘지 못한다 (amortized).
    """
    m = len(pat)
    pi = [0] * m
    k = 0                                    # 지금까지 맞춘 접두사 길이
    for i in range(1, m):                    # i=0 은 건너뛴다 (항상 0)
        while k > 0 and pat[i] != pat[k]:
            k = pi[k - 1]                    # 실패 링크를 타고 더 짧은 접두사로 후퇴
        if pat[i] == pat[k]:
            k += 1
        pi[i] = k
    return pi


def demo_pi():
    print(SEP)
    print("2. 실패 함수(prefix function) - pi 배열")
    print(SEP)
    for pat in ["ababaca", "aabaaab", "aaaa", "abcd", "abcabcabc"]:
        pi = build_pi(pat)
        print("  P  = %-12s" % pat, " ".join(pat))
        print("  pi = %-12s" % "", " ".join(str(v) for v in pi))
        print("     -> 마지막 pi = %d  (접두사이자 접미사인 최장 길이)" % pi[-1])
        print()


# ===========================================================================
# 3. KMP 탐색 - O(N+M). 텍스트 포인터 i 는 절대 되돌아가지 않는다.
# ===========================================================================
def kmp_search(text, pat):
    """pat 이 나타나는 모든 시작 인덱스. 겹치는 매치도 전부 찾는다."""
    n, m = len(text), len(pat)
    if m == 0:
        return [0]
    if m > n:
        return []
    pi = build_pi(pat)
    res = []
    j = 0                                    # 패턴에서 맞춘 길이
    for i in range(n):                       # i 는 단조 증가! 되돌림이 없다
        while j > 0 and text[i] != pat[j]:
            j = pi[j - 1]                    # 패턴만 후퇴
        if text[i] == pat[j]:
            j += 1
        if j == m:
            res.append(i - m + 1)
            j = pi[j - 1]                    # 리셋(0)이 아니라 후퇴 -> 겹치는 매치도 잡는다
    return res


def kmp_search_non_overlapping(text, pat):
    """겹치지 않는 매치만. 차이는 매치 후 j 를 0 으로 리셋하는 것 하나뿐이다."""
    n, m = len(text), len(pat)
    if m == 0:
        return [0]
    if m > n:
        return []
    pi = build_pi(pat)
    res = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pat[j]:
            j = pi[j - 1]
        if text[i] == pat[j]:
            j += 1
        if j == m:
            res.append(i - m + 1)
            j = 0                            # <- 여기가 유일한 차이
    return res


def demo_kmp():
    print(SEP)
    print("3. KMP 탐색 - 겹치는 매치 vs 겹치지 않는 매치")
    print(SEP)
    cases = [
        ("aaaa", "aa"),
        ("ababababa", "aba"),
        ("abababacaba", "ababaca"),
        ("hello world", "xyz"),
    ]
    for text, pat in cases:
        over = kmp_search(text, pat)
        non = kmp_search_non_overlapping(text, pat)
        naive = naive_search(text, pat)
        ok = "O" if over == naive else "X"
        print("  T=%-14s P=%-9s 겹침허용=%-12s 겹침금지=%-9s 나이브대조=%s"
              % (text, pat, over, non, ok))
    print()
    print("  주의: str.count 는 겹치는 매치를 세지 않는다.")
    print("        'aaaa'.count('aa') = %d   (KMP 는 %d 개)"
          % ("aaaa".count("aa"), len(kmp_search("aaaa", "aa"))))
    print()


# ===========================================================================
# 4. pi 배열의 응용 - 주기, 반복 판정, 모든 경계
# ===========================================================================
def min_period(s):
    """s 의 최소 주기. 반복 구조가 없으면 len(s) 를 반환한다."""
    if not s:
        return 0
    return len(s) - build_pi(s)[-1]


def is_repeated(s):
    """s 가 어떤 부분 문자열의 2번 이상 반복으로 만들어지는가? (LeetCode #459)

    주기 p 가 전체 길이를 나눠떨어뜨려야 한다는 조건(n % p == 0)이 핵심이다.
    """
    n = len(s)
    if n < 2:
        return False
    p = n - build_pi(s)[-1]
    return p < n and n % p == 0


def all_borders(s):
    """접두사이면서 접미사인 모든 길이를 내림차순으로. 실패 링크를 따라간다."""
    if not s:
        return []
    pi = build_pi(s)
    res = []
    k = pi[-1]
    while k > 0:
        res.append(k)
        k = pi[k - 1]
    return res


def demo_period():
    print(SEP)
    print("4. pi 배열의 응용 - 최소 주기와 반복 판정")
    print(SEP)
    samples = ["abcabcabc", "ababab", "abcabca", "abcd", "aaaaaa", "abaababaab"]
    print("  %-12s %-6s %-8s %-6s %s" % ("문자열", "길이", "최소주기", "반복?", "모든 경계"))
    print("  " + SUB)
    for s in samples:
        print("  %-12s %-6d %-8d %-6s %s"
              % (s, len(s), min_period(s), "O" if is_repeated(s) else "X", all_borders(s)))
    print()
    print("  'abcabca' 는 주기가 3 이지만 7 % 3 != 0 이라 반복 구성이 아니다.")
    print("  -> n % p == 0 검사를 빼먹는 것이 #459 최다 오답이다.")
    print()


# ===========================================================================
# 5. 라빈-카프 - 롤링 해시
# ===========================================================================
def rabin_karp(text, pat, base=BASE, mod=MOD, verify=True):
    """평균 O(N+M). 해시가 같을 때만 실제 문자열을 비교(verify)한다."""
    n, m = len(text), len(pat)
    if m == 0:
        return [0]
    if m > n:
        return []

    power = pow(base, m - 1, mod)            # B^(m-1) 을 미리 계산
    hp = ht = 0
    for i in range(m):
        hp = (hp * base + ord(pat[i])) % mod
        ht = (ht * base + ord(text[i])) % mod

    res = []
    for i in range(n - m + 1):
        if ht == hp and (not verify or text[i:i + m] == pat):
            res.append(i)
        if i + m < n:
            # 롤링 O(1): 앞 글자 기여를 빼고, 한 자리 올리고, 새 글자를 더한다
            ht = (ht - ord(text[i]) * power) % mod
            ht = (ht * base + ord(text[i + m])) % mod
            # 파이썬의 % 는 항상 비음수를 반환하므로 음수 보정이 필요 없다
    return res


def demo_rabin_karp():
    print(SEP)
    print("5. 라빈-카프 - 롤링 해시로 문자열을 숫자로")
    print(SEP)
    text = "abracadabra abracadabra"
    pat = "abra"
    print("  T =", text)
    print("  P =", pat)
    print("  라빈-카프 :", rabin_karp(text, pat))
    print("  KMP       :", kmp_search(text, pat))
    print("  나이브    :", naive_search(text, pat))
    print()

    # 롤링이 실제로 어떻게 굴러가는지 한 칸씩 보여준다
    print("  롤링 과정 (작은 모듈러로 값을 작게 만들어 관찰)")
    s, m, b, small = "abcde", 3, 131, 1000003
    power = pow(b, m - 1, small)
    h = 0
    for i in range(m):
        h = (h * b + ord(s[i])) % small
    print("    window=%s  hash=%d" % (s[0:m], h))
    for i in range(len(s) - m):
        h = (h - ord(s[i]) * power) % small
        h = (h * b + ord(s[i + m])) % small
        # 처음부터 다시 계산한 값과 같은지 확인한다
        chk = 0
        for c in s[i + 1:i + 1 + m]:
            chk = (chk * b + ord(c)) % small
        mark = "O" if h == chk else "X"
        print("    window=%s  hash=%d   재계산과 일치=%s" % (s[i + 1:i + 1 + m], h, mark))
    print()


# ===========================================================================
# 6. 접두사 해시 - 임의 구간 비교를 O(1) 로 (누적 합과 같은 구조)
# ===========================================================================
class RollingHash:
    """전처리 O(n) 후, 임의 구간 [l, r) 의 해시를 O(1) 에 돌려준다.

    누적 합:   sum[l..r)  = S[r] - S[l]
    롤링해시:  hash[l..r) = H[r] - H[l] * B^(r-l)
    차이는 자릿수를 맞춰 주는 B^(r-l) 뿐이다.
    """

    def __init__(self, s, base=BASE, mod=MOD):
        self.mod = mod
        n = len(s)
        self.h = [0] * (n + 1)               # h[i] = s[0..i-1] 의 해시
        self.p = [1] * (n + 1)               # p[i] = base^i
        for i, c in enumerate(s):
            self.h[i + 1] = (self.h[i] * base + ord(c)) % mod
            self.p[i + 1] = (self.p[i] * base) % mod

    def get(self, l, r):
        """구간 [l, r) 의 해시."""
        return (self.h[r] - self.h[l] * self.p[r - l]) % self.mod

    def same(self, l1, l2, length):
        """두 구간이 같은가? O(1)."""
        return self.get(l1, l1 + length) == self.get(l2, l2 + length)


def demo_prefix_hash():
    print(SEP)
    print("6. 접두사 해시 - 임의 구간 비교를 O(1) 로")
    print(SEP)
    s = "abcabcxyzabc"
    rh = RollingHash(s)
    print("  s =", s, " (인덱스 0 부터)")
    print()
    pairs = [(0, 3, 3), (0, 6, 3), (0, 9, 3), (3, 9, 3), (0, 6, 6)]
    for l1, l2, ln in pairs:
        a, b = s[l1:l1 + ln], s[l2:l2 + ln]
        fast = rh.same(l1, l2, ln)
        slow = (a == b)
        mark = "O" if fast == slow else "X"
        print("    s[%2d:%2d]=%-7s vs s[%2d:%2d]=%-7s  해시비교=%-5s 실제비교=%-5s 일치=%s"
              % (l1, l1 + ln, a, l2, l2 + ln, b, fast, slow, mark))
    print()
    print("  이 O(1) 구간 비교가 KMP 로는 불가능한 일이고, #1044 의 열쇠다.")
    print()


# ===========================================================================
# 7. Z 알고리즘 - KMP 의 사촌
# ===========================================================================
def z_function(s):
    """z[i] = s 와 s[i:] 의 최장 공통 접두사 길이. z[0] 은 0 으로 둔다."""
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])      # 이미 계산한 값을 재활용
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]               # 박스 갱신
    return z


def z_search(text, pat, sep="\x00"):
    """Z 알고리즘으로 패턴 매칭. 구분자는 입력에 없는 문자여야 한다."""
    m = len(pat)
    if m == 0:
        return [0]
    z = z_function(pat + sep + text)
    return [i - m - 1 for i in range(m + 1, len(z)) if z[i] == m]


def demo_z():
    print(SEP)
    print("7. Z 알고리즘 - KMP 와 같은 O(N+M)")
    print(SEP)
    s = "aabxaayaa"
    print("  s =", " ".join(s))
    print("  z =", " ".join(str(v) for v in z_function(s)))
    print()
    text, pat = "abababacaba", "aba"
    print("  T=%s  P=%s" % (text, pat))
    print("    Z 알고리즘 :", z_search(text, pat))
    print("    KMP        :", kmp_search(text, pat))
    print()


# ===========================================================================
# 8. 다중 패턴 - 라빈-카프가 KMP 를 이기는 지점
# ===========================================================================
def multi_pattern_search(text, patterns):
    """길이가 같은 패턴 여러 개를 한 번의 스캔으로. O(N + 패턴총길이).

    KMP 로 하면 패턴마다 한 번씩 훑어야 하므로 O(k*N) 이다.
    """
    if not patterns:
        return {}
    m = len(patterns[0])
    assert all(len(p) == m for p in patterns), "이 데모는 길이가 같은 패턴만 다룬다"

    n = len(text)
    found = {p: [] for p in patterns}
    if m == 0 or m > n:
        return found

    # 패턴 해시 -> 그 해시를 가진 패턴들 (충돌 대비로 리스트)
    table = {}
    for p in patterns:
        h = 0
        for c in p:
            h = (h * BASE + ord(c)) % MOD
        table.setdefault(h, []).append(p)

    power = pow(BASE, m - 1, MOD)
    ht = 0
    for i in range(m):
        ht = (ht * BASE + ord(text[i])) % MOD

    for i in range(n - m + 1):
        if ht in table:
            window = text[i:i + m]           # 해시가 맞을 때만 슬라이싱한다
            for p in table[ht]:
                if p == window:              # 실제 검증
                    found[p].append(i)
        if i + m < n:
            ht = (ht - ord(text[i]) * power) % MOD
            ht = (ht * BASE + ord(text[i + m])) % MOD
    return found


def demo_multi():
    print(SEP)
    print("8. 다중 패턴 매칭 - 텍스트를 한 번만 훑는다")
    print(SEP)
    text = "the cat sat on the mat with a bat and a hat"
    pats = ["cat", "bat", "hat", "mat", "rat"]
    res = multi_pattern_search(text, pats)
    print("  T =", text)
    for p in pats:
        # KMP 로 따로 구한 결과와 대조한다
        expect = kmp_search(text, p)
        mark = "O" if res[p] == expect else "X"
        print("    %-5s -> %-10s (KMP 대조 %s)" % (p, res[p], mark))
    print()
    print("  라빈-카프: O(N + 패턴총길이)   KMP 반복: O(k * N)")
    print("  패턴이 많아질수록 격차가 벌어진다.")
    print()


# ===========================================================================
# 9. 실측 비교 - 파이썬 KMP vs str.find
# ===========================================================================
def bench():
    print(SEP)
    print("9. 실측 비교 - 복잡도가 같아도 언어 상수가 승부를 가른다")
    print(SEP)

    for n in (20000, 100000):
        # 최악에 가까운 입력: 같은 문자가 반복되고 마지막에만 다른 글자
        text = "a" * n + "b"
        pat = "a" * 50 + "b"

        t0 = time.perf_counter()
        r1 = kmp_search(text, pat)
        t1 = time.perf_counter()
        pos = text.find(pat)
        r2 = [pos] if pos != -1 else []
        t2 = time.perf_counter()

        kmp_ms = (t1 - t0) * 1000
        find_ms = (t2 - t1) * 1000
        ratio = kmp_ms / find_ms if find_ms > 0 else float("inf")
        agree = "O" if (r1[:1] == r2) else "X"

        print("  N=%-7d  KMP=%8.2f ms   find=%8.4f ms   비율=%7.0f배   결과일치=%s"
              % (n, kmp_ms, find_ms, ratio, agree))

    print()
    print("  둘 다 O(N+M) 이다. 차이는 순수하게 상수(파이썬 루프 vs C 루프)다.")
    print("  -> 단순히 '찾기만' 한다면 파이썬에서는 str.find 가 정답이다.")
    print("  -> KMP 를 직접 쓰는 이유는 pi 배열(주기/경계 정보)이 필요할 때다.")
    print()


# ===========================================================================
# 자체 검증
# ===========================================================================
def self_test():
    print(SEP)
    print("자체 검증 (무작위 입력 교차 대조)")
    print(SEP)
    random.seed(2026)

    # 세 구현이 항상 같은 답을 내는지 무작위로 확인한다
    for _ in range(400):
        n = random.randint(0, 40)
        m = random.randint(0, 6)
        alpha = "ab"                          # 좁은 알파벳이 충돌/경계를 잘 유발한다
        text = "".join(random.choice(alpha) for _ in range(n))
        pat = "".join(random.choice(alpha) for _ in range(m))
        a = naive_search(text, pat)
        b = kmp_search(text, pat)
        c = rabin_karp(text, pat)
        d = z_search(text, pat)
        assert a == b, ("KMP 불일치", text, pat, a, b)
        assert a == c, ("라빈-카프 불일치", text, pat, a, c)
        assert a == d, ("Z 불일치", text, pat, a, d)
    print("  나이브 vs KMP vs 라빈-카프 vs Z : 400 케이스 전부 일치 (O)")

    # pi 배열의 정의를 완전 탐색으로 직접 검증한다
    for _ in range(200):
        m = random.randint(1, 14)
        s = "".join(random.choice("abc") for _ in range(m))
        pi = build_pi(s)
        for i in range(m):
            best = 0
            for k in range(1, i + 1):         # k = i+1 (자기 자신)은 제외
                if s[:k] == s[i + 1 - k:i + 1]:
                    best = k
            assert pi[i] == best, ("pi 불일치", s, i, pi[i], best)
    print("  pi 배열 정의 완전 탐색 대조     : 200 케이스 전부 일치 (O)")

    # 주기/반복 판정을 완전 탐색으로 검증한다
    for _ in range(200):
        m = random.randint(1, 16)
        s = "".join(random.choice("ab") for _ in range(m))
        brute = any(m % k == 0 and s == s[:k] * (m // k) for k in range(1, m))
        assert is_repeated(s) == brute, ("반복 판정 불일치", s)
    print("  반복 판정 완전 탐색 대조        : 200 케이스 전부 일치 (O)")

    # 접두사 해시의 구간 비교를 실제 비교와 대조한다
    for _ in range(100):
        s = "".join(random.choice("abc") for _ in range(random.randint(1, 30)))
        rh = RollingHash(s)
        n = len(s)
        for _ in range(20):
            ln = random.randint(1, n)
            l1 = random.randint(0, n - ln)
            l2 = random.randint(0, n - ln)
            assert rh.same(l1, l2, ln) == (s[l1:l1 + ln] == s[l2:l2 + ln])
    print("  접두사 해시 구간 비교 대조      : 2000 질의 전부 일치 (O)")
    print()


if __name__ == "__main__":
    print()
    print("Day 42 - 문자열 매칭 (KMP / 라빈-카프)")
    print()
    demo_pi()
    demo_kmp()
    demo_period()
    demo_rabin_karp()
    demo_prefix_hash()
    demo_z()
    demo_multi()
    bench()
    self_test()
    print(SEP)
    print("핵심 정리")
    print(SEP)
    print("  1) KMP = 패턴의 자기 유사성(pi 배열)을 미리 계산 -> 텍스트 포인터를 되돌리지 않는다")
    print("  2) 라빈-카프 = 문자열을 숫자로 -> 비교가 한 번, 롤링 갱신이 O(1)")
    print("  3) 최소 주기 = n - pi[n-1],  반복 판정은 n % 주기 == 0 까지 확인")
    print("  4) 접두사 해시 = 문자열판 누적 합 -> 임의 구간 비교 O(1)")
    print("  5) 파이썬에서 단순 탐색은 str.find 가 가장 빠르다 (C 구현)")
    print("  6) KMP 를 직접 쓰는 진짜 이유는 탐색이 아니라 pi 배열 그 자체다")
    print()
