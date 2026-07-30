"""Day 39 - 트라이 (Trie / Prefix Tree) 연습문제 해설

문제 출처: 프로그래머스 / LeetCode 만 사용.
플랫폼 시그니처를 그대로 유지하고, assert 로 자체 검증한다.

실행: PYTHONIOENCODING=cp949 python solutions.py

수록 문제
  1. LeetCode #208     Implement Trie (Prefix Tree)               - 기초
  2. 프로그래머스 #42577  전화번호 목록                              - 중급
  3. LeetCode #211     Design Add and Search Words Data Structure - 중급
  4. LeetCode #1268    Search Suggestions System                  - 중급
  5. 프로그래머스 #60060  가사 검색 (2020 카카오 블라인드)             - 기출
  6. LeetCode #212     Word Search II                             - 심화
"""

import random
import time
from bisect import bisect_left, bisect_right
from collections import defaultdict
from typing import List


def title(text):
    """섹션 제목 (cp949 안전: ASCII 기호만)."""
    print()
    print("=" * 70)
    print(text)
    print("=" * 70)


def yn(flag):
    return "O" if flag else "X"


# ===========================================================================
# 1. LeetCode #208 - Implement Trie (Prefix Tree)
#    https://leetcode.com/problems/implement-trie-prefix-tree/
#
#    핵심: search 와 startsWith 는 is_end 를 보느냐 마느냐 한 줄 차이다.
# ===========================================================================

class Trie:
    """접근 1: 클래스 노드 + __slots__ (가장 명시적. 확장하기 쉽다)

    insert     : O(L)
    search     : O(L)
    startsWith : O(L)
    공간       : O(총 글자 수)

    L = 문자열 길이. 저장된 단어 수 N 과 무관하다 -> log 가 없다.
    """

    class _Node:
        __slots__ = ("children", "is_end")

        def __init__(self):
            self.children = {}
            self.is_end = False

    def __init__(self):
        self.root = self._Node()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = self._Node()
            node = node.children[ch]
        node.is_end = True  # 마지막에 도장. 이걸 빼먹으면 트라이가 망가진다

    def _walk(self, s):
        """s 경로를 따라 내려가 도착 노드. 끊기면 None. 중복 제거용 헬퍼."""
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end  # is_end 를 본다

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None    # is_end 를 안 본다


class TrieDict:
    """접근 2: 중첩 dict (코테에서 가장 빠르게 쓰는 형태. 클래스 정의 불필요)

    복잡도는 접근 1과 동일. 코드가 짧지만 확장성은 떨어진다.
    끝 표시 키는 실제 문자와 절대 겹치지 않아야 한다 -> None 사용.
    """

    END = None

    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})  # 없으면 만들고, 있으면 재사용
        node[self.END] = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and self.END in node

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None


def test_p1():
    title("1. LeetCode #208 - Implement Trie (Prefix Tree)")

    for label, cls in (("클래스 노드", Trie), ("중첩 dict", TrieDict)):
        t = cls()
        t.insert("apple")
        assert t.search("apple") is True
        assert t.search("app") is False, "경로는 있어도 단어가 아니다"
        assert t.startsWith("app") is True, "접두사로는 존재한다"
        t.insert("app")
        assert t.search("app") is True, "이제 단어로 등록됐다"

        # 경계 케이스
        t2 = cls()
        assert t2.search("x") is False
        assert t2.startsWith("x") is False
        t2.insert("card")
        assert t2.search("car") is False, "card 만 넣었으면 car 는 단어가 아니다"
        assert t2.startsWith("car") is True
        assert t2.startsWith("cards") is False, "경로가 끊긴다"
        print("  {:<14} 통과".format(label))

    print()
    print("문제 예시 재현 (LeetCode 공식 예제):")
    t = Trie()
    ops = [("insert", "apple"), ("search", "apple"), ("search", "app"),
           ("startsWith", "app"), ("insert", "app"), ("search", "app")]
    expected = [None, True, False, True, None, True]
    for (op, arg), exp in zip(ops, expected):
        got = getattr(t, op)(arg)
        assert got == exp, (op, arg, got, exp)
        print("  {:<12}({!r:<9}) -> {}".format(op, arg, got))

    print()
    print("복잡도: 세 연산 모두 O(L). 단어 수 N 과 무관하다.")
    print("  BST 는 O(L log N), 정렬+이분탐색도 O(L log N). 트라이만 log 가 없다.")


# ===========================================================================
# 2. 프로그래머스 #42577 - 전화번호 목록
#    https://school.programmers.co.kr/learn/courses/30/lessons/42577
#
#    한 번호가 다른 번호의 접두어면 False, 아니면 True.
#    (반환값 방향이 직관과 반대다. 주의!)
# ===========================================================================

def solution_42577_hash(phone_book):
    """접근 1: 해시 - 각 번호의 모든 접두사를 set 에서 조회

    시간 O(sum(L^2))  (슬라이싱 비용 포함. L <= 20 이므로 실전 OK)
    공간 O(sum(L))
    """
    s = set(phone_book)
    for number in phone_book:
        for i in range(1, len(number)):
            if number[:i] in s:
                return False
    return True


def solution_42577_sort(phone_book):
    """접근 2: 정렬 - 사전 순 정렬 후 '인접한 쌍'만 검사  <- 이 문제의 실전 최적해

    시간 O(N log N x L)
    공간 O(N)

    정당성: a 가 b 의 접두사면, 사전 순에서 a 와 b 사이에 오는 모든 문자열도
            a 로 시작한다(접두사가 같은 것끼리 뭉쳐 있다).
            따라서 접두사 관계가 존재하면 반드시 '인접한 쌍'으로 나타난다.
    """
    arr = sorted(phone_book)
    for a, b in zip(arr, arr[1:]):
        if b.startswith(a):
            return False
    return True


def solution_42577_trie(phone_book):
    """접근 3: 트라이 - 삽입 중 두 방향으로 접두사 관계를 감지

    시간 O(sum(L))   <- 이론상 최선
    공간 O(sum(L))

    감지 조건 두 가지 (한쪽만 보면 절반을 놓친다):
      (1) 내려가는 도중 이미 END 인 노드를 만났다 -> 기존 단어가 내 접두사
      (2) 삽입을 마친 노드에 자식이 이미 있다     -> 내가 기존 단어의 접두사
    """
    END = None
    root = {}
    for number in phone_book:
        node = root
        for ch in number:
            if END in node:          # (1)
                return False
            node = node.setdefault(ch, {})
        if node:                     # (2) 단어 끝인데 자식이 있다
            return False
        node[END] = True
    return True


# 프로그래머스 제출용 시그니처
def solution(phone_book):
    return solution_42577_sort(phone_book)


def test_p2():
    title("2. 프로그래머스 #42577 - 전화번호 목록")

    cases = [
        (["119", "97674223", "1195524421"], False, "119 가 1195524421 의 접두어"),
        (["123", "456", "789"], True, "접두사 관계 없음"),
        (["12", "123", "1235", "567", "88"], False, "12 -> 123 -> 1235"),
        (["1"], True, "번호 1개"),
        (["12", "21"], True, "서로 접두사 아님"),
        (["7", "77"], False, "짧은 것이 먼저 와도 감지해야 한다"),
        (["77", "7"], False, "긴 것이 먼저 와도 감지 (조건 (1)/(2) 둘 다 필요)"),
    ]

    impls = [
        ("해시", solution_42577_hash),
        ("정렬", solution_42577_sort),
        ("트라이", solution_42577_trie),
    ]

    print("{:<34} {:<7} {:<7} {:<8} 기대".format("입력", "해시", "정렬", "트라이"))
    print("-" * 72)
    for book, expected, _note in cases:
        results = []
        for label, fn in impls:
            got = fn(book)
            assert got == expected, (book, label, got, expected)
            results.append(got)
        assert solution(book) == expected
        shown = str(book)
        if len(shown) > 32:
            shown = shown[:31] + "]"
        print("{:<34} {:<7} {:<7} {:<8} {}".format(
            shown, yn(results[0]), yn(results[1]), yn(results[2]), yn(expected)))

    print()
    print("주의: ['77','7'] 케이스가 조건 (2)의 존재 이유다.")
    print("      긴 번호가 먼저 삽입되면 '도중에 END 만남'으로는 잡히지 않는다.")
    print()

    # 성능 비교 (N = 20만, 길이 고정 8, 서로 다른 번호)
    #
    # 주의: 문제가 "같은 전화번호가 중복해서 들어 있지 않다"를 보장하므로
    #       벤치마크 입력도 반드시 중복을 제거해야 한다. 중복이 섞이면
    #       정렬 풀이는 b.startswith(a) 에서 a == b 를 접두사로 보아 False,
    #       해시 풀이는 '진짜 접두사'(i < len)만 보므로 True 를 내어 서로 어긋난다.
    #       알고리즘 버그가 아니라 문제 전제를 어긴 입력의 문제다.
    random.seed(39)
    n = 200000
    pool = set()
    while len(pool) < n:
        pool.add(str(random.randrange(10 ** 7, 10 ** 8)))
    big = list(pool)
    assert len(big) == len(set(big)) == n, "중복 없는 입력이어야 한다"

    # 길이가 모두 8로 같고 서로 다르므로 접두사 관계가 존재할 수 없다
    # -> 세 방식 모두 '끝까지 훑는' 최악 경로를 타는 공정한 비교가 된다
    print("N={} (8자리 고정, 중복 없음) 성능:".format(n))
    base = None
    for label, fn in impls:
        t0 = time.perf_counter()
        r = fn(big)
        dt = time.perf_counter() - t0
        if base is None:
            base = r
        assert r == base, (label, r, base)
        print("  {:<8}: {:.4f}s   결과 {}".format(label, dt, yn(r)))
    print("  세 방식 결과 일치:", yn(True))
    print()
    print("길이가 고정 8이라 정렬의 'x L' 이 작다 -> 정렬이 유리한 조건이다.")
    print("교훈: 트라이가 항상 최적은 아니다. 한 번만 판정하면 정렬이 낫다.")
    print("      트라이는 같은 사전에 접두사 질의를 여러 번 던질 때 값어치가 있다.")


# ===========================================================================
# 3. LeetCode #211 - Design Add and Search Words Data Structure
#    https://leetcode.com/problems/design-add-and-search-words-data-structure/
#
#    '.' 은 아무 글자 하나. 트라이 위 백트래킹이다.
# ===========================================================================

class WordDictionary:
    """접근 1: 트라이 + '.' 에서 모든 자식 분기 (표준 풀이)

    addWord : O(L)
    search  : 평균 O(L), '.' 이 k개면 최악 O(26^k x L)
    공간    : O(총 글자 수)

    제약이 '.' 을 최대 2개로 묶어준 덕에 26^2 = 676 배까지만 벌어진다.
    """

    def __init__(self):
        self.root = {}
        self.END = None
        self.by_len = defaultdict(int)  # 길이별 단어 수 (전부 '.' 인 질의 O(1) 처리)

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node[self.END] = True
        self.by_len[len(word)] += 1

    def search(self, word: str) -> bool:
        # 최적화: 전부 '.' 이면 "그 길이의 단어가 있는가" -> O(1)
        if word and all(c == "." for c in word):
            return self.by_len[len(word)] > 0

        END = self.END

        def dfs(node, i):
            if i == len(word):
                return END in node
            ch = word[i]
            if ch == ".":
                for key, child in node.items():
                    if key is END:      # 끝 표시 키는 자식이 아니다
                        continue
                    if dfs(child, i + 1):
                        return True
                return False
            nxt = node.get(ch)
            return nxt is not None and dfs(nxt, i + 1)

        return dfs(self.root, 0)


class WordDictionaryByLen:
    """접근 2: 길이별 버킷 + 문자 단위 비교 (트라이 없이)

    addWord : O(1)
    search  : O(그 길이의 단어 수 x L)
    공간    : O(총 글자 수)

    호출이 10^4 회뿐이라 이 단순 풀이도 통과한다.
    '트라이가 항상 필요한 것은 아니다'를 보여주는 대조군.
    """

    def __init__(self):
        self.buckets = defaultdict(list)

    def addWord(self, word: str) -> None:
        self.buckets[len(word)].append(word)

    def search(self, word: str) -> bool:
        for cand in self.buckets[len(word)]:
            if all(a == "." or a == b for a, b in zip(word, cand)):
                return True
        return False


def test_p3():
    title("3. LeetCode #211 - Design Add and Search Words Data Structure")

    for label, cls in (("트라이", WordDictionary), ("길이별 버킷", WordDictionaryByLen)):
        wd = cls()
        for w in ["bad", "dad", "mad"]:
            wd.addWord(w)
        assert wd.search("pad") is False
        assert wd.search("bad") is True
        assert wd.search(".ad") is True
        assert wd.search("b..") is True
        # 경계
        assert wd.search("...") is True, "길이 3 단어가 있다"
        assert wd.search("....") is False, "길이 4 단어는 없다"
        assert wd.search("ba") is False, "길이가 다르면 매칭 안 됨"
        assert wd.search("b.") is False
        assert wd.search("m.d") is True
        assert wd.search(".a.") is True
        wd.addWord("a")
        assert wd.search("a") is True
        assert wd.search(".") is True
        print("  {:<14} 통과".format(label))

    print()
    print("문제 예시 재현:")
    wd = WordDictionary()
    for w in ["bad", "dad", "mad"]:
        wd.addWord(w)
    for q, exp in [("pad", False), ("bad", True), (".ad", True), ("b..", True)]:
        got = wd.search(q)
        assert got == exp
        print("  search({!r:<6}) -> {}".format(q, got))

    print()
    print("'.' 이 k개면 최악 26^k 분기. 제약('.' 최대 2개)이 폭발을 막는다.")
    print("전부 '.' 인 질의는 길이별 카운트로 O(1) 처리했다 (위 by_len).")


# ===========================================================================
# 4. LeetCode #1268 - Search Suggestions System
#    https://leetcode.com/problems/search-suggestions-system/
#
#    각 접두사마다 사전 순 최소 3개. 파이썬 dict 는 사전 순이 아니다!
# ===========================================================================

class Solution1268:
    def suggestedProducts_trie(self, products: List[str],
                               searchWord: str) -> List[List[str]]:
        """접근 1: 트라이 + 노드에 답을 미리 캐싱

        구축 O(N log N + sum(L))   (정렬 + 삽입)
        질의 O(len(searchWord))    <- 노드의 리스트를 읽기만 한다
        공간 O(sum(L))

        핵심: products 를 '먼저 정렬'해 삽입하면, 지나가는 노드에
              앞선 3개가 자동으로 사전 순으로 쌓인다.
        """
        SUG = "#"  # 추천 리스트 키 (소문자 알파벳과 겹치지 않는다)
        root = {SUG: []}

        for word in sorted(products):          # 정렬이 사전 순을 보장한다
            node = root
            for ch in word:
                if ch not in node:
                    node[ch] = {SUG: []}
                node = node[ch]
                if len(node[SUG]) < 3:         # 앞선 3개만 담는다
                    node[SUG].append(word)

        out, node = [], root
        for ch in searchWord:
            node = node.get(ch) if node else None
            out.append(node[SUG] if node else [])   # 끊기면 이후 전부 빈 리스트
        return out

    def suggestedProducts_bisect(self, products: List[str],
                                 searchWord: str) -> List[List[str]]:
        """접근 2: 정렬 + 이분 탐색 (트라이 없이. 메모리가 훨씬 적다)

        구축 O(N log N x L)
        질의 O(len(searchWord) x log N)
        공간 O(N)

        접두사 p 로 시작하는 구간은 정렬 배열에서 연속이다.
        시작 = bisect_left(arr, p), 끝 = bisect_right(arr, p + '{')
        ('{' 은 'z' 다음 ASCII 문자라 모든 소문자 뒤에 온다)
        """
        arr = sorted(products)
        out = []
        prefix = ""
        for ch in searchWord:
            prefix += ch
            lo = bisect_left(arr, prefix)
            hi = bisect_right(arr, prefix + "{")
            out.append(arr[lo:min(lo + 3, hi)])
        return out


# LeetCode 제출용 시그니처
class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        return Solution1268().suggestedProducts_trie(products, searchWord)


def test_p4():
    title("4. LeetCode #1268 - Search Suggestions System")

    s = Solution1268()
    cases = [
        (["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse",
         [["mobile", "moneypot", "monitor"],
          ["mobile", "moneypot", "monitor"],
          ["mouse", "mousepad"],
          ["mouse", "mousepad"],
          ["mouse", "mousepad"]]),
        (["havana"], "havana", [["havana"]] * 6),
        (["bags", "baggage", "banner", "box", "cloths"], "bags",
         [["baggage", "bags", "banner"],
          ["baggage", "bags", "banner"],
          ["baggage", "bags"],
          ["bags"]]),
        (["havana"], "tatiana", [[], [], [], [], [], [], []]),
    ]

    for products, word, expected in cases:
        r_trie = s.suggestedProducts_trie(products, word)
        r_bis = s.suggestedProducts_bisect(products, word)
        assert r_trie == expected, ("trie", products, word, r_trie, expected)
        assert r_bis == expected, ("bisect", products, word, r_bis, expected)
        assert Solution().suggestedProducts(products, word) == expected

    print("두 접근 모두 {}개 케이스 통과 (트라이 / 정렬+이분탐색)".format(len(cases)))
    print()

    products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    print("products =", products)
    print("searchWord = 'mouse' 를 한 글자씩 입력:")
    for i, sug in enumerate(s.suggestedProducts_trie(products, "mouse"), 1):
        print("  {:<7} -> {}".format("mouse"[:i], sug))
    print()
    print("경로가 끊긴 뒤(예: 'tatiana')는 이후 전부 빈 리스트. 재탐색 불필요.")
    print()
    print("함정: 파이썬 dict 는 '삽입 순서'를 보존한다 (사전 순이 아니다).")
    print("      -> products 를 미리 정렬하거나 sorted(children) 로 순회해야 한다.")


# ===========================================================================
# 5. 프로그래머스 #60060 - 가사 검색 (2020 KAKAO BLIND RECRUITMENT)
#    https://school.programmers.co.kr/learn/courses/30/lessons/60060
#
#    '?' 는 접두사 또는 접미사에만 몰려 나온다.
#    핵심 관찰: "fro??" = "길이 5 이고 fro 로 시작" -> '?' 를 처리할 필요가 없다!
# ===========================================================================

class _CountTrie:
    """노드마다 cnt 만 두는 초경량 트라이. 루트 cnt = 전체 단어 수."""

    CNT = 0  # 문자와 겹치지 않는 정수 키

    __slots__ = ("root",)

    def __init__(self):
        self.root = {self.CNT: 0}

    def insert(self, word):
        node = self.root
        node[self.CNT] += 1              # 루트에는 전체 개수
        for ch in word:
            if ch not in node:
                node[ch] = {self.CNT: 0}
            node = node[ch]
            node[self.CNT] += 1          # 삽입 때 미리 센다 (질의는 읽기만)

    def count(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return 0
            node = node[ch]
        return node[self.CNT]

    def total(self):
        return self.root[self.CNT]


def solution_60060_trie(words, queries):
    """접근 1: 길이별 정방향/역방향 트라이 + 접두사 카운터 (정석)

    구축 O(sum(len(words)))
    질의 O(len(query)) 각각
    전체 O(sum|words| + sum|queries|)

    설계:
      fwd[n] = 길이 n 인 단어들의 정방향 트라이
      bwd[n] = 길이 n 인 단어들을 뒤집어 넣은 트라이
      "fro??" -> fwd[5].count("fro")
      "??ro"  -> bwd[4].count("or")     ('ro' 를 뒤집어 'or')
      "?????" -> fwd[5].total()
    """
    fwd = defaultdict(_CountTrie)
    bwd = defaultdict(_CountTrie)
    for w in words:
        n = len(w)
        fwd[n].insert(w)
        bwd[n].insert(w[::-1])

    answer = []
    for q in queries:
        n = len(q)
        if q[0] != "?":                        # '?' 가 뒤쪽
            prefix = q.rstrip("?")
            answer.append(fwd[n].count(prefix) if n in fwd else 0)
        elif q[-1] != "?":                     # '?' 가 앞쪽 -> 뒤집는다
            suffix = q.lstrip("?")
            answer.append(bwd[n].count(suffix[::-1]) if n in bwd else 0)
        else:                                  # 전부 '?'
            answer.append(fwd[n].total() if n in fwd else 0)
    return answer


def solution_60060_bisect(words, queries):
    """접근 2: 길이별 정렬 + 이분 탐색 (메모리가 훨씬 적다)

    구축 O(sum|words| x log)
    질의 O(len(query) + log N)
    공간 O(N)   <- 트라이의 O(총 글자 수) 보다 훨씬 작다

    단어 길이 합이 200만이라 트라이 메모리가 실제로 부담된다.
    이 풀이가 실전에서 더 안전할 수 있다.
    """
    by_len = defaultdict(list)
    by_len_rev = defaultdict(list)
    for w in words:
        by_len[len(w)].append(w)
        by_len_rev[len(w)].append(w[::-1])
    for n in by_len:
        by_len[n].sort()
        by_len_rev[n].sort()

    def count_prefix(arr, prefix):
        if not prefix:
            return len(arr)
        lo = bisect_left(arr, prefix)
        hi = bisect_right(arr, prefix + "{")   # 'z' 다음 ASCII
        return hi - lo

    answer = []
    for q in queries:
        n = len(q)
        if q[0] != "?":
            answer.append(count_prefix(by_len.get(n, []), q.rstrip("?")))
        elif q[-1] != "?":
            answer.append(count_prefix(by_len_rev.get(n, []), q.lstrip("?")[::-1]))
        else:
            answer.append(len(by_len.get(n, [])))
    return answer


def solution_60060_brute(words, queries):
    """접근 3: 브루트포스 (정답 검증용. 제출하면 시간 초과)

    O(len(queries) x len(words) x L)
    10만 x 10만 = 100억 -> 절대 불가. 그래도 정답 기준으로는 유용하다.
    """
    def match(word, q):
        if len(word) != len(q):
            return False
        return all(c == "?" or c == w for w, c in zip(word, q))

    return [sum(1 for w in words if match(w, q)) for q in queries]


# 프로그래머스 제출용 (파일 안에 solution 이 둘일 수 없어 이름을 분리해 둔다)
def solution_60060(words, queries):
    return solution_60060_trie(words, queries)


def test_p5():
    title("5. 프로그래머스 #60060 - 가사 검색 (2020 카카오 블라인드)")

    words = ["frodo", "front", "frost", "frozen", "frame", "kakao"]
    queries = ["fro??", "????o", "fr???", "fro???", "pro?"]
    expected = [3, 2, 4, 1, 0]

    r_trie = solution_60060_trie(words, queries)
    r_bis = solution_60060_bisect(words, queries)
    r_brute = solution_60060_brute(words, queries)
    assert r_trie == expected, ("trie", r_trie, expected)
    assert r_bis == expected, ("bisect", r_bis, expected)
    assert r_brute == expected, ("brute", r_brute, expected)
    assert solution_60060(words, queries) == expected

    print("문제 공식 예제:")
    print("  words   =", words)
    print("  queries =", queries)
    print("  기대     =", expected)
    print()
    print("{:<10} {:<8} {:<8} {:<10} 해석".format("질의", "트라이", "이분", "브루트"))
    print("-" * 68)
    notes = {
        "fro??": "길이 5 & 'fro' 로 시작 -> frodo, front, frost",
        "????o": "길이 5 & 'o' 로 끝남 -> frodo, kakao (역방향 트라이)",
        "fr???": "길이 5 & 'fr' 로 시작 -> +frame",
        "fro???": "길이 6 & 'fro' 로 시작 -> frozen",
        "pro?": "길이 4 & 'pro' 로 시작 -> 없음",
    }
    for i, q in enumerate(queries):
        print("{:<10} {:<8} {:<8} {:<10} {}".format(
            q, r_trie[i], r_bis[i], r_brute[i], notes[q]))
    print()

    # 추가 경계 케이스 - 브루트포스를 정답 기준으로 교차 검증
    extra_cases = [
        (["a", "ab", "abc"], ["?", "??", "???", "a?", "?c", "a??", "??c", "????"]),
        (["aaa", "aab", "abb", "bbb"], ["a??", "??b", "?????", "aab", "???", "?aa"]),
        (["zzzz"], ["????", "z???", "???z", "y???", "??z?"]),
    ]
    total_extra = 0
    for ws, qs in extra_cases:
        exp = solution_60060_brute(ws, qs)
        got_t = solution_60060_trie(ws, qs)
        got_b = solution_60060_bisect(ws, qs)
        assert got_t == exp, ("trie", ws, qs, got_t, exp)
        assert got_b == exp, ("bisect", ws, qs, got_b, exp)
        total_extra += len(qs)
    print("추가 경계 케이스 {}건 교차 검증 통과 (트라이 == 이분 == 브루트포스)".format(total_extra))
    print()

    # 성능: 브루트포스가 왜 불가능한지 체감
    random.seed(39)
    alpha = "abcdefg"
    nw, nq = 1500, 1500
    big_words = ["".join(random.choice(alpha) for _ in range(8)) for _ in range(nw)]
    big_queries = []
    for _ in range(nq):
        k = random.randrange(1, 8)
        core = "".join(random.choice(alpha) for _ in range(k))
        if random.random() < 0.5:
            big_queries.append(core + "?" * (8 - k))
        else:
            big_queries.append("?" * (8 - k) + core)

    t0 = time.perf_counter()
    a1 = solution_60060_trie(big_words, big_queries)
    t1 = time.perf_counter()
    a2 = solution_60060_bisect(big_words, big_queries)
    t2 = time.perf_counter()
    a3 = solution_60060_brute(big_words, big_queries)
    t3 = time.perf_counter()
    assert a1 == a2 == a3

    print("단어 {}개 x 질의 {}개 성능:".format(nw, nq))
    print("  트라이      : {:.4f}s".format(t1 - t0))
    print("  정렬+이분   : {:.4f}s".format(t2 - t1))
    print("  브루트포스  : {:.4f}s".format(t3 - t2))
    print("  실제 제약은 10만 x 10만 -> 위 브루트포스의 약 4400배 규모다.")
    print("  세 결과 일치:", yn(a1 == a2 == a3))
    print()
    print("핵심 정리:")
    print("  1) '?' 를 처리하지 않는다. '길이 + 접두사' 로 분해하면 사라진다.")
    print("  2) 접미사 조건은 문자열을 뒤집어 접두사 조건으로 바꾼다.")
    print("  3) 개수는 삽입 시점에 cnt 로 누적한다 (질의는 O(L) 읽기).")
    print("  4) 전부 '?' 인 질의는 그 길이의 전체 개수 -> 빼먹으면 부분 점수.")


# ===========================================================================
# 6. LeetCode #212 - Word Search II
#    https://leetcode.com/problems/word-search-ii/
#
#    트라이는 저장소가 아니라 '가망 없는 분기를 즉시 끊는 필터'다.
# ===========================================================================

class Solution212:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """접근 1: 트라이 + 격자 백트래킹 + pruning (표준 풀이)

        시간 O(m x n x 4 x 3^(L-1)) 최악. 트라이 가지치기로 실전은 훨씬 빠르다
        공간 O(sum(len(words)))

        최적화 3종:
          (1) 트라이 노드를 함께 내려가며 없는 문자에서 즉시 중단
          (2) 찾은 단어는 노드에서 pop -> 중복 자동 방지
          (3) 자식이 소진된 노드는 부모에서 제거 -> 탐색 공간이 계속 줄어든다
        """
        WORD = "$"
        root = {}
        for w in words:
            node = root
            for ch in w:
                node = node.setdefault(ch, {})
            node[WORD] = w

        rows, cols = len(board), len(board[0])
        found = []

        def backtrack(r, c, parent):
            ch = board[r][c]
            node = parent.get(ch)
            if node is None:          # (1) 이 방향으로는 어떤 단어도 못 만든다
                return

            word = node.pop(WORD, None)   # (2) 찾으면 꺼낸다
            if word is not None:
                found.append(word)

            board[r][c] = "#"             # 방문 표시 (한 단어 안에서 재사용 금지)
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                    backtrack(nr, nc, node)
            board[r][c] = ch              # 복원 (빼먹으면 격자가 오염된다)

            if not node:                  # (3) 다 쓴 가지는 잘라낸다
                parent.pop(ch, None)

        for r in range(rows):
            for c in range(cols):
                backtrack(r, c, root)
        return found

    def findWords_naive(self, board: List[List[str]], words: List[str]) -> List[str]:
        """접근 2: 단어별 개별 DFS (트라이 없이. 검증용 대조군)

        시간 O(W x m x n x 4^L)  <- W=3만이면 시간 초과
        공간 O(L)

        트라이가 줄여주는 비용을 눈으로 확인하기 위한 비교 대상.
        'abc','abd','abe' 를 각각 처음부터 세 번 훑는다는 점이 핵심 낭비다.
        """
        rows, cols = len(board), len(board[0])

        def exists(word):
            def dfs(r, c, i):
                if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
                    return False
                if i == len(word) - 1:
                    return True
                saved = board[r][c]
                board[r][c] = "#"
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    if dfs(r + dr, c + dc, i + 1):
                        board[r][c] = saved
                        return True
                board[r][c] = saved
                return False

            for r in range(rows):
                for c in range(cols):
                    if dfs(r, c, 0):
                        return True
            return False

        return [w for w in words if exists(w)]


def test_p6():
    title("6. LeetCode #212 - Word Search II")

    s = Solution212()
    cases = [
        # 공식 예제
        ([["o", "a", "a", "n"],
          ["e", "t", "a", "e"],
          ["i", "h", "k", "r"],
          ["i", "f", "l", "v"]],
         ["oath", "pea", "eat", "rain"],
         ["eat", "oath"]),
        # 같은 칸을 재사용할 수 없다
        ([["a", "b"], ["c", "d"]], ["abcb"], []),
        # 1x1
        ([["a"]], ["a"], ["a"]),
        # 2x2 전수: 격자는 a-b-d-c-a 4-사이클. 대각선 이동은 불가
        ([["a", "b"], ["c", "d"]],
         ["ab", "cb", "ad", "bd", "ac", "ca", "da", "bc", "db", "adcb", "dabc", "abb", "acb"],
         ["ab", "bd", "ac", "ca", "db"]),
    ]

    for board, words, expected in cases:
        got = s.findWords([row[:] for row in board], words)
        got_naive = s.findWords_naive([row[:] for row in board], words)
        assert sorted(got) == sorted(expected), (words, sorted(got), sorted(expected))
        assert sorted(got_naive) == sorted(expected), (
            "naive", words, sorted(got_naive), sorted(expected))

    print("두 접근 모두 {}개 케이스 통과 (트라이 백트래킹 / 단어별 DFS)".format(len(cases)))
    print()
    print("2x2 격자 [[a,b],[c,d]] 는 a-b-d-c-a 4-사이클이다 (대각선 이동 없음).")
    print("  'ad','da','bc','cb' 는 대각선이라 불가. 'abb' 는 같은 칸 재사용이라 불가.")
    print()

    board = [["o", "a", "a", "n"],
             ["e", "t", "a", "e"],
             ["i", "h", "k", "r"],
             ["i", "f", "l", "v"]]
    print("격자:")
    for row in board:
        print("   ", " ".join(row))
    words = ["oath", "pea", "eat", "rain", "hklf", "hf"]
    print("단어:", words)
    print("결과:", sorted(s.findWords([r[:] for r in board], words)))
    print()

    # 성능: 단어가 많아질 때 트라이의 효과
    random.seed(39)
    alpha = "abcd"
    big_board = [[random.choice(alpha) for _ in range(6)] for _ in range(6)]
    big_words = sorted({"".join(random.choice(alpha)
                                for _ in range(random.randrange(3, 6)))
                        for _ in range(250)})

    t0 = time.perf_counter()
    r_trie = s.findWords([row[:] for row in big_board], big_words)
    t1 = time.perf_counter()
    r_naive = s.findWords_naive([row[:] for row in big_board], big_words)
    t2 = time.perf_counter()
    assert sorted(r_trie) == sorted(r_naive), (sorted(r_trie), sorted(r_naive))

    print("6x6 격자 x 단어 {}개 성능:".format(len(big_words)))
    print("  트라이 백트래킹 : {:.4f}s  (찾은 단어 {}개)".format(t1 - t0, len(r_trie)))
    print("  단어별 개별 DFS : {:.4f}s  (찾은 단어 {}개)".format(t2 - t1, len(r_naive)))
    print("  결과 일치:", yn(sorted(r_trie) == sorted(r_naive)))
    print()
    print("트라이가 줄여주는 것: 공통 접두사를 가진 단어들이 탐색을 '공유'한다.")
    print("  단어별 DFS 는 'abc','abd','abe' 를 각각 처음부터 세 번 훑는다.")
    print("  트라이는 'ab' 까지 한 번만 내려간 뒤 갈라진다.")


# ===========================================================================
# main
# ===========================================================================

def main():
    print("Day 39 - 트라이 (Trie / Prefix Tree) 연습문제 해설")
    print("출처: 프로그래머스 / LeetCode. 표준 라이브러리만 사용.")

    test_p1()
    test_p2()
    test_p3()
    test_p4()
    test_p5()
    test_p6()

    title("전체 정리")
    print("[문제별 핵심]")
    print("  #208   search 와 startsWith 는 is_end 를 보느냐 마느냐 한 줄 차이")
    print("  #42577 해시/정렬/트라이 3방식. 한 번만 판정하면 '정렬'이 실전 최적해")
    print("  #211   '.' 은 모든 자식 분기 = 백트래킹. 제약이 지수 폭발을 막아준다")
    print("  #1268  products 를 먼저 정렬해 삽입 -> 노드에 앞선 3개가 자동 캐싱")
    print("  #60060 '길이 + 접두사' 로 분해하면 '?' 가 사라진다. 접미사는 뒤집는다")
    print("  #212   트라이는 저장소가 아니라 '가망 없는 분기를 끊는 필터'다")
    print()
    print("[자료구조 선택 판단]")
    print("  완전 일치만 필요       -> 해시 (더 짧고 더 가볍다)")
    print("  접두사 질의가 한 번    -> 정렬 + 이분 탐색 (메모리 유리)")
    print("  접두사 질의가 반복     -> 트라이 (질의당 O(L) 확정)")
    print("  개수를 물으면          -> 삽입 시점에 cnt 누적")
    print("  접미사 조건            -> 문자열 뒤집기")
    print("  길이가 조건에 섞이면   -> 길이별로 트라이/배열 분리")
    print()
    print("모든 assert 통과.")


if __name__ == "__main__":
    main()
