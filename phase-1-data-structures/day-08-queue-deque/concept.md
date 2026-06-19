---
day: 8
phase: 1-data-structures
title: 큐와 덱 (Queue & Deque)
category: [자료구조]
difficulty: 기초
status: done
prev: [[day-07-stack/concept|Day 07 — 스택]]
next: [[day-09-hashing/concept|Day 09 — 해시 dict/set]]
related:
  - "[[day-07-stack/concept|Day 07 — 스택]]"
  - "[[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/42586
  - https://school.programmers.co.kr/learn/courses/30/lessons/42587
  - https://leetcode.com/problems/implement-queue-using-stacks/
  - https://leetcode.com/problems/design-circular-queue/
  - https://leetcode.com/problems/sliding-window-maximum/
  - https://school.programmers.co.kr/learn/courses/30/lessons/118667
tags: [phase/1, topic/queue]
---

# Day 08 — 큐와 덱 (Queue & Deque)

> [!abstract] 한눈 요약 (TL;DR)
> 큐는 **앞에서 빼고 뒤에서 넣는** 선입선출(FIFO) 자료구조다. 파이썬에서는 `list.pop(0)`(O(n))이 아닌 **`collections.deque` + `popleft()`**(O(1))가 유일한 정답이다. 덱(deque)은 양끝 O(1)로 스택·큐를 모두 흉내 낼 수 있으며, 슬라이딩 윈도우 최대/최소(모노토닉 덱)와 BFS의 핵심 도구다.

> [!note]- 1. 정의와 직관
> **큐(queue)**는 **한쪽 끝(뒤, rear)으로 넣고 반대쪽 끝(앞, front)으로 빼는** 자료구조다. 가장 **먼저 넣은(First In)** 원소가 가장 **먼저 나온다(First Out)**. 이 규칙을 **선입선출(FIFO)**이라 한다. Day 7의 스택(LIFO)과 정확히 반대다.
>
> 일상 비유는 **줄 서기(대기열)**다. 매표소 앞에 줄을 서면, 먼저 온 사람이 먼저 표를 산다. 새치기가 없다면 들어온 순서대로 처리된다. 프린터의 인쇄 대기열, 콜센터 대기 전화, 운영체제의 작업 스케줄링이 모두 큐다.
>
> ```
>         enqueue(40)                         dequeue() -> 10
>         (뒤에 넣음)                          (앞에서 뺌)
>             |                                    |
>             v                                    v
>    front [10 | 20 | 30 | 40] rear     front [20 | 30 | 40] rear
>          (가장 먼저 들어온 10이 가장 먼저 나온다 = FIFO)
> ```
>
> **덱(deque, Double-Ended Queue)**은 **양쪽 끝(앞·뒤) 모두에서** 삽입·삭제가 가능한 큐의 일반화다. 앞에서만 빼면 큐(FIFO), 한쪽 끝에서만 넣고 빼면 스택(LIFO)처럼 쓸 수 있다.
>
> | 동작 | 큐(Queue) | 스택(Stack) | 덱(Deque) |
> |---|---|---|---|
> | 넣는 곳 | 뒤(rear) | 위(top=뒤) | 앞·뒤 모두 |
> | 빼는 곳 | 앞(front) | 위(top=뒤) | 앞·뒤 모두 |
> | 규칙 | FIFO | LIFO | 양쪽 자유 |
>
> **큐의 기본 연산 (`collections.deque`):**
>
> | 연산 | 의미 | 파이썬 |
> |---|---|---|
> | `enqueue(x)` | 뒤에 x를 넣는다 | `q.append(x)` |
> | `dequeue()` | 앞 원소를 빼서 반환 | `q.popleft()` |
> | `front()` / `peek()` | 앞 원소를 **보기만** 함 | `q[0]` |
> | `isEmpty()` | 비었는지 확인 | `not q` |
> | `size()` | 원소 개수 | `len(q)` |
>
> 덱은 여기에 `appendleft(x)`(앞에 넣기)와 `pop()`(뒤에서 빼기)이 추가된다.

> [!gear]- 2. 동작 원리
> **왜 `list.pop(0)`은 느리고 `deque.popleft()`는 빠른가**
>
> `list`는 연속된 메모리 배열(Day 6)이다. 맨 앞 원소를 빼면 그 뒤의 모든 원소를 한 칸씩 앞으로 **이동(shift)**해야 한다. 원소가 n개면 n번 이동 -> **O(n)**.
>
> ```
> list.pop(0):   [A][B][C][D]  ->  [B][C][D]      (B,C,D를 전부 왼쪽으로 이동: O(n))
>                 ^빼고 나머지 시프트
>
> deque.popleft: front 포인터만 한 칸 옮김 -> O(1)  (이동 없음)
> ```
>
> `deque`는 양끝에 포인터(블록 링크)를 두어, 앞/뒤 어디서 빼도 **이동이 없다.** 그래서 O(1). 대신 **임의 인덱스 접근 `q[i]`는 O(n)**(양끝 제외)이라, 중간을 자주 조회한다면 `list`가 낫다.
>
> **원형 큐 (Circular Queue / Ring Buffer)**
>
> 고정 크기 배열로 큐를 직접 구현하면, 앞에서 dequeue를 반복할수록 배열 앞쪽 공간이 비어도 재사용을 못 하는 문제가 생긴다. **원형 큐**는 배열의 **끝과 처음을 연결**해 비는 앞 공간을 다시 채워 쓴다. `front`와 `rear` 인덱스를 **모듈러 연산(`% capacity`)**으로 회전시키는 것이 핵심이다.
>
> ```
> 용량 5 ring buffer. (f=front, r=rear, 빈칸=.)
> 초기 enqueue 4개:  [10][20][30][40][. ]   f=0, r=4
> dequeue 2번:       [. ][. ][30][40][. ]   f=2, r=4
> enqueue 50,60:     [60][. ][30][40][50]   r가 끝을 지나 0으로 '회전' (r=(4+1)%5=0 ...)
>                     ^ 앞쪽 빈 공간 재사용 = 원형의 이점
> ```
>
> 운영체제의 입출력 버퍼, 네트워크 패킷 버퍼, 스트리밍 데이터 처리에서 핵심으로 쓰인다. LeetCode #622가 바로 이 자료구조를 직접 구현하는 문제다.
>
> **모노토닉 덱 (Monotonic Deque)**
>
> Day 7의 모노토닉 스택처럼, **덱 안의 원소가 항상 단조(증가/감소)를 유지**하도록 관리하는 기법이다. **슬라이딩 윈도우(sliding window)에서 구간 최댓값/최솟값을 O(n)에 구할 때** 결정적이다.
>
> 핵심: 덱에 **인덱스**를 저장한다. 새 원소가 들어올 때
> 1. **뒤에서**: 새 값보다 작은(최댓값을 구한다면) 원소들은 더 이상 답이 될 수 없으니 `pop`으로 제거.
> 2. **앞에서**: 윈도우 범위를 벗어난(오래된) 인덱스는 `popleft`로 제거.
> 3. 그러면 **덱의 맨 앞(`q[0]`)이 항상 현재 윈도우의 최댓값 인덱스**가 된다.
>
> 각 원소가 최대 한 번 push, 한 번 pop되므로 전체 **O(n)**. 양끝을 모두 써야 하므로 **스택이 아니라 덱**이 필요하다. LeetCode #239 Sliding Window Maximum이 대표 문제다.
>
> ```
> nums=[1,3,-1,-3,5], k=3 (창 크기 3), 덱엔 인덱스 저장(값 내림차순 유지)
> i=0 v=1  덱=[0]
> i=1 v=3  뒤의 1<3 제거 -> 덱=[1]
> i=2 v=-1 덱=[1,2]  창[1,3,-1] 최대=nums[1]=3
> i=3 v=-3 덱=[1,2,3] 앞(1)이 범위밖? i-k=0 -> 1>0 유지. 창 최대=nums[1]=3
> i=4 v=5  뒤 전부<5 제거, 앞(1)범위밖 제거 -> 덱=[4] 창 최대=nums[4]=5
> ```
>
> **큐가 빛나는 상황:**
>
> 1. **BFS (너비 우선 탐색, Day 26):** 가까운 노드부터 차례로 방문 -> 큐가 핵심. 최단 거리 탐색의 토대.
> 2. **작업/요청 대기열:** 프린터 인쇄 큐, 메시지 큐, 운영체제 작업 스케줄링.
> 3. **시뮬레이션:** 순서대로 처리되는 모든 대기 상황(은행 창구, 콜센터 등).
> 4. **슬라이딩 윈도우 + 덱:** 구간 최대/최소 O(n)(모노토닉 덱).
> 5. **최근 N개 관리:** `deque(maxlen=N)`으로 가장 오래된 것을 자동으로 밀어내는 버퍼.

> [!chart]- 3. 복잡도 (시간/공간)
> | 연산 | `collections.deque` | `list` (큐로 쓸 때) | 비고 |
> |---|---|---|---|
> | 뒤에 넣기 `append` | O(1) | 분할상환 O(1) | |
> | 앞에서 빼기 `popleft` / `pop(0)` | **O(1)** | **O(n)** | list는 시프트 발생 |
> | 앞에 넣기 `appendleft` / `insert(0,x)` | **O(1)** | **O(n)** | list는 시프트 발생 |
> | 뒤에서 빼기 `pop` | O(1) | O(1) | |
> | 앞/뒤 조회 `q[0]`, `q[-1]` | O(1) | O(1) | |
> | 임의 인덱스 `q[i]` | **O(n)** | O(1) | deque는 중간 접근 느림 |
> | 전체 저장 | O(n) | O(n) | n = 원소 수 |
>
> **요약:** "앞에서 빼는" 큐/덱 용도라면 **무조건 `deque`**. 중간 임의 접근이 잦으면 `list`.

> [!tip]- 💡 이해를 돕는 팁
> - **"먼저 온 것부터(선착순)" 키워드를 만나면 큐**: 대기열, 순서대로 처리, 가까운 것부터(BFS). 반대로 "가장 최근 것부터"는 스택(Day 7)이다.
>   - 참고: [Queue (FIFO) 개념 (GeeksforGeeks)](https://www.geeksforgeeks.org/queue-data-structure/)
>
> - **파이썬 큐는 list가 아니라 deque**: 공식 문서가 `list.pop(0)`은 O(n)이라 큐에 부적합하다고 명시하고, "큐에는 `collections.deque`를 쓰라"고 안내한다.
>   - 참고: [Using lists as queues (Python 공식 튜토리얼)](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues)
>
> - **deque는 양끝 O(1), 중간 접근 O(n)**: 이중 연결 블록 구조라 양끝은 빠르지만 `q[i]`(중간)는 느리다. 양끝만 쓰면 deque, 인덱싱이 잦으면 list로 판단한다.
>   - 참고: [collections.deque (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.deque)
>
> - **`maxlen`은 슬라이딩 버퍼의 마법**: `deque(maxlen=N)`은 꽉 찬 상태에서 한쪽으로 넣으면 반대쪽이 자동으로 빠진다. "최근 N개 로그/이동평균" 같은 문제를 한 줄로 만든다.
>   - 참고: [deque maxlen 동작 (Real Python)](https://realpython.com/python-deque/)
>
> - **모노토닉 덱은 "각 원소 최대 1번 push/pop"이라 O(n)**: while이 안에 있어도 전체 연산은 2n을 넘지 않는다(분할 상환). 슬라이딩 윈도우 최대/최소의 표준 도구다.
>   - 참고: [Sliding Window Maximum 풀이 (LeetCode #239, algo.monster)](https://algo.monster/liteproblems/239)
>
> - **큐 두 개로 스택, 스택 두 개로 큐**: 면접 단골. LeetCode #232(스택으로 큐), #225(큐로 스택)는 "왜 amortized O(1)인가"를 설명할 수 있어야 한다.
>   - 참고: [Implement Queue using Stacks (LeetCode #232)](https://leetcode.com/problems/implement-queue-using-stacks/)

> [!warning]- ⚠️ 개발자 필수 상식
> 1. **큐에 `list.pop(0)`은 금지**: 가장 흔한 코테 시간초과(TLE) 원인 중 하나다. 입력이 크면 O(n^2)이 되어 통과 못 한다. 큐는 **반드시 `deque.popleft()`**(O(1)).
>
> 2. **`appendleft`/`insert(0,x)`도 마찬가지**: 앞에 넣을 일이 있으면 `list.insert(0,x)`(O(n)) 대신 `deque.appendleft(x)`(O(1)).
>
> 3. **빈 큐에서 `popleft`/`pop` 금지**: 빈 `deque`에서 `popleft()`는 `IndexError: pop from an empty deque`. **반드시 `if q:`로 먼저 확인**하거나 `while q:` 루프 조건으로 막는다.
>
> 4. **`deque`는 인덱싱이 느리다**: `q[len(q)//2]` 같은 중간 접근은 O(n)이다. 양끝만 쓸 때만 deque의 이점이 살아난다. 정렬·이진탐색처럼 임의 접근이 필요하면 `list`를 쓴다.
>
> 5. **덱은 스택도 큐도 된다**: `append`+`pop`이면 스택(LIFO), `append`+`popleft`면 큐(FIFO). 한 자료형으로 둘 다 되니, 헷갈리면 deque로 통일해도 무방하다(스택은 list가 더 직관적이지만).
>
> 6. **`q[0]`은 제거하지 않는다**: front를 **보기만** 한다. "확인 후 조건에 따라 빼기"는 `q[0]`로 보고 조건 충족 시 `q.popleft()`하는 2단계로(프로세스/우선순위 시뮬레이션의 패턴).
>
> 7. **BFS의 본체는 큐**: BFS에서 큐 대신 스택을 쓰면 DFS가 된다. "가까운 것부터(최단)"가 필요하면 반드시 큐여야 함을 기억한다(Day 26).
>
> 8. **`queue.Queue`와 혼동 주의**: 표준 라이브러리에 `queue.Queue`도 있지만 이는 **스레드 간 통신용(thread-safe)**이라 락 오버헤드가 있다. **단일 스레드 알고리즘 풀이에는 `collections.deque`**가 정답이다. 코테에서 `queue.Queue`를 쓰면 느려서 손해다.

> [!example]- 예제 코드
> ```python
> from collections import deque
>
> # 1) 큐 (FIFO): 뒤로 넣고 앞에서 뺀다
> q = deque()
> q.append(10)          # enqueue
> q.append(20)
> x = q.popleft()       # dequeue -> 10
> front = q[0]          # peek (제거 안 함)
>
> # 2) 덱 (양끝): 앞/뒤 모두 O(1)
> dq = deque([1, 2, 3])
> dq.appendleft(0)      # 앞에 넣기 -> deque([0, 1, 2, 3])
> dq.append(4)          # 뒤에 넣기 -> deque([0, 1, 2, 3, 4])
> dq.popleft()          # 앞에서 빼기 -> 0
> dq.pop()              # 뒤에서 빼기 -> 4
>
> # 3) maxlen: 최근 N개만 유지 (오래된 것 자동 제거)
> recent = deque(maxlen=3)
> for v in [1, 2, 3, 4, 5]:
>     recent.append(v)  # 항상 최근 3개만: 끝엔 deque([3, 4, 5])
>
> # 4) BFS 표준 골격 (Day 26 예고)
> def bfs(start, graph):
>     visited = {start}
>     q = deque([start])
>     order = []
>     while q:
>         node = q.popleft()        # 가까운 것부터
>         order.append(node)
>         for nxt in graph[node]:
>             if nxt not in visited:
>                 visited.add(nxt)
>                 q.append(nxt)
>     return order
>
> # 5) 모노토닉 덱 골격 (슬라이딩 윈도우 최댓값)
> def max_sliding_window(nums, k):
>     dq = deque()                  # 인덱스 저장, 값 내림차순 유지
>     ans = []
>     for i, v in enumerate(nums):
>         while dq and nums[dq[-1]] < v:   # 뒤에서 작은 값 제거
>             dq.pop()
>         dq.append(i)
>         if dq[0] <= i - k:               # 앞에서 범위 벗어난 것 제거
>             dq.popleft()
>         if i >= k - 1:
>             ans.append(nums[dq[0]])      # 맨 앞 = 현재 창 최댓값
>     return ans
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | 기능개발 | [프로그래머스 #42586](https://school.programmers.co.kr/learn/courses/30/lessons/42586) | 🟢기초 | 큐/시뮬레이션 |
> | 2 | 프로세스 | [프로그래머스 #42587](https://school.programmers.co.kr/learn/courses/30/lessons/42587) | 🟡중급 | 큐/시뮬레이션 |
> | 3 | Implement Queue using Stacks | [LeetCode #232](https://leetcode.com/problems/implement-queue-using-stacks/) | 🟡중급 | 자료구조 설계 |
> | 4 | Design Circular Queue | [LeetCode #622](https://leetcode.com/problems/design-circular-queue/) | 🟡중급 | 원형 큐 설계 |
> | 5 | Sliding Window Maximum | [LeetCode #239](https://leetcode.com/problems/sliding-window-maximum/) | 🔴심화 | 모노토닉 덱 |
> | 6 | 두 큐 합 같게 만들기 | [프로그래머스 #118667](https://school.programmers.co.kr/learn/courses/30/lessons/118667) | ⚫기출 | 덱/투포인터 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-07-stack/concept|Day 07 — 스택]]
- ➡️ 다음: [[day-09-hashing/concept|Day 09 — 해시 dict/set]]
- 🧭 관련:
  - [[day-07-stack/concept|Day 07 — 스택]] — LIFO vs FIFO 비교
  - [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]] — collections.deque
- 🗺️ 지도: [[Phase-1 MOC]] · [[00 Algorithm MOC]]
