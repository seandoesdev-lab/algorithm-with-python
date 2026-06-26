---
day: 15
phase: 1-data-structures
title: 자료구조 종합 복습 (Data Structures Review) — 연습문제
tags: [phase/1, topic/review, problems]
---

# Day 15 — 연습문제 (자료구조 종합 복습)

> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 풀이 코드는 [solutions.py](solutions.py) 참고. **출처는 LeetCode·프로그래머스만.**
> 이 세트의 목적은 "푸는 것"보다 **문제 신호를 보고 어떤 자료구조를 꺼낼지 1초 만에 판단**하는 것이다.

---

## 1. Valid Parentheses 🟢

- **출처:** [LeetCode #20](https://leetcode.com/problems/valid-parentheses/)
- **자료구조:** 스택 (Stack)
- **요약:** `(`, `)`, `{`, `}`, `[`, `]`로 이루어진 문자열이 올바르게 짝지어졌는지 판별하라.
- **예:** `"()[]{}"` → `True`, `"([)]"` → `False`
- **신호:** "괄호/짝/중첩" → 스택. 여는 괄호는 push, 닫는 괄호를 만나면 스택 맨 위와 짝이 맞는지 확인. 끝났을 때 스택이 비어 있어야 한다.

## 2. Implement Queue using Stacks 🟢

- **출처:** [LeetCode #232](https://leetcode.com/problems/implement-queue-using-stacks/)
- **자료구조:** 스택 2개로 큐(FIFO) 구현
- **요약:** 스택 연산(push/pop/peek)만으로 FIFO 큐를 구현하라.
- **힌트:** `in` 스택과 `out` 스택을 둔다. pop/peek 때 `out`이 비어 있으면 `in`을 통째로 뒤집어 옮긴다. 각 원소가 정확히 한 번씩만 옮겨지므로 분할 상환(amortized) O(1). 스택과 큐의 관계를 몸으로 이해하는 문제.

## 3. Two Sum 🟢

- **출처:** [LeetCode #1](https://leetcode.com/problems/two-sum/)
- **자료구조:** 해시맵 (dict)
- **요약:** 배열에서 더해서 `target`이 되는 두 수의 인덱스를 반환하라.
- **예:** `nums=[2,7,11,15], target=9` → `[0,1]`
- **신호:** "두 수의 합/짝", "본 적 있는 값". 이중 루프 O(n²) 대신, 순회하며 `target - x`를 이미 본 적 있는지 dict로 확인하면 O(n). 코테 해시의 출발점.

## 4. Reverse Linked List 🟢

- **출처:** [LeetCode #206](https://leetcode.com/problems/reverse-linked-list/)
- **자료구조:** 연결 리스트 (Linked List)
- **요약:** 단일 연결 리스트를 뒤집어라.
- **예:** `1->2->3->4->5` → `5->4->3->2->1`
- **힌트:** `prev`, `cur` 두 포인터로 방향을 하나씩 뒤집는다(반복 O(1) 공간). **다음 노드를 끊기 전에 반드시 임시 변수에 저장**(포인터 꼬임 1순위 버그). 재귀 풀이와 비교해 보면 좋다.

## 5. Maximum Depth of Binary Tree 🟢

- **출처:** [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
- **자료구조:** 트리 (Tree)
- **요약:** 이진 트리의 최대 깊이(루트에서 가장 먼 리프까지 노드 수)를 구하라.
- **힌트:** 깊이는 `1 + max(왼쪽 깊이, 오른쪽 깊이)`로 재귀 DFS가 가장 간결. 큐 BFS로 레벨 수를 세도 된다. **DFS=재귀/스택, BFS=큐**라는 트리 순회의 두 축을 확인.

## 6. Daily Temperatures 🟡

- **출처:** [LeetCode #739](https://leetcode.com/problems/daily-temperatures/)
- **자료구조:** 단조 스택 (Monotonic Stack)
- **요약:** 각 날짜마다 "더 따뜻한 날"이 올 때까지 며칠 기다려야 하는지 배열로 반환하라.
- **예:** `[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`
- **신호:** "이전보다 큰 다음 원소", "온도/주가". 아직 더 큰 값을 못 만난 인덱스를 스택에 쌓아 두고, 더 큰 값이 오면 스택에서 꺼내며 거리(일수)를 채운다. O(n). "다음 큰 원소(next greater element)" 패턴의 대표.

## 7. Top K Frequent Elements 🟡

- **출처:** [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/)
- **자료구조:** 해시(Counter) + 힙(또는 버킷 정렬)
- **요약:** 가장 빈번하게 등장한 상위 `k`개 원소를 반환하라.
- **예:** `nums=[1,1,1,2,2,3], k=2` → `[1,2]`
- **힌트:** `Counter`로 빈도를 센 뒤, 크기 K 힙(`heapq.nlargest`)으로 O(n log k). 빈도를 인덱스로 쓰는 **버킷 정렬**이면 O(n)까지. 해시와 힙이 결합되는 전형.

## 8. Kth Largest Element in a Stream 🟢

- **출처:** [LeetCode #703](https://leetcode.com/problems/kth-largest-element-in-a-stream/)
- **자료구조:** 크기 K 최소 힙
- **요약:** 스트림에 값이 계속 추가될 때, 매번 K번째로 큰 값을 반환하는 클래스를 구현하라.
- **힌트:** **크기를 항상 K로 유지하는 최소 힙**을 두면, 힙의 최솟값(`heap[0]`)이 곧 K번째로 큰 값. 추가될 때마다 push 후 크기가 K를 넘으면 pop. 추가당 O(log k). "스트림에서 순위 유지" 신호.

## 9. 기능개발 🟡 ⚫(프로그래머스)

- **출처:** [프로그래머스 #42586](https://school.programmers.co.kr/learn/courses/30/lessons/42586)
- **자료구조:** 큐 (앞 작업이 끝나야 함께 배포)
- **요약:** 각 기능의 진도 `progresses`와 속도 `speeds`가 주어진다. 앞 기능이 배포될 때, 그보다 먼저 끝난 뒤 기능들이 함께 배포된다. 각 배포 회차마다 배포되는 기능 수를 반환하라.
- **예:** `progresses=[93,30,55], speeds=[1,30,5]` → `[2,1]`
- **힌트:** 각 작업의 완료 일수 = `ceil((100 - 진도) / 속도)`. 앞에서부터 "현재 기준 완료일 이하면 같은 배포로 묶고, 더 크면 새 배포 시작". 큐(FIFO)처럼 앞에서부터 순서대로 처리하는 사고가 핵심.

## 10. 베스트앨범 🟡 ⚫(프로그래머스)

- **출처:** [프로그래머스 #42579](https://school.programmers.co.kr/learn/courses/30/lessons/42579)
- **자료구조:** 해시(그룹핑) + 정렬
- **요약:** 장르별 총 재생수가 높은 장르 순으로, 각 장르에서 가장 많이 재생된 곡 최대 2개씩 모아 베스트앨범의 곡 인덱스를 반환하라.
- **힌트:** dict로 (1) 장르별 총 재생수, (2) 장르별 (재생수, 인덱스) 목록을 만든다. 장르는 총 재생수 내림차순, 장르 내 곡은 **(재생수 내림차순, 인덱스 오름차순)**으로 정렬해 상위 2곡. 동점 처리(인덱스 작은 곡 우선)가 함정.

---

## 풀이 전략 요약 (신호 → 자료구조)

| 문제의 신호 | 떠올릴 자료구조 | 이 세트의 예 |
|---|---|---|
| "괄호/짝/중첩", "되돌리기" | 스택 | #20 |
| "스택만으로 FIFO" | 스택 2개 = 큐 | #232 |
| "두 수의 합", "본 적 있나" | 해시(dict) | #1 |
| "포인터로 노드 재배선" | 연결 리스트 | #206 |
| "트리 깊이/레벨" | 재귀(DFS)·큐(BFS) | #104 |
| "다음으로 큰/작은 원소" | 단조 스택 | #739 |
| "빈도수 상위 K개" | 해시(Counter)+힙 | #347 |
| "스트림에서 K번째 큰 값" | 크기 K 힙 | #703 |
| "앞 순서대로 묶어 처리" | 큐 | #42586 |
| "그룹별 상위 + 정렬" | 해시 그룹핑 + 정렬 | #42579 |

> 관련 개념: [[concept]] · 각 자료구조의 자세한 설명은 [[Phase-1 MOC]]의 Day 06~14 참고.
