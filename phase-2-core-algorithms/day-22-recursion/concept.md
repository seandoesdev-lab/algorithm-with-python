---
day: 22
phase: 2-core-algorithms
title: 재귀와 분할정복 (Recursion & Divide-Conquer)
category: [알고리즘, 재귀]
difficulty: 중급
status: done
prev: "[[day-21-greedy/concept|Day 21 — 그리디]]"
next: "[[day-23-review/concept|Day 23 — 알고리즘 기초 복습]]"
related:
  - "[[day-17-sorting/concept|Day 17 — 정렬]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-25-dfs/concept|Day 25 — DFS]]"
sources:
  - https://leetcode.com/problems/fibonacci-number/
  - https://leetcode.com/problems/powx-n/
  - https://leetcode.com/problems/sort-an-array/
  - https://leetcode.com/problems/maximum-subarray/
  - https://leetcode.com/problems/majority-element/
  - https://leetcode.com/problems/kth-largest-element-in-an-array/
  - https://leetcode.com/problems/different-ways-to-add-parentheses/
  - https://leetcode.com/problems/merge-k-sorted-lists/
  - https://school.programmers.co.kr/learn/courses/30/lessons/12946
  - https://school.programmers.co.kr/learn/courses/30/lessons/68936
  - https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)
tags: [phase/2, topic/recursion, topic/divide-and-conquer, topic/algorithm]
---

# Day 22 — 재귀와 분할정복 (Recursion & Divide-Conquer)

> [!abstract] 한눈 요약 (TL;DR)
> **재귀(recursion)는 "문제를 자기 자신과 똑같은 형태의 더 작은 문제로 표현해, 함수가 스스로를 호출하며 푸는" 기법**이다. 모든 재귀는 두 부분으로 이루어진다 — 더 이상 쪼갤 수 없는 **기저 조건(base case)** 과, 문제를 한 단계 줄여 자신을 다시 부르는 **재귀 단계(recursive step)**. 기저 조건이 없거나 문제가 줄어들지 않으면 무한 재귀 → `RecursionError`(스택 오버플로)가 난다. **분할정복(divide and conquer)** 은 재귀의 대표적 설계 패턴으로, ① 문제를 **분할(divide)** 하고 ② 각 부분을 재귀로 **정복(conquer)** 한 뒤 ③ 결과를 **결합(combine)** 한다. 병합 정렬·퀵 정렬([[day-17-sorting/concept|정렬]]), [[day-18-binary-search/concept|이분 탐색]], 거듭제곱 `pow(x, n)`, 최근접 점쌍 등이 모두 이 골격이다. 분할정복의 시간복잡도는 **점화식(recurrence relation)** 으로 세우고 **마스터 정리(master theorem)** 로 푼다(예: `T(n)=2T(n/2)+O(n)` → `O(n log n)`). 코테에서 재귀는 [[day-11-tree-basics/concept|트리]] 순회, 백트래킹, [[day-25-dfs/concept|DFS]]의 기반이자, 겹치는 부분 문제를 만나면 **메모이제이션(memoization) → DP**로 이어지는 출발점이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **재귀(recursion)** 는 함수가 자신을 호출해 문제를 푸는 방식이다. 핵심 아이디어는 단 하나 — **"큰 문제의 답을, 같은 모양의 작은 문제의 답으로 정의할 수 있다"**. 예를 들어 `n! = n * (n-1)!` 이고 `0! = 1` 이다. 여기서 `0! = 1` 이 **기저 조건**, `n * (n-1)!` 이 **재귀 단계**다.
>
> **일상 비유 — 러시아 인형(마트료시카)과 거울.** 인형을 열면 똑같이 생긴 더 작은 인형이 나온다. 가장 안쪽의 "더 못 여는 인형"이 기저 조건이다. 또는 두 거울을 마주 세우면 상(像) 안에 또 상이 무한히 비치는데, 재귀에 기저 조건이 없으면 딱 이 무한 반사처럼 끝나지 않는다.
>
> **재귀를 신뢰하는 법 — "재귀의 도약(recursive leap of faith)".** 재귀 함수를 짤 때 머릿속으로 콜스택을 끝까지 따라가려 하면 금방 길을 잃는다. 대신 **"더 작은 입력에 대해서는 이 함수가 이미 정답을 준다"고 믿고**, 그 결과를 어떻게 조합해 현재 답을 만들지에만 집중한다. `factorial(n-1)`이 옳다고 믿으면 `factorial(n) = n * factorial(n-1)`은 자명하다.
>
> **분할정복(divide and conquer)** 은 재귀를 "문제를 여러 조각으로 나눠" 적용하는 전략이다. 정렬되지 않은 배열을 반으로 잘라 각각 정렬(재귀)하고 두 정렬된 반쪽을 병합하면 전체가 정렬된다(병합 정렬). "반으로 나눈다"가 divide, "각 반을 정렬"이 conquer, "병합"이 combine이다. 재귀가 **문법/기법**이라면, 분할정복은 그 기법으로 짜는 **대표적 알고리즘 설계 패턴**이다.
>
> **재귀 vs 반복(iteration).** 모든 재귀는 이론상 반복문(+명시적 스택)으로 바꿀 수 있고 그 반대도 가능하다. 재귀는 트리·분할정복·백트래킹처럼 **문제 구조 자체가 재귀적**일 때 코드가 훨씬 짧고 직관적이다. 반복은 함수 호출 오버헤드와 스택 깊이 제한이 없어 성능·안정성에서 유리하다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(1) 재귀 함수의 3요소.**
> ```
> def recurse(문제):
>     if 기저 조건:              # 1) 더 못 쪼개는 가장 작은 경우 -> 즉시 답 반환
>         return 직접 답
>     작은문제 = 문제를 한 단계 줄임   # 2) 반드시 기저 조건을 향해 "줄어들어야" 한다
>     결과 = recurse(작은문제)        # 3) 자기 호출(재귀 단계)
>     return 결과를 조합한 답
> ```
> 세 가지가 모두 있어야 한다: ① 기저 조건, ② 매 호출마다 입력이 기저 조건에 **가까워지는** 진행, ③ 자기 호출. 하나라도 빠지면 무한 재귀다.
>
> **(2) 콜스택(call stack)의 관점.** 함수를 호출할 때마다 지역 변수·복귀 주소가 담긴 **스택 프레임(stack frame)** 이 쌓인다. 기저 조건에 닿으면 값을 반환하며 프레임이 하나씩 걷힌다(unwind). `factorial(3)`의 진행:
> ```
> factorial(3)
>  -> 3 * factorial(2)
>          -> 2 * factorial(1)
>                  -> 1 * factorial(0)
>                          -> 1          (기저 조건)
>                  <- 1 * 1 = 1
>          <- 2 * 1 = 2
>  <- 3 * 2 = 6
> ```
> 파이썬 기본 재귀 한도는 약 1000이다(`sys.getrecursionlimit()`). 깊이가 이를 넘으면 `RecursionError`.
>
> **(3) 분할정복의 골격 — Divide / Conquer / Combine.**
> ```
> def divide_and_conquer(문제):
>     if 문제가 충분히 작으면:        # 기저 조건
>         return 직접 해결
>     부분들 = 문제를 나눈다            # Divide
>     결과들 = [divide_and_conquer(p) for p in 부분들]   # Conquer(재귀)
>     return 결과들을 합친다           # Combine
> ```
>
> **예시 — 병합 정렬(merge sort).**
> ```
> 정렬 대상:        [5, 2, 8, 1, 9, 3]
> Divide:      [5, 2, 8]        [1, 9, 3]
> Divide:    [5] [2, 8]        [1] [9, 3]
> Divide:        [2] [8]            [9] [3]
> Conquer/Combine(병합, 오름차순):
>            [2, 8]              [3, 9]
>       [2, 5, 8]            [1, 3, 9]
> Combine:  [1, 2, 3, 5, 8, 9]
> ```
> 매 단계 반으로 나누므로 깊이는 `log n`, 각 깊이에서 병합에 총 `O(n)` → 전체 `O(n log n)`.
>
> **예시 — 빠른 거듭제곱(fast power, `x^n`).** `x^n = (x^(n/2))^2` 를 이용해 지수를 절반씩 줄인다. `x^10 = (x^5)^2`, `x^5 = x * (x^2)^2` ... 곱셈 횟수가 `n`번(선형)에서 `log n`번으로 줄어 `O(log n)`.
>
> **(4) 점화식과 마스터 정리(master theorem).** 분할정복 비용은 점화식 `T(n) = a·T(n/b) + f(n)` 로 표현한다(부분 문제 `a`개, 각 크기 `n/b`, 분할·결합 비용 `f(n)`). 마스터 정리로 `n^(log_b a)` 와 `f(n)` 을 비교해 답을 얻는다.
> - 병합 정렬: `T(n)=2T(n/2)+O(n)` → `O(n log n)`
> - 이분 탐색: `T(n)=1·T(n/2)+O(1)` → `O(log n)`
> - 단순 순회형 분할: `T(n)=2T(n/2)+O(1)` → `O(n)`

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> | 알고리즘 | 점화식 | 시간복잡도 | 공간(스택 포함) |
> |---|---|---|---|
> | 팩토리얼·단순 선형 재귀 | `T(n)=T(n-1)+O(1)` | O(n) | O(n) 스택 |
> | 나이브 피보나치 | `T(n)=T(n-1)+T(n-2)+O(1)` | O(φ^n)≈O(2^n) | O(n) 스택 |
> | 메모이제이션 피보나치 | 각 상태 1회 | O(n) | O(n) |
> | 빠른 거듭제곱 | `T(n)=T(n/2)+O(1)` | O(log n) | O(log n) |
> | [[day-18-binary-search/concept\|이분 탐색]] | `T(n)=T(n/2)+O(1)` | O(log n) | O(log n) 재귀형 |
> | 병합 정렬 | `T(n)=2T(n/2)+O(n)` | O(n log n) | O(n) 병합 버퍼 + O(log n) 스택 |
> | 퀵 정렬(평균) | `T(n)=2T(n/2)+O(n)` | O(n log n) 평균 / O(n²) 최악 | O(log n) 평균 스택 |
> | 퀵셀렉트(평균) | `T(n)=T(n/2)+O(n)` | O(n) 평균 / O(n²) 최악 | O(1)~O(log n) |
>
> - **재귀는 "숨은 공간 비용"이 있다.** 콜스택 프레임이 깊이만큼 쌓이므로, 깊이 `d`인 재귀는 최소 `O(d)` 메모리를 쓴다. 반복문 버전은 이 비용이 없다.
> - **나이브 재귀는 지수 폭발에 주의.** 피보나치를 그냥 재귀로 짜면 같은 값을 수없이 다시 계산해 `O(2^n)`. **메모이제이션**으로 이미 계산한 값을 저장하면 `O(n)`으로 급감한다 → 이것이 DP의 씨앗.
> - **분할정복 성능은 "균형"이 좌우.** 반씩 균등하게 나뉘면 `log n` 깊이지만, 퀵 정렬에서 피벗이 최악으로 치우치면 한쪽이 `n-1`개가 되어 깊이 `n`, 시간 `O(n²)`이 된다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **먼저 "기저 조건"부터 쓰고 시작하라.** 재귀 함수를 짤 때 재귀 단계보다 **기저 조건을 제일 먼저** 확정하면 무한 재귀를 원천 차단한다. "입력이 가장 작을 때 답이 뭔가?"를 한 줄로 적고 출발한다.
> - **"입력이 줄어드는가"를 눈으로 확인.** 매 호출에서 인자가 반드시 기저 조건 쪽으로 **작아지는지** 손으로 짚어라. `f(n)`이 다시 `f(n)`을 부르거나 `f(n-0)`을 부르면 무한 루프다. ([Recursion, Wikipedia](https://en.wikipedia.org/wiki/Recursion_(computer_science)))
> - **파이썬 재귀 한도 조정.** 깊은 재귀(예: 10만 깊이 트리/DFS)에서는 `import sys; sys.setrecursionlimit(10**6)` 로 한도를 올린다. 단, 근본적으로 깊이가 크면 **반복문 + 명시적 스택**으로 바꾸는 편이 안전하다.
> - **분할정복 = "반으로 나눌 수 있는가?"를 먼저 질문.** 배열/구간/지수/2D 격자를 균등하게 쪼개 각각 독립적으로 풀 수 있고, 결합이 싸면 분할정복 신호다. ([Master theorem](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)))
> - **겹치는 부분 문제가 보이면 즉시 메모이제이션.** 같은 인자로 재귀가 여러 번 불린다면(피보나치처럼) `functools.lru_cache` 나 dict 캐시를 붙여라. 재귀의 명료함은 유지하면서 지수 → 다항으로 떨어진다. ([functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache))
> - **꼬리 재귀(tail recursion)에 기대지 말 것.** 일부 언어는 꼬리 재귀를 반복으로 최적화하지만 **파이썬(CPython)은 하지 않는다.** 깊은 꼬리 재귀도 스택을 쌓으니, 파이썬에서는 반복문으로 직접 바꿔야 한다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **기저 조건 누락 = 스택 오버플로.** 재귀 버그의 1순위. 기저 조건이 없거나, 있어도 도달하지 못하면(입력이 안 줄면) `RecursionError: maximum recursion depth exceeded`. 항상 "① 기저 조건이 있는가 ② 매번 입력이 그쪽으로 줄어드는가"를 점검하라.
> 2. **파이썬 기본 재귀 한도는 약 1000.** `sys.getrecursionlimit()`이 보통 1000이다. 코테에서 배열·트리 깊이가 이를 넘으면 답이 맞아도 런타임 에러가 난다. `setrecursionlimit`로 올리거나 반복문으로 전환하라.
> 3. **나이브 재귀의 지수 폭발.** 피보나치를 순수 재귀로 짜면 `fib(40)`도 버겁다(약 10억 호출). **"같은 인자가 반복 호출되면 메모이제이션"** 은 반드시 몸에 익혀야 한다. 재귀 → 메모이제이션 → 상향식 DP가 하나의 스펙트럼이다.
> 4. **재귀는 스택 메모리를 쓴다.** 시간복잡도만 보고 공간을 잊기 쉽다. 깊이 `d` 재귀는 `O(d)` 스택을 소비하므로, 큰 `d`에서는 메모리도 병목이 될 수 있다.
> 5. **분할정복의 "결합 비용"을 빼먹지 말 것.** 시간복잡도는 분할·재귀뿐 아니라 **combine 단계 `f(n)`** 까지 합산해야 한다. 병합 정렬이 `O(n log n)`인 것은 각 레벨의 병합 비용 `O(n)` 때문이다.
> 6. **퀵 정렬·퀵셀렉트는 최악 `O(n²)`.** 피벗 선택이 나쁘면(이미 정렬된 입력에서 끝 원소를 피벗으로) 균형이 깨져 최악이 된다. 랜덤 피벗·median-of-three 로 완화한다. 코테에서 안정적 `O(n log n)`이 필요하면 병합 정렬이나 언어 내장 정렬(파이썬 Timsort)을 쓴다.
> 7. **리스트 슬라이싱 재귀의 숨은 비용.** `arr[:mid]` 슬라이싱은 매번 `O(n)` 복사를 유발한다. 성능이 중요하면 슬라이스 대신 **인덱스 `(lo, hi)` 를 넘겨** 부분 배열을 표현하라.
> 8. **재귀 ↔ 반복은 상호 변환 가능.** 스택 오버플로가 우려되거나 극한의 성능이 필요하면, 명시적 스택(리스트)으로 재귀를 반복문으로 바꿀 수 있다. [[day-25-dfs/concept|DFS]]에서 재귀형/스택형을 모두 다룬다.
> 9. **가변 기본 인자(mutable default)와 재귀.** `def f(x, acc=[])` 처럼 리스트를 기본값으로 쓰면 호출 간에 공유되어 버그가 난다. 누산기는 `None` 기본값 후 내부에서 생성하거나 인자로 명시 전달하라.

> [!example]- 예제 코드 (Examples)
> ```python
> import sys
> from functools import lru_cache
>
> # 1) 기본 재귀: 팩토리얼 (기저 조건 + 재귀 단계)
> def factorial(n):
>     if n <= 1:              # 기저 조건
>         return 1
>     return n * factorial(n - 1)
>
> # 2) 나이브 재귀 vs 메모이제이션: 피보나치
> def fib_naive(n):           # O(2^n) - 같은 값 재계산
>     if n < 2:
>         return n
>     return fib_naive(n - 1) + fib_naive(n - 2)
>
> @lru_cache(maxsize=None)    # O(n) - 각 n 한 번만 계산
> def fib_memo(n):
>     if n < 2:
>         return n
>     return fib_memo(n - 1) + fib_memo(n - 2)
>
> # 3) 분할정복: 병합 정렬 (Divide / Conquer / Combine)
> def merge_sort(arr):
>     if len(arr) <= 1:                     # 기저 조건
>         return arr
>     mid = len(arr) // 2
>     left = merge_sort(arr[:mid])          # Divide + Conquer
>     right = merge_sort(arr[mid:])
>     return _merge(left, right)            # Combine
>
> def _merge(a, b):
>     merged, i, j = [], 0, 0
>     while i < len(a) and j < len(b):
>         if a[i] <= b[j]:
>             merged.append(a[i]); i += 1
>         else:
>             merged.append(b[j]); j += 1
>     merged.extend(a[i:])
>     merged.extend(b[j:])
>     return merged
>
> # 4) 분할정복: 빠른 거듭제곱 x^n  (O(log n))
> def fast_pow(x, n):
>     if n == 0:                            # 기저 조건
>         return 1
>     half = fast_pow(x, n // 2)
>     return half * half if n % 2 == 0 else half * half * x
> ```
>
> 전체 실행 가능한 예제(재귀 한도·하노이·거듭제곱·병합 정렬 데모 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 앞쪽은 **기저 조건이 명확한 기본 재귀**, 중간은 **분할정복 골격(거듭제곱·병합·2D 분할)**, 뒤로 갈수록 **퀵셀렉트·연산자 분할·리스트 병합**으로 어려워진다.
>
> | 번호 | 문제 | 출처 | 난이도 | 핵심 |
> |---|---|---|---|---|
> | 1 | Fibonacci Number | [LeetCode #509](https://leetcode.com/problems/fibonacci-number/) | 🟢기초 | 재귀 + 메모이제이션 |
> | 2 | 하노이의 탑 | [프로그래머스 #12946](https://school.programmers.co.kr/learn/courses/30/lessons/12946) | 🟢기초 | 전형적 재귀 분해 |
> | 3 | Pow(x, n) | [LeetCode #50](https://leetcode.com/problems/powx-n/) | 🟡중급 | 분할정복 거듭제곱 |
> | 4 | Sort an Array | [LeetCode #912](https://leetcode.com/problems/sort-an-array/) | 🟡중급 | 병합 정렬(분할정복) |
> | 5 | Maximum Subarray | [LeetCode #53](https://leetcode.com/problems/maximum-subarray/) | 🟡중급 | 분할정복 vs 카데인 |
> | 6 | 쿼드압축 후 개수 세기 | [프로그래머스 #68936](https://school.programmers.co.kr/learn/courses/30/lessons/68936) | 🟡중급 | 2D 사분면 분할 |
> | 7 | Majority Element | [LeetCode #169](https://leetcode.com/problems/majority-element/) | 🟡중급 | 분할정복 vs 보이어-무어 |
> | 8 | Kth Largest Element in an Array | [LeetCode #215](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 🔴심화 | 퀵셀렉트(평균 O(n)) |
> | 9 | Different Ways to Add Parentheses | [LeetCode #241](https://leetcode.com/problems/different-ways-to-add-parentheses/) | 🔴심화 | 연산자 기준 분할 + 메모 |
> | 10 | Merge k Sorted Lists | [LeetCode #23](https://leetcode.com/problems/merge-k-sorted-lists/) | 🔴심화 | 리스트 쌍 분할정복 병합 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 기저 조건·점화식·정당성 + 여러 접근(재귀 vs 반복, 분할정복 vs 선형)과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-21-greedy/concept|Day 21 — 그리디]] — 그리디가 정당화되지 않는 문제는 모든 경우를 나눠 푸는 재귀·분할정복(그리고 DP)으로 넘어간다
- ➡️ **다음(next):** [[day-23-review/concept|Day 23 — 알고리즘 기초 복습]] — 정렬·이분 탐색·투 포인터·그리디·재귀를 한데 모아 복습한다
- 🧭 **관련(related):**
  - [[day-17-sorting/concept|Day 17 — 정렬]] — 병합 정렬·퀵 정렬이 분할정복의 대표 사례
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — `T(n)=T(n/2)+O(1)` 로 절반씩 줄이는 분할정복의 최소 형태
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 점화식·마스터 정리로 분할정복 복잡도를 계산하는 근거
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 트리는 구조 자체가 재귀적이라 순회가 곧 재귀
  - [[day-25-dfs/concept|Day 25 — DFS]] — 재귀 호출 스택으로 그래프/트리를 파고드는 깊이 우선 탐색의 기반
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]
