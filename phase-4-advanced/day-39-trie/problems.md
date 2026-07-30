---
day: 39
type: problems
title: Day 39 연습문제 — 트라이 (Trie / Prefix Tree)
tags: [problems, phase/4, topic/trie, topic/prefix-tree]
---

# Day 39 연습문제 — 트라이 (Trie / Prefix Tree)

개념 노트: [[concept|Day 39 — 트라이 (Trie / Prefix Tree)]] · 해설 코드: [solutions.py](solutions.py)

> [!info] 문제 출처 원칙
> **프로그래머스(programmers.co.kr)** 와 **LeetCode(leetcode.com)** 만 사용한다.
> 두 플랫폼은 함수 반환형이라 stdin 파싱이 필요 없고, 로컬에서 `assert`로 바로 검증할 수 있다.

## 풀이 순서 (권장)

**기본 구현 → 접두사 판별 → 와일드카드 → 자동완성 → 기출 → 트라이+백트래킹**

| # | 문제 | 출처 | 난이도 | 핵심 유형 |
|---|---|---|---|---|
| 1 | Implement Trie (Prefix Tree) | [LeetCode #208](https://leetcode.com/problems/implement-trie-prefix-tree/) | 🟢기초 | 트라이 기본 3연산 |
| 2 | 전화번호 목록 | [프로그래머스 #42577](https://school.programmers.co.kr/learn/courses/30/lessons/42577) | 🟡중급 | 접두사 존재 판별 |
| 3 | Design Add and Search Words Data Structure | [LeetCode #211](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 🟡중급 | 와일드카드 `.` 매칭 |
| 4 | Search Suggestions System | [LeetCode #1268](https://leetcode.com/problems/search-suggestions-system/) | 🟡중급 | 자동완성 |
| 5 | 가사 검색 | [프로그래머스 #60060](https://school.programmers.co.kr/learn/courses/30/lessons/60060) | ⚫기출 | 길이별 정·역방향 트라이 |
| 6 | Word Search II | [LeetCode #212](https://leetcode.com/problems/word-search-ii/) | 🔴심화 | 트라이 + 격자 백트래킹 |

---

## 1. 🟢 Implement Trie (Prefix Tree)

**출처:** [LeetCode #208](https://leetcode.com/problems/implement-trie-prefix-tree/) (Medium)

### 문제
`Trie` 클래스를 구현한다.

- `Trie()` — 트라이 객체 초기화
- `insert(word: str) -> None` — `word`를 트라이에 삽입
- `search(word: str) -> bool` — `word`가 **삽입된 적이 있으면** `True`
- `startsWith(prefix: str) -> bool` — **`prefix`로 시작하는 단어가 삽입된 적이 있으면** `True`

### 제약
- `1 <= word.length, prefix.length <= 2000`
- 소문자 영어 알파벳만
- 호출 총 3·10⁴회 이하

### 예시
```
입력: ["Trie","insert","search","search","startsWith","insert","search"]
      [[],     ["apple"],["apple"],["app"],  ["app"],    ["app"],  ["app"]]
출력: [null,   null,     true,     false,    true,       null,     true]
```

> [!question]- 힌트 1 — 노드에 무엇을 저장하는가
> 딱 두 가지다. **자식 맵**(문자 → 다음 노드)과 **`is_end`**(여기서 끝나는 단어가 있는가).
> 문자열 자체는 **어디에도 저장하지 않는다**. 경로가 곧 문자열이다.

> [!question]- 힌트 2 — `search`와 `startsWith`의 차이
> 세 번째 호출 `search("app")`이 `false`인 이유를 설명할 수 있어야 한다.
> `"apple"`을 넣으면 `a→p→p` 경로는 생기지만 `p` 노드에 `is_end`가 켜지지 않는다.
> **경로 존재 ≠ 단어 등록.** 두 메서드는 `is_end`를 보느냐 마느냐만 다르다.

> [!question]- 힌트 3 — 공통 부분을 함수로 빼라
> `_walk(s)`를 만들어 "s 경로를 따라간 도착 노드 또는 `None`"을 반환하게 하면,
> `search`는 `node and node.is_end`, `startsWith`는 `node is not None`이 된다.
> 중복이 사라지고 버그가 줄어든다.

**복잡도 목표:** 모든 연산 **O(L)**. 저장된 단어 수와 무관해야 한다.

---

## 2. 🟡 전화번호 목록

**출처:** [프로그래머스 #42577](https://school.programmers.co.kr/learn/courses/30/lessons/42577) (Level 2, 해시 분류)

### 문제
전화번호부에 적힌 전화번호 중 **한 번호가 다른 번호의 접두어인 경우가 있는지** 확인한다.
접두어인 경우가 **있으면 `False`**, 없으면 `True`를 반환한다.

### 제약
- `phone_book`의 길이는 1 이상 1,000,000 이하
- 각 전화번호의 길이는 1 이상 20 이하
- 같은 전화번호가 중복해서 들어 있지 않다

### 예시
```
phone_book = ["119", "97674223", "1195524421"]   ->  False
    ("119"가 "1195524421"의 접두어)
phone_book = ["123","456","789"]                 ->  True
phone_book = ["12","123","1235","567","88"]      ->  False
```

### 시그니처
```python
def solution(phone_book):
    ...
```

> [!question]- 힌트 1 — 세 가지 접근이 모두 가능하다
> ① **해시**: 각 번호의 모든 접두사를 잘라 `set`에 있는지 조회.
> ② **정렬**: 사전 순 정렬 후 **인접한 쌍만** `startswith` 검사.
> ③ **트라이**: 삽입하며 접두사 관계를 감지.
> **셋을 다 구현해 복잡도를 비교하는 것이 이 문제의 학습 목표다.**

> [!question]- 힌트 2 — 정렬 풀이의 정당성
> 왜 **인접한 쌍만** 보면 충분한가? `a`가 `b`의 접두사라면 사전 순에서 `a`와 `b` 사이에 오는
> 모든 문자열도 `a`로 시작한다(접두사가 같은 것끼리 사전 순으로 뭉쳐 있다).
> 따라서 **접두사 관계인 쌍이 존재하면 반드시 어딘가에서 인접한 쌍으로 나타난다.**
> 이 논증을 스스로 재구성할 수 있어야 한다.

> [!question]- 힌트 3 — 트라이 풀이의 두 가지 감지 조건
> 삽입 중 다음 두 경우에 접두사 관계다.
> ① 내려가는 **도중에 이미 단어 끝인 노드**를 만났다 → 기존 단어가 내 접두사.
> ② 삽입을 마친 노드에 **자식이 이미 있다** → 내가 기존 단어의 접두사.
> **한쪽만 검사하면 절반의 케이스를 놓친다.**

> [!question]- 힌트 4 — 함정: 반환값 방향
> "접두어인 경우가 **있으면 `False`**"다. 직관과 반대라 부호를 뒤집기 쉽다.
> 문제 문장을 다시 읽고 예시로 확인하라.

**복잡도 목표:** 정렬 O(N log N × L) 또는 트라이 O(ΣL). N이 100만이므로 O(N²)은 불가.

---

## 3. 🟡 Design Add and Search Words Data Structure

**출처:** [LeetCode #211](https://leetcode.com/problems/design-add-and-search-words-data-structure/) (Medium)

### 문제
단어를 추가하고, 추가된 단어와 일치하는지 찾는 자료구조 `WordDictionary`를 설계한다.

- `WordDictionary()` — 초기화
- `addWord(word: str) -> None` — `word` 추가
- `search(word: str) -> bool` — 추가된 단어 중 `word`와 일치하는 것이 있으면 `True`.
  **`word`에는 `.`이 포함될 수 있고, `.`은 아무 글자 하나와 매칭된다.**

### 제약
- `1 <= word.length <= 25`
- `addWord`의 `word`는 소문자 알파벳만
- `search`의 `word`는 소문자 알파벳 또는 `.`
- **`search`에서 `.`은 최대 2개**
- 호출 총 10⁴회 이하

### 예시
```
addWord("bad"); addWord("dad"); addWord("mad")
search("pad") -> false
search("bad") -> true
search(".ad") -> true
search("b..") -> true
```

> [!question]- 힌트 1 — `.`을 만나면 백트래킹이다
> 일반 문자는 자식 하나로 확정 이동. `.`은 **현재 노드의 모든 자식으로 각각 내려가 시도**하고
> 하나라도 성공하면 `True`. 정확히 [[../day-27-backtracking/concept|백트래킹(Day 27)]] 구조다.

> [!question]- 힌트 2 — 재귀 함수의 인자를 정하라
> `dfs(node, i)` — "`node`에서 시작해 `word[i:]`를 매칭할 수 있는가".
> 종료 조건은 `i == len(word)`일 때 `node.is_end`를 반환. 이 두 줄이 골격 전부다.

> [!question]- 힌트 3 — 제약이 알려주는 것
> `.`이 **최대 2개**라는 제약이 왜 있는가? `.`이 k개면 최악 26^k 분기다.
> k=2면 676배로 감당 가능하지만 k=25면 불가능하다.
> **제약을 보고 지수 폭발이 허용되는지 판단하는 훈련**이 이 문제의 숨은 목표다.

> [!question]- 힌트 4 — 최적화 아이디어(선택)
> 전부 `.`인 질의(`"..."`)는 사실 "그 길이의 단어가 있는가"다.
> **길이별 단어 개수를 dict로 따로 들고 있으면 O(1)** 에 답할 수 있다.

**복잡도 목표:** `addWord` O(L), `search` 평균 O(L), `.`이 k개일 때 최악 O(26^k · L).

---

## 4. 🟡 Search Suggestions System

**출처:** [LeetCode #1268](https://leetcode.com/problems/search-suggestions-system/) (Medium)

### 문제
상품명 배열 `products`와 검색어 `searchWord`가 주어진다.
`searchWord`의 **각 글자를 입력할 때마다** 그 시점의 접두사로 시작하는 상품명 중
**사전 순으로 가장 앞선 최대 3개**를 추천한다. 전체 추천 목록을 반환한다.

### 제약
- `1 <= products.length <= 1000`
- `1 <= products[i].length <= 3000`
- `1 <= sum(products[i].length) <= 2 · 10⁴`
- `products[i]`는 서로 다르고 소문자 알파벳만
- `1 <= searchWord.length <= 1000`

### 예시
```
products = ["mobile","mouse","moneypot","monitor","mousepad"]
searchWord = "mouse"

출력:
[["mobile","moneypot","monitor"],
 ["mobile","moneypot","monitor"],
 ["mouse","mousepad"],
 ["mouse","mousepad"],
 ["mouse","mousepad"]]
```

> [!question]- 힌트 1 — 사전 순을 보장하는 두 가지 방법
> ① **삽입 전에 `products`를 정렬**하고, 각 노드에 "이 접두사로 시작하는 앞선 3개"를 미리 저장.
> ② 순회할 때 **`sorted(node.children)`** 으로 문자 순 방문.
> **파이썬 dict는 삽입 순서를 보존한다 — 사전 순이 아니다.** 이걸 놓치면 오답이다.

> [!question]- 힌트 2 — 노드에 답을 미리 캐싱하기
> 정렬된 순서로 삽입하면서, 지나가는 각 노드의 `suggestions` 리스트에
> **길이가 3보다 작을 때만** 현재 단어를 append 한다.
> 질의는 경로를 따라가 그 노드의 `suggestions`를 읽기만 하면 끝 → **O(L)**.

> [!question]- 힌트 3 — 트라이 없이도 풀린다
> `products`를 정렬해두고 **이분 탐색으로 접두사 범위(lower/upper bound)를 좁혀가는** 풀이,
> 또는 그냥 매 단계 필터링하는 풀이도 제약 안에서 통과한다.
> **트라이를 쓰는 이유를 한 문장으로 말할 수 있어야** 진짜로 이해한 것이다.

> [!question]- 힌트 4 — 경로가 끊긴 뒤
> 접두사가 어떤 상품과도 맞지 않게 되면, 그 이후의 모든 단계도 **빈 리스트**다.
> 매번 다시 탐색하지 말고 즉시 빈 리스트로 채우고 끝내라.

**복잡도 목표:** 구축 O(ΣL log N), 질의 전체 O(|searchWord|).

---

## 5. ⚫ 가사 검색

**출처:** [프로그래머스 #60060](https://school.programmers.co.kr/learn/courses/30/lessons/60060) (Level 4, 2020 KAKAO BLIND RECRUITMENT)

### 문제
친구가 좋아하는 노래 가사에 사용된 단어들이 `words`로 주어진다.
찾고자 하는 키워드 `queries`가 주어지면, 각 키워드에 **매치되는 단어가 몇 개인지** 배열로 반환한다.

키워드는 **와일드카드 `?`** 를 포함한다. `?`는 **글자 하나**를 의미하며 어떤 문자와도 매치된다.
예: `"fro??"` → `"frodo"`, `"front"`, `"frost"`에 매치. `"frame"`, `"frozen"`에는 매치되지 않는다.

### 제약
- `words`의 길이(가사 단어의 개수)는 2 이상 100,000 이하
- 각 단어의 길이는 1 이상 10,000 이하, 모든 단어 길이의 합은 2,000,000 이하
- 단어는 알파벳 소문자로만
- `queries`의 길이(검색 키워드 개수)는 2 이상 100,000 이하
- 각 키워드의 길이는 1 이상 10,000 이하, 모든 키워드 길이의 합은 2,000,000 이하
- **`?`는 각 키워드의 접두사나 접미사 중 하나로만 나타난다** (`"fro??"`, `"??ro"` 형태. `"fr?do"`는 없다)
- 키워드는 `?`로만 이루어질 수도 있다 (`"?????"`)

### 예시
```
words   = ["frodo","front","frost","frozen","frame","kakao"]
queries = ["fro??","????o","fr???","fro???","pro?"]
결과     = [3, 2, 4, 1, 0]
```

### 시그니처
```python
def solution(words, queries):
    ...
```

> [!question]- 힌트 1 — 왜 브루트포스가 안 되는가
> 단어 10만 개 × 키워드 10만 개 = **100억 번 비교**. 절대 불가능하다.
> 질의당 **O(키워드 길이)** 로 답해야 한다는 뜻이고, 그러면 **미리 세어두는** 수밖에 없다.

> [!question]- 힌트 2 — 가장 중요한 관찰
> `"fro??"` 는 **"길이가 5이고 `fro`로 시작하는 단어"** 와 **완전히 동치**다.
> 즉 **`?`를 처리할 필요가 아예 없다** — 길이 조건과 접두사 조건으로 분해되기 때문이다.
> **길이별로 트라이를 따로 만들면** `?`가 사라진다.

> [!question]- 힌트 3 — 접미사 `?`는 뒤집어라
> `"??ro"` 는 "길이 4이고 `ro`로 **끝나는** 단어"다.
> 단어를 **뒤집어 넣은 트라이**를 하나 더 만들면 `"or"`로 **시작하는** 단어를 세는 문제가 된다.
> **정방향 트라이 + 역방향 트라이, 각각 길이별로.** 이게 정석 풀이의 자료구조다.

> [!question]- 힌트 4 — 개수는 삽입 시점에 세라
> 각 노드에 `cnt`(이 노드를 지나간 단어 수)를 두고, 삽입하며 `cnt += 1`.
> 질의는 경로를 따라가 `cnt`를 **읽기만** 하면 O(L)에 끝난다.
> 질의 때 서브트리를 세면 다시 느려진다.

> [!question]- 힌트 5 — 전부 `?`인 경우
> `"?????"` 는 "길이 5인 단어 전부"다. 루트의 `cnt`(또는 길이별 총 개수)로 O(1)에 답한다.
> **이 케이스를 빼먹으면 부분 점수만 받는다.**

> [!question]- 힌트 6 — 대안: 정렬 + 이분 탐색
> 길이별로 단어를 정렬해두고, 접두사의 **lower/upper bound를 이분 탐색**으로 찾아 개수를 구할 수도 있다.
> 트라이보다 메모리가 훨씬 적게 든다(단어 길이 합이 200만이므로 트라이 메모리가 실제로 부담된다).
> **두 풀이를 다 구현해보는 것을 권한다.**

**복잡도 목표:** 구축 O(ΣL), 질의당 O(키워드 길이). 전체 O(ΣL + Σ|query|).

---

## 6. 🔴 Word Search II

**출처:** [LeetCode #212](https://leetcode.com/problems/word-search-ii/) (Hard)

### 문제
`m × n` 문자 격자 `board`와 문자열 배열 `words`가 주어진다.
**격자 위에서 만들 수 있는 `words`의 단어를 모두** 반환한다.

단어는 **인접한 칸**(가로·세로, 대각선 아님)의 문자를 순서대로 이어 만들 수 있어야 하며,
**한 칸을 한 단어 안에서 두 번 사용할 수 없다.**

### 제약
- `1 <= m, n <= 12`
- `board[i][j]`는 소문자 알파벳
- `1 <= words.length <= 3 · 10⁴`
- `1 <= words[i].length <= 10`
- `words[i]`는 소문자 알파벳, 서로 다르다

### 예시
```
board = [["o","a","a","n"],
         ["e","t","a","e"],
         ["i","h","k","r"],
         ["i","f","l","v"]]
words = ["oath","pea","eat","rain"]
출력   = ["oath","eat"]
```

> [!question]- 힌트 1 — 단어별로 DFS하면 왜 죽는가
> 단어 3만 개 × 격자 144칸 × 4^10 분기. 각 단어를 따로 찾으면 시간 초과다.
> **격자를 한 번만 훑으면서 모든 단어를 동시에 추적**해야 한다. 그 도구가 트라이다.

> [!question]- 힌트 2 — 트라이의 역할은 저장소가 아니라 필터다
> 격자를 DFS하면서 **트라이 노드를 함께 내려간다**.
> 현재 칸의 문자가 트라이 노드의 자식에 **없으면 그 방향으로는 어떤 단어도 만들 수 없다** → 즉시 중단.
> 이 가지치기가 이 문제의 본질이다. 공통 접두사를 가진 단어들이 탐색을 공유한다.

> [!question]- 힌트 3 — 방문 표시와 복원
> 한 단어 안에서 같은 칸을 재사용할 수 없으므로, 들어갈 때 `board[r][c] = '#'`로 바꾸고
> 나올 때 **원래 문자로 복원**한다. 별도 `visited` 배열 없이 격자를 직접 쓰는 관용구다.
> 복원을 빼먹으면 격자가 오염되어 이후 탐색이 전부 틀린다.

> [!question]- 힌트 4 — 중복 방지
> 같은 단어가 격자에서 여러 경로로 만들어질 수 있다.
> 찾은 순간 노드에서 **단어를 꺼내버리면**(`node.pop(WORD_KEY)`) 중복이 자동으로 막힌다.
> `set`을 쓰는 것보다 깔끔하고, 다음 힌트의 pruning과 자연스럽게 이어진다.

> [!question]- 힌트 5 — pruning: 다 쓴 가지를 잘라내라
> 어떤 노드의 자식이 모두 소진되고 단어도 없어지면 **부모에서 그 노드를 제거**한다.
> 탐색이 진행될수록 트라이가 작아져 체감 속도가 크게 뛴다.
> 재귀에서 돌아온 직후 `if not node: parent.pop(ch)` 한 줄이다.

> [!question]- 힌트 6 — 추가 최적화(선택)
> 격자에 없는 문자로 시작하는 단어는 애초에 트라이에 넣지 않는다.
> 격자의 문자 빈도를 세어, **단어가 요구하는 문자 수가 격자에 있는 수보다 많으면** 제외한다.
> 어떤 단어를 **뒤집어 넣는 것이 유리한 경우**도 있다(첫 글자가 격자에 흔하고 마지막 글자가 희귀할 때).

**복잡도 목표:** O(m · n · 4 · 3^(L-1)) — 트라이 가지치기로 실전 성능은 훨씬 좋다.

---

## 스스로 점검 (Self-Check)

풀이 후 다음 질문에 막힘 없이 답할 수 있는지 확인하라.

1. `search("app")`이 `false`인데 `startsWith("app")`은 `true`인 상황을 예로 설명할 수 있는가?
2. 트라이와 해시(`set`)의 복잡도가 둘 다 O(L)인데, **트라이를 쓰는 이유**를 한 문장으로 말할 수 있는가?
3. 트라이 DFS가 사전 순 결과를 주려면 **무엇을 반드시 해야** 하는가? (파이썬 dict의 순회 순서는?)
4. `"car"`를 삭제할 때 `"card"`가 남아 있으면 어떤 노드를 지워야 하고 어떤 노드는 남겨야 하는가?
5. `"fro??"`를 **`?` 처리 없이** 답하는 방법은? `"??ro"`는?
6. `.`이 k개인 와일드카드 검색의 최악 복잡도는? 문제 제약이 왜 `.`을 2개로 제한하는가?
7. 비트 트라이에서 XOR을 최대화할 때 **왜 상위 비트부터** 반대쪽으로 가는가?
8. #212에서 트라이가 없다면 무엇이 문제인가? 트라이가 정확히 어떤 비용을 줄여주는가?
9. 트라이의 메모리를 줄이는 세 가지 방법을 말할 수 있는가?
10. 접두사(prefix)·접미사(suffix)·부분 문자열(substring) 중 **트라이가 직접 다루는 것**은? 나머지는 어떻게 하는가?

---

## 관련 문서

- 개념: [[concept|Day 39 — 트라이 (Trie / Prefix Tree)]]
- 예제 코드: [examples.py](examples.py)
- 해설 코드: [solutions.py](solutions.py)
- 이전: [[../day-38-topological-sort/concept|Day 38 — 위상 정렬 (Topological Sort)]]
- 지도: [[Phase-4 MOC]] · [[00 Algorithm MOC]]
