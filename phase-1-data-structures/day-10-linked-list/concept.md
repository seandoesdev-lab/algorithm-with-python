---
day: 10
phase: 1-data-structures
title: 연결 리스트 (Linked List)
category: [자료구조, 연결리스트]
difficulty: 기초
status: done
prev: "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
next: "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
related:
  - "[[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]"
  - "[[day-07-stack/concept|Day 07 — 스택]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
sources:
  - https://leetcode.com/problems/reverse-linked-list/
  - https://leetcode.com/problems/merge-two-sorted-lists/
  - https://leetcode.com/problems/middle-of-the-linked-list/
  - https://leetcode.com/problems/linked-list-cycle/
  - https://leetcode.com/problems/remove-nth-node-from-end-of-list/
  - https://leetcode.com/problems/add-two-numbers/
  - https://leetcode.com/problems/linked-list-cycle-ii/
  - https://leetcode.com/problems/palindrome-linked-list/
  - https://leetcode.com/problems/intersection-of-two-linked-lists/
tags: [phase/1, topic/linked-list]
---

# Day 10 — 연결 리스트 (Linked List)

> [!abstract] 한눈 요약 (TL;DR)
> **연결 리스트(linked list)**는 데이터를 담은 **노드(node)**들이 "다음 노드를 가리키는 포인터"로 줄줄이 이어진 자료구조다. 배열과 달리 **연속된 메모리가 필요 없어** 중간 삽입·삭제가 노드 연결만 바꾸면 **O(1)**이지만, **인덱스 임의 접근이 안 돼** k번째 원소를 찾으려면 앞에서부터 **O(k)** 걸어야 한다. 코테에서 직접 연결 리스트를 쓸 일은 드물지만(파이썬은 `list`·`deque`로 대체), **LeetCode 단골 유형**이고 **포인터 조작·두 포인터(fast/slow)** 사고력을 길러준다. `head`부터 `next`를 따라가며 "포인터를 어디로 돌릴지"가 모든 문제의 핵심이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **연결 리스트**는 각 원소를 **노드(node)**라는 작은 상자에 담고, 그 상자에 **"다음 상자의 위치"**(참조/포인터)를 함께 적어두어 줄줄이 잇는 자료구조다. 노드 하나는 보통 두 칸으로 이뤄진다: 값을 담는 `val`(또는 `data`)과 다음 노드를 가리키는 `next`.
>
> 일상 비유는 **보물찾기 쪽지**다. 첫 쪽지(`head`)를 받으면 거기에 보물(값)과 "다음 쪽지는 화단 밑에"라는 안내(`next`)가 적혀 있다. 안내를 따라가다 마지막 쪽지에는 "다음 없음"(`None`)이 적혀 있어 끝을 안다. **전체 위치를 한 번에 알 수 없고 반드시 처음부터 따라가야** 한다는 점이 배열과의 결정적 차이다.
>
> ```
>  head
>   |
>   v
> +----+----+    +----+----+    +----+----+
> | 10 |  *-+--->| 20 |  *-+--->| 30 | / |   (/ = None, 끝)
> +----+----+    +----+----+    +----+----+
>  val  next      val  next      val  next
> ```
>
> **배열(list) vs 연결 리스트 — 무엇이 다른가**
>
> | 구분 | 배열(파이썬 `list`) | 연결 리스트 |
> |---|---|---|
> | 메모리 배치 | **연속**된 한 덩어리 | 노드가 **흩어져** 있고 포인터로 연결 |
> | k번째 접근 | **O(1)** (주소 계산) | **O(k)** (앞에서부터 이동) |
> | 맨 앞 삽입/삭제 | O(n) (전부 밀기) | **O(1)** (포인터만 변경) |
> | 중간 삽입/삭제 | O(n) | **O(1)** (단, 해당 위치 노드를 이미 알 때) |
> | 추가 메모리 | 적음 | 노드마다 `next` 포인터분 더 듦 |
>
> **종류**
>
> - **단일 연결 리스트(singly linked list):** `next`만 있음. 한 방향으로만 이동.
> - **이중 연결 리스트(doubly linked list):** `prev`+`next`. 양방향 이동 가능(파이썬 `collections.deque`의 내부 구조).
> - **원형 연결 리스트(circular):** 마지막 노드의 `next`가 다시 `head`를 가리킴.

> [!gear]- 2. 동작 원리 (How It Works)
> 모든 연산은 **"어느 포인터를 어디로 다시 연결하느냐"**로 귀결된다. 파이썬에는 표준 연결 리스트 클래스가 없으므로 노드를 직접 정의한다.
>
> ```python
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val
>         self.next = next
> ```
>
> **(1) 순회 (Traversal)** — `head`에서 시작해 `next`가 `None`이 될 때까지 이동.
>
> ```
> cur = head
> while cur is not None:
>     # cur.val 처리
>     cur = cur.next
> ```
>
> **(2) 맨 앞 삽입 (Prepend, O(1))** — 새 노드의 `next`를 기존 `head`로, `head`를 새 노드로.
>
> ```
> 삽입 전:        head -> [20] -> [30] -> None
> new=[10]; new.next = head;  head = new
> 삽입 후:  head -> [10] -> [20] -> [30] -> None
> ```
>
> **(3) 중간 삭제 (O(1), 앞 노드를 알 때)** — 지울 노드의 **앞 노드(prev)**의 `next`를 지울 노드의 `next`로 건너뛰게 한다.
>
> ```
> 삭제 전: ... [A] -> [B(삭제)] -> [C] ...
> prev=A;  A.next = B.next   (즉 A.next = C)
> 삭제 후: ... [A] ---------> [C] ...   (B는 더 이상 도달 불가)
> ```
>
> **(4) 뒤집기 (Reverse, O(n))** — 핵심 코테 기법. 세 포인터 `prev/cur/nxt`로 화살표를 하나씩 뒤로 돌린다.
>
> ```
> prev = None
> cur = head
> while cur:
>     nxt = cur.next   # 다음 노드 백업(끊기 전에)
>     cur.next = prev  # 화살표 반대로
>     prev = cur       # prev 한 칸 전진
>     cur = nxt        # cur 한 칸 전진
> # 끝나면 prev가 새 head
> ```
>
> **(5) 더미 헤드 (Dummy / Sentinel Node)** — `head`가 바뀌거나 비어 있는 경우를 따로 처리하지 않으려고 **가짜 노드 하나**를 앞에 둔다. 삽입·삭제·병합에서 코드가 크게 단순해진다.
>
> ```
> dummy = ListNode(0, head)   # dummy.next = head
> # ... dummy 뒤에서 자유롭게 조작 ...
> return dummy.next           # 진짜 head 반환
> ```
>
> **(6) 두 포인터: 빠른/느린 (Fast & Slow)** — `slow`는 한 칸, `fast`는 두 칸씩. `fast`가 끝에 닿으면 `slow`는 **중앙**. 사이클 탐지·중간 찾기의 핵심.
>
> ```
> slow = fast = head
> while fast and fast.next:
>     slow = slow.next        # +1
>     fast = fast.next.next   # +2
> # slow == 중앙 노드
> ```

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> | 연산 | 단일 연결 리스트 | 배열(`list`) | 설명 |
> |---|---|---|---|
> | k번째 접근 (`get(k)`) | **O(n)** | **O(1)** | 리스트는 앞에서부터 걸어야 함 |
> | 맨 앞 삽입/삭제 | **O(1)** | O(n) | 포인터만 변경 vs 전부 밀기 |
> | 맨 뒤 삽입 | O(n) / O(1)* | 분할상환 O(1) | *tail 포인터가 있으면 O(1) |
> | 중간 삽입/삭제 | **O(1)**† | O(n) | †앞 노드를 이미 알고 있을 때 |
> | 탐색 (값으로 찾기) | O(n) | O(n) | 둘 다 순차 탐색 |
> | 전체 순회 | O(n) | O(n) | |
> | 공간 | O(n) (+포인터) | O(n) | 노드마다 `next` 오버헤드 |
>
> **요약:** 연결 리스트의 강점은 **맨 앞/중간의 O(1) 삽입·삭제**, 약점은 **O(n) 임의 접근**. 배열은 정반대다. "어디에 자주 끼워넣고 빼는가" vs "임의 위치에 자주 접근하는가"로 선택이 갈린다.
>
> > **현실 체크:** 파이썬 `list`는 맨 앞 삽입(`insert(0, x)`)이 O(n)이라 양끝 삽입·삭제가 잦으면 **`collections.deque`**(이중 연결 리스트 기반)가 정답이다. 즉 코테에서 "연결 리스트가 필요하다" = 대개 `deque`로 해결된다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"포인터를 끊기 전에 백업하라."** `cur.next = prev`로 화살표를 돌리면 원래의 다음 노드를 잃는다. 반드시 `nxt = cur.next`로 **먼저 저장**한 뒤 끊는다. 연결 리스트 버그 1순위가 "백업 안 하고 끊어서 리스트가 잘림"이다.
>   - 참고: [Reverse Linked List (LeetCode #206)](https://leetcode.com/problems/reverse-linked-list/)
>
> - **더미 헤드(dummy node)를 습관화하라.** "head가 바뀌나? 빈 리스트인가?" 같은 경계 조건을 따로 안 짜도 되게 해준다. 삽입·삭제·병합 문제는 거의 항상 `dummy = ListNode(0, head)`로 시작하면 깔끔하다.
>   - 참고: [Merge Two Sorted Lists (LeetCode #21)](https://leetcode.com/problems/merge-two-sorted-lists/)
>
> - **fast/slow 두 포인터는 만능 도구.** 중간 찾기, 사이클 탐지(플로이드 토끼와 거북이), 뒤에서 k번째 찾기가 전부 이 패턴이다. `while fast and fast.next:` 조건을 정확히 외워두면 절반은 푼 셈.
>   - 참고: [Floyd's Cycle Detection (GeeksforGeeks)](https://www.geeksforgeeks.org/floyds-cycle-finding-algorithm/)
>
> - **그림을 그려라.** 연결 리스트는 머릿속으로 포인터를 추적하면 반드시 헷갈린다. 노드 3~4개를 종이에 그리고 화살표를 직접 다시 그려보면 코드가 정확해진다.
>   - 참고: [Linked List study guide (LeetCode Discuss)](https://leetcode.com/discuss/post/2725900/linked-list-study-guide-by-sunyingbao-yi2w/)
>
> - **파이썬에서는 대부분 `list`/`deque`로 우회 가능.** 실전 코테(특히 프로그래머스)는 입력을 배열로 주므로 직접 노드를 만들 일이 적다. 그래도 LeetCode와 면접에서는 포인터 조작을 직접 요구하므로 원리는 반드시 익혀둔다.
>   - 참고: [collections.deque (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.deque)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **임의 접근이 O(n)이다.** `linked_list[k]` 같은 인덱싱이 없다. k번째 노드를 보려면 `head`부터 k번 `next`를 타야 한다. "연결 리스트에서 이진 탐색" 같은 건 의미 없다(중간으로 점프를 못 함).
>
> 2. **포인터를 끊기 전 백업은 필수.** `cur.next = prev` 전에 `nxt = cur.next`. 안 하면 뒷부분 전체가 가비지 컬렉션 대상이 되어 사라진다.
>
> 3. **`None` 체크를 빠뜨리지 말라.** `cur.next.next`에 접근하기 전에 `cur`와 `cur.next`가 `None`이 아닌지 확인. 빈 리스트(`head is None`), 노드 1개짜리 리스트는 항상 따로 테스트해야 하는 경계 케이스다.
>
> 4. **사이클(cycle)이 있으면 단순 순회는 무한 루프.** `while cur:`가 영원히 안 끝난다. 사이클 가능성이 있으면 fast/slow로 먼저 탐지하거나 방문 노드를 `set`에 기록(`id(node)` 또는 노드 자체)한다.
>
> 5. **더미 노드의 반환값은 `dummy.next`다.** `dummy`는 가짜이므로 절대 그대로 반환하지 말 것. 진짜 시작은 `dummy.next`.
>
> 6. **삭제는 "앞 노드"가 있어야 O(1)이다.** 지울 노드만 가지고는 그 앞 노드의 `next`를 못 고친다(단일 연결). 그래서 보통 `prev`를 함께 들고 순회한다. (값 복사 트릭으로 우회하는 특수 문제도 있다 — LeetCode #237.)
>
> 7. **파이썬 재귀 뒤집기는 깊이 제한 주의.** 연결 리스트를 재귀로 처리하면 길이만큼 콜 스택이 쌓여 긴 리스트에서 `RecursionError`가 날 수 있다(기본 한계 약 1000). 길이가 크면 반복문 버전을 쓴다.
>
> 8. **`deque`가 곧 이중 연결 리스트다.** 양끝 삽입·삭제가 O(1)인 이유가 내부적으로 doubly linked list라서다. "연결 리스트의 장점이 필요하다"면 직접 구현 전에 `deque`를 먼저 떠올린다.

> [!example]- 예제 코드 (Examples)
> ```python
> class ListNode:
>     def __init__(self, val=0, next=None):
>         self.val = val
>         self.next = next
>
> # 리스트 <-> 연결 리스트 변환 (테스트용)
> def build(values):
>     dummy = ListNode()
>     cur = dummy
>     for v in values:
>         cur.next = ListNode(v)
>         cur = cur.next
>     return dummy.next
>
> def to_list(head):
>     out = []
>     while head:
>         out.append(head.val)
>         head = head.next
>     return out
>
> # 1) 순회
> def traverse(head):
>     cur = head
>     while cur:
>         print(cur.val)   # 값 처리
>         cur = cur.next
>
> # 2) 뒤집기 (반복문, O(n) 시간 / O(1) 공간)
> def reverse(head):
>     prev = None
>     cur = head
>     while cur:
>         nxt = cur.next    # 끊기 전 백업
>         cur.next = prev   # 화살표 반대로
>         prev = cur
>         cur = nxt
>     return prev           # 새 head
>
> # 3) 중간 노드 찾기 (fast/slow)
> def middle(head):
>     slow = fast = head
>     while fast and fast.next:
>         slow = slow.next
>         fast = fast.next.next
>     return slow           # 짝수 길이면 두 번째 중앙
>
> # 4) 더미 헤드로 값이 target인 노드 모두 삭제
> def remove_all(head, target):
>     dummy = ListNode(0, head)
>     prev = dummy
>     cur = head
>     while cur:
>         if cur.val == target:
>             prev.next = cur.next   # 건너뛰기
>         else:
>             prev = cur
>         cur = cur.next
>     return dummy.next
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | Reverse Linked List | [LeetCode #206](https://leetcode.com/problems/reverse-linked-list/) | 🟢기초 | 뒤집기 |
> | 2 | Merge Two Sorted Lists | [LeetCode #21](https://leetcode.com/problems/merge-two-sorted-lists/) | 🟢기초 | 병합·더미 |
> | 3 | Middle of the Linked List | [LeetCode #876](https://leetcode.com/problems/middle-of-the-linked-list/) | 🟢기초 | fast/slow |
> | 4 | Linked List Cycle | [LeetCode #141](https://leetcode.com/problems/linked-list-cycle/) | 🟡중급 | 사이클 탐지 |
> | 5 | Remove Nth Node From End of List | [LeetCode #19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | 🟡중급 | 두 포인터·더미 |
> | 6 | Add Two Numbers | [LeetCode #2](https://leetcode.com/problems/add-two-numbers/) | 🟡중급 | 자릿수·올림 |
> | 7 | Linked List Cycle II | [LeetCode #142](https://leetcode.com/problems/linked-list-cycle-ii/) | 🔴심화 | 플로이드 |
> | 8 | Palindrome Linked List | [LeetCode #234](https://leetcode.com/problems/palindrome-linked-list/) | 🔴심화 | 중간+뒤집기 |
> | 9 | Intersection of Two Linked Lists | [LeetCode #160](https://leetcode.com/problems/intersection-of-two-linked-lists/) | ⚫기출 | 두 포인터 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-09-hashing/concept|Day 09 — 해시 dict/set]]
- ➡️ **다음(next):** [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 트리는 "노드+포인터"를 자식 방향으로 확장한 구조
- 🧭 **관련(related):**
  - [[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]] — 연속 메모리 vs 포인터 연결의 대비
  - [[day-07-stack/concept|Day 07 — 스택]] — 연결 리스트로 스택을 O(1)에 구현 가능
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — `deque`가 곧 이중 연결 리스트
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 노드·포인터 사고의 확장
- 🗺️ **지도(MOC):** [[Phase-1 MOC]] · [[00 Algorithm MOC]]
