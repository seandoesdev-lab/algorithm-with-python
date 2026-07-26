# Day 36 — 연습문제: 서로소 집합 (Union-Find / Disjoint Set)

> 출처는 **프로그래머스 / LeetCode만** 사용합니다.
> 난이도: 🟢기초 · 🟡중급 · 🔴심화 · ⚫기출
> 코드 해설 → [solutions.py](solutions.py) · 개념 → [concept.md](concept.md)

풀이 순서는 **연결 요소 세기 → 사이클 판별 → 제약 그룹핑 → 응용**으로,
"연결됐나?"는 `find(a)==find(b)`, "합쳐라"는 `union`, "이미 같은 그룹인데 또 이으면 사이클"을 몸에 익히도록 배치했다.

---

## 1. Number of Provinces 🟡
- **출처:** [LeetCode #547](https://leetcode.com/problems/number-of-provinces/)
- **유형:** **연결 요소 개수**(Union-Find 기본)
- **문제:** `n`개 도시의 인접 행렬 `isConnected`(`isConnected[i][j] == 1`이면 i, j 직접 연결)가 주어진다. 직접·간접으로 연결된 도시 묶음을 **주(province)** 라 할 때, 주의 개수를 구하라.
- **입력/출력:** `isConnected: List[List[int]]` → `int`
- **제약:** `1 <= n <= 200`, `isConnected[i][i] == 1`, 대칭 행렬
- **핵심 힌트:**
  - 상삼각(`j > i`)만 훑어 `isConnected[i][j] == 1`이면 `union(i, j)`.
  - 답은 최종 **서로 다른 root 수**(= `dsu.count`).
  - DFS/BFS로도 풀리지만, "연결 요소 = Union-Find" 감을 잡는 정석 문제.

---

## 2. 네트워크 ⚫ (기출)
- **출처:** [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162)
- **유형:** **연결 요소 개수** — 프로그래머스 시그니처(`def solution`)로 Union-Find 적용
- **문제:** 컴퓨터 수 `n`, 연결 정보 `computers`(`computers[i][j] == 1`이면 i, j 연결)가 주어진다. 직접·간접으로 연결된 컴퓨터 묶음이 하나의 네트워크다. **네트워크 개수**를 구하라.
- **입력/출력:** `n: int, computers: List[List[int]]` → `int`
- **제약:** `1 <= n <= 200`, `computers[i][i] == 1`, 대칭
- **핵심 힌트:**
  - 547과 사실상 동일한 문제(자기 자신 `i==j`는 건너뛰기). `computers[i][j] == 1`이면 `union(i, j)`.
  - 원 분류는 DFS/BFS지만 Union-Find가 코드가 짧다. **두 접근을 모두 익혀 비교**하면 좋다.
  - 답은 서로 다른 root 수.

---

## 3. Redundant Connection 🟡
- **출처:** [LeetCode #684](https://leetcode.com/problems/redundant-connection/)
- **유형:** **무방향 사이클 판별** — union 실패 간선이 정답
- **문제:** 노드 `1..n`의 **트리에 간선 하나를 추가**한 그래프가 `edges`로 주어진다(길이 n). 제거하면 다시 트리가 되는 간선을 반환하라. 답이 여럿이면 **입력에서 가장 뒤에 오는** 간선.
- **입력/출력:** `edges: List[List[int]]` → `List[int]`
- **제약:** `3 <= n <= 1000`, 각 간선은 서로 다른 무방향 간선, 노드는 `1..n`
- **핵심 힌트:**
  - 간선을 순서대로 `union`. **처음으로 `union`이 실패(두 끝의 root가 이미 같음)** 하는 간선이 사이클을 완성 → 그게 정답.
  - 트리 + 간선 1개이므로 사이클은 정확히 하나. "가장 뒤 간선"은 앞에서부터 처리하면 자연히 마지막에 걸리는 간선이 답.
  - 노드가 1-based이므로 `parent` 크기를 `n+1`로.

---

## 4. Satisfiability of Equality Equations 🟡
- **출처:** [LeetCode #990](https://leetcode.com/problems/satisfiability-of-equality-equations/)
- **유형:** **등식/부등식 제약** — 등식 먼저 union, 부등식으로 검사(2-pass)
- **문제:** 길이 4 문자열 배열 `equations`가 주어진다. 각 원소는 `"a==b"` 또는 `"a!=b"`(소문자 변수). 모든 식을 만족하도록 변수에 정수를 배정할 수 있으면 `True`, 아니면 `False`.
- **입력/출력:** `equations: List[str]` → `bool`
- **제약:** `1 <= equations.length <= 500`, 변수는 소문자 한 글자(a~z)
- **핵심 힌트:**
  - 변수는 26개뿐 → `parent` 크기 26(`ord(c) - ord('a')`).
  - **1-pass:** `==` 식을 모두 `union`(같은 그룹으로 묶기).
  - **2-pass:** `!=` 식에서 `find(a) == find(b)`인 게 하나라도 있으면 모순 → `False`. 없으면 `True`.
  - **순서가 핵심**(등식을 먼저 다 처리해야 전이 관계가 완성됨).

---

## 5. Number of Operations to Make Network Connected 🔴
- **출처:** [LeetCode #1319](https://leetcode.com/problems/number-of-operations-to-make-network-connected/)
- **유형:** **컴포넌트 수−1 + 여분 간선 개수** 로 실현 가능성 판단
- **문제:** 컴퓨터 `n`대와 케이블 `connections[i] = [a, b]`. 직접 연결된 두 컴퓨터의 케이블을 뽑아 연결 안 된 쌍에 옮길 수 있다. **모두 연결**되게 하는 최소 이동 횟수를 구하라. 불가능하면 `-1`.
- **입력/출력:** `n: int, connections: List[List[int]]` → `int`
- **제약:** `1 <= n <= 10^5`, `1 <= connections.length <= min(n*(n-1)/2, 10^5)`, 중복 간선 없음
- **핵심 힌트:**
  - 컴포넌트 `c`개를 하나로 잇는 데 필요한 케이블은 **`c − 1`개**.
  - 케이블이 남으려면 **여분 간선(사이클을 만드는 간선) 수 ≥ c − 1**이어야 한다. 즉 `len(connections) >= n - 1`이면 항상 가능.
  - **간단 공식:** `len(connections) < n - 1`이면 `-1`, 아니면 답은 **컴포넌트 수 − 1**. (여분 간선을 굳이 세지 않아도 됨.)
  - 큰 `n`이라 경로 압축·사이즈 합치기 필수.

---

## 6. Accounts Merge 🔴
- **출처:** [LeetCode #721](https://leetcode.com/problems/accounts-merge/)
- **유형:** **문자열 dict 인덱싱 + 그룹핑** — 공통 이메일로 계정 병합
- **문제:** `accounts[i] = [name, email1, email2, ...]`. 두 계정이 **공통 이메일**을 하나라도 공유하면 같은 사람이다(이름이 같아도 이메일이 다르면 다른 사람일 수 있음). 병합 후 각 계정을 `[name, 정렬된 이메일들...]`로 반환하라.
- **입력/출력:** `accounts: List[List[str]]` → `List[List[str]]`
- **제약:** `1 <= accounts.length <= 1000`, 이메일 총수 큼
- **핵심 힌트:**
  - **이메일 → 계정 인덱스** 매핑을 만든다. 이미 본 이메일이면 그 계정과 현재 계정을 `union`(같은 사람).
  - 각 이메일을 소속 계정의 **root로 그룹핑**(`root -> set(emails)`).
  - 그룹마다 이메일 정렬 후 앞에 이름을 붙여 결과 구성. 이름은 그 계정의 첫 필드로 복원.
  - 대안: 이메일을 노드로 보는 그래프 + DFS도 가능(둘 다 통과). Union-Find가 병합에 간결.

---

### 학습 체크리스트
- [ ] "연결됐나?"는 `find(a)==find(b)`, "합쳐라"는 `union`을 반사적으로 쓴다 (1·2번)
- [ ] 연결 요소 개수는 `dsu.count`(성공한 union으로 감소) 또는 서로 다른 root 수 (1·2번)
- [ ] 무방향 사이클 = `union`이 실패하는 간선. 그 간선을 답으로 낸다 (3번)
- [ ] 등식(==)을 **먼저** 다 union하고, 부등식(!=)으로 모순을 검사한다 (4번)
- [ ] "모두 연결" 최소 비용 = `컴포넌트 수 − 1`, 간선이 `n−1`개 미만이면 `-1` (5번)
- [ ] 문자열·이메일 원소는 dict로 정수 인덱싱해 배열 Union-Find에 태운다 (6번)
- [ ] 큰 입력엔 경로 압축 + 사이즈 합치기를 반드시 함께 쓴다 (5·6번)
