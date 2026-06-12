---
day: 1
phase: phase-0-python-basics
title: 빠른 입출력 (Fast I/O)
category: [입출력]
difficulty: 기초
status: done
prev: 
next: [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]
related: [[[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]]
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/120906
  - https://school.programmers.co.kr/learn/courses/30/lessons/12912
  - https://leetcode.com/problems/add-digits/
  - https://school.programmers.co.kr/learn/courses/30/lessons/81301
tags: [phase/0, topic/io]
---

# Day 01 — 빠른 입출력 (Fast I/O)

> [!abstract] 한눈 요약 (TL;DR)
> `input()`은 프롬프트 처리와 추가 함수 호출 오버헤드로 인해 대량 입력 시 느리다. `sys.stdin.readline`으로 `input`을 재정의하거나, `sys.stdin.read().split()`으로 전체를 한 번에 토큰화하면 stdin 기반 저지에서 TLE를 방지할 수 있다. 출력도 `'\n'.join()`으로 한 번에 처리하면 flush 오버헤드를 줄인다.

> [!note]- 1. 정의와 직관
>
> ### input() 이란?
>
> 파이썬 내장 함수 `input()`은 표준 입력(stdin)에서 한 줄을 읽어 **문자열**로 반환한다.
> 내부적으로 다음 두 가지 작업을 수행한다.
>
> 1. **프롬프트 출력 처리**: `input(prompt)` 형태로 호출하면 프롬프트 문자열을 stdout에 flush한다. 프롬프트가 없어도 이 경로는 항상 거친다.
> 2. **라인 단위 오버헤드**: CPython 구현에서 `input()`은 C 레벨에서 `PyOS_Readline()`을 호출하며, 추가적인 함수 호출 스택과 문자열 처리 과정을 포함한다.
>
> ### sys.stdin.readline() 이란?
>
> `sys.stdin`은 파이썬이 프로세스 시작 시 열어 두는 **텍스트 스트림(TextIOWrapper)** 객체다.
> `.readline()`은 버퍼에서 다음 개행(`\n`)까지를 읽어 반환하는 저수준(low-level) 메서드로, 프롬프트 처리나 추가 함수 호출 오버헤드가 없다.
>
> ### 직관적 비교
>
> | 항목 | `input()` | `sys.stdin.readline()` |
> |---|---|---|
> | 내부 경로 | `PyOS_Readline` → 프롬프트 처리 → 문자열 생성 | TextIOWrapper 버퍼 → 직접 문자열 반환 |
> | 개행 포함 여부 | 자동으로 `\n` 제거됨 | `\n` **포함**하여 반환 |
> | 속도 | 느림 (상수 배 느림) | 빠름 |
> | 사용 편의성 | 높음 (인터랙티브 셸에 적합) | 보통 (`.rstrip()` 등 추가 처리 필요) |

> [!gear]- 2. 동작 원리
>
> ### 표준 입력 버퍼링 (Standard Input Buffering)
>
> 운영체제는 프로세스가 stdin에서 읽을 때 **커널 버퍼**에 데이터를 모아 둔다.
> 파이썬의 `sys.stdin`은 그 위에 **유저스페이스 버퍼(user-space buffer)**를 추가로 유지한다.
> 한 번에 많은 데이터를 읽을수록 시스템 콜(system call) 횟수가 줄어 빠르다.
>
> ```
> stdin 데이터  ──▶  커널 버퍼  ──▶  TextIOWrapper 내부 버퍼  ──▶  readline() 반환
> ```
>
> ### readline()의 개행('\n') 포함 반환
>
> `sys.stdin.readline()`은 줄 끝의 `\n`을 포함해서 반환한다.
>
> ```python
> import sys, io
> sys.stdin = io.StringIO("hello\nworld\n")
> line = sys.stdin.readline()
> print(repr(line))   # 'hello\n'
> ```
>
> - **정수 변환(`int()`)에는 영향 없음**: `int("42\n")` == 42 (파이썬이 자동으로 공백/개행을 무시)
> - **문자열로 사용할 때는 반드시 `.rstrip()` 또는 `.strip()` 필요**:
>
> ```python
> name = sys.stdin.readline().rstrip('\n')   # 또는 .rstrip()
> ```
>
> ### sys.stdin 전체를 한 번에 read().split()으로 토큰화
>
> 입력이 복잡하거나 여러 줄에 걸쳐 숫자가 섞여 있을 때 가장 빠른 패턴:
>
> ```python
> import sys
> data = sys.stdin.read().split()   # 전체 읽기 후 공백/개행 기준 토큰 리스트
> idx = 0
>
> n = int(data[idx]); idx += 1
> a = [int(data[idx + i]) for i in range(n)]; idx += n
> ```
>
> - `sys.stdin.read()`는 **단 한 번의 시스템 콜**로 모든 입력을 읽는다.
> - `.split()`은 공백·탭·개행을 모두 구분자로 처리하므로, 줄 구조와 무관하게 숫자를 순서대로 뽑아낼 수 있다.
> - 대량 입력(10^6 토큰 이상)에서도 매우 빠르다.
>
> ### 파이썬 관용구
>
> **관용구 1: input 함수 재정의 (가장 많이 쓰는 패턴)**
>
> ```python
> import sys
> input = sys.stdin.readline   # input()을 호출하는 기존 코드를 바꾸지 않아도 됨
>
> n = int(input())
> a, b = map(int, input().split())
> ```
>
> **관용구 2: map(int, input().split())**
>
> ```python
> a, b = map(int, input().split())          # 한 줄에 두 정수
> row = list(map(int, input().split()))     # 한 줄에 여러 정수
> ```
>
> **관용구 3: 출력 모아서 한 번에 출력**
>
> ```python
> results = []
> for i in range(n):
>     results.append(str(answer))
>
> print('\n'.join(results))                     # 방법 A: print + join
> sys.stdout.write('\n'.join(results) + '\n')   # 방법 B: sys.stdout.write
> ```

> [!chart]- 3. 복잡도 (시간/공간)
>
> N줄 입력 기준 (각 줄에 정수 1개)
>
> | 방법 | 시간 복잡도 | 실질 상수 | N=10^5 예상 | N=10^6 예상 |
> |---|---|---|---|---|
> | `input()` 반복 | O(N) | 큼 (~5–10×) | ~1–2 초 | 10–20 초 (TLE) |
> | `sys.stdin.readline()` 반복 | O(N) | 보통 | ~0.3–0.5 초 | ~1–2 초 |
> | `sys.stdin.read().split()` | O(N) | 작음 | ~0.1–0.2 초 | ~0.5–1 초 |
>
> 시간복잡도(Time Complexity)는 세 방법 모두 O(N)이지만, **상수 인수(constant factor)**의 차이가 실제 채점 환경에서 시간 초과(TLE, Time Limit Exceeded)를 결정짓는다.
> stdin 기반 온라인저지(Codeforces, Kattis 등) 기준 파이썬 시간 제한은 보통 1~2초이며, N ≥ 10^5인 문제에서 `input()`은 높은 확률로 TLE를 유발한다.
> **프로그래머스/LeetCode는 함수 기반 채점**이므로 stdin 속도 문제는 발생하지 않는다. 그러나 내부 로직의 알고리즘 복잡도(예: O(N^2) vs O(N))는 여전히 TLE의 원인이 된다.

> [!tip]- 💡 이해를 돕는 팁
>
> ### 팁 1: 플랫폼별 I/O 전략
>
> - **프로그래머스 / LeetCode**: 함수 기반 채점. `def solution(...)` 또는 `class Solution:`을 구현하면 플랫폼이 직접 호출한다. stdin을 읽을 필요가 없으며, `sys.stdin.readline`은 사용하지 않는다.
> - **Codeforces / Kattis 등 stdin 기반 저지**: 입력이 수십만 줄 이상이면 `sys.stdin.readline` 또는 `sys.stdin.read().split()`이 TLE를 막는 핵심 기술이다.
> - **PyPy3**: Codeforces 등 일부 저지는 PyPy3 제출 옵션을 제공한다. JIT(Just-In-Time) 컴파일로 CPython 대비 **2–10배** 빠른 속도를 낼 수 있다. 시간 제한이 빡빡한 stdin 기반 문제에서 Python3가 TLE라면 PyPy3를 시도해 볼 수 있다.
>
> ### 팁 2: 여러 줄 한 번에 읽기 — readlines()
>
> ```python
> import sys
> lines = sys.stdin.readlines()   # 모든 줄을 리스트로 반환 (각 줄에 \n 포함)
> for line in lines:
>     a, b = map(int, line.split())
>     print(a + b)
> ```
>
> - `readlines()`는 전체를 한 번에 읽어 줄 단위 리스트로 반환한다.
> - `read().split()`보다 줄 구조를 유지해야 할 때 유리하다.
> - 참고: [파이썬 빠른 입력 — velog](https://velog.io/@codesigner/Python-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%B9%A0%EB%A5%B8-%EC%9E%85%EB%A0%A5-sys.stdin.readline)
>
> ### 팁 3: sys.stdin.readline 사용이 권장되는 환경
>
> stdin 기반 저지(예: Codeforces, Kattis)에서는 공식적으로 "Python을 사용한다면 `input` 대신 `sys.stdin.readline`을 사용하라"고 안내하는 경우가 많다.
> 프로그래머스/LeetCode에서는 해당 없지만, stdin 기반 환경으로 전환할 때 즉시 적용할 수 있도록 숙지해 두는 것이 좋다.
> 참고: [Python sys.stdin 공식 문서](https://docs.python.org/3/library/sys.html#sys.stdin)

> [!warning]- ⚠️ 개발자 필수 상식
>
> ### 함정 1: readline() 개행 처리
>
> ```python
> import sys, io
> sys.stdin = io.StringIO("apple\n")
> s = sys.stdin.readline()
> print(s == "apple")      # False! s == "apple\n"
> print(s.rstrip() == "apple")  # True
> ```
>
> 문자열 비교, 딕셔너리 키, 파일명 등에 사용할 때는 반드시 `.rstrip()` 또는 `.strip()` 처리를 한다.
>
> ### 함정 2: 공백 줄 및 빈 입력 처리
>
> ```python
> line = sys.stdin.readline()
> if not line or line == '\n':
>     # 빈 줄이거나 EOF
>     pass
> ```
>
> - `readline()`이 `''`(빈 문자열)을 반환하면 **EOF(End of File)**에 도달한 것이다.
> - `'\n'`을 반환하면 빈 줄이다.
>
> ### 함정 3: EOF 처리 두 가지 패턴
>
> **패턴 A — try/except (EOFError 방식)**:
> ```python
> import sys
> while True:
>     try:
>         a, b = map(int, input().split())
>         print(a + b)
>     except EOFError:
>         break
> ```
>
> **패턴 B — sys.stdin 직접 순회**:
> ```python
> import sys
> for line in sys.stdin:
>     a, b = map(int, line.split())
>     print(a + b)
> ```
>
> 패턴 B가 더 파이썬다운(Pythonic) 방식이며, EOF에 도달하면 자동으로 루프가 종료된다.
>
> ### 함정 4: int(input()) vs input().split()
>
> ```python
> # 한 줄에 정수 하나
> n = int(input())          # OK
>
> # 한 줄에 정수 여러 개
> a, b = map(int, input().split())   # OK
>
> # 잘못된 예 — input()이 "1 2\n" 반환 시
> n = int(input())   # ValueError: invalid literal '1 2\n'
> ```
>
> ### 함정 5: print() 반복 호출이 느린 이유
>
> `print()`는 기본적으로 매 호출마다 `sys.stdout`을 **flush**한다(정확히는 line-buffered). N=10^6번 호출하면 flush 오버헤드가 누적되어 느려진다. 해결책: 결과를 리스트에 모아 `'\n'.join()`으로 한 번에 출력.
>
> ### 함정 6: 입력에 따른 strip 주의
>
> | 상황 | 권장 처리 |
> |---|---|
> | 정수 하나 | `int(input())` — `\n` 자동 무시 |
> | 문자열 비교·저장 | `.rstrip('\n')` 또는 `.strip()` |
> | 공백으로 구분된 토큰 | `.split()` — 앞뒤 공백·개행 자동 제거 |
>
> ### 언제 쓰는가 (When to Use)
>
> | 상황 | 권장 방법 |
> |---|---|
> | 입력이 수만 줄 이상 (N ≥ 10^5) | **반드시** `sys.stdin.readline` 또는 `sys.stdin.read().split()` 사용 |
> | 입력이 소규모 (N < 1000) | `input()` 으로 충분, 가독성 우선 |
> | 모든 입력을 한 번에 처리 | `sys.stdin.read().split()` 최적 |
> | 출력도 많을 때 (N ≥ 10^5 줄) | `'\n'.join(...)` 또는 `sys.stdout.write` |
> | 인터랙티브 프로그램 | `input()` (프롬프트 지원) |
>
> **결론**: stdin 기반 코딩테스트(Codeforces 등)에서 입력 줄 수가 많거나 제한 시간이 촉박하면, 습관적으로 파일 상단에 `import sys; input = sys.stdin.readline`을 추가하는 것을 권장한다.

> [!example]- 예제 코드
>
> ```python
> import sys
> input = sys.stdin.readline  # 핵심 트릭: input 재정의
>
> # 정수 하나
> n = int(input())
>
> # 한 줄에 두 정수
> a, b = map(int, input().split())
>
> # 전체 입력 토큰화 (대량 입력 최적 패턴)
> data = sys.stdin.read().split()
> ptr = 0
> n = int(data[ptr]); ptr += 1
>
> # 출력 모아서 한 번에 (flush 오버헤드 최소화)
> results = []
> for i in range(n):
>     results.append(str(i))
> sys.stdout.write('\n'.join(results) + '\n')
> ```
>
> 전체 실행 예제: [examples.py](examples.py)

> [!question]- 연습문제
>
> | # | 문제 | 플랫폼 | 난이도 | 핵심 개념 |
> |---|---|---|---|---|
> | 1 | 자릿수 더하기 | 프로그래머스 | 🟢 기초 | 문자열 순회, int 변환, 자릿수 합산 |
> | 2 | 두 정수 사이의 합 | 프로그래머스 | 🟢 기초 | range, sum, 조건 분기 |
> | 3 | Add Digits | LeetCode #258 | 🟡 중급 | 반복 합산, 수학적 공식(digital root) |
> | 4 | 숫자 문자열과 영단어 | 프로그래머스 (카카오) | ⚫ 기출 | 문자열 치환, 파싱, replace/split |
>
> 전체 문제 목록 및 힌트: [problems.md](problems.md)

> [!check]- 해설
>
> 각 문제의 접근법, 복잡도 분석, 다중 풀이 비교는 [solutions.py](solutions.py) 참고.

---
## 🔗 관계 (Relationships)

- ⬅️ 이전: (없음)
- ➡️ 다음: [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]
- 🧭 관련: [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]] — 입력 파싱에 map·컴프리헨션 사용
- 🗺️ 지도: [[Phase-0 MOC]] · [[00 Algorithm MOC]]
