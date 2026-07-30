---
day: 39
phase: 4-advanced
title: 트라이 (Trie / Prefix Tree)
category: [자료구조, 트라이, Trie, 접두사, Prefix, 문자열, 자동완성, 비트 트라이]
difficulty: 중급
status: done
prev: "[[day-38-topological-sort/concept|Day 38 — 위상 정렬 (Topological Sort)]]"
next: "[[day-40-segment-tree/concept|Day 40 — 세그먼트 트리 (Segment Tree)]]"
related:
  - "[[day-38-topological-sort/concept|Day 38 — 위상 정렬 (Topological Sort)]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-27-backtracking/concept|Day 27 — 백트래킹]]"
  - "[[day-04-strings/concept|Day 04 — 문자열 다루기]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-05-math/concept|Day 05 — 수학·진법·비트 기초]]"
sources:
  - https://leetcode.com/problems/implement-trie-prefix-tree/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42577
  - https://leetcode.com/problems/design-add-and-search-words-data-structure/
  - https://leetcode.com/problems/search-suggestions-system/
  - https://school.programmers.co.kr/learn/courses/30/lessons/60060
  - https://leetcode.com/problems/word-search-ii/
  - https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/
  - https://en.wikipedia.org/wiki/Trie
tags: [phase/4, topic/trie, topic/prefix-tree, topic/string, topic/autocomplete, topic/hashing, topic/backtracking, topic/bit-trie]
---

# Day 39 — 트라이 (Trie / Prefix Tree)

> [!abstract] 한눈 요약 (TL;DR)
> **트라이(trie, 접두사 트리/prefix tree)** 는 **문자열 집합을 "글자 하나 = 간선 하나"로 쪼개서 공통 접두사를 하나의 경로로 공유하는 트리**다. 이름은 re**trie**val에서 왔고 보통 "트라이"로 읽는다. 핵심 성질 하나만 기억하면 된다: **길이 L인 문자열의 삽입·검색이 저장된 단어 수 N과 완전히 무관하게 O(L)** 이다. 단어가 100개든 100만 개든, `"apple"`을 찾는 비용은 언제나 5번의 자식 탐색이다. [[day-09-hashing/concept|해시(Day 09)]]도 O(L)에 **완전 일치**를 판정하지만, 트라이가 이기는 지점은 딱 하나다 — **접두사(prefix)**. `"app"`로 시작하는 단어가 있는지, 몇 개인지, 그 목록이 무엇인지를 해시는 전수 조사(O(N·L))해야 하지만 트라이는 **경로를 따라 내려가면 그 지점의 서브트리가 곧 답**이다. 그래서 트라이는 **자동완성(autocomplete), 검색어 추천, 사전 접두사 판별, 오타 교정, 와일드카드 매칭**의 기본 자료구조가 된다. 구현은 놀랍도록 짧다 — 파이썬에서는 **중첩 dict 한 줄**(`node = node.setdefault(ch, {})`)로 끝난다. 대가는 **메모리**다. 최악의 경우 노드 수가 총 글자 수만큼 생기고 노드마다 자식 테이블이 붙는다. 확장 두 가지가 코테 단골이다: 문자 대신 **비트**를 내려가는 **비트 트라이(bit trie)** 로 XOR 최댓값을 O(32N)에 구하고([[day-05-math/concept|비트 Day 05]]), 트라이 위에서 [[day-27-backtracking/concept|백트래킹(Day 27)]]을 돌려 격자에서 여러 단어를 동시에 찾는다(LeetCode #212). 핵심 한 줄: **"접두사를 공유하면 경로를 공유한다 — 그래서 접두사 질의는 내려가기만 하면 끝."**

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **정의.** 트라이는 각 **간선(edge)** 에 문자 하나가 붙은 **뿌리 있는 트리(rooted tree)** 로, 뿌리에서 어떤 노드까지의 경로에 적힌 문자들을 이으면 그 노드가 대표하는 **접두사**가 된다. 노드 하나에는 보통 두 가지만 저장한다 — **자식 맵**(문자 → 다음 노드)과 **"여기서 끝나는 단어가 있다"는 표시**(`is_end`). 저장된 단어 집합은 "뿌리에서 `is_end` 노드까지의 모든 경로"와 정확히 일치한다.
>
> **핵심은 "값을 저장한다"가 아니라 "경로가 값이다".** 일반 트리·해시는 노드나 버킷 **안에** 데이터를 넣는다. 트라이는 데이터를 **경로 자체로 표현**한다. `"cat"`은 어디에도 문자열로 저장되지 않는다 — c→a→t 경로가 존재하고 t 노드에 `is_end=True`가 켜져 있을 뿐이다. 이 발상 전환이 트라이 이해의 전부다.
>
> **일상 비유 — 종이 백과사전의 색인 탭.** 사전에서 "algorithm"을 찾을 때 A 탭을 펼치고, AL 구역으로, ALG 구역으로 좁혀 들어간다. 각 단계에서 **후보 집합이 접두사로 걸러진다**. "AL로 시작하는 단어를 전부 보여줘"는 사전에서 AL 구역만 펼치면 되는 일이고, 이게 트라이의 접두사 질의다. 반면 해시는 **모든 단어를 무작위 서랍에 흩어 넣은 상태** — "AL로 시작하는 것"을 찾으려면 서랍을 전부 열어봐야 한다.
>
> **또 다른 비유 — 전화 자동응답 메뉴.** "1번 계좌 → 1번 조회 → 2번 거래내역". 눌러온 숫자열이 곧 현재 위치이고, 지금 노드의 자식이 "다음에 누를 수 있는 번호"다. 트라이 노드를 상태(state)로 보면 트라이는 **접두사를 상태로 갖는 결정적 유한 오토마타(DFA)** 이며, 실제로 문자열 검색 알고리즘(아호-코라식/Aho-Corasick)이 이 관점 위에 실패 링크를 얹어 만들어진다.
>
> **해시와의 역할 분담이 정확한 이해다.**
>
> | 질문 | 해시(set/dict) | 트라이 |
> |---|---|---|
> | `"apple"`이 있나? | **O(L)** ✅ | O(L) ✅ |
> | `"app"`로 시작하는 게 있나? | O(N·L) ❌ | **O(L)** ✅ |
> | `"app"`로 시작하는 단어 k개 나열 | O(N·L) ❌ | **O(L + 출력량)** ✅ |
> | `"a?ple"` 같은 와일드카드 매칭 | 불가 ❌ | **가능**(분기 탐색) ✅ |
> | 사전 순 전체 순회 | 정렬 필요 O(N log N) | **DFS만 하면 정렬됨** ✅ |
> | 메모리 | 작다 ✅ | **크다** ❌ |
>
> 결론은 단순하다. **완전 일치만 필요하면 해시가 옳다**(더 짧고 더 가볍다). **접두사 개념이 문제에 등장하는 순간 트라이를 꺼낸다.** 프로그래머스 #42577 "전화번호 목록"이 정확히 이 갈림길에 서 있는 문제다(정렬로도, 해시로도, 트라이로도 풀린다 — 그리고 셋을 비교해보는 것이 이 유형 학습의 핵심이다).
>
> **트라이 순회는 사전 순 정렬을 공짜로 준다.** 자식을 문자 순서대로 방문하며 [[day-25-dfs/concept|DFS(Day 25)]]하면 나오는 단어 순서가 **곧 사전 순(lexicographic order)** 이다. 비교 정렬을 한 번도 하지 않는데 정렬 결과가 나온다 — 기수 정렬(radix sort)이 비교 없이 정렬하는 것과 같은 원리다. LeetCode #1268 "사전 순 최소 3개 추천"이 이 성질을 그대로 쓴다.

> [!gear]- 2. 동작 원리 (How It Works)
> **예제.** `["cat", "car", "card", "dog"]`를 넣은 트라이:
> ```
>              (root)
>              /    \
>            c        d
>           /          \
>          a            o
>         / \            \
>        t*  r*           g*
>            |
>            d*
>
>   * = is_end (여기서 끝나는 단어가 있음)
>
>   "cat"  : root -c-> -a-> -t*
>   "car"  : root -c-> -a-> -r*        <- "ca" 경로를 cat 과 공유
>   "card" : root -c-> -a-> -r* -> -d* <- "car" 가 접두사이자 그 자체로 단어
>   "dog"  : root -d-> -o-> -g*
>
>   총 글자 수 3+3+4+3 = 13 인데 노드는 8개 -> 공통 접두사만큼 절약
> ```
>
> **(A) 삽입 (insert) — 없으면 만들고, 끝에서 도장을 찍는다.**
> ```
> insert(word):
>     node = root
>     for ch in word:
>         if ch not in node.children:
>             node.children[ch] = 새 노드      # 없으면 새 가지
>         node = node.children[ch]             # 한 칸 내려간다
>     node.is_end = True                       # 마지막에 도장
> ```
> `"car"` 다음 `"card"`를 넣으면 c,a,r 은 **이미 있어 재사용**되고 d만 새로 생긴다. **`is_end`를 켜는 것을 잊으면** 트라이에 경로는 있는데 "단어로 등록"은 안 된 상태가 되어 검색이 실패한다.
>
> **(B) 검색 (search) vs 접두사 검색 (startsWith) — 딱 한 줄 차이.**
> ```
> _walk(s):                         # s 경로를 따라 내려가 도착 노드 반환
>     node = root
>     for ch in s:
>         if ch not in node.children:
>             return None           # 경로가 끊겼다 -> 없다
>         node = node.children[ch]
>     return node
>
> search(word)     : node = _walk(word);   return node is not None and node.is_end
> startsWith(pref) : node = _walk(pref);   return node is not None
>                                          ^^^^^^^^^^^^^^^^^^^^^^^
>                                          is_end 을 안 볼 뿐이다!
> ```
> ```
> search("car")     -> 경로 O, is_end O  ->  True
> search("ca")      -> 경로 O, is_end X  ->  False   (접두사일 뿐 단어 아님)
> startsWith("ca")  -> 경로 O            ->  True
> startsWith("cb")  -> c 에서 b 없음     ->  False
> ```
> **이 대비가 LeetCode #208의 전부**이고, 트라이 유형 최다 오답 지점이다. "존재한다"와 "단어로 등록되었다"는 다르다.
>
> **(C) 파이썬 최단 구현 — 중첩 dict + `setdefault`.**
> ```
> trie = {}
> for word in words:
>     node = trie
>     for ch in word:
>         node = node.setdefault(ch, {})   # 없으면 {} 만들고, 있으면 그것을 반환
>     node['$'] = True                     # 단어 끝 표시 (문자와 겹치지 않는 키)
> ```
> ```
> ["cat","car"] 를 넣으면:
> {'c': {'a': {'t': {'$': True},
>              'r': {'$': True}}}}
>
> 클래스 정의도, 노드 객체도 없다. 코테에서 가장 빠르게 쓸 수 있는 형태.
> 단, '$' 같은 끝 표시 키는 실제 문자와 절대 겹치지 않아야 한다.
> ```
>
> **(D) 접두사로 시작하는 단어 개수 — 노드에 카운터를 얹는다.**
> ```
> insert 할 때 지나가는 모든 노드에서 cnt += 1
>     -> node.cnt = "이 접두사로 시작하는 단어 수"
>
> ["cat","car","card"] 삽입 후:
>     root.cnt=3, c.cnt=3, a.cnt=3, t.cnt=1, r.cnt=2, d.cnt=1
>
> count_prefix("ca")  ->  _walk("ca").cnt  =  3     # O(L), 세지 않는다!
> count_prefix("car") ->  _walk("car").cnt =  2
> ```
> **이 한 줄 추가가 프로그래머스 #60060 "가사 검색"의 열쇠**다. 질의마다 후보를 세는 게 아니라 **삽입 시점에 미리 세어둔다**.
>
> **(E) 와일드카드 `.` 매칭 — 갈림길에서 전부 시도(백트래킹).**
> ```
> search("b.d"):
>     '.' 을 만나면 현재 노드의 모든 자식으로 각각 내려가 본다
>
>     dfs(node, i):
>         if i == len(word):      return node.is_end
>         ch = word[i]
>         if ch == '.':
>             for child in node.children.values():   # 모든 분기 시도
>                 if dfs(child, i+1): return True
>             return False
>         return ch in node.children and dfs(node.children[ch], i+1)
> ```
> ```
> "bad","bed" 저장 상태에서 search("b.d"):
>     b -> '.' -> 자식 {a, e} 둘 다 시도 -> a 경로에서 d 발견 -> True
>
> 최악 복잡도: '.' 이 k개면 O(26^k) 분기 -> #211 의 제약(단어 길이 <= 25,
> '.' 최대 2개)이 이 폭발을 막아준다.
> ```
> [[day-27-backtracking/concept|백트래킹(Day 27)]] 그대로다 — 트라이가 "가지치기된 탐색 공간"을 제공하고, 없는 문자에서 즉시 끊긴다.
>
> **(F) 고정 길이 wildcard 최적화 — 길이별 트라이 분리 (가사 검색 패턴).**
> ```
> 문제: "fro??" 처럼 '?' 가 뒤에만(또는 앞에만) 붙는 질의가 10만 개.
>
> 관찰 1: "fro??" 는 "길이 5 이고 fro 로 시작" 과 완전히 동치다.
>         -> 길이별로 트라이를 따로 만들면 '?' 를 셀 필요조차 없다.
> 관찰 2: "??ro" 처럼 앞에 붙으면? 문자열을 뒤집어 넣은 트라이를 하나 더.
>         "??ro" -> "or??" -> 역방향 트라이에서 "or" 접두사 개수.
> 관찰 3: "?????" 처럼 전부 '?' 면 그 길이의 단어 수 전체.
>
> 자료구조: trie_fwd[길이], trie_bwd[길이]  (각 노드에 cnt)
> 질의 O(L), 전체 O(총글자수 + 질의수 x L)
> ```
> **문자열 뒤집기 트릭은 트라이 문제의 핵심 패턴**이다. "접미사(suffix) 조건"은 뒤집으면 접두사 조건이 된다.
>
> **(G) 비트 트라이 (bit trie) — 문자 대신 0/1을 내려간다.**
> ```
> 정수를 상위 비트부터 31, 30, ..., 0 순으로 0/1 간선을 타고 내려간다
> (자식은 최대 2개 -> 깊이 32의 이진 트리)
>
> XOR 최대화: x 와 짝지을 값을 찾을 때, 각 비트에서 x 의 비트와
>             '반대' 자식으로 가려 시도한다 (반대면 그 비트가 1 -> 이득)
>             반대 자식이 없으면 같은 쪽으로 (어쩔 수 없이 0)
>
>     for b in 31..0:
>         want = 1 - ((x >> b) & 1)
>         node = node[want] if want in node else node[1-want]
>
> -> LeetCode #421 을 O(32N) 에 해결. 브루트포스 O(N^2) 대비 압승.
> ```
> **"상위 비트부터 그리디"** 가 성립하는 이유: 상위 비트 1개가 그 아래 전부를 합친 것보다 크기 때문이다([[day-05-math/concept|비트 Day 05]], [[day-21-greedy/concept|그리디 Day 21]]).
>
> **(H) 격자 + 트라이 = 여러 단어 동시 탐색 (LeetCode #212).**
> ```
> 단어 W개를 격자에서 각각 DFS하면 O(W x 격자 x 4^L) -> 시간 초과.
>
> 트라이에 W개를 다 넣고, 격자를 한 번만 DFS하면서 트라이 노드를 함께 내려간다:
>     현재 칸의 문자가 트라이 노드의 자식에 없으면 -> 즉시 가지치기
>     (그 방향으로는 어떤 단어도 만들 수 없다는 뜻)
>
> 추가 최적화: 단어를 찾으면 is_end 를 끄고,
>             자식이 없어진 노드는 부모에서 제거(pruning) -> 탐색 공간이 계속 줄어든다
> ```
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. **N** = 단어 수, **L** = 단어 길이, **Σ** = 알파벳 크기(소문자 26), **M** = 총 글자 수(Σ|wᵢ|).
>
> | 연산 | 시간복잡도 | 공간 | 설명 |
> |---|---|---|---|
> | **삽입 (insert)** | **O(L)** | 최악 O(L) 신규 노드 | **N과 무관.** 글자마다 자식 맵 조회 1회 |
> | **검색 (search)** | **O(L)** | O(1) | 경로 추적 + `is_end` 확인 |
> | **접두사 존재 (startsWith)** | **O(L)** | O(1) | `is_end`만 안 볼 뿐 |
> | **접두사 단어 수** | **O(L)** | O(1) | 노드에 `cnt`를 미리 얹어둔 경우 |
> | 접두사로 시작하는 단어 나열 | O(L + 출력 글자 수) | O(깊이) | 서브트리 DFS. 출력에 비례 |
> | 삭제 (delete) | O(L) | O(L) 재귀 | `is_end` 끄고 빈 노드 되짚어 제거 |
> | 와일드카드 `.` 검색 | O(Σ^k · L) 최악 | O(L) 재귀 | `.` k개의 분기 폭발 |
> | 전체 트라이 구축 | **O(M)** | **O(M·Σ)** 최악 | 공통 접두사가 많으면 훨씬 작다 |
> | 사전 순 전체 순회 | O(M) | O(깊이) | **비교 정렬 없이 정렬됨** |
> | 비트 트라이 XOR 최대 | **O(32N)** = O(N) | O(32N) | 브루트포스 O(N²) 대체 |
> | 격자 + 트라이 (#212) | O(격자 · 4·3^(L-1)) | O(M) | 트라이가 분기를 가지치기 |
>
> > **"N과 무관"이 트라이의 진짜 값어치다.** 단어가 100만 개여도 `"apple"` 검색은 5스텝이다. 이진 탐색 트리(BST)는 O(L log N), 정렬 후 [[day-18-binary-search/concept|이분 탐색(Day 18)]]도 O(L log N)이다. 트라이만 **log가 없다**.
> >
> > **해시와 같은 O(L)인데 왜 쓰는가.** 완전 일치만 보면 해시가 낫다(상수가 작고 메모리도 적다). **트라이의 우위는 오직 접두사 질의**다. 해시의 O(L)은 "문자열 전체를 해싱하는 비용"이고 트라이의 O(L)은 "한 글자씩 내려가는 비용"이다 — 후자는 **중간에 멈춰서 그 지점을 질의할 수 있다**. 이게 결정적 차이다.
> >
> > **메모리가 진짜 비용이다.** 노드마다 dict(파이썬 빈 dict만 ~64바이트 + 항목당 오버헤드)를 들면 총 글자 수만큼 dict가 생긴다. 글자 100만 개면 수백 MB로 튈 수 있다. 대안: ① 자식을 `[None]*26` 배열로(문자 집합이 작고 밀집할 때 빠르다), ② **자식이 1개뿐인 사슬을 하나로 압축**한 **압축 트라이(radix tree / Patricia trie)** → 노드 수 O(N)으로 감소, ③ 정말 큰 사전은 DAWG/DAFSA로 접미사까지 공유.
> >
> > **Σ가 복잡도에 숨어 있다.** 자식을 배열로 잡으면 노드 하나가 Σ칸을 차지해 공간이 O(M·Σ)로 부풀지만 자식 조회는 확정 O(1)이다. dict면 공간은 실제 자식 수에 비례하지만 해싱 상수가 붙는다. **코테에서는 dict가 정답**이다(구현이 짧고 유니코드/숫자/대문자 혼재에도 안전).
> >
> > **와일드카드는 지수다 — 제약을 반드시 확인하라.** `.`이 k개면 최악 Σ^k 분기다. LeetCode #211이 "`.` 최대 2개, 길이 ≤ 25"로 제약을 준 것은 **그 폭발을 막으라는 신호**다. 제약 없이 `.`이 많으면 트라이가 아니라 다른 접근(길이별 분리, 롤링 해시)을 생각해야 한다.
> >
> > **#212에서 4^L이 4·3^(L-1)인 이유.** 첫 칸은 4방향이지만 그 다음부터는 **왔던 방향으로 되돌아가지 않으므로** 3방향이다. 여기에 트라이 가지치기가 얹히면 실전 성능은 이론치보다 훨씬 좋다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **암기 문장.** **"접두사를 공유하면 경로를 공유한다."** 여기서 모든 성질이 따라 나온다 — 접두사 질의가 O(L), DFS가 사전 순, 메모리는 공통 접두사만큼 절약. ([Trie 위키](https://en.wikipedia.org/wiki/Trie))
> - **파이썬은 `setdefault` 한 줄이면 트라이다.** `node = node.setdefault(ch, {})`. 클래스 없이 중첩 dict로 끝난다. 코테에서 3분 안에 쓰는 형태를 손에 익혀두라. ([LeetCode #208](https://leetcode.com/problems/implement-trie-prefix-tree/))
> - **`search`와 `startsWith`의 차이를 소리 내어 확인하라.** 둘은 `is_end`를 보느냐 마느냐만 다르다. 이걸 헷갈려 `search("ca")`가 True를 반환하는 게 트라이 최다 버그다.
> - **"접두사/접미사/자동완성/사전/시작하는" 이라는 단어가 문제에 보이면 트라이를 의심하라.** 반대로 **"완전 일치만"** 이면 해시가 더 짧고 빠르다. 트라이를 쓸 이유를 한 문장으로 말할 수 없으면 [[day-09-hashing/concept|해시(Day 09)]]로 가라.
> - **접미사 조건은 문자열을 뒤집어라.** "~로 끝나는"은 뒤집으면 "~로 시작하는"이 된다. 정방향/역방향 트라이 두 개를 두는 것이 [가사 검색(프로그래머스 #60060)](https://school.programmers.co.kr/learn/courses/30/lessons/60060)의 정석 풀이다.
> - **개수를 세는 문제는 삽입 시점에 카운터를 얹어라.** 질의 때 서브트리를 세면 O(출력량)이지만, 삽입 때 지나가는 노드마다 `cnt += 1` 해두면 질의가 **O(L)로 확정**된다. 질의가 많은 문제(10만 건)에서 이 차이가 통과/시간초과를 가른다.
> - **길이가 조건에 섞이면 길이별로 트라이를 쪼개라.** `"fro??"` = "길이 5 & fro 로 시작". 딕셔너리 `defaultdict(dict)`로 `trie[len]`을 만들면 와일드카드를 아예 처리하지 않아도 된다.
> - **비트 트라이는 "문자 = 비트, 알파벳 = {0,1}, 길이 = 32"인 트라이일 뿐이다.** 새로 배우는 자료구조가 아니다. XOR 최댓값은 상위 비트부터 반대쪽으로 그리디. ([LeetCode #421](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/))
> - **트라이 + 백트래킹은 "가지치기 도구로서의 트라이"다.** [격자 단어 찾기(LeetCode #212)](https://leetcode.com/problems/word-search-ii/)에서 트라이는 저장소가 아니라 **"이 방향은 가망 없다"를 즉시 알려주는 필터**로 쓰인다. 단어를 찾은 뒤 노드를 제거하는 pruning까지 하면 체감 속도가 크게 뛴다.
> - **정렬만으로 풀리는지 먼저 보라.** [전화번호 목록(프로그래머스 #42577)](https://school.programmers.co.kr/learn/courses/30/lessons/42577)은 문자열 정렬 후 **인접한 쌍만** 검사하면 O(N log N)에 끝난다(사전 순으로 붙어 있는 것끼리만 접두사 관계가 가능하다). **트라이가 항상 최적은 아니다** — 트라이는 "질의가 반복될 때" 값어치가 있다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **`is_end`(단어 끝 표시)가 없는 트라이는 망가진 트라이다.** 경로 존재 ≠ 단어 등록. `["card"]`만 넣고 `search("car")`를 물으면 경로는 있지만 답은 False여야 한다. `is_end`를 빼먹으면 **접두사 전부를 단어로 인정**하는 조용한 오답이 난다.
> 2. **중첩 dict를 쓸 때 끝 표시 키는 실제 문자와 절대 겹치면 안 된다.** `'$'`, `'*'`, `None`, `('end',)` 등을 쓰되 **입력에 그 문자가 나올 수 있는지 확인**하라. 숫자·기호가 섞인 입력(전화번호, 파일 경로)에서 `'#'`이나 `'*'`를 끝 표시로 쓰면 충돌한다. 가장 안전한 것은 문자열이 될 수 없는 키(`None` 또는 정수 `0`).
> 3. **빈 문자열 `""`은 항상 경계 케이스다.** `insert("")`는 root에 `is_end`를 켜는 것이고, `startsWith("")`는 트라이가 비어 있지 않으면 True다. 문제가 빈 문자열을 허용하는지 제약을 확인하라.
> 4. **트라이는 메모리를 먹는다 — 파이썬에서 특히.** 노드마다 dict를 만들면 총 글자 수만큼 dict가 생긴다. 총 글자 10⁶이면 수백 MB까지 갈 수 있다. `__slots__`를 쓴 클래스, `[None]*26` 배열, 또는 압축 트라이(radix/Patricia)를 고려하라. **"트라이 쓰면 되지"가 메모리 초과로 돌아오는 경우가 실제로 있다.**
> 5. **삭제는 겉보기보다 까다롭다.** `is_end`를 끄는 것만으로는 노드가 남아 메모리가 새고 접두사 카운트가 틀어진다. 올바른 삭제는 **재귀로 내려가 `is_end`를 끈 뒤, 되돌아 나오며 "자식 없고 `is_end`도 아닌 노드"를 부모에서 제거**하는 것이다. 그리고 `"car"`를 지울 때 `"card"`가 남아 있으면 **노드를 절대 지워서는 안 된다**(자식 존재 확인 필수).
> 6. **접두사 카운터(`cnt`)를 쓰면 삭제 시 감소도 잊지 마라.** 삽입에서 +1 한 모든 노드에서 삭제 시 −1 해야 한다. 한쪽만 구현하면 질의가 서서히 틀린 값을 내는 최악의 버그가 된다.
> 7. **와일드카드 검색은 지수 시간이 될 수 있다.** `.`이 k개면 최악 Σ^k. 제약(`.` 개수, 길이)을 확인하지 않고 제출하면 TLE다. `"......"`처럼 전부 `.`인 질의는 사실상 "그 길이의 단어가 있는가"이므로 **길이별 카운트를 따로 들고 있으면 O(1)** 로 답할 수 있다.
> 8. **파이썬 재귀 깊이.** 트라이 DFS 깊이는 최대 단어 길이라 보통 안전하지만(≤ 10³), 매우 긴 문자열이나 비트 트라이 32단계는 문제없다. 다만 격자 백트래킹(#212)에서는 깊이가 격자 크기까지 갈 수 있으니 반복문 변환이나 `sys.setrecursionlimit`을 염두에 두라.
> 9. **자식 순회 순서가 결과 순서를 결정한다.** 파이썬 3.7+ dict는 **삽입 순서**를 보존한다 — **사전 순이 아니다**. 사전 순 결과가 필요하면 `sorted(node.children)`으로 명시적으로 정렬하거나, 애초에 단어를 정렬해 삽입하라. **"트라이 DFS는 사전 순"은 자식을 문자 순으로 방문할 때만 성립한다.** LeetCode #1268에서 이걸 놓치면 오답이다.
> 10. **트라이 vs 해시는 면접 단골 비교다.** 정답 요지: "둘 다 완전 일치는 O(L)이지만, **트라이는 중간 지점(접두사)을 질의할 수 있고 사전 순 순회가 공짜**다. 대가는 메모리와 구현 복잡도. 접두사 질의가 없으면 해시를 쓴다."
> 11. **트라이 vs 이분 탐색.** 정렬된 배열 + 이분 탐색으로도 접두사 범위(lower/upper bound)를 O(L log N)에 찾을 수 있다. **한 번만 질의하면 정렬+이분이 메모리 면에서 유리**하고, **질의가 반복되면 트라이가 유리**하다. 프로그래머스 #60060은 이분 탐색으로도 풀리는 대표적 예다.
> 12. **접두사(prefix)와 접미사(suffix), 부분 문자열(substring)을 구분하라.** 트라이는 **접두사** 전용이다. 접미사는 뒤집어서 해결하고, **임의의 부분 문자열**을 다루려면 접미사 트라이/접미사 배열(suffix array)·아호-코라식 같은 상급 도구가 필요하다. 문제 문장에서 이 셋을 혼동하면 자료구조 선택 자체가 틀린다.
> 13. **실무에서 트라이가 실제로 쓰이는 곳.** 라우터의 **IP 라우팅 테이블**(최장 접두사 일치, longest prefix match — 비트 트라이/Patricia trie), 검색창 **자동완성**, IDE **코드 자동완성**, 스펠 체커, T9 문자 입력, 사전형 압축. "접두사로 조회한다"는 요구가 있는 곳마다 트라이가 있다.
> 14. **압축 트라이(radix/Patricia)를 이름은 알아두라.** 자식이 하나뿐인 사슬을 한 노드로 합쳐 **노드 수를 O(N)으로 줄인 트라이**다. 리눅스 커널 라우팅, etcd/Ethereum의 상태 트리(Merkle Patricia Trie) 등 실전에서 널리 쓰인다. 코테에서 직접 구현하는 일은 드물지만 "트라이 메모리를 어떻게 줄이나?"의 표준 답이다.

> [!example]- 예제 코드 (Examples)
> ```python
> # ---- (1) 최소 트라이: 중첩 dict + setdefault (코테 최속 형태) ----
> END = None                              # 실제 문자와 절대 겹치지 않는 끝 표시
>
> def build_trie(words):
>     root = {}
>     for w in words:
>         node = root
>         for ch in w:
>             node = node.setdefault(ch, {})    # 없으면 만들고, 있으면 재사용
>         node[END] = True
>     return root
>
> def walk(root, s):
>     """s 경로를 따라 내려가 도착 노드 반환. 끊기면 None."""
>     node = root
>     for ch in s:
>         if ch not in node:
>             return None
>         node = node[ch]
>     return node
>
> def has_word(root, w):
>     node = walk(root, w)
>     return node is not None and END in node       # is_end 를 본다
>
> def has_prefix(root, p):
>     return walk(root, p) is not None              # is_end 를 안 본다
>
>
> # ---- (2) 클래스 트라이 (LeetCode #208 시그니처) ----
> class TrieNode:
>     __slots__ = ('children', 'is_end', 'cnt')     # 메모리 절약
>     def __init__(self):
>         self.children = {}
>         self.is_end = False
>         self.cnt = 0                              # 이 접두사로 시작하는 단어 수
>
> class Trie:
>     def __init__(self):
>         self.root = TrieNode()
>
>     def insert(self, word: str) -> None:
>         node = self.root
>         for ch in word:
>             if ch not in node.children:
>                 node.children[ch] = TrieNode()
>             node = node.children[ch]
>             node.cnt += 1                         # 지나가며 카운터 누적
>         node.is_end = True
>
>     def _walk(self, s):
>         node = self.root
>         for ch in s:
>             if ch not in node.children:
>                 return None
>             node = node.children[ch]
>         return node
>
>     def search(self, word: str) -> bool:
>         node = self._walk(word)
>         return node is not None and node.is_end
>
>     def startsWith(self, prefix: str) -> bool:
>         return self._walk(prefix) is not None
>
>     def count_prefix(self, prefix: str) -> int:
>         node = self._walk(prefix)                 # O(L), 세지 않는다
>         return node.cnt if node else 0
>
>
> # ---- (3) 접두사로 시작하는 단어 사전 순 나열 (자동완성) ----
> def autocomplete(trie, prefix, limit=3):
>     node = trie._walk(prefix)
>     if node is None:
>         return []
>     out = []
>     def dfs(nd, path):
>         if len(out) == limit:
>             return
>         if nd.is_end:
>             out.append(prefix + path)
>         for ch in sorted(nd.children):            # 사전 순은 명시적 정렬!
>             if len(out) == limit:
>                 return
>             dfs(nd.children[ch], path + ch)
>     dfs(node, '')
>     return out
>
>
> # ---- (4) 와일드카드 '.' 검색 (LeetCode #211) ----
> def search_wildcard(trie, word):
>     def dfs(node, i):
>         if i == len(word):
>             return node.is_end
>         ch = word[i]
>         if ch == '.':
>             for child in node.children.values():  # 모든 분기 시도
>                 if dfs(child, i + 1):
>                     return True
>             return False
>         nxt = node.children.get(ch)
>         return nxt is not None and dfs(nxt, i + 1)
>     return dfs(trie.root, 0)
>
>
> # ---- (5) 삭제: is_end 끄고 빈 노드 되짚어 제거 ----
> def delete(trie, word):
>     def rec(node, i):
>         """반환값: 이 노드를 부모에서 지워도 되는가"""
>         if i == len(word):
>             if not node.is_end:
>                 return False                      # 없던 단어 -> 변경 없음
>             node.is_end = False
>             return len(node.children) == 0        # 자식 있으면 남겨둔다
>         ch = word[i]
>         child = node.children.get(ch)
>         if child is None:
>             return False
>         if rec(child, i + 1):
>             del node.children[ch]
>         return not node.children and not node.is_end
>     rec(trie.root, 0)
>
>
> # ---- (6) 비트 트라이: XOR 최댓값 (LeetCode #421) ----
> BITS = 31
>
> def max_xor(nums):
>     root = {}
>     for x in nums:                                # 삽입
>         node = root
>         for b in range(BITS, -1, -1):             # 상위 비트부터
>             bit = (x >> b) & 1
>             node = node.setdefault(bit, {})
>     best = 0
>     for x in nums:                                # 질의
>         node, cur = root, 0
>         for b in range(BITS, -1, -1):
>             bit = (x >> b) & 1
>             want = 1 - bit                        # 반대쪽이면 그 비트가 1
>             if want in node:
>                 cur |= 1 << b
>                 node = node[want]
>             else:
>                 node = node[bit]                  # 어쩔 수 없이 같은 쪽
>         best = max(best, cur)
>     return best
> ```
>
> 전체 실행 가능한 예제(길이별 정·역방향 트라이로 와일드카드 카운트, 격자+트라이 백트래킹, 해시/정렬/트라이 3방식 성능 비교 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> **기본 구현 → 접두사 판별 → 와일드카드 → 자동완성 → 기출 → 트라이+백트래킹** 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Implement Trie (Prefix Tree) | [LeetCode #208](https://leetcode.com/problems/implement-trie-prefix-tree/) | 🟢기초 | 트라이 기본 3연산(`search` vs `startsWith`) |
> | 2 | 전화번호 목록 | [프로그래머스 #42577](https://school.programmers.co.kr/learn/courses/30/lessons/42577) | 🟡중급 | 접두사 존재 판별(해시·정렬·트라이 3방식 비교) |
> | 3 | Design Add and Search Words Data Structure | [LeetCode #211](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 🟡중급 | 와일드카드 `.` 매칭 = 트라이 위 백트래킹 |
> | 4 | Search Suggestions System | [LeetCode #1268](https://leetcode.com/problems/search-suggestions-system/) | 🟡중급 | 자동완성: 접두사별 사전 순 최소 3개 |
> | 5 | 가사 검색 | [프로그래머스 #60060](https://school.programmers.co.kr/learn/courses/30/lessons/60060) | ⚫기출 | 2020 카카오 블라인드 Level 4. 길이별 정·역방향 트라이 + 접두사 카운터 |
> | 6 | Word Search II | [LeetCode #212](https://leetcode.com/problems/word-search-ii/) | 🔴심화 | 격자 백트래킹의 가지치기 도구로서의 트라이 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> `search`와 `startsWith`를 한 줄 차이로 구현하는 요령, 전화번호 목록을 해시·정렬·트라이 세 가지로 풀고 복잡도를 비교하는 법, 와일드카드 분기 폭발을 제약으로 막는 근거, 자동완성에서 사전 순을 보장하는 두 방법(삽입 전 정렬 vs `sorted(children)`), 가사 검색의 길이별 정·역방향 트라이 설계와 `?????` 전체 와일드카드 처리, 격자 백트래킹에서 트라이 노드를 동시에 내려가며 가지치기하고 찾은 단어를 pruning하는 기법, 프로그래머스/LeetCode 시그니처별 구현과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-38-topological-sort/concept|Day 38 — 위상 정렬 (Topological Sort)]] — 그래프 계열(최단 경로·MST·위상 정렬)을 마무리하고, 문자열 전용 자료구조로 넘어왔다. 트라이도 결국 "간선에 문자가 붙은 그래프"라는 점에서 연속선상에 있다
- ➡️ **다음(next):** [[day-40-segment-tree/concept|Day 40 — 세그먼트 트리 (Segment Tree)]] — 트라이가 **문자열 집합**을 트리로 조직했다면, 세그먼트 트리는 **구간(range)** 을 트리로 조직해 구간 질의·갱신을 O(log N)에 처리한다. [[day-14-prefix-sum/concept|누적 합(Day 14)]]의 상위 도구
- 🧭 **관련(related):**
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — 트라이의 직접 경쟁자. 완전 일치는 해시가 낫고 접두사 질의는 트라이가 낫다. 이 갈림길 판단이 문제 풀이의 첫 단계
  - [[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]] — 파이썬 트라이는 사실상 "dict를 중첩한 dict". `setdefault`/`defaultdict` 감각이 그대로 재사용된다
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 트라이는 뿌리 있는 다진 트리(k-ary tree)다. 노드·간선·깊이 개념이 전제
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 접두사 아래 단어 나열, 사전 순 순회, 삭제 시 되짚어 올라가는 정리가 모두 DFS
  - [[day-27-backtracking/concept|Day 27 — 백트래킹]] — 와일드카드 `.` 매칭(#211)과 격자 단어 찾기(#212)에서 트라이는 "가망 없는 분기를 즉시 끊는 가지치기 장치"로 쓰인다
  - [[day-04-strings/concept|Day 04 — 문자열 다루기]] — 접두사·접미사·부분 문자열의 구분, 문자열 뒤집기 트릭의 기초
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — 정렬된 배열의 lower/upper bound로도 접두사 범위를 O(L log N)에 찾을 수 있다. 가사 검색의 대안 풀이
  - [[day-05-math/concept|Day 05 — 수학·진법·비트 기초]] — 비트 트라이는 "알파벳이 {0,1}이고 길이가 32인 트라이". XOR 최댓값의 상위 비트 그리디가 여기서 나온다
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
