# Day 8 연습문제 — 큐와 덱 (Queue & Deque)

> 난이도 표기: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(대기업·빈출)
> 출처: 프로그래머스(programmers.co.kr), LeetCode(leetcode.com)
> 해설·여러 접근 비교는 `solutions.py` 참고.

---

## 🟢 문제 1. 기능개발
- 출처: 프로그래머스 #42586 — https://school.programmers.co.kr/learn/courses/30/lessons/42586
- 카테고리: 큐 / 시뮬레이션 (기초)
- 요약: 각 기능의 진척도 `progresses`와 개발 속도 `speeds`가 주어진다. 각 기능은 진도가 100%가
  되어야 배포되며, **앞 기능이 배포될 때 그보다 먼저 끝난 뒤 기능들이 함께 배포**된다.
  각 배포마다 몇 개 기능이 함께 나가는지 순서대로 반환한다.
- 💭 힌트: 각 기능이 완성되는 데 걸리는 **남은 일수**를 올림으로 계산해 큐(또는 리스트)에 넣는다.
  맨 앞(가장 먼저 배포될 것)의 완성일을 기준으로, 그 이하인 뒤 기능들을 함께 빼며 센다.
  앞에서 빼는 처리라 **큐(`deque.popleft`)**가 자연스럽다.

## 🟡 문제 2. 프로세스
- 출처: 프로그래머스 #42587 — https://school.programmers.co.kr/learn/courses/30/lessons/42587
- 카테고리: 큐 / 시뮬레이션 (우선순위 확인)
- 요약: 실행 대기 큐의 프로세스 중요도 `priorities`와 알고 싶은 프로세스의 위치 `location`이 주어진다.
  큐 맨 앞을 꺼내되, 뒤에 더 높은 우선순위가 있으면 **맨 뒤로 다시 보낸다**. 그렇지 않으면 실행한다.
  `location` 위치의 프로세스가 **몇 번째로 실행**되는지 반환한다.
- 💭 힌트: `(원래 인덱스, 우선순위)` 튜플을 **덱**에 넣는다. 앞을 꺼내 `max(남은 우선순위)`보다 작으면
  `append`로 뒤로 보내고, 아니면 실행 카운트 증가. 꺼낸 것이 우리가 찾던 `location`이면 거기서 종료.
  앞에서 빼고 뒤로 보내는 회전이라 **큐/덱**이 정확히 들어맞는다.

## 🟡 문제 3. Implement Queue using Stacks
- 출처: LeetCode #232 — https://leetcode.com/problems/implement-queue-using-stacks/
- 카테고리: 큐 / 자료구조 설계
- 요약: **스택 두 개만** 사용해 FIFO 큐(`push`, `pop`, `peek`, `empty`)를 구현한다.
- 💭 힌트: 입력 스택(`in`)과 출력 스택(`out`)을 둔다. `push`는 `in`에 쌓고, `pop`/`peek` 시
  `out`이 비었으면 `in`의 전부를 `out`으로 옮긴다(순서가 뒤집혀 FIFO가 됨). 각 원소는 최대
  한 번 옮겨지므로 **분할 상환(amortized) O(1)**.

## 🟡 문제 4. Design Circular Queue
- 출처: LeetCode #622 — https://leetcode.com/problems/design-circular-queue/
- 카테고리: 큐 / 원형 큐(ring buffer) 설계
- 요약: 고정 용량 `k`의 **원형 큐**를 직접 구현한다. `enQueue`, `deQueue`, `Front`, `Rear`,
  `isEmpty`, `isFull`을 지원하며 내장 큐 자료형을 쓰지 않는다.
- 💭 힌트: 크기 `k` 배열과 `head` 인덱스, `count`(현재 원소 수)를 둔다. 삽입 위치는
  `(head + count) % k`, 삭제는 `head = (head + 1) % k`. **모듈러 연산**으로 인덱스를 회전시키는 것이 핵심.

## 🔴 문제 5. Sliding Window Maximum
- 출처: LeetCode #239 — https://leetcode.com/problems/sliding-window-maximum/
- 카테고리: 덱 / 모노토닉 덱 (슬라이딩 윈도우)
- 요약: 배열 `nums`와 창 크기 `k`가 주어질 때, 창을 한 칸씩 옮기며 **각 창의 최댓값**을 모두 반환한다.
- 💭 힌트: 매 창마다 `max()`를 부르면 O(nk). **모노토닉 덱**으로 O(n): 덱에 **인덱스**를 저장하고
  값이 내림차순이 되도록 뒤에서 작은 값을 제거, 앞에서 범위를 벗어난 인덱스를 제거한다.
  그러면 **덱 맨 앞이 항상 현재 창의 최댓값 인덱스**다.

## ⚫ 문제 6. 두 큐 합 같게 만들기 (2022 KAKAO TECH 인턴십)
- 출처: 프로그래머스 #118667 — https://school.programmers.co.kr/learn/courses/30/lessons/118667
- 카테고리: 덱 / 투 포인터 (기업 기출)
- 요약: 길이가 같은 두 큐 `queue1`, `queue2`가 주어진다. 한 큐에서 원소를 빼서 다른 큐에 넣는
  연산을 반복해 **두 큐의 합을 같게** 만들 때 필요한 **최소 연산 횟수**를 반환한다. 불가능하면 -1.
- 💭 힌트: 두 큐를 **하나의 덱으로 이어 붙이고** 두 포인터로 보는 방식, 또는 각각 덱으로 두고
  **합이 큰 쪽에서 빼서 작은 쪽으로 넘기는** 그리디. 전체 합이 홀수면 즉시 -1. 무한 루프 방지를 위해
  연산 횟수 상한(약 두 큐 길이의 3~4배)을 둔다. `popleft`/`append`가 잦으니 **반드시 `deque`**.
