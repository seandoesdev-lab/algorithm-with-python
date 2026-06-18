---
day: 7
phase: 1-data-structures
title: 스택 (Stack)
category: [자료구조]
difficulty: 기초
status: done
prev: [[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]
next: [[day-08-queue-deque/concept|Day 08 — 큐와 덱]]
related:
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/12909
  - https://leetcode.com/problems/valid-parentheses/
  - https://leetcode.com/problems/min-stack/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42584
  - https://leetcode.com/problems/daily-temperatures/
  - https://school.programmers.co.kr/learn/courses/30/lessons/64061
tags: [phase/1, topic/stack]
---

# Day 07 — 스택 (Stack)

> [!abstract] 한눈 요약 (TL;DR)
> 스택은 **한쪽 끝(top)에서만** 넣고 빼는 자료구조로, 가장 나중에 넣은 것이 가장 먼저 나오는 **후입선출(LIFO)** 규칙을 따른다. 파이썬에서는 `list`의 `append`/`pop()`으로 완전히 구현된다. 괄호 매칭, Undo, DFS, 모노토닉 스택이 대표 활용이다.

> [!note]- 1. 정의와 직관
> **스택(stack)**은 **한쪽 끝에서만** 데이터를 넣고 빼는 자료구조다. 가장 **나중에 넣은(Last In)** 원소가 가장 **먼저 나온다(First Out)**. 이 규칙을 **후입선출(LIFO)**이라 부른다.
>
> 일상 비유로는 **접시 더미**나 **프링글스 통**이 정확하다. 새 접시는 맨 위에 올리고(push), 뺄 때도 맨 위 접시부터 뺀다(pop). 맨 아래 접시를 꺼내려면 위의 접시를 전부 치워야 한다. 또 다른 비유는 **웹 브라우저의 뒤로가기**다. 방문한 페이지를 차곡차곡 쌓아 두고, 뒤로가기를 누르면 가장 최근 페이지부터 꺼낸다.
>
> ```
>         push(40)                       pop() -> 40
>           |                               ^
>           v                               |
>        +------+                        +------+
>  top ->|  40  |                  top ->|  30  |
>        +------+                        +------+
>        |  30  |                        |  20  |
>        +------+                        +------+
>        |  20  |                        |  10  |
>        +------+                        +------+
>        |  10  |   <- bottom            (40이 가장 먼저 나온다 = LIFO)
>        +------+
> ```
>
> **기본 연산:**
>
> | 연산 | 의미 | 파이썬 (`list`) |
> |---|---|---|
> | `push(x)` | 맨 위에 x를 쌓는다 | `stack.append(x)` |
> | `pop()` | 맨 위 원소를 빼서 반환한다 | `stack.pop()` |
> | `peek()` / `top()` | 맨 위 원소를 **보기만** 한다(제거 X) | `stack[-1]` |
> | `isEmpty()` | 비었는지 확인 | `not stack` |
> | `size()` | 원소 개수 | `len(stack)` |
>
> 핵심은 **모든 접근이 "맨 위(top)"에서만** 일어난다는 점이다. 중간이나 맨 아래 원소에는 직접 손댈 수 없다. 이 제약이 오히려 문제를 단순하게 만들어 준다.

> [!gear]- 2. 동작 원리
> **파이썬에서 스택 구현하기**
>
> 파이썬에는 별도의 Stack 클래스가 없다. **`list`를 그대로 스택으로 쓴다.** 리스트의 **맨 뒤**가 스택의 **top**이다. `append`와 `pop()`(인자 없는, 맨 뒤)은 **분할 상환 O(1)**이라 스택 용도로 완벽하다.
>
> **list vs deque:**
>
> | 기준 | `list` | `collections.deque` |
> |---|---|---|
> | 맨 뒤 push/pop | 분할상환 O(1) | O(1) |
> | 인덱스 임의 접근 `s[i]` | O(1) 가능 | **O(n)** (양끝 빼고 느림) |
> | 스레드 안전(thread-safe) | X | append/pop은 안전 |
> | 코테에서 스택 용도 | **권장(가장 흔함)** | 큐/덱일 때 권장 |
>
> **결론:** **순수 스택**이라면 보통 `list`로 충분하고 더 빠르며 직관적이다. `deque`는 **큐(queue)**나 **양끝(deque)**이 필요할 때(Day 8) 쓴다.
>
> **스택이 빛나는 상황:**
>
> 1. **괄호 짝 맞추기:** 여는 괄호를 push, 닫는 괄호를 만나면 pop해서 짝이 맞는지 확인. 가장 최근에 연 괄호가 가장 먼저 닫혀야 하므로 LIFO와 정확히 일치한다.
> 2. **수식 계산:** 후위 표기법(postfix) 계산, 중위->후위 변환.
> 3. **되돌리기/실행취소:** 에디터의 Ctrl+Z, 브라우저 뒤로가기.
> 4. **함수 호출 스택:** 프로그램이 함수 호출/반환을 관리하는 방식 자체가 스택이다. 재귀가 깊어지면 이 스택이 넘쳐 `RecursionError`가 난다.
> 5. **DFS:** 재귀 DFS는 호출 스택을, 반복 DFS는 명시적 스택을 쓴다(Day 25).
> 6. **모노토닉 스택:** "다음에 나보다 큰/작은 원소"를 O(n)에 찾는 기법. 주식가격, 일일 온도 같은 문제의 핵심 도구다.
>
> **모노토닉 스택 동작:**
>
> 스택 안의 원소가 항상 **단조 증가 또는 단조 감소**를 유지하도록 관리한다. 이중 루프 O(n^2) 대신 **O(n)**으로 "다음 큰 원소"를 구한다.
>
> ```
> "다음 더 큰 값까지 며칠?" 온도 = [73, 74, 75, 71, 72]
> 인덱스를 스택에 쌓고, 더 따뜻한 날을 만나면 pop하며 거리(일수)를 기록한다.
>   i=0 push 0                stack=[0]
>   i=1 73<74 -> pop0 ans[0]=1; push1   stack=[1]
>   i=2 74<75 -> pop1 ans[1]=1; push2   stack=[2]
>   i=3 75>71 -> push3                  stack=[2,3]
>   i=4 71<72 -> pop3 ans[3]=1; push4   stack=[2,4]
>   결과 ans = [1,1,?,1,?]  (남은 2,4는 더 큰 날 없음 -> 0)
> ```

> [!chart]- 3. 복잡도 (시간/공간)
> | 연산 | 시간복잡도 | 공간 | 비고 |
> |---|---|---|---|
> | `push` (`append`) | O(1) 분할상환 | - | 초과 할당 덕분(Day 6) |
> | `pop` (맨 뒤) | O(1) | - | 인자 없는 `pop()` |
> | `peek` (`s[-1]`) | O(1) | - | 제거하지 않음 |
> | `isEmpty` (`not s`) | O(1) | - | |
> | 탐색 `x in s` | O(n) | - | 스택은 탐색용이 아님 |
> | 전체 스택 저장 | - | O(n) | n = 원소 수 |
>
> 괄호 검사, 모노토닉 스택 같은 대표 문제는 입력을 한 번 훑으므로 전체 **O(n)**, 공간 **O(n)**이다.

> [!tip]- 💡 이해를 돕는 팁
> - **"가장 최근 것부터" 키워드를 만나면 스택**: 괄호, Undo, 뒤로가기, "직전", "다음 큰 값"이 보이면 스택을 의심하자. 반대로 "먼저 온 것부터(선착순)"는 큐(Day 8)다.
>   - 참고: [Stack (LIFO) 개념과 활용 (GeeksforGeeks)](https://www.geeksforgeeks.org/stack-data-structure/)
>
> - **파이썬 스택은 그냥 list**: 별도 자료형이 없다. `append`/`pop()`이면 끝. 공식 문서도 "리스트를 스택으로 쓰라"고 안내한다.
>   - 참고: [Using lists as stacks (Python 공식 튜토리얼)](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks)
>
> - **큐로 쓸 땐 list 금지, deque 사용**: `pop(0)`은 O(n)이라 큐엔 부적합. 스택은 list로 OK지만 큐/양끝은 `collections.deque`.
>   - 참고: [collections.deque (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.deque)
>
> - **모노토닉 스택은 "각 원소 최대 1번 push/pop"이라 O(n)**: while 루프가 안에 있어도 전체 반복 횟수는 2n을 넘지 않는다(분할 상환). 이 직관을 잡아 두면 면접에서 복잡도 설명이 쉽다.
>   - 참고: [Monotonic Stack 입문 (LeetCode Discuss)](https://leetcode.com/discuss/post/5085517/templates-for-monotonic-stacks-and-queue-2lfq/)
>
> - **재귀는 곧 호출 스택**: 깊은 재귀는 `RecursionError`를 낸다. 파이썬 기본 한계는 약 1000. 필요하면 `sys.setrecursionlimit`로 늘리거나, **반복 + 명시적 스택**으로 바꿔 DFS를 짠다(Day 25).
>   - 참고: [sys.setrecursionlimit (Python 공식 문서)](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)

> [!warning]- ⚠️ 개발자 필수 상식
> 1. **LIFO가 전부다**: 스택은 "맨 위"만 만진다. 중간 원소에 접근하고 싶다면 스택이 잘못된 선택이다.
>
> 2. **빈 스택에서 pop/peek 금지**: 빈 `list`에서 `pop()`은 `IndexError: pop from empty list`, `s[-1]`도 `IndexError`. **반드시 `if stack:`로 먼저 확인**하거나 길이를 추적한다.
>
> 3. **스택의 pop은 인자 없는 `pop()`**: `pop(0)`은 맨 앞을 빼는 O(n) 연산으로, 의미가 다르고 느리다. 스택에선 절대 `pop(0)`를 쓰지 않는다.
>
> 4. **`peek`은 제거하지 않는다**: `s[-1]`은 보기만 한다. "확인 후 조건에 따라 빼기"가 필요하면 `s[-1]`로 보고, 조건 충족 시 `s.pop()`을 호출하는 2단계로 짠다(모노토닉 스택의 핵심 패턴).
>
> 5. **괄호 문제는 끝에 스택이 비어야 성공**: 닫는 괄호를 다 처리했어도 스택에 여는 괄호가 남아 있으면 짝이 안 맞은 것이다(예: `"(()"`). 마지막에 `not stack` 검사를 빠뜨리지 말자.
>
> 6. **여러 종류 괄호는 매핑 딕셔너리로**: `()[]{}`처럼 종류가 섞이면 `{')':'(', ']':'[', '}':'{'}`같은 닫힘->열림 매핑으로 top과 비교한다. "개수만 세면" 종류 불일치(`"(]"`)를 못 잡는다.
>
> 7. **재귀 깊이도 스택**: 시스템 호출 스택은 유한하다. 그래프/트리가 깊으면 반복 DFS(명시적 스택)로 바꿔야 스택 오버플로를 피한다.
>
> 8. **`list`는 스택, `deque`는 큐**: 면접에서 "왜 list?" "왜 deque?"를 물으면 "스택은 맨 뒤만 쓰니 list로 충분, 큐는 맨 앞 pop이 필요해 deque" 라고 답할 수 있어야 한다.

> [!example]- 예제 코드
> ```python
> from collections import deque
>
> # 1) list 를 스택으로 (가장 흔함)
> stack = []
> stack.append(10)       # push
> stack.append(20)
> top = stack[-1]        # peek -> 20
> x = stack.pop()        # pop  -> 20
>
> # 2) 비었는지 확인은 truthiness 로 (len 비교보다 관용적)
> if not stack:
>     print("스택이 비었음")
>
> # 3) 빈 스택 pop 방어 (IndexError 예방)
> x = stack.pop() if stack else None
>
> # 4) deque 로도 스택 가능 (양끝 O(1))
> dq = deque()
> dq.append(1)           # push
> dq.pop()               # pop (맨 뒤)
>
> # 5) 괄호 매칭 표준 골격
> pairs = {')': '(', ']': '[', '}': '{'}
> st = []
> for ch in s:
>     if ch in '([{':
>         st.append(ch)
>     else:                       # 닫는 괄호
>         if not st or st[-1] != pairs[ch]:
>             # 짝이 안 맞음 -> 실패
>             ...
>         st.pop()
> ok = (not st)                   # 끝에 남으면 실패
>
> # 6) 모노토닉 스택 골격 (다음 큰 원소까지 거리)
> def next_greater_distance(nums):
>     ans = [0] * len(nums)
>     st = []                     # 아직 답 못 찾은 인덱스들
>     for i, v in enumerate(nums):
>         while st and nums[st[-1]] < v:
>             j = st.pop()
>             ans[j] = i - j
>         st.append(i)
>     return ans
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | 올바른 괄호 | [프로그래머스 #12909](https://school.programmers.co.kr/learn/courses/30/lessons/12909) | 🟢기초 | 괄호 매칭 |
> | 2 | Valid Parentheses | [LeetCode #20](https://leetcode.com/problems/valid-parentheses/) | 🟡중급 | 괄호 매칭 |
> | 3 | Min Stack | [LeetCode #155](https://leetcode.com/problems/min-stack/) | 🟡중급 | 자료구조 설계 |
> | 4 | 주식가격 | [프로그래머스 #42584](https://school.programmers.co.kr/learn/courses/30/lessons/42584) | 🔴심화 | 모노토닉 스택 |
> | 5 | Daily Temperatures | [LeetCode #739](https://leetcode.com/problems/daily-temperatures/) | 🔴심화 | 모노토닉 스택 |
> | 6 | 크레인 인형뽑기 게임 | [프로그래머스 #64061](https://school.programmers.co.kr/learn/courses/30/lessons/64061) | ⚫기출 | 시뮬레이션 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]
- ➡️ 다음: [[day-08-queue-deque/concept|Day 08 — 큐와 덱]]
- 🧭 관련:
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — LIFO vs FIFO 비교
- 🗺️ 지도: [[Phase-1 MOC]] · [[00 Algorithm MOC]]
