"""Day 39 - 트라이 (Trie / Prefix Tree) 예제 모음

표준 라이브러리만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py

핵심 한 줄:
    "접두사를 공유하면 경로를 공유한다 -> 접두사 질의는 내려가기만 하면 끝."
"""

import random
import sys
import time
from collections import defaultdict


def title(text):
    """섹션 제목 출력 (cp949 안전: ASCII 기호만)."""
    print()
    print("=" * 68)
    print(text)
    print("=" * 68)


def yn(flag):
    """불리언을 O / X 로 (cp949 안전)."""
    return "O" if flag else "X"


# ===========================================================================
# 1. 최소 트라이: 중첩 dict + setdefault (코테에서 가장 빠르게 쓰는 형태)
# ===========================================================================

END = None  # 실제 문자와 절대 겹치지 않는 끝 표시 키


def build_trie(words):
    """단어 목록으로 중첩 dict 트라이를 만든다. O(총 글자 수)."""
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})  # 없으면 만들고, 있으면 재사용
        node[END] = True  # 단어 끝 도장
    return root


def walk(root, s):
    """s 경로를 따라 내려가 도착 노드를 반환. 경로가 끊기면 None. O(len(s))."""
    node = root
    for ch in s:
        if ch not in node:
            return None
        node = node[ch]
    return node


def has_word(root, w):
    """w 가 단어로 등록되어 있는가 (END 를 본다)."""
    node = walk(root, w)
    return node is not None and END in node


def has_prefix(root, p):
    """p 로 시작하는 단어가 있는가 (END 를 안 본다)."""
    return walk(root, p) is not None


def count_nodes(node):
    """트라이의 노드 수를 센다 (END 키는 제외)."""
    total = 1
    for k, child in node.items():
        if k is not END:
            total += count_nodes(child)
    return total


def demo_min_trie():
    title("1. 최소 트라이 (중첩 dict + setdefault)")

    words = ["cat", "car", "card", "dog"]
    root = build_trie(words)
    print("삽입한 단어:", words)
    print()
    print("트라이 구조 (dict 중첩, END=None 은 단어 끝):")
    print("  ", root)
    print()

    print("총 글자 수:", sum(len(w) for w in words), "/ 실제 노드 수:", count_nodes(root))
    print("  -> 공통 접두사 'ca', 'car' 를 공유해 노드를 절약했다")
    print()

    print("has_word  vs  has_prefix  (딱 END 를 보느냐 마느냐 차이)")
    print("  {:<8} {:<12} {:<12}".format("질의", "has_word", "has_prefix"))
    print("  " + "-" * 34)
    for q in ["car", "ca", "card", "cards", "dog", "do"]:
        print("  {:<8} {:<12} {:<12}".format(
            q, yn(has_word(root, q)), yn(has_prefix(root, q))))
    print()
    print("핵심: 'ca' 는 경로는 있지만 단어가 아니다 -> has_word X, has_prefix O")
    print("      이 구분을 놓치는 것이 트라이 유형 최다 버그다.")


# ===========================================================================
# 2. 클래스 트라이 (LeetCode #208 시그니처 + 접두사 카운터)
# ===========================================================================

class TrieNode:
    __slots__ = ("children", "is_end", "cnt")  # 메모리 절약

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.cnt = 0  # 이 노드를 지나는 단어 수 = 이 접두사로 시작하는 단어 수


class Trie:
    """트라이 기본 3연산 + 접두사 개수 + 삭제."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """O(L). L = len(word). 저장된 단어 수 N 과 무관하다."""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.cnt += 1  # 지나가며 카운터 누적 (질의 때 세지 않기 위해)
        node.is_end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        """단어로 등록되었는가. O(L)."""
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        """이 접두사로 시작하는 단어가 있는가. O(L)."""
        return self._walk(prefix) is not None

    def count_prefix(self, prefix):
        """이 접두사로 시작하는 단어 수. O(L) -- 세지 않는다!"""
        node = self._walk(prefix)
        return node.cnt if node else 0

    def delete(self, word):
        """단어 삭제. is_end 를 끄고, 빈 노드를 되짚어 올라가며 제거한다."""
        if not self.search(word):
            return False  # 없던 단어면 아무것도 건드리지 않는다 (cnt 보호)

        def rec(node, i):
            """반환값: 이 노드를 부모에서 지워도 되는가"""
            if i == len(word):
                node.is_end = False
                return len(node.children) == 0  # 자식 있으면 남겨둔다
            ch = word[i]
            child = node.children[ch]
            child.cnt -= 1  # 삽입에서 +1 한 만큼 -1 (한쪽만 하면 조용한 버그)
            if rec(child, i + 1):
                del node.children[ch]
            return not node.children and not node.is_end

        rec(self.root, 0)
        return True

    def words_sorted(self):
        """사전 순 전체 순회. 자식을 '문자 순으로' 방문해야 사전 순이 된다."""
        out = []

        def dfs(node, path):
            if node.is_end:
                out.append(path)
            for ch in sorted(node.children):  # dict 는 삽입 순서 -> 명시적 정렬 필수
                dfs(node.children[ch], path + ch)

        dfs(self.root, "")
        return out


def demo_class_trie():
    title("2. 클래스 트라이: 기본 3연산 + 접두사 카운터 + 삭제")

    t = Trie()
    words = ["cat", "car", "card", "care", "dog"]
    for w in words:
        t.insert(w)
    print("삽입:", words)
    print()

    print("{:<8} {:<10} {:<12} {:<14}".format("질의", "search", "startsWith", "count_prefix"))
    print("-" * 46)
    for q in ["car", "ca", "care", "cart", "dog", "d"]:
        print("{:<8} {:<10} {:<12} {:<14}".format(
            q, yn(t.search(q)), yn(t.startsWith(q)), t.count_prefix(q)))
    print()
    print("count_prefix 는 서브트리를 세지 않는다. 삽입 때 미리 누적해둔 값을")
    print("O(L) 에 읽기만 한다 -> 질의 10만 건에도 안전 (가사 검색의 핵심).")
    print()

    print("사전 순 전체 순회 (비교 정렬 없이 정렬된다):")
    print("  ", t.words_sorted())
    print()

    print("삭제 검증:")
    print("  삭제 전  search('car') =", yn(t.search("car")),
          " count_prefix('car') =", t.count_prefix("car"))
    t.delete("car")
    print("  'car' 삭제 후")
    print("    search('car')       =", yn(t.search("car")), "  <- 단어 등록 해제")
    print("    search('card')      =", yn(t.search("card")), "  <- 'card' 는 살아있어야 한다!")
    print("    search('care')      =", yn(t.search("care")), "  <- 'care' 도 살아있어야 한다")
    print("    count_prefix('car') =", t.count_prefix("car"), "  <- 3 에서 2 로 감소")
    print("  핵심: 자식이 있는 노드는 절대 지우면 안 된다.")


# ===========================================================================
# 3. 자동완성: 접두사 아래 단어를 사전 순으로 k개
# ===========================================================================

def autocomplete(trie, prefix, limit=3):
    """접두사로 시작하는 단어를 사전 순 최대 limit 개. O(L + 출력량)."""
    node = trie._walk(prefix)
    if node is None:
        return []
    out = []

    def dfs(nd, path):
        if len(out) == limit:
            return
        if nd.is_end:
            out.append(prefix + path)
        for ch in sorted(nd.children):  # 사전 순 보장은 명시적 정렬로
            if len(out) == limit:
                return
            dfs(nd.children[ch], path + ch)

    dfs(node, "")
    return out


def demo_autocomplete():
    title("3. 자동완성 (LeetCode #1268 패턴)")

    products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
    t = Trie()
    for p in products:
        t.insert(p)
    print("상품 목록:", products)
    print()

    search_word = "mouse"
    print("'{}' 를 한 글자씩 입력할 때마다 추천 3개:".format(search_word))
    for i in range(1, len(search_word) + 1):
        pref = search_word[:i]
        print("  {:<8} -> {}".format(pref, autocomplete(t, pref, 3)))
    print()
    print("주의: 파이썬 dict 는 '삽입 순서'를 보존한다 (사전 순이 아니다).")
    print("      sorted(node.children) 를 빼먹으면 순서가 틀려 오답이 된다.")


# ===========================================================================
# 4. 와일드카드 '.' 검색 (LeetCode #211) = 트라이 위 백트래킹
# ===========================================================================

def search_wildcard(trie, word):
    """'.' 은 아무 글자 하나. '.' 을 만나면 모든 자식으로 분기해 시도한다."""
    def dfs(node, i):
        if i == len(word):
            return node.is_end
        ch = word[i]
        if ch == ".":
            for child in node.children.values():  # 모든 분기 시도
                if dfs(child, i + 1):
                    return True
            return False
        nxt = node.children.get(ch)
        return nxt is not None and dfs(nxt, i + 1)

    return dfs(trie.root, 0)


def demo_wildcard():
    title("4. 와일드카드 '.' 검색 (LeetCode #211)")

    t = Trie()
    words = ["bad", "dad", "mad", "bed"]
    for w in words:
        t.insert(w)
    print("저장:", words)
    print()

    print("{:<8} {:<8} 설명".format("질의", "결과"))
    print("-" * 50)
    cases = [
        ("pad", "저장 안 된 단어"),
        ("bad", "완전 일치"),
        (".ad", "첫 글자 아무거나 -> bad/dad/mad"),
        ("b..", "bad, bed 둘 다 후보"),
        ("b.d", "a 또는 e 분기에서 성공"),
        ("...", "길이 3 인 단어가 있으면 True"),
        ("....", "길이 4 인 단어는 없다"),
    ]
    for q, note in cases:
        print("{:<8} {:<8} {}".format(q, yn(search_wildcard(t, q)), note))
    print()
    print("복잡도: '.' 이 k개면 최악 O(26^k) 분기.")
    print("        #211 의 제약('.' 최대 2개, 길이 25 이하)이 폭발을 막는다.")


# ===========================================================================
# 5. 길이별 정/역방향 트라이 - 와일드카드 카운트 (가사 검색 패턴)
# ===========================================================================

class CountTrie:
    """노드마다 cnt 만 들고 있는 초경량 트라이 (중첩 dict + 카운터)."""

    CNT = 0  # 문자와 겹치지 않는 카운터 키 (정수 0)

    def __init__(self):
        self.root = {self.CNT: 0}

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                node[ch] = {self.CNT: 0}
            node = node[ch]
            node[self.CNT] += 1
        self.root[self.CNT] += 1  # 루트에는 전체 단어 수

    def count(self, prefix):
        """prefix 로 시작하는 단어 수. O(len(prefix))."""
        node = self.root
        for ch in prefix:
            if ch not in node:
                return 0
            node = node[ch]
        return node[self.CNT]

    def total(self):
        return self.root[self.CNT]


def build_length_tries(words):
    """길이별 정방향/역방향 트라이를 만든다.

    '?' 가 뒤에 붙는 질의("fro??")는 정방향 트라이에서,
    앞에 붙는 질의("??ro")는 뒤집어서 역방향 트라이에서 처리한다.
    """
    fwd = defaultdict(CountTrie)
    bwd = defaultdict(CountTrie)
    for w in words:
        n = len(w)
        fwd[n].insert(w)
        bwd[n].insert(w[::-1])
    return fwd, bwd


def wildcard_count(fwd, bwd, query):
    """'?' 가 앞이나 뒤에 몰려 있는 질의의 매칭 개수. O(len(query))."""
    n = len(query)
    if query[0] != "?":
        # 뒤쪽에 '?' -> 정방향 트라이에서 접두사 카운트
        prefix = query.rstrip("?")
        return fwd[n].count(prefix) if n in fwd else 0
    if query[-1] != "?":
        # 앞쪽에 '?' -> 뒤집어서 역방향 트라이
        suffix = query.lstrip("?")
        return bwd[n].count(suffix[::-1]) if n in bwd else 0
    # 전부 '?' -> 그 길이의 단어 수 전체
    return fwd[n].total() if n in fwd else 0


def demo_length_tries():
    title("5. 길이별 정/역방향 트라이 (프로그래머스 #60060 가사 검색 패턴)")

    words = ["frodo", "front", "frost", "frozen", "frame", "kakao"]
    queries = ["fro??", "????o", "fr???", "fro???", "?????", "??????"]
    print("단어:", words)
    print()

    fwd, bwd = build_length_tries(words)
    print("길이별 트라이 구축: 길이 ->", sorted(fwd.keys()))
    print()

    print("{:<10} {:<7} 해석".format("질의", "개수"))
    print("-" * 58)
    notes = {
        "fro??": "길이 5 이고 'fro' 로 시작 -> frodo, front, frost",
        "????o": "길이 5 이고 'o' 로 끝남 -> 역방향에서 'o' 접두사",
        "fr???": "길이 5 이고 'fr' 로 시작 -> frodo, front, frost, frame",
        "fro???": "길이 6 이고 'fro' 로 시작 -> frozen",
        "?????": "길이 5 인 단어 전부",
        "??????": "길이 6 인 단어 전부 -> frozen",
    }
    for q in queries:
        print("{:<10} {:<7} {}".format(q, wildcard_count(fwd, bwd, q), notes[q]))
    print()
    print("포인트 1: '?' 를 하나도 처리하지 않았다. 길이로 쪼개니 사라졌다.")
    print("포인트 2: 접미사 조건은 문자열을 뒤집으면 접두사 조건이 된다.")
    print("포인트 3: 질의당 O(L). 질의 10만 건 x 길이 10 이면 100만 연산.")


# ===========================================================================
# 6. 비트 트라이: XOR 최댓값 (LeetCode #421)
# ===========================================================================

BITS = 31  # 0 <= nums[i] < 2^31


def max_xor_trie(nums):
    """비트 트라이로 XOR 최댓값. O(32N)."""
    root = {}
    for x in nums:  # 삽입: 상위 비트부터 0/1 간선을 타고 내려간다
        node = root
        for b in range(BITS, -1, -1):
            bit = (x >> b) & 1
            node = node.setdefault(bit, {})

    best = 0
    for x in nums:  # 질의: 각 비트에서 '반대쪽'으로 가려고 시도
        node, cur = root, 0
        for b in range(BITS, -1, -1):
            bit = (x >> b) & 1
            want = 1 - bit  # 반대면 그 비트가 1 -> 이득
            if want in node:
                cur |= 1 << b
                node = node[want]
            else:
                node = node[bit]  # 반대가 없으면 같은 쪽 (그 비트는 0)
        best = max(best, cur)
    return best


def max_xor_brute(nums):
    """브루트포스 O(N^2). 검증용."""
    best = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            best = max(best, nums[i] ^ nums[j])
    return best


def demo_bit_trie():
    title("6. 비트 트라이: XOR 최댓값 (LeetCode #421)")

    print("아이디어: 문자 대신 비트를 내려간다.")
    print("          알파벳 = {0, 1}, 문자열 길이 = 32. 트라이가 맞다.")
    print()

    nums = [3, 10, 5, 25, 2, 8]
    print("입력:", nums)
    print("트라이 O(32N)     =", max_xor_trie(nums))
    print("브루트포스 O(N^2) =", max_xor_brute(nums))
    print("  (25 ^ 5 = 28)")
    print()

    print("왜 상위 비트부터 그리디인가:")
    print("  25  = {:05b}".format(25))
    print("   5  = {:05b}".format(5))
    print("  XOR = {:05b} = 28".format(25 ^ 5))
    print("  상위 비트 1개(16)가 그 아래 전부(8+4+2+1=15)보다 크다.")
    print("  -> 위쪽에서 1을 만들 수 있으면 무조건 그렇게 하는 게 최적이다.")
    print()

    random.seed(39)
    big = [random.randrange(1 << 20) for _ in range(1500)]

    t0 = time.perf_counter()
    r1 = max_xor_trie(big)
    t1 = time.perf_counter()
    r2 = max_xor_brute(big)
    t2 = time.perf_counter()

    print("N=1500 성능 비교:")
    print("  비트 트라이 O(32N) : {:.4f}s  결과 {}".format(t1 - t0, r1))
    print("  브루트포스 O(N^2)  : {:.4f}s  결과 {}".format(t2 - t1, r2))
    print("  결과 일치:", yn(r1 == r2))


# ===========================================================================
# 7. 격자 + 트라이 백트래킹 (LeetCode #212 Word Search II)
# ===========================================================================

WORD_KEY = "$"  # 이 노드에서 끝나는 단어 (실제 문자와 겹치지 않게)


def find_words(board, words):
    """격자에서 words 에 있는 단어를 모두 찾는다. 트라이로 가지치기."""
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node[WORD_KEY] = w

    rows, cols = len(board), len(board[0])
    found = []

    def backtrack(r, c, parent):
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:  # 트라이에 없는 문자 -> 이 방향은 가망 없다 (핵심 가지치기)
            return

        word = node.pop(WORD_KEY, None)  # 찾으면 꺼내서 중복 방지
        if word is not None:
            found.append(word)

        board[r][c] = "#"  # 방문 표시
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                backtrack(nr, nc, node)
        board[r][c] = ch  # 복원

        if not node:  # 자식이 다 소진된 노드는 부모에서 제거 (탐색 공간 축소)
            parent.pop(ch, None)

    for r in range(rows):
        for c in range(cols):
            backtrack(r, c, root)
    return found


def demo_word_search():
    title("7. 격자 + 트라이 백트래킹 (LeetCode #212)")

    board = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
    words = ["oath", "pea", "eat", "rain", "hklf", "hf"]
    print("격자:")
    for row in board:
        print("   ", " ".join(row))
    print("찾을 단어:", words)
    print()

    result = find_words([row[:] for row in board], words)
    print("찾은 단어:", sorted(result))
    print()
    print("트라이가 하는 일: 저장소가 아니라 '가지치기 필터'다.")
    print("  현재 칸의 문자가 트라이 노드의 자식에 없으면 -> 즉시 중단.")
    print("  단어 W개를 각각 DFS하면 O(W x 격자 x 4^L) 이지만,")
    print("  트라이에 다 넣고 격자를 한 번만 훑으면 공통 접두사를 공유한다.")
    print()
    print("추가 최적화: 찾은 단어는 pop 하고, 빈 노드는 부모에서 제거한다.")
    print("             -> 탐색이 진행될수록 트라이가 계속 작아진다.")


# ===========================================================================
# 8. 해시 vs 정렬 vs 트라이 - 접두사 존재 판별 3방식 (#42577 패턴)
# ===========================================================================

def prefix_exists_hash(words):
    """해시: 각 단어의 모든 접두사를 set 에서 조회. O(sum(L^2)) (슬라이싱 포함)."""
    s = set(words)
    for w in words:
        for i in range(1, len(w)):
            if w[:i] in s:
                return True
    return False


def prefix_exists_sort(words):
    """정렬: 사전 순 정렬 후 '인접한 쌍'만 검사. O(N log N x L)."""
    arr = sorted(words)
    for a, b in zip(arr, arr[1:]):
        if b.startswith(a):  # 접두사 관계는 사전 순으로 반드시 인접한다
            return True
    return False


def prefix_exists_trie(words):
    """트라이: 삽입 중 (1) 지나는 길에 END 를 만나거나 (2) 끝에 자식이 있으면 접두사 관계."""
    root = {}
    for w in words:
        node = root
        for ch in w:
            if END in node:  # 지금까지 온 경로가 이미 하나의 단어다
                return True
            node = node.setdefault(ch, {})
        if node:  # 단어 끝인데 자식이 있다 -> 내가 남의 접두사다
            return True
        node[END] = True
    return False


def demo_three_ways():
    title("8. 해시 vs 정렬 vs 트라이 (프로그래머스 #42577 전화번호 목록)")

    cases = [
        (["119", "97674223", "1195524421"], True, "119 가 1195524421 의 접두사"),
        (["123", "456", "789"], False, "접두사 관계 없음"),
        (["12", "123", "1235", "567", "88"], True, "12 -> 123 -> 1235"),
        (["1"], False, "단어 1개"),
    ]
    print("{:<32} {:<7} {:<7} {:<8} 기대".format("입력", "해시", "정렬", "트라이"))
    print("-" * 70)
    for words, expected, _note in cases:
        h = prefix_exists_hash(words)
        s = prefix_exists_sort(words)
        t = prefix_exists_trie(words)
        assert h == s == t == expected, (words, h, s, t, expected)
        shown = str(words)
        if len(shown) > 30:
            shown = shown[:29] + "]"
        print("{:<32} {:<7} {:<7} {:<8} {}".format(
            shown, yn(h), yn(s), yn(t), yn(expected)))
    print()
    print("세 방식 모두 정답. 그러면 무엇을 쓰나?")
    print("  해시  : 접두사를 전부 슬라이싱해 조회 -> O(sum(L^2)), 짧은 문자열엔 충분")
    print("  정렬  : O(N log N x L). 코드가 3줄. 이 문제의 실전 최적해")
    print("  트라이: O(sum(L)). 이론상 최선이고, 질의가 '반복될 때' 진짜 값어치")
    print()
    print("교훈: 트라이가 항상 최적은 아니다. 한 번만 판정하면 정렬이 낫다.")
    print("      트라이는 같은 사전에 접두사 질의를 여러 번 던질 때 쓴다.")

    random.seed(39)
    n = 20000
    nums = [str(random.randrange(10 ** 7, 10 ** 8)) for _ in range(n)]

    t0 = time.perf_counter()
    r_sort = prefix_exists_sort(nums)
    t1 = time.perf_counter()
    r_trie = prefix_exists_trie(nums)
    t2 = time.perf_counter()

    print()
    print("N={} 8자리 번호 성능:".format(n))
    print("  정렬  : {:.4f}s  결과 {}".format(t1 - t0, yn(r_sort)))
    print("  트라이: {:.4f}s  결과 {}".format(t2 - t1, yn(r_trie)))
    print("  (길이가 고정 8이라 정렬의 x L 이 작다 -> 정렬이 유리한 조건)")


# ===========================================================================
# 9. 메모리 감각: dict 트라이가 얼마나 커지는가
# ===========================================================================

def demo_memory():
    title("9. 메모리 감각 - 트라이의 진짜 비용")

    words_shared = ["prefix{:04d}".format(i) for i in range(2000)]  # 접두사 공유 큼
    random.seed(39)
    alpha = "abcdefghijklmnopqrstuvwxyz"
    words_random = ["".join(random.choice(alpha) for _ in range(10)) for _ in range(2000)]

    for label, ws in (("공통 접두사 많음", words_shared), ("무작위 문자열", words_random)):
        root = build_trie(ws)
        total_chars = sum(len(w) for w in ws)
        nodes = count_nodes(root)
        print("{}:".format(label))
        print("  단어 수 {:>6} / 총 글자 수 {:>6} / 트라이 노드 수 {:>6}".format(
            len(ws), total_chars, nodes))
        print("  노드/글자 비율 = {:.2f}".format(nodes / total_chars))
        print()

    print("빈 dict 하나의 크기: {} bytes".format(sys.getsizeof({})))
    print("노드가 총 글자 수만큼 생기면 글자 100만 개 = dict 100만 개.")
    print("  -> 수백 MB 로 튈 수 있다. 이것이 트라이의 실제 제약이다.")
    print()
    print("줄이는 방법:")
    print("  1) __slots__ 를 쓴 클래스 노드 (위 TrieNode)")
    print("  2) 자식을 [None]*26 배열로 (문자 집합이 작고 밀집할 때)")
    print("  3) 자식 1개인 사슬을 압축 -> 압축 트라이 (radix / Patricia trie)")
    print("     노드 수가 O(단어 수) 로 줄어든다. 리눅스 라우팅 테이블이 이 방식.")


# ===========================================================================
# main
# ===========================================================================

def main():
    print("Day 39 - 트라이 (Trie / Prefix Tree)")
    print("표준 라이브러리만 사용. cp949 콘솔 안전 출력.")

    demo_min_trie()
    demo_class_trie()
    demo_autocomplete()
    demo_wildcard()
    demo_length_tries()
    demo_bit_trie()
    demo_word_search()
    demo_three_ways()
    demo_memory()

    title("정리")
    print("1. 트라이는 '경로가 값'이다. 접두사를 공유하면 경로를 공유한다.")
    print("2. 삽입/검색 O(L). 저장된 단어 수 N 과 무관 -> log 가 없다.")
    print("3. search 와 startsWith 는 is_end 를 보느냐 마느냐 한 줄 차이다.")
    print("4. 개수를 물으면 삽입 때 cnt 를 누적해라. 질의가 O(L) 로 확정된다.")
    print("5. 접미사 조건은 문자열을 뒤집어라. 길이 조건은 길이별로 쪼개라.")
    print("6. 비트 트라이 = 알파벳 {0,1}, 길이 32 인 트라이. XOR 최댓값 O(32N).")
    print("7. 백트래킹에서 트라이는 '가망 없는 분기를 즉시 끊는 필터'다.")
    print("8. 대가는 메모리다. 접두사 질의가 없으면 해시나 정렬을 써라.")


if __name__ == "__main__":
    main()
