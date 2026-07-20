# Day 29 — 트리 순회·응용 (Tree Traversal): 연습문제

> 트리 순회의 세 축을 익히는 문제들이다. **① 전위/중위/후위(DFS)의 순회 시점 차이**,
> **② 레벨 순회(BFS)로 층을 다루는 법**, **③ 순회를 얹어 푸는 응용**(깊이·대칭·경로 합·
> BST 검증·LCA·트리 재구성)을 순서대로 밟는다.
> 출처는 **프로그래머스 / LeetCode만** 사용한다. 해설·코드는 [solutions.py](solutions.py).

## 문제 목록

| # | 문제 | 출처 | 난이도 | 핵심 유형 |
|---|---|---|---|---|
| 1 | Binary Tree Inorder Traversal | [LeetCode #94](https://leetcode.com/problems/binary-tree-inorder-traversal/) | 🟢기초 | 중위 순회(재귀·반복) |
| 2 | Maximum Depth of Binary Tree | [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 🟢기초 | 깊이(DFS·BFS) |
| 3 | Invert Binary Tree | [LeetCode #226](https://leetcode.com/problems/invert-binary-tree/) | 🟢기초 | 좌우 교환 재귀 |
| 4 | Same Tree | [LeetCode #100](https://leetcode.com/problems/same-tree/) | 🟢기초 | 동시 순회 비교 |
| 5 | Symmetric Tree | [LeetCode #101](https://leetcode.com/problems/symmetric-tree/) | 🟡중급 | 거울 대칭 재귀 |
| 6 | Binary Tree Level Order Traversal | [LeetCode #102](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟡중급 | 레벨 순회(BFS) |
| 7 | Path Sum | [LeetCode #112](https://leetcode.com/problems/path-sum/) | 🟡중급 | 루트-리프 경로 합 |
| 8 | Validate Binary Search Tree | [LeetCode #98](https://leetcode.com/problems/validate-binary-search-tree/) | 🟡중급 | 중위=오름차순 / 경계 전파 |
| 9 | Lowest Common Ancestor of a Binary Tree | [LeetCode #236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | 🔴심화 | 후위 순회 LCA |
| 10 | 길 찾기 게임 | [프로그래머스 #42892](https://school.programmers.co.kr/learn/courses/30/lessons/42892) | ⚫기출 | 트리 재구성 + 전위·후위 |

---

## 상세 설명

### 1. Binary Tree Inorder Traversal 🟢 (LeetCode #94)
이진 트리의 노드 값을 **중위(inorder: 왼쪽 → 루트 → 오른쪽)** 순서로 반환하라.
- **힌트:** 재귀는 세 줄이면 끝난다(왼쪽 재귀 → 값 기록 → 오른쪽 재귀). 반복 버전은 스택에 왼쪽 끝까지 쌓고, 꺼내 기록한 뒤 오른쪽으로 이동한다.
- **왜 중요한가:** 세 DFS 순회의 차이는 오직 "값을 기록하는 시점"임을 몸에 익히는 문제. 이후 모든 트리 문제의 뼈대다.

### 2. Maximum Depth of Binary Tree 🟢 (LeetCode #104)
루트에서 가장 먼 리프까지의 노드 수(최대 깊이)를 구하라.
- **힌트:** `depth(node) = 1 + max(depth(left), depth(right))`, 빈 노드는 0. BFS라면 층을 셀 때마다 +1.
- **함정:** 깊이(노드 수)와 높이(간선 수)를 문제마다 다르게 정의한다. 여기선 노드 수.

### 3. Invert Binary Tree 🟢 (LeetCode #226)
모든 노드의 왼쪽·오른쪽 자식을 서로 바꾼 트리를 반환하라(거울상).
- **힌트:** 각 노드에서 `left, right = invert(right), invert(left)`. 후위든 전위든 한 번씩 방문하면 된다.
- **비하인드:** "화이트보드에 이걸 못 풀어서 떨어졌다"는 유명한 트윗의 그 문제. 실전은 4줄이면 끝난다.

### 4. Same Tree 🟢 (LeetCode #100)
두 이진 트리가 **구조와 값이 모두 같은지** 판정하라.
- **힌트:** 두 노드를 동시에 내려가며 비교. 둘 다 None이면 True, 하나만 None이거나 값이 다르면 False, 아니면 좌·우 재귀 AND.

### 5. Symmetric Tree 🟡 (LeetCode #101)
트리가 자기 자신의 **거울 대칭**인지 판정하라.
- **힌트:** 루트의 왼쪽·오른쪽을 짝지어 검사하되, "왼쪽의 왼쪽 ↔ 오른쪽의 오른쪽", "왼쪽의 오른쪽 ↔ 오른쪽의 왼쪽"을 비교한다.
- **함정:** Same Tree와 헷갈리기 쉽다. 대칭은 **교차 비교**(left.left vs right.right)라는 점이 다르다.

### 6. Binary Tree Level Order Traversal 🟡 (LeetCode #102)
층(level)별로 노드 값을 묶어 2차원 리스트로 반환하라.
- **힌트:** BFS. `for _ in range(len(q))`로 **현재 층 크기만큼만** 꺼내면 층 경계가 자동으로 나뉜다.
- **응용 확장:** 지그재그 순회(#103), 우측면도(#199), 층 평균(#637)이 전부 이 골격의 변형이다.

### 7. Path Sum 🟡 (LeetCode #112)
루트에서 리프까지 값을 더한 합이 `targetSum`이 되는 경로가 있는지 판정하라.
- **힌트:** 내려가며 `targetSum - node.val`을 자식에게 넘기고, **리프에서** 남은 합이 노드 값과 같은지 본다.
- **함정:** "리프"는 자식이 **둘 다 없는** 노드다. 한쪽 자식만 없는 노드에서 멈추면 오답.

### 8. Validate Binary Search Tree 🟡 (LeetCode #98)
주어진 이진 트리가 유효한 **이진 탐색 트리(BST)**인지 판정하라.
- **접근 A (중위 순회):** BST의 중위 순회는 **엄격히 증가**한다. 순회하며 직전 값보다 큰지 검사.
- **접근 B (경계 전파):** 각 노드가 `(low, high)` 열린 구간 안에 있는지 확인하며 좌·우로 경계를 좁혀 내려간다.
- **함정:** "부모와만" 비교하면 틀린다. `[5,1,4,null,null,3,6]`에서 3은 부모 4보단 작지만 조상 5보다 작아 위반. 서브트리 전체 경계를 봐야 한다.

### 9. Lowest Common Ancestor of a Binary Tree 🔴 (LeetCode #236)
두 노드 p, q의 **최소 공통 조상(LCA)**을 구하라(일반 이진 트리, BST 아님).
- **힌트:** 후위 순회. 현재 노드가 p나 q이면 자신을 반환. 좌·우 재귀 결과가 **둘 다 non-None**이면 갈림점 = 현재 노드가 LCA. 하나만 있으면 그것을 위로 전달.
- **왜 후위인가:** 자식의 탐색 결과가 나와야 현재 노드가 갈림점인지 판단할 수 있으므로 "자식 먼저"인 후위가 자연스럽다.

### 10. 길 찾기 게임 ⚫기출 (프로그래머스 #42892, 2019 KAKAO BLIND)
노드 좌표 배열 `nodeinfo`가 주어진다. 규칙에 맞는 이진 트리를 만든 뒤 **전위 순회**와 **후위 순회** 결과를 2차원 배열로 반환하라. 규칙: 왼쪽 서브트리의 모든 x는 부모보다 작고, 오른쪽은 크다(x에 대한 BST). 부모는 자식보다 y가 크다(위에 있다).
- **접근:**
  1. `(x, y, 노드번호)`를 만들고 **y 내림차순, 같으면 x 오름차순**으로 정렬 → 위에서 아래로 삽입 순서 확정.
  2. 그 순서대로 **x 기준 BST 삽입**(반복)으로 트리를 구성.
  3. **전위·후위 순회**를 반환. 노드가 최대 10,000개라 한쪽으로 치우친 트리에서 재귀가 깊이 한계에 걸릴 수 있으니 **반복 순회**(명시적 스택)로 안전하게.
- **함정:** 모든 노드의 x가 서로 달라 삽입 위치가 유일하게 정해진다. 재귀 순회를 쓸 거면 `sys.setrecursionlimit`을 반드시 올려라.

---

## 학습 순서 추천
1. **순회의 기본기부터:** 1(중위 재귀·반복) → 2(깊이 DFS·BFS) → 6(레벨 순회)로 세 순회를 손에 익힌다.
2. **동시 순회·구조 비교:** 3(뒤집기) → 4(같은 트리) → 5(대칭)으로 두 위치를 함께 다루는 감각을 만든다.
3. **순회를 얹은 응용:** 7(경로 합) → 8(BST 검증) → 9(LCA)로 "순회 시점 선택"이 답을 좌우함을 체감한다.
4. **기출로 통합:** 10(길 찾기 게임)에서 트리 재구성 + 전위·후위 + 재귀 깊이 관리를 한 번에 경험한다.
