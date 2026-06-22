# Day 11 — 트리 기본 (Tree Basics) 연습문제

> 출처는 **LeetCode**와 **프로그래머스**만 사용한다.
> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 풀이 코드는 [solutions.py](solutions.py) 참고 (각 문제 다중 접근 + assert 자체 테스트).

---

## 1. Maximum Depth of Binary Tree 🟢기초
- **출처:** [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
- **요약:** 이진 트리의 루트가 주어질 때 **최대 깊이**(루트에서 가장 먼 잎까지의 노드 수)를 반환.
- **핵심 아이디어:** 재귀 기본 틀. `depth(node) = 1 + max(depth(left), depth(right))`, 빈 노드는 0.
- **힌트:** BFS로 레벨 수를 세도 된다. 둘 다 O(N).

## 2. Invert Binary Tree 🟢기초
- **출처:** [LeetCode #226](https://leetcode.com/problems/invert-binary-tree/)
- **요약:** 트리를 좌우로 **뒤집어**(거울상) 루트를 반환.
- **핵심 아이디어:** 각 노드에서 `left`와 `right`를 **스왑**하고, 두 서브트리에 재귀.
- **힌트:** 파이썬은 `node.left, node.right = node.right, node.left` 한 줄로 스왑. BFS/DFS 모두 가능.

## 3. Same Tree 🟢기초
- **출처:** [LeetCode #100](https://leetcode.com/problems/same-tree/)
- **요약:** 두 이진 트리가 **구조와 값**이 모두 같은지 판정.
- **핵심 아이디어:** 두 트리를 **동시에** 순회. 둘 다 None이면 True, 한쪽만 None이거나 값이 다르면 False, 아니면 좌·우 동시 재귀.
- **힌트:** 경계: 둘 다 빈 트리는 같은 트리(True).

## 4. Binary Tree Inorder Traversal 🟢기초
- **출처:** [LeetCode #94](https://leetcode.com/problems/binary-tree-inorder-traversal/)
- **요약:** 이진 트리의 **중위 순회**(왼→부모→오) 결과를 리스트로 반환.
- **핵심 아이디어:** 재귀 또는 **명시적 스택**으로 반복 구현(팔로업 단골).
- **힌트:** BST를 중위 순회하면 오름차순. 반복 버전은 "왼쪽으로 끝까지 내려가며 스택에 쌓기 → pop 후 오른쪽으로".

## 5. Symmetric Tree 🟡중급
- **출처:** [LeetCode #101](https://leetcode.com/problems/symmetric-tree/)
- **요약:** 트리가 자기 자신을 거울에 비춘 듯 **좌우 대칭**인지 판정.
- **핵심 아이디어:** 두 서브트리가 **서로의 거울**인지 검사하는 도우미 함수. `mirror(a, b)`: 값 같고, `a.left ~ b.right`, `a.right ~ b.left`.
- **힌트:** "같은 트리(#100)"의 변형 — 비교 방향만 교차시킨다.

## 6. Balanced Binary Tree 🟡중급
- **출처:** [LeetCode #110](https://leetcode.com/problems/balanced-binary-tree/)
- **요약:** 모든 노드에서 **좌우 서브트리 높이 차가 1 이하**인지(높이 균형) 판정.
- **핵심 아이디어:** 높이를 구하면서 **동시에** 불균형을 감지. 불균형이면 -1 같은 신호를 위로 전파해 O(N)에 끝낸다(매 노드 높이를 따로 구하면 O(N^2)).
- **힌트:** 후위 순회(자식 높이부터). 한 번이라도 -1이 올라오면 전체 False.

## 7. Diameter of Binary Tree 🟡중급
- **출처:** [LeetCode #543](https://leetcode.com/problems/diameter-of-binary-tree/)
- **요약:** 트리에서 임의의 두 노드를 잇는 **가장 긴 경로의 간선 수**(지름)를 반환. 경로가 루트를 안 지날 수도 있다.
- **핵심 아이디어:** 각 노드를 "꺾이는 정점"으로 보면 그 지점 경로 길이는 `왼쪽 높이 + 오른쪽 높이`. 높이 계산 중 전역 최댓값을 갱신.
- **힌트:** 높이를 반환하는 DFS에 `self.best = max(self.best, lh + rh)` 한 줄을 끼운다.

## 8. Convert Sorted Array to Binary Search Tree 🟡중급
- **출처:** [LeetCode #108](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/)
- **요약:** 오름차순 정렬 배열로 **높이 균형 BST**를 만든다.
- **핵심 아이디어:** **가운데 원소를 루트**로 잡고, 왼쪽 절반→왼쪽 서브트리, 오른쪽 절반→오른쪽 서브트리로 재귀(분할정복).
- **힌트:** 중위 순회하면 다시 원래 정렬 배열이 나와야 한다(검증 트릭).

## 9. Lowest Common Ancestor of a Binary Search Tree 🔴심화
- **출처:** [LeetCode #235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)
- **요약:** BST에서 두 노드 p, q의 **최소 공통 조상(LCA)** 을 반환.
- **핵심 아이디어:** **BST 성질** 활용. 두 값이 모두 현재 노드보다 작으면 왼쪽, 모두 크면 오른쪽으로 이동. 갈라지는(또는 한쪽이 현재 노드인) 첫 지점이 LCA.
- **힌트:** 일반 이진 트리 LCA(#236)와 달리 정렬 성질로 O(h)에 끝난다. 반복문으로 O(1) 공간 가능.

## 10. 길 찾기 게임 ⚫기출 (카카오 2019 블라인드)
- **출처:** [프로그래머스 #42892](https://school.programmers.co.kr/learn/courses/30/lessons/42892)
- **요약:** 노드들의 (x, y) 좌표가 주어진다. **y가 큰 노드가 위, x로 좌우를 가르는** 이진 트리를 만들고, **전위 순회**와 **후위 순회** 결과(노드 번호 순서)를 반환.
- **핵심 아이디어:** y 내림차순(같으면 x 오름차순)으로 정렬하면 삽입 순서가 곧 위에서 아래 순서. x를 BST 키처럼 비교하며 삽입한 뒤 전위·후위 순회.
- **힌트:** 파이썬 기본 재귀 한계(약 1000)에 걸릴 수 있어 `sys.setrecursionlimit`를 올리거나 순회를 반복문으로 구현한다(노드 최대 10,000개).

---

### 추천 풀이 순서
1) #104 → #226 → #100 → #94 (재귀 기본 틀 + 순회 감 잡기)
2) #101 → #110 → #543 (재귀 응용: 대칭·높이·경로)
3) #108 → #235 (BST 성질)
4) 프로그래머스 #42892 (기출 종합: 트리 구성 + 순회)
