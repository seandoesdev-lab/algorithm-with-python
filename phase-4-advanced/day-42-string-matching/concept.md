---
day: 42
phase: 4-advanced
title: 문자열 매칭 (KMP·라빈-카프)
category: [문자열 매칭, String Matching, 패턴 탐색, Pattern Searching, KMP, Knuth-Morris-Pratt, 실패 함수, Failure Function, 접두사 함수, Prefix Function, LPS, 라빈-카프, Rabin-Karp, 롤링 해시, Rolling Hash, 다항식 해시, Polynomial Hashing, Z 알고리즘, Z Algorithm, 주기성, Periodicity]
difficulty: 심화
status: done
prev: "[[day-41-bitmask/concept|Day 41 — 비트마스킹 (Bitmasking & Bitmask DP)]]"
next: "[[day-43-lca/concept|Day 43 — 최소 공통 조상 (LCA)]]"
related:
  - "[[day-41-bitmask/concept|Day 41 — 비트마스킹 (Bitmasking)]]"
  - "[[day-04-strings/concept|Day 04 — 문자열 다루기]]"
  - "[[day-39-trie/concept|Day 39 — 트라이 (Trie / Prefix Tree)]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]]"
  - "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합 (Prefix Sum)]]"
  - "[[day-31-dp/concept|Day 31 — 동적 계획법 입문]]"
  - "[[day-24-brute-force/concept|Day 24 — 완전 탐색 (Brute Force)]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
sources:
  - https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
  - https://leetcode.com/problems/repeated-substring-pattern/
  - https://leetcode.com/problems/repeated-dna-sequences/
  - https://leetcode.com/problems/shortest-palindrome/
  - https://leetcode.com/problems/longest-duplicate-substring/
  - https://school.programmers.co.kr/learn/courses/30/lessons/17683
  - https://leetcode.com/discuss/post/2984946/KMP-and-Z-algorithm-Notes-(In-progress)/
  - https://leetcode.com/discuss/study-guide/2099715/rolling-hash-explanation/
  - https://leetcode.com/tag/rolling-hash/
tags: [phase/4, topic/string-matching, topic/kmp, topic/rabin-karp, topic/rolling-hash, topic/string, topic/hashing, topic/z-algorithm, topic/prefix-function]
---

# Day 42 — 문자열 매칭 (KMP·라빈-카프)

> [!abstract] 한눈 요약 (TL;DR)
> **문자열 매칭(string matching)** 은 길이 `N`의 텍스트에서 길이 `M`의 패턴이 어디에 등장하는지 찾는 문제다. 가장 순진한 방법은 **모든 시작 위치에서 한 글자씩 비교**하는 `O(N·M)`이고, 이것이 `"aaaa...a"`에서 `"aaa...ab"`를 찾는 최악 케이스에서 그대로 터진다. 오늘 배우는 두 알고리즘은 **정확히 반대 방향의 아이디어로 이 `M`을 없앤다.** **KMP(Knuth-Morris-Pratt)** 는 **"패턴 자기 자신의 반복 구조를 미리 계산해 두면, 실패했을 때 텍스트 포인터를 되돌릴 필요가 없다"** 는 통찰이다. 그 전처리 결과가 **실패 함수(failure function) = 접두사 함수(prefix function) = LPS 배열**이며, `pi[i]` = `pattern[0..i]`에서 **접두사이면서 동시에 접미사인 가장 긴 진부분 문자열의 길이**다. 전처리 `O(M)` + 탐색 `O(N)` = **`O(N+M)` 결정론적 보장**. **라빈-카프(Rabin-Karp)** 는 **"문자열 비교를 숫자 비교로 바꾼다"** 는 통찰이다. 길이 `M`짜리 구간을 **다항식 롤링 해시(polynomial rolling hash)** 로 정수 하나로 만들고, 한 칸 밀 때 **앞 글자를 빼고 뒤 글자를 더하는 O(1) 갱신**으로 모든 구간 해시를 얻는다 — [[day-20-sliding-window/concept|슬라이딩 윈도우(Day 20)]]의 문자열판이다. 평균 `O(N+M)`이지만 **해시 충돌 시 최악 `O(N·M)`** 이라 확률적이며, 대신 **패턴이 여러 개거나 "임의 구간 두 개가 같은가"를 O(1)에 묻고 싶을 때 KMP가 못 하는 일을 한다.** 실전 판단은 이렇다: **단일 패턴 1회 탐색이면 파이썬은 `haystack.find(needle)`이 정답**(CPython 내부가 C로 짜인 Two-Way 알고리즘이라 손으로 쓴 KMP보다 빠르다). **KMP를 직접 쓰는 진짜 이유는 탐색이 아니라 `pi` 배열 자체** 다 — 문자열의 **주기(period) = `n - pi[n-1]`** 라는 성질 하나로 [반복 부분 문자열(#459)](https://leetcode.com/problems/repeated-substring-pattern/)과 [최단 팰린드롬(#214)](https://leetcode.com/problems/shortest-palindrome/)이 세 줄에 풀린다. **롤링 해시를 쓰는 진짜 이유는 "부분 문자열 비교를 O(1)로 만들어 [[day-18-binary-search/concept|이분 탐색(Day 18)]]과 결합"** 하는 것이다([가장 긴 중복 부분 문자열 #1044](https://leetcode.com/problems/longest-duplicate-substring/)). 핵심 한 줄: **"KMP는 패턴의 자기 유사성을 미리 계산하고, 라빈-카프는 문자열을 숫자로 바꾼다."**

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **문제 정의.** 텍스트 `T`(길이 `N`)와 패턴 `P`(길이 `M`)가 주어질 때, `T[i..i+M-1] == P`인 모든 `i`를 찾아라.
>
> **먼저 나이브(naive)가 왜 느린지 정확히 보자.**
> ```
>   T = "aaaaaaaaab"   (N = 10)
>   P = "aaab"         (M = 4)
>
>   i=0:  aaaa vs aaab  ->  3글자 맞고 4번째에서 실패
>   i=1:  aaaa vs aaab  ->  3글자 맞고 4번째에서 실패
>   i=2:  aaaa vs aaab  ->  3글자 맞고 4번째에서 실패
>   ...                     매번 M 번 비교하고 매번 실패
>
>   총 비교 횟수 = O(N·M).  N=M=10^5 이면 10^10 -> 절대 불가능.
> ```
> **핵심 낭비는 "이미 확인한 정보를 버리는 것"이다.** `i=0`에서 우리는 `T[0..2] == "aaa"`라는 **사실을 알아냈는데**, `i=1`로 옮기면서 그 지식을 통째로 버리고 처음부터 다시 센다. 두 알고리즘은 이 낭비를 서로 다른 방법으로 없앤다.
>
> ---
>
> ### KMP의 직관 — "패턴은 자기 자신을 알고 있다"
>
> **비유: 자물쇠 다이얼 맞추기.** 4자리 자물쇠 `1234`를 맞추려는데 `1231`까지 돌렸다가 마지막에서 틀렸다고 하자. 순진한 사람은 다이얼을 **전부 처음으로 되돌린다**. 그러나 영리한 사람은 **"방금 입력한 마지막 글자 `1`이 정답의 첫 글자와 같다"** 는 것을 알아채고, **그 `1`을 새 시도의 첫 글자로 재활용**한다. 되돌리는 대신 **"지금까지 맞춘 것 중 살릴 수 있는 부분"** 만 남기는 것이다.
>
> "살릴 수 있는 부분"이 정확히 무엇인가? **지금까지 맞춘 부분 `P[0..j-1]`의 접미사(suffix)이면서 동시에 `P`의 접두사(prefix)인 것 중 가장 긴 것**이다. 이것을 미리 표로 만들어 둔 것이 **실패 함수**다.
>
> ```
>   P = "ababaca"
>
>   pi[i] = P[0..i] 에서 "접두사이면서 접미사인 가장 긴 진부분문자열"의 길이
>           (진부분문자열 = 자기 자신은 제외)
>
>   i :  0   1   2   3   4   5   6
>   P :  a   b   a   b   a   c   a
>   pi:  0   0   1   2   3   0   1
>
>   pi[3] = 2 인 이유:  "abab" 의 접두사 = a, ab, aba
>                        "abab" 의 접미사 = b, ab, bab
>                        공통 중 가장 긴 것 = "ab"  ->  길이 2
>
>   pi[4] = 3 인 이유:  "ababa" -> "aba" 가 앞에도 뒤에도 있다  ->  3
>   pi[5] = 0 인 이유:  "ababac" -> 'c' 로 끝나는데 P 는 'a' 로 시작  ->  0
> ```
>
> **이 표가 탐색에서 어떻게 쓰이는가.** 텍스트를 훑다가 `P[0..j-1]`까지 맞추고 `P[j]`에서 실패했다면, **텍스트 포인터는 그대로 두고 패턴 포인터만 `j = pi[j-1]`로 점프**한다. `pi[j-1]`은 "이미 맞춘 부분의 접미사 중 패턴의 접두사인 최장 길이"이므로, **그만큼은 이미 맞춰져 있다고 확신**할 수 있다.
>
> ```
>   T = "a b a b a b a c a"
>   P = "a b a b a c a"
>
>   i=0..4 까지 "ababa" 5글자가 맞았다.  (j=5)
>   i=5:  T[5]='b'  vs  P[5]='c'   ->  실패!
>
>   나이브라면:  i 를 1 로 되돌리고 j=0 부터 다시  ->  이미 본 글자를 또 본다
>   KMP 라면  :  j = pi[4] = 3 으로 점프.  i 는 5 그대로!
>                "이미 맞춘 ababa 의 뒤쪽 aba 는 P 의 앞쪽 aba 와 같다"
>                는 사실을 pi 가 보장하므로 3글자는 공짜로 맞춘 셈
>   i=5:  T[5]='b'  vs  P[3]='b'   ->  성공, 계속 진행
> ```
>
> **결정적 성질: 텍스트 포인터 `i`는 절대 뒤로 가지 않는다.** `i`는 `0`에서 `N`까지 단조 증가하고, `j`는 늘어날 때 최대 `N`번, 줄어들 때 늘어난 만큼만 줄어든다(**amortized analysis**). 그래서 **총 `O(N)`** 이다. 이것이 KMP가 스트리밍 입력(파일·네트워크 스트림)에도 쓸 수 있는 이유다 — **텍스트를 저장할 필요조차 없다.**
>
> ---
>
> ### 라빈-카프의 직관 — "문자열을 숫자로 보면 비교가 한 번이다"
>
> **비유: 지문 대조.** 100명의 사람 중 특정인을 찾는데 얼굴을 하나하나 뜯어보며 대조하면 오래 걸린다. 대신 **각자에게서 "지문(fingerprint)"이라는 숫자 하나를 뽑아** 두면, 대조는 **숫자 하나 비교**로 끝난다. 지문이 다르면 확실히 다른 사람이고, **지문이 같으면 "아마도" 같은 사람**이다(우연히 같을 확률은 있다 — 이것이 **해시 충돌(collision)**).
>
> **다항식 해시(polynomial hash).** 문자열을 **B진법 수**로 읽는다.
> $$ H(s) = s_0 B^{m-1} + s_1 B^{m-2} + \cdots + s_{m-1} B^0 \pmod{p} $$
> ```
>   "abc" 를 B=131 로 읽으면
>     H = 'a'·131^2 + 'b'·131^1 + 'c'·131^0   (mod p)
>
>   진법 표기와 똑같다. 10진수 "523" = 5·10^2 + 2·10^1 + 3·10^0 인 것처럼,
>   문자열도 "문자를 숫자로 본 B진수" 로 읽는 것뿐이다.
> ```
>
> **롤링(rolling)이 핵심이다.** 윈도우를 한 칸 밀 때 해시를 처음부터 다시 계산하면 `O(M)`이라 의미가 없다. 그런데 **맨 앞 글자의 기여를 빼고, 전체를 `B`배 하고, 새 글자를 더하면** `O(1)`이다.
> ```
>   윈도우:  "abc"  ->  "bcd"   (a 가 빠지고 d 가 들어온다)
>
>   H("abc") = a·B^2 + b·B + c
>
>   1) 맨 앞 a 의 기여 제거 :  H - a·B^2  =  b·B + c
>   2) 한 자리 올림         :  (b·B + c)·B  =  b·B^2 + c·B
>   3) 새 글자 d 추가       :  b·B^2 + c·B + d  =  H("bcd")   <- 완성!
>
>   H_next = (H - s[i]·B^(m-1)) · B + s[i+m]      (mod p)
>
>   곱셈 2번 + 덧셈 2번 = O(1).  Day 20 슬라이딩 윈도우와 완전히 같은 사고방식이다.
>   (누적 합에서 "앞을 빼고 뒤를 더하는" 것의 문자열 버전 — Day 14 와도 이어진다)
> ```
>
> **확률적 알고리즘이라는 점을 정확히 이해하라.** 해시가 다르면 **문자열은 확실히 다르다**(단방향 보장). 해시가 같으면 **같을 "가능성이 매우 높다"** 뿐이다. 그래서 정석 구현은 **해시가 같을 때 실제 문자열을 한 번 비교**(verify)한다. 충돌이 드물면 이 검증은 거의 안 일어나므로 평균 `O(N+M)`이고, 악의적인 입력으로 충돌을 유도당하면 최악 `O(N·M)`이 된다.
>
> ---
>
> ### 둘을 언제 쓰는가 — 역할 분담표
>
> | 상황 | 도구 | 이유 |
> |---|---|---|
> | 단일 패턴, 파이썬, 그냥 찾기만 | **`T.find(P)` / `in`** ✅ | C 구현(Two-Way)이 손코딩보다 빠르다 |
> | 최악 케이스 `O(N+M)` 보장이 필요 | **KMP** | 결정론적. 충돌 개념 자체가 없다 |
> | 문자열의 **주기·반복 구조**를 알고 싶다 | **KMP의 `pi` 배열** ✅ | `n - pi[n-1]` = 최소 주기 |
> | 접두사=접미사 관계를 이용 (#214) | **KMP의 `pi` 배열** ✅ | `s + '#' + rev(s)` 트릭 |
> | 스트리밍(텍스트를 저장 못 함) | **KMP** | `i`가 되돌아가지 않는다 |
> | 패턴이 **여러 개** 동시에 | **라빈-카프** ✅ | 패턴 해시를 `set`에 넣고 한 번만 훑는다 |
> | **임의 두 구간이 같은가**를 여러 번 질의 | **롤링 해시 전처리** ✅ | 전처리 `O(N)` 후 질의 `O(1)` |
> | 길이에 대한 이분 탐색과 결합 (#1044) | **롤링 해시** ✅ | KMP로는 불가능한 조합 |
> | 패턴이 아주 많고 접두사를 공유 | [[day-39-trie/concept\|트라이(Day 39)]] / 아호-코라식 | 트라이 + KMP = Aho-Corasick |
> | 2차원 격자 패턴 매칭 | 롤링 해시 | 행 해시 → 열 해시 2단계 |
>
> **한 문장 요약.** **KMP는 "패턴 하나를 확실하게", 라빈-카프는 "여러 개를/유연하게".** 그리고 파이썬 코딩테스트에서 **탐색 자체는 `str.find`에 맡기고, 두 알고리즘은 "그것으로 못 푸는 문제"에 꺼내 쓰는 것**이 실전 감각이다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 실패 함수(prefix function) 만들기 — KMP의 심장.**
>
> `pi[i]` = `P[0..i]`의 **진접두사이면서 진접미사인 최장 문자열의 길이**.
>
> **놀라운 점: 이 표를 만드는 과정 자체가 "패턴에서 패턴을 찾는 KMP"다.** 즉 자기 자신에게 KMP를 돌린다.
> ```
>   pi = [0] * m
>   k = 0                                  # 지금까지 맞춘 접두사 길이
>   for i in range(1, m):
>       while k > 0 and P[i] != P[k]:
>           k = pi[k - 1]                  # 실패 -> 더 짧은 접두사로 후퇴
>       if P[i] == P[k]:
>           k += 1                         # 한 글자 더 맞았다
>       pi[i] = k
> ```
> ```
>   P = "aabaaab" 을 손으로 따라가 보자
>
>   i=1 'a': k=0, P[1]='a' == P[0]='a'  ->  k=1,  pi[1]=1
>   i=2 'b': k=1, P[2]='b' != P[1]='a'  ->  k=pi[0]=0
>            k=0, P[2]='b' != P[0]='a'  ->  while 종료(k=0)
>            일치 없음                   ->  pi[2]=0
>   i=3 'a': k=0, P[3]='a' == P[0]      ->  k=1,  pi[3]=1
>   i=4 'a': k=1, P[4]='a' == P[1]='a'  ->  k=2,  pi[4]=2
>   i=5 'a': k=2, P[5]='a' != P[2]='b'  ->  k=pi[1]=1
>            k=1, P[5]='a' == P[1]='a'  ->  k=2,  pi[5]=2
>   i=6 'b': k=2, P[6]='b' == P[2]='b'  ->  k=3,  pi[6]=3
>
>   결과:  P  :  a  a  b  a  a  a  b
>          pi :  0  1  0  1  2  2  3
>
>   pi[6]=3 -> "aabaaab" 의 앞 3글자 "aab" 와 뒤 3글자 "aab" 가 같다
> ```
> ```
>   왜 실패하면 k = pi[k-1] 인가 (KMP 전체에서 가장 중요한 한 줄)
>
>     지금 "길이 k 짜리 접두사" 까지 맞춘 상태에서 다음 글자가 틀렸다.
>     그러면 "길이 k 보다 짧으면서 여전히 유효한 접두사" 로 물러나야 한다.
>     그 후보들이 정확히:  pi[k-1], pi[pi[k-1]-1], ... 의 연쇄다.
>     (이 연쇄를 "실패 링크(failure link)" 라 부르고, 모든 경계(border)를 훑는다)
>
>     시간 분석: k 는 for 문에서 최대 1씩 증가하므로 총 증가량 <= m 이고,
>               while 은 k 를 줄이기만 하므로 총 감소량도 <= m.
>               따라서 while 전체 반복 합이 O(m) -> 전처리 O(m).  (amortized)
> ```
>
> **(B) KMP 탐색 — 텍스트 포인터는 절대 되돌아가지 않는다.**
> ```
>   j = 0                                  # 패턴에서 맞춘 길이
>   for i in range(n):                     # i 는 단조 증가! 되돌림 없음
>       while j > 0 and T[i] != P[j]:
>           j = pi[j - 1]                  # 패턴만 후퇴
>       if T[i] == P[j]:
>           j += 1
>       if j == m:                         # 전부 맞았다
>           found.append(i - m + 1)        # 시작 위치
>           j = pi[j - 1]                  # 겹치는 다음 매치도 찾기 위해 후퇴
>
>   시간: 전처리 O(m) + 탐색 O(n)  =  O(n + m).  최악에도 보장된다.
>   공간: O(m)  (pi 배열만)
> ```
> ```
>   매치 후 j = pi[m-1] 로 후퇴하는 이유 = "겹치는 매치(overlapping)" 를 놓치지 않기 위해
>
>     T = "aaaa",  P = "aa"
>     정답은 0, 1, 2 세 곳이다 (서로 겹친다).
>     j = 0 으로 리셋하면 0, 2 만 찾는다.  j = pi[1] = 1 로 후퇴해야 셋 다 찾는다.
>
>     "겹치지 않는 매치만" 원한다면 j = 0 으로 리셋한다. 문제 조건을 꼭 확인하라.
> ```
>
> **(C) `pi` 배열의 진짜 보물 — 문자열의 주기(period).**
> ```
>   정리:  길이 n 인 문자열 s 의 최소 주기 = n - pi[n-1]
>
>     s = "abcabcabc"  (n=9)
>     pi[8] = 6  ("abcabc" 가 접두사이자 접미사)
>     최소 주기 = 9 - 6 = 3  ->  "abc" 가 3번 반복
>
>     s = "ababab"     (n=6),  pi[5]=4,  주기 = 2  ->  "ab" x 3
>     s = "abcabca"    (n=7),  pi[6]=4,  주기 = 3  ->  딱 안 떨어진다 (7 % 3 != 0)
>     s = "abcd"       (n=4),  pi[3]=0,  주기 = 4  ->  반복 없음
>
>   "정확히 k(>=2)번 반복된 문자열인가?" 판정:
>       p = n - pi[n-1]
>       반복이다  <=>  pi[n-1] > 0  이고  n % p == 0
>
>   왜 n % p == 0 이어야 하는가:
>     주기가 p 라도 딱 떨어지지 않으면 (예: "abcabca") 마지막 조각이 잘린다.
>     "타일을 정확히 채우려면 타일 길이가 전체 길이를 나눠야 한다"
> ```
> **이 세 줄이 [Repeated Substring Pattern #459](https://leetcode.com/problems/repeated-substring-pattern/)의 정답 전부다.**
>
> **(D) `pi` 활용 2 — 최단 팰린드롬(#214)의 `#` 트릭.**
> ```
>   문제: s 앞에만 문자를 붙여 팰린드롬을 만들 때 가장 짧은 결과는?
>
>   관찰: 앞에 k 글자를 붙인다는 것은
>         "s 의 앞부분 중 가장 긴 팰린드롬 접두사" 를 찾는 것과 같다.
>         그 팰린드롬 접두사 뒤에 남는 부분을 뒤집어 앞에 붙이면 끝.
>
>   트릭:  combined = s + '#' + reverse(s)
>          pi[-1] = "s 의 접두사" 이면서 "reverse(s) 의 접미사" 인 최장 길이
>                 = "s 의 접두사" 이면서 "s 를 뒤집은 것의 접미사"
>                 = s 의 가장 긴 팰린드롬 접두사의 길이!
>
>   예)  s = "aacecaaa"
>        combined = "aacecaaa" + "#" + "aaacecaa"
>        pi[-1] = 7  ->  "aacecaa" 가 가장 긴 팰린드롬 접두사
>        남는 부분 s[7:] = "a"  ->  뒤집어서 앞에 붙인다
>        답: "a" + "aacecaaa" = "aaacecaaa"
>
>   '#' 는 왜 넣는가 (필수!):
>     구분자가 없으면 매치가 두 문자열의 경계를 넘어가서 pi 가 n 을 넘을 수 있다.
>     예) s = "aaa" 면 "aaaaaa" 가 되어 pi[-1] = 5 > 3 (말이 안 된다).
>     '#' 는 s 에 절대 안 나오는 문자여야 한다. 문제 제약(소문자만 등)을 확인하라.
> ```
>
> **(E) 라빈-카프 구현 — 세 가지 결정 사항.**
> ```
>   1) 밑(base) B :  문자 종류 수보다 커야 한다. 보통 131, 137, 31, 256.
>                    (충돌 공격 방지를 원하면 실행마다 random 하게 고른다)
>   2) 모듈러 p   :  큰 소수. 10^9+7, 998244353, 또는 2^61-1(메르센 소수).
>                    작으면 충돌이 잦고, 파이썬은 큰 수도 잘 다루니 크게 잡아라.
>   3) 검증 여부  :  해시가 같을 때 실제 문자열을 비교할 것인가?
>                    -> 정확성이 필요하면 반드시 한다 (평균 비용은 거의 0)
> ```
> ```
>   def rabin_karp(text, pat, B=131, MOD=(1<<61)-1):
>       n, m = len(text), len(pat)
>       if m > n: return []
>       power = pow(B, m - 1, MOD)                 # B^(m-1) 미리 계산
>
>       hp = 0                                     # 패턴 해시
>       for c in pat:
>           hp = (hp * B + ord(c)) % MOD
>
>       ht = 0                                     # 첫 윈도우 해시
>       for i in range(m):
>           ht = (ht * B + ord(text[i])) % MOD
>
>       res = []
>       for i in range(n - m + 1):
>           if ht == hp and text[i:i+m] == pat:    # 해시 일치 -> 실제 검증
>               res.append(i)
>           if i + m < n:                          # 한 칸 롤링
>               ht = (ht - ord(text[i]) * power) % MOD
>               ht = (ht * B + ord(text[i + m])) % MOD
>       return res
> ```
> ```
>   파이썬 모듈러 주의:  (ht - ord(...)*power) 가 음수가 될 수 있다.
>                       파이썬의 % 는 항상 비음수를 반환하므로 안전하다.
>                       (C/Java 는 음수가 나온다! 거기서는 += MOD 가 필요)
> ```
>
> **(F) 롤링 해시의 진짜 무기 — 접두사 해시로 임의 구간을 O(1)에.**
>
> 라빈-카프를 "패턴 찾기"로만 쓰면 절반만 쓰는 것이다. **접두사 해시 배열**을 만들어 두면 **어떤 구간 `s[l..r]`의 해시든 `O(1)`** 에 꺼낼 수 있다 — [[day-14-prefix-sum/concept|누적 합(Day 14)]]과 정확히 같은 구조다.
> ```
>   H[i] = s[0..i-1] 의 해시  (H[0] = 0)
>   H[i+1] = H[i] * B + s[i]
>
>   구간 [l, r) 의 해시 = H[r] - H[l] * B^(r-l)          (mod p)
>
>   +-- 누적 합과의 대응 ---------------------------+
>   |  누적 합:  sum[l..r) = S[r] - S[l]            |
>   |  롤링해시: hash[l..r) = H[r] - H[l]·B^(r-l)   |
>   |  차이는 "자릿수를 맞춰 주는 B^(r-l)" 뿐이다   |
>   +-----------------------------------------------+
>
>   전처리 O(n),  구간 질의 O(1)  ->  "두 구간이 같은가?" 를 O(1) 에 답한다!
>   이것이 KMP 로는 절대 못 하는 일이고, #1044 의 열쇠다.
> ```
>
> **(G) #1044 — 이분 탐색 + 롤링 해시의 결합.**
> ```
>   문제: 두 번 이상 등장하는 가장 긴 부분 문자열을 찾아라. (n <= 3·10^4)
>
>   관찰 1 (단조성):  길이 L 짜리 중복이 존재하면, 길이 L-1 짜리도 반드시 존재한다
>                    (그 부분 문자열의 앞 L-1 글자를 보면 된다).
>                    -> "중복이 존재하는가" 는 L 에 대해 단조 감소하는 술어
>                    -> Day 18 의 "결정 문제로 바꿔 이분 탐색" 이 그대로 적용된다
>
>   관찰 2 (판정을 빠르게):  "길이 L 짜리 중복이 있는가?" 를 O(n) 에 답해야 한다
>                    -> 길이 L 인 모든 윈도우의 롤링 해시를 dict 에 넣으면서
>                       이미 본 해시가 나오면 중복 발견
>
>   전체:  O(n log n).   n=3·10^4 이면 log n ~ 15 -> 45만 연산. 여유롭다.
>
>   함정: LeetCode #1044 는 단일 모듈러 해시를 저격하는 테스트가 있다.
>         -> 이중 해시(서로 다른 두 (B, MOD) 쌍을 튜플로) 또는
>            2^61-1 모듈러 + 랜덤 밑 을 써야 안전하다.
> ```
>
> **(H) 보너스 — Z 알고리즘(Z Algorithm).**
> ```
>   Z[i] = s 와 s[i:] 의 최장 공통 접두사 길이   (Z[0] 은 보통 n 또는 0 으로 정의)
>
>     s   = a  a  b  x  a  a  y  a  a
>     Z   = -  1  0  0  2  1  0  2  1
>           (Z[4]=2: "aa" 가 s 의 앞 2글자와 같다)
>
>   패턴 매칭:  Z( P + '#' + T ) 를 계산해 Z[i] == m 인 곳을 찾는다.
>   KMP 와 복잡도가 같고(O(n+m)) 코드가 조금 더 짧다는 사람도 많다.
>   "[l, r] 박스" 를 유지하며 이미 계산한 Z 값을 재활용하는 것이 핵심.
>
>   KMP 의 pi 와 Z 는 서로 O(n) 에 변환 가능하다. 둘 중 손에 익은 하나면 충분하다.
> ```
>
> **(I) 파이썬 현실 — 손코딩 KMP가 `str.find`보다 느리다.**
> ```
>   CPython 의 str.find / in / index 는 C 로 구현되어 있고,
>   짧은 패턴에는 Bloom 필터를 얹은 Boyer-Moore-Horspool 변형을,
>   긴 패턴에는 Two-Way 알고리즘(Crochemore-Perrin)을 쓴다.
>   Two-Way 는 KMP 와 같은 O(n+m) 최악 보장을 가진다. (CPython 3.10+)
>
>   -> "단순히 찾기만" 하면 T.find(P) 가 파이썬 KMP 보다 보통 10~100배 빠르다.
>      파이썬 KMP 는 루프가 인터프리터에서 돌기 때문이다.
>
>   그렇다면 KMP 를 왜 배우는가?
>     1) pi 배열 자체가 답인 문제들 (#459 주기, #214 팰린드롬 접두사)
>     2) 최악 복잡도를 "설명" 해야 하는 면접
>     3) 아호-코라식·접미사 자동자 같은 상위 개념의 기반
>     4) find 로 표현할 수 없는 변형 (온라인/스트리밍, 겹치는 매치 세기 등)
> ```
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. **N** = 텍스트 길이, **M** = 패턴 길이, **k** = 패턴 개수.
>
> | 알고리즘 / 연산 | 시간복잡도 | 공간 | 설명 |
> |---|---|---|---|
> | 나이브 탐색 | **O(N·M)** | O(1) | 모든 시작 위치 × 전체 비교 |
> | KMP 전처리(`pi` 배열) | **O(M)** | O(M) | amortized. `k`의 총 증감량이 `O(M)` |
> | KMP 탐색 | **O(N)** | O(1) 추가 | `i`가 되돌아가지 않는다 |
> | **KMP 전체** | **O(N + M)** ✅ | O(M) | **최악에도 보장** |
> | 라빈-카프 전처리 | O(M) | O(1) | 패턴 해시 + `B^(M-1)` |
> | 라빈-카프 탐색(평균) | **O(N + M)** | O(1) | 충돌이 드물다는 가정 |
> | 라빈-카프 탐색(최악) | **O(N·M)** ⚠️ | O(1) | 모든 윈도우가 충돌할 때 |
> | 라빈-카프, 패턴 `k`개 | **O(N + ΣM)** ✅ | O(k) | 패턴 해시를 `set`에 — **KMP는 `O(k·N)`** |
> | 접두사 해시 전처리 | **O(N)** | O(N) | `H[]`와 `B^i` 배열 |
> | 임의 구간 해시 질의 | **O(1)** ✅ | O(1) | 누적 합과 동일 구조 |
> | Z 알고리즘 | O(N + M) | O(N + M) | KMP와 동급 |
> | #1044 (이분 + 롤링 해시) | **O(N log N)** | O(N) | 판정 `O(N)` × `log N`회 |
> | 아호-코라식(참고) | O(N + ΣM + 매치수) | O(ΣM·Σ) | 트라이 + 실패 링크 |
> | 접미사 배열(참고) | O(N log N) | O(N) | 정렬 기반. 더 강력하지만 무겁다 |
> | **CPython `str.find`** | O(N+M) 최악 ✅ | O(1) | Two-Way(3.10+). **실측 최속** |
>
> > **"손코딩 KMP vs `str.find`"의 실측 감각 — 이것이 파이썬 실전의 핵심이다.**
> >
> > | N (텍스트 길이) | 파이썬 KMP | `T.find(P)` | 비고 |
> > |---|---|---|---|
> > | 10³ | ~0.5 ms | ~0.001 ms | 둘 다 무의미하게 빠름 |
> > | 10⁵ | ~50 ms | ~0.05 ms | **약 1000배 차이** |
> > | 10⁶ | ~500 ms | ~0.5 ms | KMP는 TLE 위험 |
> >
> > 복잡도는 **둘 다 `O(N+M)`으로 같다.** 차이는 **순수하게 상수**다 — 파이썬 바이트코드 루프 vs C 루프. **"복잡도가 같으면 언어 상수가 승부를 가른다"** 는 교훈이 문자열에서 가장 극적으로 드러난다. [[day-41-bitmask/concept|Day 41]]의 "지수끼리는 가지치기가 승부를 가른다"와 같은 종류의 실전 감각이다. (표의 수치는 대략적인 자릿수 감각이며, 정확한 값은 `examples.py`의 실측 섹션에서 직접 확인하라.)
> >
> > **그러나 `find`를 반복문 안에서 부르면 이야기가 달라진다.** `for i in range(n): T[i:].find(P)`처럼 쓰면 **슬라이싱이 `O(N)` 복사**를 유발해 전체가 `O(N²)`가 된다. `T.find(P, start)`의 **`start` 인자**를 써서 슬라이싱을 피하라 — 파이썬 문자열 문제의 최다 TLE 원인 중 하나다([[day-04-strings/concept|Day 04]]).
>
> > **`O(N·M)`이 실제로 얼마나 위험한가.**
> >
> > | N = M | N·M | 파이썬 판정 |
> > |---|---|---|
> > | 10³ | 10⁶ | 여유 |
> > | 10⁴ | 10⁸ | **위험** (수십 초) |
> > | 10⁵ | 10¹⁰ | ❌ 불가능 |
> > | 3×10⁴ (#1044) | 9×10⁸ | ❌ → `O(N log N)` 필요 |
> >
> > **제약에 `N ≤ 10⁵`이고 "부분 문자열"이 나오면, `O(N·M)` 나이브는 이미 오답 방향**이다. `O(N+M)`(KMP·해시) 또는 `O(N log N)`(이분+해시)을 목표로 잡아라.
>
> > **해시 충돌 확률 — "생일 문제"로 계산하라.** 서로 다른 부분 문자열 `q`개의 해시를 모듈러 `p`로 만들 때, 충돌이 하나라도 생길 확률은 대략 $q^2 / (2p)$다.
> >
> > | 상황 | q (비교 대상 수) | p = 10⁹+7 | p = 2⁶¹-1 |
> > |---|---|---|---|
> > | `n = 10⁴` 구간 전부 | 10⁴ | 5×10⁻² (**5%**) | 2×10⁻¹³ |
> > | `n = 10⁵` 구간 전부 | 10⁵ | **사실상 확실** | 2×10⁻¹¹ |
> >
> > **`10⁹+7` 단일 해시는 `n`이 커지면 생각보다 쉽게 충돌한다.** 그래서 실전 처방은 셋이다: **① 해시 일치 시 실제 문자열 검증**(가장 확실), **② 이중 해시**(서로 다른 두 모듈러의 튜플 — 충돌 확률이 곱해져 사실상 0), **③ `2⁶¹-1` 모듈러 + 랜덤 밑**(공격 방어). LeetCode #1044처럼 **단일 해시 저격 테스트가 있는 문제**에서는 ①이나 ②가 필수다.
>
> **KMP는 재귀를 쓰지 않으므로 재귀 깊이 걱정이 없다.** `pi` 계산의 `while k > 0: k = pi[k-1]`은 반복문이고, amortized로 총 `O(M)`이다. **"while 루프가 안에 있으니 `O(M²)` 아닌가?"는 면접 단골 함정 질문**이며, 정답은 "`k`는 for 문에서 최대 `M`번 증가하고 while은 감소만 하므로 총 반복은 `O(M)`"이다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **암기 문장 둘.** **"KMP는 패턴의 자기 유사성을 미리 계산하고, 라빈-카프는 문자열을 숫자로 바꾼다."** 그리고 **"`pi[i]` = 접두사이자 접미사인 최장 길이."** 이 두 줄이면 나머지는 유도된다.
> - **`pi` 배열을 손으로 3개만 만들어 보라.** `"aabaaab"`, `"ababaca"`, `"aaaa"`. 특히 `"aaaa"` → `pi = [0,1,2,3]`을 직접 확인하면 "실패해도 조금만 물러난다"는 감각이 몸에 붙는다. **KMP는 읽어서 이해하는 게 아니라 손으로 표를 채워야 이해된다.**
> - **파이썬에서는 `str.find`를 먼저 써라 — 이건 부끄러운 게 아니다.** [Find the Index of the First Occurrence #28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)의 정답은 `haystack.find(needle)` 한 줄이다. **먼저 통과시키고, 그다음 KMP를 직접 구현해 같은 답이 나오는지 교차 검증**하는 것이 가장 효율적인 학습 순서다.
> - **`n - pi[n-1]`을 외워라 — 문자열의 최소 주기.** 이 한 줄로 [Repeated Substring Pattern #459](https://leetcode.com/problems/repeated-substring-pattern/)가 끝난다: `pi[n-1] > 0 and n % (n - pi[n-1]) == 0`. **"반복 구조"라는 단어가 문제에 나오면 `pi`부터 떠올려라.**
> - **#459의 유명한 세 줄 트릭도 알아 두라.** `(s + s)[1:-1].find(s) != -1`. **왜 되는가:** `s`가 `t`의 `k(≥2)`번 반복이면 `s+s`의 중간 어딘가에 `s`가 다시 나타난다. 양 끝 한 글자씩 잘라내는 것은 **원래 위치(0)와 끝 위치의 자명한 매치를 제외**하기 위함이다. 아름답지만 **왜 되는지 설명 못 하면 면접에서 위험하다** — `pi` 해법을 주력으로 삼고 이건 검산용으로 쓰라.
> - **`s + '#' + reverse(s)`는 팰린드롬 문제의 표준 무기다.** 구분자를 **반드시** 넣어라. 안 넣으면 매치가 경계를 넘어 `pi > n`이 되어 조용히 틀린다. 구분자는 **입력에 절대 나오지 않는 문자**여야 한다(문제 제약이 "소문자만"이면 `#`, `\x00`, `1` 등).
> - **롤링 해시는 [[day-20-sliding-window/concept|슬라이딩 윈도우(Day 20)]]이고, 접두사 해시는 [[day-14-prefix-sum/concept|누적 합(Day 14)]]이다.** 새 개념이 아니라 **이미 아는 두 패턴을 문자열에 적용한 것**이다. `hash[l..r) = H[r] - H[l]·B^(r-l)`가 `sum[l..r) = S[r] - S[l]`와 같은 모양이라는 걸 보면 외울 게 없어진다.
> - **모듈러는 `2⁶¹-1`을 기본값으로 삼아라.** 파이썬은 큰 정수를 공짜로 다루므로 `10⁹+7`을 고집할 이유가 없다. 충돌 확률이 `10⁻¹¹` 수준으로 떨어져 **검증 없이도 실전에서 안전**하다. ([롤링 해시 정리 — LeetCode 스터디 가이드](https://leetcode.com/discuss/study-guide/2099715/rolling-hash-explanation/))
> - **밑(base)을 `random.randint`로 뽑는 습관.** LeetCode·Codeforces에는 **고정된 해시 파라미터를 저격하는 테스트**가 실재한다. `B = random.randint(256, MOD-2)`면 출제자가 미리 충돌을 만들 수 없다. [Longest Duplicate Substring #1044](https://leetcode.com/problems/longest-duplicate-substring/)가 대표적인 안티해시 문제다.
> - **`ord(c) - ord('a')` 대신 `ord(c) - ord('a') + 1`을 쓰라.** `+1`이 중요하다. `'a'`를 `0`으로 매핑하면 `"a"`, `"aa"`, `"aaa"`의 해시가 전부 `0`이 되어 **길이가 다른데 해시가 같아진다**. 롤링 해시 최다 버그 중 하나다.
> - **"고정 길이 부분 문자열의 중복"은 해시 없이도 된다.** [Repeated DNA Sequences #187](https://leetcode.com/problems/repeated-dna-sequences/)은 길이가 10으로 **고정**이라 `s[i:i+10]`을 그냥 `set`에 넣어도 통과한다(`n ≤ 10⁵`, 슬라이싱 10글자 = 상수). **롤링 해시는 "길이가 크거나 가변일 때" 필요한 것**이고, #187은 두 방법을 나란히 구현해 비교하기 좋은 연습대다.
> - **기출에서 문자열 매칭은 "정규화"와 함께 나온다.** [방금그곡(프로그래머스 #17683)](https://school.programmers.co.kr/learn/courses/30/lessons/17683)의 핵심은 매칭 자체가 아니라 **`C#` 같은 두 글자 음을 한 글자로 정규화하는 전처리**다. 정규화를 빼먹으면 `"C#"`이 `"C"` 매칭에 잘못 걸린다. **"매칭 전에 표현을 정규화하라"** 는 것이 실무·기출 공통의 교훈이다. 참고로 **"A가 B의 회전인가?"는 `len(A)==len(B) and A in B+B`** 한 줄이다.
> - **KMP의 `while`을 보고 `O(M²)`라고 답하지 마라.** amortized 분석이 면접 단골이다. **"`k`는 for에서 최대 `M`번 증가하고 while은 감소만 하므로 총 while 반복 횟수 ≤ 총 증가량 ≤ `M`"** 이라고 답하라. [[day-06-array-list/concept|동적 배열의 amortized `O(1)`]]과 정확히 같은 논법이다.
> - **패턴이 여러 개면 KMP는 즉시 불리해진다.** 패턴 `k`개면 KMP는 `O(k·N)`이지만, **라빈-카프는 패턴 해시를 `set`에 넣고 텍스트를 한 번만 훑어 `O(N + ΣM)`** 이다(길이가 같을 때). 길이가 제각각이면 **[[day-39-trie/concept|트라이(Day 39)]]에 실패 링크를 붙인 아호-코라식(Aho-Corasick)** 이 정답 — **"KMP + 트라이 = 아호-코라식"** 이라는 계보를 기억해 두라. ([KMP·Z 알고리즘 노트 — LeetCode 토론](https://leetcode.com/discuss/post/2984946/KMP-and-Z-algorithm-Notes-(In-progress)/))
> - **`pi`를 구했으면 "모든 경계(border)"를 공짜로 얻은 것이다.** `pi[n-1]`, `pi[pi[n-1]-1]`, ... 를 따라가면 그 문자열의 **접두사=접미사인 모든 길이**가 내림차순으로 나온다. "모든 가능한 겹침"을 묻는 변형 문제에서 바로 쓴다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **`pi[i]`는 "진(proper)부분문자열"이다 — 자기 자신은 제외한다.** `"aaa"`의 `pi[2]`는 `3`이 아니라 `2`다. 제외하지 않으면 항상 `i+1`이 되어 아무 정보도 없는 표가 된다. 구현에서 이것을 보장하는 것은 **`for i in range(1, m)`으로 `i=0`을 건너뛰고 `pi[0]=0`으로 두는 것**이다.
> 2. **KMP 탐색에서 텍스트 인덱스 `i`를 절대 되돌리지 마라.** `i`가 되돌아가는 순간 그것은 KMP가 아니라 나이브다. **패턴 인덱스 `j`만 `pi[j-1]`로 후퇴**한다. 이 불변식(invariant)이 `O(N)` 보장의 전부다.
> 3. **매치 후 `j = pi[m-1]`(리셋 아님)** 을 잊지 마라. `j = 0`으로 리셋하면 **겹치는 매치를 놓친다**(`"aaaa"`에서 `"aa"`를 2개만 찾는다). 반대로 문제가 "겹치지 않는 개수"를 물으면 의도적으로 `j = 0`을 써야 한다. **문제를 읽고 결정하라.**
> 4. **`s + '#' + rev(s)`에서 구분자를 빼먹으면 조용히 틀린다.** `s="aaa"`일 때 구분자 없이는 `pi[-1] = 5`가 나와 `s`의 길이 3을 넘는다. **`pi[-1] = min(pi[-1], n)`으로 방어**하는 코드도 흔하지만, **구분자를 넣는 것이 정석**이다. 구분자는 반드시 입력 알파벳 밖의 문자여야 한다.
> 5. **롤링 해시에서 문자를 `0`으로 매핑하지 마라.** `ord(c) - ord('a')`를 쓰면 `'a' → 0`이 되어 `"a"`, `"aa"`, `"aaa"`가 모두 해시 `0`이다. **`+1`을 더해 `1`부터 시작**하거나 `ord(c)`를 그대로 쓰라.
> 6. **해시가 같다고 문자열이 같은 것이 아니다.** 라빈-카프는 **확률적 알고리즘**이다. 정확성이 필요하면 **해시 일치 시 실제 문자열을 비교**하라. `text[i:i+m] == pat`는 평균적으로 거의 실행되지 않으므로 **공짜에 가깝고, 최악을 `O(N·M)`으로 만드는 대신 정답을 보장**한다.
> 7. **단일 모듈러 `10⁹+7`은 `n`이 크면 충돌한다.** 생일 문제로 `n = 10⁵`개 구간이면 충돌 확률이 사실상 1이다. **`2⁶¹-1`을 쓰거나, 이중 해시(두 모듈러의 튜플)를 쓰거나, 검증을 붙여라.** "해시니까 안전하겠지"가 가장 위험한 가정이다.
> 8. **파이썬 슬라이싱은 `O(길이)` 복사다.** `T[i:i+m] == P`를 모든 `i`에 대해 하면 그 자체로 `O(N·M)`이다. 라빈-카프의 검증 단계는 **해시가 같을 때만** 실행되어야 의미가 있다. 마찬가지로 `T[i:].find(P)`는 슬라이싱 때문에 `O(N²)`이니 **`T.find(P, i)`** 를 써라.
> 9. **`in` 연산자의 복잡도를 알고 있어라.** `P in T`는 CPython 3.10+에서 **최악 `O(N+M)`(Two-Way 알고리즘)** 이다. 그 이전 버전은 Boyer-Moore-Horspool 변형이라 **최악 `O(N·M)`** 이었다. 면접에서 "파이썬 `in`은 몇인가요?"에 **"버전에 따라 다르며 3.10부터 최악 선형 보장"** 이라고 답하면 매우 좋은 인상을 준다.
> 10. **문자열은 불변(immutable)이라 `+=`가 `O(길이)`다.** 매칭 결과를 문자열에 이어 붙이는 루프는 `O(N²)`가 된다. **리스트에 모아 `''.join()`** 하라([[day-04-strings/concept|Day 04]]). 문자열 문제에서 알고리즘보다 이것 때문에 TLE 나는 경우가 더 많다.
> 11. **최소 주기 공식의 조건을 정확히 외워라.** `p = n - pi[n-1]`이 **최소 주기**인 것은 항상 참이지만, **"`k`번 반복으로 정확히 구성된다"는 것은 `n % p == 0`일 때만**이다. `"abcabca"`는 주기 3이지만 반복 구성이 아니다. **`n % p == 0` 검사를 빼먹는 것이 #459 최다 오답**이다.
> 12. **빈 패턴·빈 텍스트 경계를 처리하라.** `M == 0`이면 보통 `0`을 반환한다(파이썬 `"abc".find("")`는 `0`). `M > N`이면 즉시 실패다. **KMP 루프에 들어가기 전에 이 두 줄을 넣어 두는 것이 습관**이 되어야 한다.
> 13. **`str.count`는 겹치는 매치를 세지 않는다.** `"aaaa".count("aa")`는 `3`이 아니라 **`2`** 다. **겹치는 매치가 필요하면 KMP를 직접 쓰거나 `find(p, i+1)` 루프**를 돌려야 한다. 이 차이를 모르고 `count`를 쓰다 틀리는 경우가 매우 흔하다.
> 14. **실무에서의 문자열 매칭.** `grep`·`ripgrep`(Boyer-Moore/SIMD), 데이터베이스의 `LIKE '%x%'`, 안티바이러스 시그니처 스캔(아호-코라식), DNA 서열 정렬(접미사 배열·BWT), Git의 델타 압축(롤링 해시), `rsync`의 블록 동기화(롤링 해시), 표절 탐지(k-gram 해시) — **롤링 해시는 "큰 파일에서 바뀐 부분만 찾기"라는 형태로 인프라 전반에 깔려 있다.**
> 15. **면접 단골 비교: KMP vs 라빈-카프.** 정답 요지: "**KMP는 결정론적 `O(N+M)` 보장**이고 패턴의 `pi` 배열이 **주기·경계 정보**를 부수적으로 준다. **라빈-카프는 평균 `O(N+M)`이지만 충돌 시 최악 `O(N·M)`인 확률적 기법**이며, 대신 **다중 패턴과 임의 구간 비교로 확장**된다. 파이썬 실전에서는 단일 패턴 탐색이라면 C로 구현된 `str.find`가 둘 다보다 빠르므로, **두 알고리즘은 탐색 자체가 아니라 그 부산물(`pi` 배열, 구간 해시)이 필요할 때 꺼내 쓴다**."
> 16. **KMP는 상위 개념의 입구다.** 실패 링크 개념은 **아호-코라식(다중 패턴)**, **접미사 자동자(suffix automaton)**, **팰린드롬 트리(Eertree)** 로 이어진다. 롤링 해시는 **접미사 배열의 `O(n log²n)` 구축**과 **2차원 패턴 매칭**으로 이어진다. **오늘 배운 두 가지가 문자열 알고리즘 전체의 뿌리**다.

> [!example]- 예제 코드 (Examples)
> ```python
> # ---- (1) 나이브 탐색: O(N·M) 기준선 ----
> def naive_search(text, pat):
>     n, m = len(text), len(pat)
>     return [i for i in range(n - m + 1) if text[i:i + m] == pat]
>
>
> # ---- (2) 실패 함수(prefix function) - KMP의 심장, O(M) ----
> def build_pi(pat):
>     """pi[i] = pat[0..i] 에서 접두사이자 접미사인 최장 진부분문자열의 길이."""
>     m = len(pat)
>     pi = [0] * m
>     k = 0                                   # 지금까지 맞춘 접두사 길이
>     for i in range(1, m):                   # i=0 은 항상 0 (진부분문자열이므로)
>         while k > 0 and pat[i] != pat[k]:
>             k = pi[k - 1]                   # 실패 링크를 타고 후퇴
>         if pat[i] == pat[k]:
>             k += 1
>         pi[i] = k
>     return pi
>
> # build_pi("ababaca") -> [0, 0, 1, 2, 3, 0, 1]
>
>
> # ---- (3) KMP 탐색: O(N + M), 겹치는 매치까지 전부 ----
> def kmp_search(text, pat):
>     n, m = len(text), len(pat)
>     if m == 0:
>         return [0]
>     if m > n:
>         return []
>     pi = build_pi(pat)
>     res, j = [], 0
>     for i in range(n):                      # i 는 절대 되돌아가지 않는다!
>         while j > 0 and text[i] != pat[j]:
>             j = pi[j - 1]                   # 패턴만 후퇴
>         if text[i] == pat[j]:
>             j += 1
>         if j == m:
>             res.append(i - m + 1)
>             j = pi[j - 1]                   # 겹치는 매치를 위해 리셋이 아닌 후퇴
>     return res
>
>
> # ---- (4) pi 배열의 응용: 최소 주기와 반복 판정 ----
> def min_period(s):
>     """s 의 최소 주기. 반복이 없으면 len(s)."""
>     return len(s) - build_pi(s)[-1] if s else 0
>
> def is_repeated(s):
>     """s 가 어떤 부분 문자열의 2번 이상 반복인가? (LeetCode #459)"""
>     n = len(s)
>     if n < 2:
>         return False
>     p = n - build_pi(s)[-1]
>     return p < n and n % p == 0             # n % p == 0 검사 필수!
>
>
> # ---- (5) 라빈-카프: 롤링 해시로 O(N + M) 평균 ----
> MOD = (1 << 61) - 1                          # 메르센 소수. 충돌 확률이 극히 낮다
> BASE = 131
>
> def rabin_karp(text, pat):
>     n, m = len(text), len(pat)
>     if m == 0:
>         return [0]
>     if m > n:
>         return []
>     power = pow(BASE, m - 1, MOD)            # B^(m-1)
>     hp = ht = 0
>     for i in range(m):
>         hp = (hp * BASE + ord(pat[i])) % MOD
>         ht = (ht * BASE + ord(text[i])) % MOD
>     res = []
>     for i in range(n - m + 1):
>         if ht == hp and text[i:i + m] == pat:    # 해시 일치 -> 실제 검증
>             res.append(i)
>         if i + m < n:                            # O(1) 롤링
>             ht = (ht - ord(text[i]) * power) % MOD
>             ht = (ht * BASE + ord(text[i + m])) % MOD
>     return res
>
>
> # ---- (6) 접두사 해시: 임의 구간 비교를 O(1) 로 (누적 합과 같은 구조) ----
> class RollingHash:
>     def __init__(self, s, base=BASE, mod=MOD):
>         self.mod = mod
>         n = len(s)
>         self.h = [0] * (n + 1)               # h[i] = s[0..i-1] 의 해시
>         self.p = [1] * (n + 1)               # p[i] = base^i
>         for i, c in enumerate(s):
>             self.h[i + 1] = (self.h[i] * base + ord(c)) % mod
>             self.p[i + 1] = (self.p[i] * base) % mod
>
>     def get(self, l, r):                     # 구간 [l, r) 의 해시
>         return (self.h[r] - self.h[l] * self.p[r - l]) % self.mod
>         # 누적 합 S[r] - S[l] 과 같은 모양. 자릿수 보정이 p[r-l] 뿐이다
>
>     def same(self, l1, l2, length):          # 두 구간이 같은가? O(1)
>         return self.get(l1, l1 + length) == self.get(l2, l2 + length)
>
>
> # ---- (7) Z 알고리즘: KMP 의 사촌 ----
> def z_function(s):
>     """z[i] = s 와 s[i:] 의 최장 공통 접두사 길이."""
>     n = len(s)
>     z = [0] * n
>     l = r = 0
>     for i in range(1, n):
>         if i < r:
>             z[i] = min(r - i, z[i - l])      # 이미 계산한 값 재활용
>         while i + z[i] < n and s[z[i]] == s[i + z[i]]:
>             z[i] += 1
>         if i + z[i] > r:
>             l, r = i, i + z[i]               # 박스 갱신
>     return z
> ```
>
> 전체 실행 파일(비교 실측·검증 포함) → [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> | # | 문제 | 출처 | 난이도 | 핵심 유형 |
> |---|---|---|---|---|
> | 1 | Find the Index of the First Occurrence in a String | [LeetCode #28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | 🟢기초 | KMP 기본형 (`find`와 교차 검증) |
> | 2 | Repeated DNA Sequences | [LeetCode #187](https://leetcode.com/problems/repeated-dna-sequences/) | 🟢기초 | 고정 길이 롤링 해시 |
> | 3 | Repeated Substring Pattern | [LeetCode #459](https://leetcode.com/problems/repeated-substring-pattern/) | 🟡중급 | `pi` 배열 = 최소 주기 |
> | 4 | [3차] 방금그곡 | [프로그래머스 #17683](https://school.programmers.co.kr/learn/courses/30/lessons/17683) | ⚫기출 | 정규화 전처리 + 부분 문자열 매칭 |
> | 5 | Shortest Palindrome | [LeetCode #214](https://leetcode.com/problems/shortest-palindrome/) | 🔴심화 | `s + '#' + rev(s)` 트릭 |
> | 6 | Longest Duplicate Substring | [LeetCode #1044](https://leetcode.com/problems/longest-duplicate-substring/) | 🔴심화 | 이분 탐색 + 이중 롤링 해시 |
>
> 상세 설명·힌트 → [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제를 **플랫폼 시그니처**(LeetCode `class Solution` / 프로그래머스 `def solution`)로 구현하고, 가능한 곳은 **다중 접근 + 교차 검증**을 붙였다.
> - **#28** — `str.find` / 나이브 / KMP 세 가지를 무작위 입력으로 대조
> - **#187** — `set` 슬라이싱 / 2비트 인코딩 롤링 해시 두 가지
> - **#459** — `pi` 주기 / `(s+s)[1:-1]` 트릭 / 약수 완전 탐색 세 가지
> - **#17683** — 음 정규화 후 `in` 연산, 조건 비교로 최적 곡 선택
> - **#214** — `pi` 트릭 `O(n)` / 나이브 `O(n²)` 대조
> - **#1044** — 이분 탐색 + 이중 해시 `O(n log n)`, 나이브와 소규모 대조
>
> 코드 → [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-41-bitmask/concept|Day 41 — 비트마스킹 (Bitmasking & Bitmask DP)]]
- ➡️ **다음(next):** [[day-43-lca/concept|Day 43 — 최소 공통 조상 (LCA)]]
- 🧭 **관련(related):**
  - [[day-04-strings/concept|Day 04 — 문자열 다루기]] — 슬라이싱 비용·불변성·`join`. 오늘의 TLE 대부분이 여기서 나온다.
  - [[day-39-trie/concept|Day 39 — 트라이 (Trie / Prefix Tree)]] — 트라이 + KMP의 실패 링크 = **아호-코라식**. 다중 패턴 매칭의 정석.
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — 라빈-카프의 충돌·해시 함수 설계가 그대로 이어진다.
  - [[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]] — "본 것을 dict에 넣고 재등장을 감지"가 #187·#1044의 골격.
  - [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — **롤링 해시 = 문자열판 슬라이딩 윈도우.** 앞을 빼고 뒤를 더한다.
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합 (Prefix Sum)]] — **접두사 해시 = 문자열판 누적 합.** 구간 질의가 `O(1)`.
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — "길이에 대한 이분 탐색 + `O(N)` 판정"이 #1044의 전부.
  - [[day-31-dp/concept|Day 31 — 동적 계획법 입문]] — `pi[i]`는 `pi[i-1]`에서 전이되는 **DP 테이블**이다.
  - [[day-24-brute-force/concept|Day 24 — 완전 탐색 (Brute Force)]] — 나이브 `O(N·M)`이 기준선이자 검증용 정답.
  - [[day-41-bitmask/concept|Day 41 — 비트마스킹]] — #187의 2비트 인코딩(A/C/G/T → 00/01/10/11)이 비트 사고의 직접 응용.
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — `pi` 계산의 **amortized 분석**이 오늘의 대표 사례.
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
