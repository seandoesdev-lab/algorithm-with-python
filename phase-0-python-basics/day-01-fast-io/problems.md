# Day 01 — 빠른 입출력 (Fast I/O) 연습 문제

---

> **플랫폼 안내**: 프로그래머스(Programmers)와 LeetCode는 **함수 기반 채점** 방식이다.
> 즉, `def solution(...)` 또는 `class Solution:`의 메서드를 구현하면 플랫폼이 직접 호출한다.
> stdin을 직접 읽을 필요가 없으므로, stdin 기반 저지에서 발생하는 TLE-on-input 문제는 발생하지 않는다.
> 그러나 **문자열 파싱, int 변환, 반복 합산** 같은 기초 기술은 그대로 훈련된다.

---

## 문제 목록

| # | 문제 | 플랫폼 | 난이도 | 핵심 개념 |
|---|---|---|---|---|
| 1 | 자릿수 더하기 | 프로그래머스 | 🟢 기초 | 문자열 순회, int 변환, 자릿수 합산 |
| 2 | 두 정수 사이의 합 | 프로그래머스 | 🟢 기초 | range, sum, 조건 분기 |
| 3 | Add Digits | LeetCode | 🟡 중급 | 반복 합산, 수학적 공식(digital root) |
| 4 | 숫자 문자열과 영단어 | 프로그래머스 | ⚫ 카카오 | 문자열 치환, 파싱, replace/split |

---

## 🟢 문제 1 — 자릿수 더하기

- **출처**: 프로그래머스 (Programmers)
- **링크**: [자릿수 더하기](https://school.programmers.co.kr/learn/courses/30/lessons/120906)
- **카테고리**: 문자열, 수학

### 문제 요약

정수 `n`이 주어질 때, `n`의 각 자릿수의 합을 반환한다.

예시:
```
solution(1234)  ->  10   (1+2+3+4)
solution(930211) ->  16   (9+3+0+2+1+1)
```

- 제한: 0 <= n <= 1,000,000

### 💭 힌트

1. `str(n)`으로 숫자를 문자열로 변환하면 각 문자가 한 자릿수다.
2. `sum(int(c) for c in str(n))` 한 줄로 처리할 수 있다.
3. 또는 `sum(map(int, str(n)))`으로도 가능하다 — `map()`은 C 레벨에서 동작해 이론적으로 더 빠르다.
4. `divmod(n, 10)` 을 반복하는 수학적 방법도 있다 (문자열 변환 없이 각 자릿수를 추출).

---

## 🟢 문제 2 — 두 정수 사이의 합

- **출처**: 프로그래머스 (Programmers)
- **링크**: [두 정수 사이의 합](https://school.programmers.co.kr/learn/courses/30/lessons/12912)
- **카테고리**: 수학, 반복

### 문제 요약

두 정수 `a`, `b`가 주어질 때, `a`와 `b` 사이의 모든 정수의 합(양 끝 포함)을 반환한다.
`a`와 `b`의 대소 관계는 정해져 있지 않다.

예시:
```
solution(3, 5)   ->  12   (3+4+5)
solution(3, 3)   ->  3
solution(5, 3)   ->  12   (3+4+5, 순서 무관)
```

- 제한: -10,000,000 <= a, b <= 10,000,000

### 💭 힌트

1. `min(a, b)`와 `max(a, b)`로 순서를 정규화한 후 `range(lo, hi+1)`을 사용한다.
2. `sum(range(lo, hi+1))`이 가장 직관적인 방법이다.
3. 수학 공식: `(lo + hi) * (hi - lo + 1) // 2` — O(1)로 처리 가능하다.
4. a == b 엣지케이스도 두 방법 모두 자연스럽게 처리된다.

---

## 🟡 문제 3 — Add Digits

- **출처**: LeetCode
- **번호 및 링크**: [258. Add Digits](https://leetcode.com/problems/add-digits/)
- **카테고리**: 수학, 문자열 파싱

### 문제 요약

음수가 아닌 정수 `num`이 주어질 때, 결과가 한 자릿수(single digit)가 될 때까지 각 자릿수를 반복해서 더한다.

예시:
```
num = 38 -> 3+8=11 -> 1+1=2  ->  2
num = 0  ->  0
```

- 추가 도전: O(1) 시간, O(1) 공간으로 풀 수 있는가?

### 💭 힌트

**방법 A — 단순 반복 (O(log n) 시간)**:
```python
while num >= 10:
    num = sum(int(c) for c in str(num))
return num
```

**방법 B — Digital Root 수학 공식 (O(1) 시간)**:
- 0이면 0, 9의 배수면 9, 나머지는 `num % 9`.
- 공식: `0 if num == 0 else 1 + (num - 1) % 9`
- 자릿수를 거듭 더하면 결국 9로 나눈 나머지와 같다는 수론(number theory) 성질을 이용한다.

---

## ⚫ 문제 4 — 숫자 문자열과 영단어 (2021 카카오 인턴십)

- **출처**: 프로그래머스 (Programmers) — 2021 카카오 채용연계형 인턴십
- **링크**: [숫자 문자열과 영단어](https://school.programmers.co.kr/learn/courses/30/lessons/81301)
- **카테고리**: 문자열, 파싱

### 문제 요약

숫자의 일부 자릿수가 영어 단어로 바뀐 문자열 `s`가 주어진다.
영어 단어를 해당 숫자로 변환하여 원래 수를 반환한다.

영단어 매핑:
```
zero->0, one->1, two->2, three->3, four->4,
five->5, six->6, seven->7, eight->8, nine->9
```

예시:
```
solution("one4seveneight")  ->  1478
solution("23four5six7")     ->  234567
solution("2three45sixseven") ->  234567
solution("123")             ->  123
```

### 💭 힌트

1. `str.replace(word, digit)` 를 모든 단어에 대해 반복 적용하면 깔끔하다.
2. 딕셔너리 + for 루프로 한 번에 처리 가능하다.
3. 더 파이썬다운 방법: `s.split(word)`로 나눈 뒤 숫자를 사이에 끼워 `join`하는 방식도 있다.
4. 최종 결과는 문자열이므로 `int(s)`로 변환해야 한다.

---

## 정리: 함수 I/O 환경에서의 파싱 기술 요약

| 기술 | 사용 상황 | 예시 코드 |
|---|---|---|
| `str(n)` 순회 | 정수의 각 자릿수 처리 | `sum(int(c) for c in str(n))` |
| `map(int, iterable)` | 반복 가능 객체를 int로 변환 | `sum(map(int, str(n)))` |
| `range(lo, hi+1)` | 정수 범위 순회/합산 | `sum(range(a, b+1))` |
| `str.replace(old, new)` | 문자열 내 특정 패턴 치환 | `s.replace("one", "1")` |
| `divmod(n, base)` | 자릿수 추출 (문자열 불필요) | `q, r = divmod(n, 10)` |
| Digital Root 공식 | 반복 자릿수 합 O(1) 계산 | `1 + (n-1) % 9` |

> **플랫폼별 I/O 요약**: 프로그래머스/LeetCode에서는 `sys.stdin.readline`을 쓸 일이 없다.
> 하지만 **문자열 → int 파싱, 범위 합산, 문자열 치환** 기술은 모든 플랫폼에서 필수다.
> stdin 기반 저지(예: Codeforces, Kattis)에서는 `sys.stdin.readline`/`sys.stdin.read().split()`이
> 여전히 TLE를 막는 핵심 기술이다.
