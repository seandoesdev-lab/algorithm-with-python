---
day: 16
phase: 2-core-algorithms
title: 시간복잡도와 Big-O (Time Complexity & Big-O)
category: [알고리즘, 복잡도]
difficulty: 중급
status: done
prev: "[[day-15-review/concept|Day 15 — 자료구조 종합 복습]]"
next: "[[day-17-sorting/concept|Day 17 — 정렬]]"
related:
  - "[[day-15-review/concept|Day 15 — 자료구조 종합 복습]]"
  - "[[day-17-sorting/concept|Day 17 — 정렬]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합]]"
sources:
  - https://leetcode.com/problems/two-sum/
  - https://leetcode.com/problems/contains-duplicate/
  - https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
  - https://leetcode.com/problems/maximum-subarray/
  - https://leetcode.com/problems/binary-search/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42576
  - https://school.programmers.co.kr/learn/courses/30/lessons/68644
  - https://wiki.python.org/moin/TimeComplexity
  - https://en.wikipedia.org/wiki/Big_O_notation
tags: [phase/2, topic/complexity, topic/big-o]
---

# Day 16 — 시간복잡도와 Big-O (Time Complexity & Big-O)

> [!abstract] 한눈 요약 (TL;DR)
> **Big-O는 "입력이 커질 때 실행 시간(또는 메모리)이 얼마나 빨리 증가하는가"를 나타내는 공통 언어**다. 코딩테스트에서 점수를 가르는 첫 관문은 "맞는 답"이 아니라 "제한 시간 안에 도는 답"이다. 같은 문제도 O(n²) 풀이는 시간 초과(TLE)로 0점, O(n) 풀이는 만점이 된다. Big-O를 알면 **코드를 짜기 전에** "이 접근이 통과할지"를 머릿속에서 계산할 수 있다. 핵심 직관 단 하나: **입력 크기 n과 제한 시간을 보고, 허용되는 복잡도의 상한을 역산한다.** (파이썬 기준 대략 1초에 1천만~1억 번 연산.) 이 노트는 O(1)·O(log n)·O(n)·O(n log n)·O(n²)·O(2ⁿ)·O(n!)의 성장 속도, n 크기별 허용 복잡도 표, 그리고 같은 문제를 O(n²) → O(n)으로 떨어뜨리는 사고법을 다룬다. Phase 2 알고리즘 전체를 이해하는 **측정 도구**이자, 자료구조 선택을 *정당화*하는 언어다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **Big-O 표기법(Big-O notation)** 은 알고리즘의 실행 시간을 입력 크기 `n`의 함수로 보고, *n이 충분히 커질 때의 증가율(growth rate)* 만 남긴 것이다. 정확한 실행 시간(초)이 아니라 **"규모가 커지면 어떻게 나빠지는가"의 모양**을 본다.
>
> 두 가지를 버린다:
> - **상수 계수(constant factor):** `2n`도 `100n`도 모두 `O(n)`. 하드웨어·언어 속도 차이는 상수라서 규모가 커지면 의미가 사라진다.
> - **낮은 차수 항(lower-order term):** `n² + n + 7`은 `O(n²)`. n이 커지면 `n²`이 압도한다.
>
> **일상 비유 — 책에서 단어 찾기.** 사전(정렬됨)에서 단어를 찾을 땐 가운데를 펴서 절반씩 좁힌다 → `O(log n)`. 반면 정리 안 된 메모 뭉치에서 찾으려면 한 장씩 다 넘겨야 한다 → `O(n)`. 페이지가 100배 늘어도 사전은 몇 번만 더 펴면 되지만, 메모 뭉치는 100배 더 넘겨야 한다. **이 "늘어나는 비율의 차이"가 Big-O의 전부**다.
>
> 같이 쓰는 표기:
> - **O (빅오):** 상한(worst case에 자주 사용). "아무리 나빠도 이만큼."
> - **Ω (빅오메가):** 하한. "아무리 좋아도 이만큼."
> - **Θ (빅세타):** 상·하한이 같을 때(정확한 차수). 실무에선 보통 O로 최악을 말한다.
>
> 코테에서 중요한 건 보통 **최악 시간복잡도(worst-case time complexity)** 와 **공간복잡도(space complexity)** 두 가지다.

> [!gear]- 2. 동작 원리 (How It Works) — 복잡도 세는 법
> **규칙 1. 기본 연산 1회 = O(1).** 산술, 비교, 인덱싱(`arr[i]`), dict 조회는 상수 시간.
>
> **규칙 2. 반복문은 반복 횟수만큼 곱한다.**
> ```
> for i in range(n):      # n번
>     do_work()           # O(1)
> # => O(n)
> ```
>
> **규칙 3. 중첩 반복은 곱셈.**
> ```
> for i in range(n):          # n번
>     for j in range(n):      # 각 n번
>         do_work()           # O(1)
> # => O(n * n) = O(n^2)
> ```
>
> **규칙 4. 순차 실행은 덧셈 후 가장 큰 항만 남긴다.**
> ```
> for i in range(n): ...      # O(n)
> for i in range(n*n): ...    # O(n^2)
> # => O(n + n^2) = O(n^2)   (큰 항이 지배)
> ```
>
> **규칙 5. 절반씩 줄면 O(log n).** 매 단계 입력이 1/2로 → 단계 수 = log₂n. 이분 탐색이 대표.
> ```
> while n > 1:
>     n = n // 2      # 반으로
> # => O(log n)
> ```
>
> **규칙 6. 분할정복·정렬은 O(n log n)** 이 흔하다. n개를 log n 단계에 걸쳐 매번 전부 훑는 모양(병합 정렬).
>
> **성장 속도 한눈에 (작은 것이 빠름):**
> ```
> O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)
>
> n=10        n=1,000        n=1,000,000
> O(log n)      ~3            ~10            ~20
> O(n)          10            1,000          1,000,000
> O(n log n)    ~33           ~10,000        ~20,000,000
> O(n^2)        100           1,000,000      10^12  (불가)
> O(2^n)        1,024         (천문학적)      (불가)
> ```
> n이 백만일 때 O(n²)은 10¹²번 → 파이썬으로 수십 분. **n의 규모를 보면 어떤 복잡도까지 허용되는지 바로 나온다.**

> [!chart]- 3. 복잡도 (Time / Space Complexity) — n 크기별 허용 복잡도 & 파이썬 연산 비용
> **(A) 입력 크기 → 목표 복잡도 (제한 1초, 파이썬 ~10^7~10^8 연산/초 기준)**
>
> | 입력 크기 n | 허용 가능한 복잡도 | 떠올릴 접근 |
> |---|---|---|
> | n ≤ 11 | O(n!) | 순열 완전탐색 |
> | n ≤ 20~25 | O(2ⁿ) | 부분집합·비트마스킹 |
> | n ≤ 500 | O(n³) | 삼중 루프, 플로이드-워셜 |
> | n ≤ 5,000 | O(n²) | 이중 루프, DP |
> | n ≤ 100,000 | O(n log n) | 정렬, 힙, 이분 탐색 |
> | n ≤ 1,000,000 | O(n) / O(n log n) | 한 번 순회, 투 포인터 |
> | n ≥ 10,000,000 | O(n) / O(log n) | 해시, 수식, 누적합 |
>
> **(B) 파이썬 자료구조 연산 비용 (평균)**
>
> | 연산 | list | dict / set | deque |
> |---|---|---|---|
> | 인덱스 접근 `x[i]` | O(1) | — | O(n) |
> | 멤버십 `in` | O(n) | **O(1)** | O(n) |
> | 끝에 추가 append | O(1) 분할상환 | — | O(1) |
> | 앞에서 제거 | `pop(0)` O(n) | — | `popleft` **O(1)** |
> | 키/원소 삭제 | O(n) | O(1) | O(n) |
> | 정렬 `sort()` | O(n log n) | — | — |
>
> > **분할상환(amortized) O(1):** `list.append`는 가끔 내부 배열을 2배로 재할당(O(n))하지만, 평균을 내면 1회당 O(1)이다. "대부분 싸고 가끔 비싼" 연산을 평균낸 개념.
>
> **공간복잡도(space)** 도 같은 방식으로 센다. 입력 외에 크기 n 배열을 하나 더 쓰면 O(n), 2차원 DP 표를 쓰면 O(n²). 재귀는 **호출 스택 깊이**가 공간으로 잡힌다(깊이 n이면 O(n)).

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"제한 조건(constraints)을 먼저 읽어라."** 문제의 `1 ≤ n ≤ 100,000` 같은 줄이 정답 복잡도를 알려준다. n이 10만이면 O(n²)(=10¹⁰)은 탈락 → O(n log n) 이하를 노려야 한다. 코드보다 제약을 먼저 본다.
>   - 참고: [Big O notation (Wikipedia)](https://en.wikipedia.org/wiki/Big_O_notation)
> - **"로그의 밑(base)은 무시한다."** O(log₂n)이든 O(log₁₀n)이든 상수배 차이라 모두 `O(log n)`. 그래서 이분 탐색·균형 트리·힙이 전부 "log n"으로 뭉뚱그려진다.
> - **"O(n²) 이중 루프가 보이면 해시/정렬을 의심하라."** "모든 쌍을 본다"는 발상의 절반은 dict 한 번 순회(O(n))로 줄어든다(Two Sum 패턴).
>   - 참고: [Python TimeComplexity (공식 위키)](https://wiki.python.org/moin/TimeComplexity)
> - **"입력이 정렬돼 있다 / 정렬해도 된다"는 강력한 신호.** 정렬(O(n log n)) 한 번이 그 뒤의 탐색을 O(log n)이나 투 포인터 O(n)로 만든다.
> - **상수도 코테에선 가끔 중요하다.** 같은 O(n)이라도 파이썬 순수 루프보다 내장 함수(`sum`, `sorted`, set 연산)가 C로 돌아 수십 배 빠르다. 복잡도가 같아도 내장을 쓰면 통과하는 경우가 있다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **Big-O는 "규모가 커질 때의 추세"다.** n이 작으면 O(n²)이 O(n log n)보다 빠를 수도 있다(상수가 작아서). Big-O는 **충분히 큰 n**에서의 비교임을 잊지 마라. 그래서 작은 입력엔 단순 정렬, 큰 입력엔 정교한 알고리즘을 쓴다.
> 2. **최악(worst) / 평균(average) / 최선(best)을 구분하라.** 퀵정렬은 평균 O(n log n)이지만 최악 O(n²), 해시 조회는 평균 O(1)이지만 충돌 시 최악 O(n). 코테 채점은 **최악**을 기준으로 잡는 게 안전하다.
> 3. **"파이썬은 느리다"를 복잡도와 헷갈리지 마라.** 복잡도가 같아도 파이썬은 C/C++보다 상수가 크다. 그래서 같은 O(n²)이라도 파이썬에선 n이 더 작아야 통과한다. 안전 기준: **파이썬 1초 ≈ 1천만(10⁷)번 순수 연산** 정도로 보수적으로 잡아라.
> 4. **숨은 복잡도를 놓치지 마라.** `if x in my_list`는 리스트면 O(n)이라 루프 안에 있으면 전체가 O(n²)이 된다. `s = s + ch`로 문자열을 이어 붙이면 매번 새 문자열 생성으로 O(n²). 같은 일은 `set` 멤버십(O(1))·`"".join()`(O(n))으로 바꿔라.
> 5. **공간복잡도도 채점 대상이다.** 메모리 초과(MLE)도 0점이다. 크기 10⁸ 리스트는 수백 MB라 위험하다. 재귀 깊이가 깊으면 스택 오버플로(파이썬 기본 한도 ~1000)에 주의.
> 6. **log의 정체.** O(log n)은 "매 단계 문제를 일정 비율로 줄인다"는 뜻이다. n=10억이라도 log₂n ≈ 30. 이게 이분 탐색·힙·균형 트리가 강력한 이유다.
> 7. **O(n log n)은 "비교 기반 정렬의 이론적 하한"이다.** 비교만으로 정렬하면 O(n log n)보다 빠를 수 없다(증명됨). 더 빠르려면 계수 정렬처럼 비교를 안 하는 특수 조건이 필요하다.
> 8. **복잡도 분석 = 코테의 1차 필터.** 구현 전에 "n과 제한 → 목표 복잡도 → 그 복잡도를 내는 자료구조/알고리즘"을 머릿속에서 먼저 통과시켜라. 이 습관이 [[day-17-sorting/concept|정렬]]·[[day-18-binary-search/concept|이분 탐색]] 등 Phase 2 전체의 토대다.

> [!example]- 예제 코드 (Examples)
> ```python
> # 1) O(n^2) -> O(n): 중복 존재 여부
> def has_dup_slow(a):          # O(n^2): 모든 쌍 비교
>     for i in range(len(a)):
>         for j in range(i + 1, len(a)):
>             if a[i] == a[j]:
>                 return True
>     return False
>
> def has_dup_fast(a):          # O(n): set 멤버십 O(1)
>     seen = set()
>     for x in a:
>         if x in seen:
>             return True
>         seen.add(x)
>     return False
>
> # 2) O(log n): 이분 탐색 (정렬된 배열에서 절반씩)
> def binary_search(a, target):
>     lo, hi = 0, len(a) - 1
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         if a[mid] == target:
>             return mid
>         if a[mid] < target:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return -1
>
> # 3) O(n): 최대 부분합 (Kadane) - 이중 루프 O(n^2) 를 한 번 순회로
> def max_subarray(a):
>     best = cur = a[0]
>     for x in a[1:]:
>         cur = max(x, cur + x)   # 여기서 끊을지 이어갈지
>         best = max(best, cur)
>     return best
>
> # 4) 숨은 복잡도 주의: 문자열 이어붙이기
> def build_bad(words):         # O(n^2): 매번 새 문자열 생성
>     s = ""
>     for w in words:
>         s = s + w
>     return s
>
> def build_good(words):        # O(n): join 한 번
>     return "".join(words)
> ```
>
> 전체 실행 가능한 예제(성장 속도 비교 출력 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> "같은 문제를 느린 풀이 → 빠른 풀이로 떨어뜨리기"가 핵심. 각 문제에 목표 복잡도를 표시했다.
>
> | 번호 | 문제 | 출처 | 난이도 | 목표 복잡도 |
> |---|---|---|---|---|
> | 1 | Contains Duplicate | [LeetCode #217](https://leetcode.com/problems/contains-duplicate/) | 🟢기초 | O(n) 해시 |
> | 2 | Two Sum | [LeetCode #1](https://leetcode.com/problems/two-sum/) | 🟢기초 | O(n) 해시 |
> | 3 | Binary Search | [LeetCode #704](https://leetcode.com/problems/binary-search/) | 🟢기초 | O(log n) |
> | 4 | Best Time to Buy and Sell Stock | [LeetCode #121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | 🟢기초 | O(n) 1회 순회 |
> | 5 | Maximum Subarray | [LeetCode #53](https://leetcode.com/problems/maximum-subarray/) | 🟡중급 | O(n) Kadane |
> | 6 | 완주하지 못한 선수 | [프로그래머스 #42576](https://school.programmers.co.kr/learn/courses/30/lessons/42576) | 🟢기초 | O(n) 해시 |
> | 7 | 두 개 뽑아서 더하기 | [프로그래머스 #68644](https://school.programmers.co.kr/learn/courses/30/lessons/68644) | 🟢기초 | O(n²)·작은 n |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 느린 접근 vs 빠른 접근 + 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-15-review/concept|Day 15 — 자료구조 종합 복습]] — 자료구조 "선택"을 배웠다면, 오늘은 그 선택을 "정당화"하는 복잡도 언어를 배운다
- ➡️ **다음(next):** [[day-17-sorting/concept|Day 17 — 정렬]] — O(n log n)의 대표 사례. Big-O로 정렬 알고리즘들을 비교한다
- 🧭 **관련(related):**
  - [[day-15-review/concept|Day 15 — 자료구조 종합 복습]] — "왜 이 자료구조가 빠른가"의 답이 곧 복잡도
  - [[day-17-sorting/concept|Day 17 — 정렬]] — O(n log n) 하한과 정렬 비교
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — O(log n)의 전형
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — O(1) 멤버십으로 O(n²)을 O(n)으로
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — O(log n) 삽입/삭제의 근거
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합]] — 전처리로 질의를 O(1)로
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]
