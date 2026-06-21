# Day 10 — 연습문제: 연결 리스트 (Linked List)

> 출처는 **LeetCode**만 사용한다(연결 리스트는 노드 포인터를 직접 다루는 LeetCode의 대표 유형).
> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(빈출 인터뷰).
> 모든 문제의 노드 정의는 `class ListNode: def __init__(self, val=0, next=None)`.
> 해설 코드 → [solutions.py](solutions.py)

---

## 🟢 문제 1. Reverse Linked List
- **출처:** [LeetCode #206](https://leetcode.com/problems/reverse-linked-list/)
- **설명:** 단일 연결 리스트의 `head`가 주어진다. 리스트를 뒤집어 새로운 `head`를 반환하라.
- **예시:** `1->2->3->4->5` → `5->4->3->2->1`
- **힌트:** 세 포인터 `prev/cur/nxt`. `cur.next`를 끊기 **전에** `nxt = cur.next`로 백업한 뒤 `cur.next = prev`. 재귀 풀이도 가능하지만 긴 리스트에선 반복문이 안전.

## 🟢 문제 2. Merge Two Sorted Lists
- **출처:** [LeetCode #21](https://leetcode.com/problems/merge-two-sorted-lists/)
- **설명:** 정렬된 두 연결 리스트 `list1`, `list2`를 하나의 정렬된 리스트로 병합해 `head`를 반환하라.
- **예시:** `1->2->4`, `1->3->4` → `1->1->2->3->4->4`
- **힌트:** **더미 헤드(dummy)**를 두고 `tail` 포인터로 작은 값을 차례로 이어붙인다. 한쪽이 끝나면 남은 쪽을 통째로 연결. 마지막에 `dummy.next` 반환.

## 🟢 문제 3. Middle of the Linked List
- **출처:** [LeetCode #876](https://leetcode.com/problems/middle-of-the-linked-list/)
- **설명:** 연결 리스트의 중간 노드를 반환하라. 노드 수가 짝수면 **두 번째 중간 노드**를 반환.
- **예시:** `1->2->3->4->5` → `3`, `1->2->3->4->5->6` → `4`
- **힌트:** fast/slow 두 포인터. `fast`가 2칸, `slow`가 1칸씩 이동. `while fast and fast.next:`가 끝나면 `slow`가 중간.

## 🟡 문제 4. Linked List Cycle
- **출처:** [LeetCode #141](https://leetcode.com/problems/linked-list-cycle/)
- **설명:** 연결 리스트에 사이클(cycle)이 있는지 `True`/`False`로 판별하라.
- **힌트:** 두 가지 접근 — (a) 방문 노드를 `set`에 저장하며 중복 만나면 사이클(O(n) 공간). (b) **플로이드 토끼와 거북이**: fast/slow가 같아지면 사이클(O(1) 공간). 사이클이 없으면 fast가 `None`에 도달.

## 🟡 문제 5. Remove Nth Node From End of List
- **출처:** [LeetCode #19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)
- **설명:** 끝에서 n번째 노드를 삭제하고 `head`를 반환하라.
- **예시:** `1->2->3->4->5`, n=2 → `1->2->3->5`
- **힌트:** **더미 헤드** + 두 포인터. `fast`를 먼저 n칸 전진시킨 뒤, `fast`가 끝에 닿을 때까지 `slow`와 함께 이동하면 `slow`가 삭제 대상의 **앞 노드**가 된다. 한 번의 순회로 끝(one pass).

## 🟡 문제 6. Add Two Numbers
- **출처:** [LeetCode #2](https://leetcode.com/problems/add-two-numbers/)
- **설명:** 두 수를 **역순 자릿수**로 담은 연결 리스트 `l1`, `l2`가 주어진다. 두 수의 합을 같은 형식의 연결 리스트로 반환하라.
- **예시:** `2->4->3`(=342), `5->6->4`(=465) → `7->0->8`(=807)
- **힌트:** 더미 헤드 + `carry`(올림). 두 리스트를 동시에 돌며 `val1 + val2 + carry`를 10으로 나눠 자릿수/올림 갱신. 한쪽이 짧으면 0으로 취급. 마지막에 carry가 남으면 노드 추가.

## 🔴 문제 7. Linked List Cycle II
- **출처:** [LeetCode #142](https://leetcode.com/problems/linked-list-cycle-ii/)
- **설명:** 사이클이 시작되는 노드를 반환하라(없으면 `None`).
- **힌트:** 플로이드 알고리즘 2단계. (1) fast/slow로 만나는 지점을 찾는다. (2) 만난 뒤 한 포인터를 `head`로 옮기고 둘을 1칸씩 같이 전진 → 다시 만나는 곳이 사이클 시작점(수학적으로 증명됨). `set` 방식이 더 직관적이지만 O(n) 공간.

## 🔴 문제 8. Palindrome Linked List
- **출처:** [LeetCode #234](https://leetcode.com/problems/palindrome-linked-list/)
- **설명:** 연결 리스트가 회문(palindrome)인지 판별하라.
- **예시:** `1->2->2->1` → `True`, `1->2->3` → `False`
- **힌트:** O(1) 공간 풀이 — fast/slow로 **중간**을 찾고, 후반부를 **뒤집은** 뒤, 전반부와 값을 하나씩 비교. (간단히는 값을 리스트로 모아 `arr == arr[::-1]` 비교, O(n) 공간.)

## ⚫ 문제 9. Intersection of Two Linked Lists
- **출처:** [LeetCode #160](https://leetcode.com/problems/intersection-of-two-linked-lists/)
- **설명:** 두 연결 리스트가 합쳐지는(공유하는) 첫 노드를 반환하라(없으면 `None`). 노드 자체의 동일성으로 판단(값이 아님).
- **힌트:** 두 포인터 `pA`, `pB`를 각각 `headA`, `headB`에서 출발. 끝에 닿으면 상대 리스트의 head로 점프. 길이 차이가 상쇄되어 교차점(또는 동시에 `None`)에서 만난다. `set`에 한쪽 노드를 모아 다른 쪽에서 검색해도 됨(O(n) 공간).
