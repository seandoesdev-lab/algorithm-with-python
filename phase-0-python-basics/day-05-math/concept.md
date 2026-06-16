---
day: 5
phase: 0-python-basics
title: 수학·진법·비트 기초 (Math & Bits)
category: [수학, 비트]
difficulty: 기초
status: done
prev: "[[day-04-strings/concept|Day 04 — 문자열 다루기]]"
next: "[[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]"
related:
  - "[[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]"
sources:
  - https://leetcode.com/problems/number-of-1-bits/
  - https://leetcode.com/problems/power-of-two/
  - https://school.programmers.co.kr/learn/courses/30/lessons/70129
  - https://leetcode.com/problems/reverse-integer/
  - https://leetcode.com/problems/powx-n/
  - https://school.programmers.co.kr/learn/courses/30/lessons/17687
tags: [phase/0, topic/math, topic/bit]
---

# Day 05 — 수학·진법·비트 기초 (Math & Bits)

> [!abstract] 한눈 요약 (TL;DR)
> 정수 나눗셈 `//`·나머지 `%`는 파이썬에서 **음의 무한대 방향으로 내림**한다(C/Java와 다름). 모듈러 거듭제곱은 `pow(a, b, m)`으로 O(log b)에 계산한다. GCD는 `math.gcd`, 소수는 O(sqrt n) 판별 또는 에라토스테네스의 체로 범위를 한 번에 처리한다. 진법 변환은 내장 `bin/oct/hex` + `int(s, base)`, 비트 트릭(`n & (n-1)`, XOR 상쇄 등)은 코테 단골이다.

> [!note]- 1. 정의와 직관
> ### 정수 나눗셈과 나머지 (Floor Division & Modulo)
>
> 파이썬의 `//`는 **내림 나눗셈(floor division)**, `%`는 나머지(modulo)다.
> 핵심 함정은 **음수**다. 파이썬은 결과를 항상 **음의 무한대 방향으로 내림(floor)**한다.
>
> ```python
> 7 // 2     # 3
> -7 // 2    # -4   (3이 아니다! 음의 무한대로 내림)
> 7 % 3      # 1
> -7 % 3     # 2    (나머지는 항상 제수의 부호를 따라 0 이상)
> divmod(17, 5)   # (3, 2)  -> 몫과 나머지를 한 번에
> ```
>
> C/Java는 0 방향으로 자르므로 `-7 / 2 == -3`, `-7 % 2 == -1`이다. **언어마다 음수 나눗셈 결과가
> 다르다는 점**을 반드시 기억하자. 항등식 `a == (a // b) * b + (a % b)`는 파이썬에서 항상 성립한다.
>
> `divmod(a, b)`는 `(a // b, a % b)`를 튜플로 돌려줘 진법 변환·자릿수 분해에 유용하다.
>
> ### 최대공약수·최소공배수 (GCD & LCM)
>
> **유클리드 호제법(Euclidean algorithm)**: `gcd(a, b) = gcd(b, a % b)`, `b == 0`이면 `a`.
>
> ```python
> import math
>
> math.gcd(12, 18)        # 6
> math.gcd(0, 5)          # 5
> math.lcm(4, 6)          # 12   (Python 3.9+)
>
> # lcm을 직접 구할 때 (오버플로 없는 파이썬에선 안전)
> def lcm(a, b):
>     return a * b // math.gcd(a, b)   # 곱하기 전에 나누면 더 안전
> ```
>
> `math.gcd`는 여러 인자도 받는다: `math.gcd(12, 18, 24)  # 6` (Python 3.9+).
> 유클리드 호제법의 시간복잡도는 **O(log(min(a, b)))**로 매우 빠르다.
>
> ### 소수 판별과 에라토스테네스의 체 (Prime & Sieve)
>
> 단일 수 판별은 **제곱근까지만** 나눠 보면 된다(약수는 sqrt(n)을 기준으로 대칭).
>
> ```python
> def is_prime(n):
>     if n < 2:
>         return False
>     i = 2
>     while i * i <= n:        # sqrt(n)까지만 -> O(sqrt(n))
>         if n % i == 0:
>             return False
>         i += 1
>     return True
> ```
>
> 여러 수의 소수 여부를 한꺼번에 구할 땐 **에라토스테네스의 체**가 압도적으로 빠르다.
>
> ```python
> def sieve(n):
>     """0..n 중 소수 여부 리스트 반환. 시간 O(n log log n)."""
>     is_p = [True] * (n + 1)
>     is_p[0] = is_p[1] = False
>     i = 2
>     while i * i <= n:
>         if is_p[i]:
>             # i의 배수를 i*i부터 지운다 (그 아래는 이미 지워짐)
>             for j in range(i * i, n + 1, i):
>                 is_p[j] = False
>         i += 1
>     return is_p
> ```
>
> 체의 핵심 최적화 두 가지: (1) `i*i > n`이면 멈춘다, (2) 지우기 시작점을 `i*i`로 둔다
> (예: 3의 배수는 6=2*3이 이미 지워졌으므로 9부터 시작).
>
> ### 진법 변환 (Radix / Base Conversion)
>
> 10진수 -> n진수 내장 함수는 **접두사가 붙은 문자열**을 돌려준다.
>
> ```python
> bin(10)     # '0b1010'   (2진)
> oct(10)     # '0o12'     (8진)
> hex(255)    # '0xff'     (16진)
> format(255, 'b')   # '11111111'  (접두사 없이)
> format(255, 'x')   # 'ff'
> f"{10:b}"          # '1010'      (f-string 포맷)
> ```
>
> 문자열 -> 정수는 `int(s, base)`로, 2~36진수까지 지원한다.
>
> ```python
> int("1010", 2)   # 10
> int("ff", 16)    # 255
> int("z", 36)     # 35
> ```
>
> ### 비트 연산 (Bitwise Operations)
>
> | 연산 | 기호 | 예 (4비트 가정) | 의미 |
> |---|---|---|---|
> | AND | `&` | `1100 & 1010 = 1000` | 둘 다 1일 때 1 |
> | OR | `\|` | `1100 \| 1010 = 1110` | 하나라도 1이면 1 |
> | XOR | `^` | `1100 ^ 1010 = 0110` | 다르면 1 |
> | NOT | `~` | `~5 = -6` | 비트 반전 (`~x == -x-1`) |
> | 왼쪽 시프트 | `<<` | `1 << 3 = 8` | 2^k 곱하기 |
> | 오른쪽 시프트 | `>>` | `8 >> 2 = 2` | 2^k 나누기(내림) |
>
> XOR의 성질도 단골이다: `a ^ a == 0`, `a ^ 0 == a`. 배열에서 한 번만 나타나는 원소를
> 전부 XOR 하면 그 원소만 남는다(짝은 상쇄).

> [!gear]- 2. 동작 원리
> ### 거듭제곱과 모듈러 연산 (Power & Modular Arithmetic)
>
> ```python
> 2 ** 10        # 1024   (거듭제곱 연산자)
> pow(2, 10)     # 1024   (내장 함수, 동일)
> pow(2, 10, 1000)   # 24  -> (2**10) % 1000 을 한 번에, 매우 빠름
> ```
>
> `pow(a, b, m)`은 **모듈러 거듭제곱(modular exponentiation)**으로, 큰 지수도 O(log b)에 계산한다.
> `(a ** b) % m`처럼 먼저 거대한 수를 만든 뒤 나누면 느리고 메모리도 낭비된다. **항상 3-인자 `pow`를 쓰자.**
>
> 모듈러 산술의 기본 성질(코테에서 답을 `10**9 + 7`로 나누라고 할 때 사용):
>
> ```
> (a + b) % m == ((a % m) + (b % m)) % m
> (a * b) % m == ((a % m) * (b % m)) % m
> ```
>
> 주의: 뺄셈은 음수가 될 수 있으므로 `(a - b) % m` 대신 `((a - b) % m + m) % m`로 보정한다.
>
> ### 임의의 n진수로 직접 변환
>
> 내장에 없는 5진수 등은 `divmod`로 나머지를 거꾸로 모은다.
>
> ```python
> def to_base(num, base):
>     if num == 0:
>         return "0"
>     digits = "0123456789abcdefghijklmnopqrstuvwxyz"
>     out = []
>     while num > 0:
>         num, r = divmod(num, base)
>         out.append(digits[r])
>     return "".join(reversed(out))   # 나머지를 거꾸로 읽어야 정답
>
> to_base(255, 16)   # 'ff'
> to_base(13, 2)     # '1101'
> ```
>
> ### 자주 쓰는 비트 트릭 (Bit Tricks)
>
> ```python
> n & 1                 # 홀수면 1, 짝수면 0  (마지막 비트)
> n >> 1                # n // 2  (양수일 때)
> 1 << k                # 2^k
> n & (1 << k)          # k번째 비트가 켜져 있는지
> n | (1 << k)          # k번째 비트 켜기
> n & ~(1 << k)         # k번째 비트 끄기
> n ^ (1 << k)          # k번째 비트 토글
> n & (n - 1)           # 가장 낮은 켜진 비트 1개 제거
> n & (n - 1) == 0      # n이 2의 거듭제곱인지 (n>0)
> n & -n                # 가장 낮은 켜진 비트만 남기기 (LSB)
> bin(n).count("1")     # 켜진 비트 수 (popcount)
> n.bit_count()         # 켜진 비트 수 (Python 3.10+)
> n.bit_length()        # 표현에 필요한 비트 수
> ```
>
> ### 언제 쓰는가 (When to Use / Avoid)
>
> - 적합: 소수/약수/배수 문제, 진법 변환·자릿수 분해, 큰 수 모듈러 계산, 집합을 비트마스크로 표현(부분집합 열거), 2의 거듭제곱·홀짝 판정, XOR 기반 트릭
> - 적합: 소수를 범위로 자주 물으면 에라토스테네스의 체를 1회 구성해 재사용
> - 부적합: 단일 소수 1회 판별에 굳이 체를 만들기(메모리 낭비). `is_prime`이면 충분
> - 부적합: 가독성을 해치는 과도한 비트 트릭. 협업 코드에서는 의미가 분명한 산술이 나을 때가 많다
> - 부적합: 부동소수점으로 정수 제곱근·거듭제곱 비교(오차). 정수 연산(`isqrt`, 정수 `pow`)을 쓰자
>
> ### 파이썬 관용구 (Pythonic Usage)
>
> ```python
> import math
>
> # 1) 몫과 나머지 동시에
> q, r = divmod(17, 5)            # (3, 2)
>
> # 2) 모듈러 거듭제곱 (큰 수도 빠르게)
> ans = pow(7, 100, 10**9 + 7)
>
> # 3) 최소공배수
> lcm = a * b // math.gcd(a, b)
>
> # 4) 2의 거듭제곱 판별
> is_pow2 = (n > 0) and (n & (n - 1) == 0)
>
> # 5) 켜진 비트 수
> ones = bin(n).count("1")        # 또는 n.bit_count() (3.10+)
>
> # 6) n진수 변환 후 다시 10진수
> s = format(255, 'x')            # 'ff'
> back = int(s, 16)               # 255
>
> # 7) 정수 자릿수 합
> digit_sum = sum(int(d) for d in str(num))
>
> # 8) 정수 제곱근 (오차 없는 정수 연산, 3.8+)
> r = math.isqrt(50)              # 7  (floor(sqrt(50)))
> ```

> [!chart]- 3. 복잡도 (시간/공간)
>
> | 연산 | 시간복잡도 | 설명 |
> |---|---|---|
> | `a // b`, `a % b`, `divmod` | O(1)* | 작은 정수 기준 |
> | `pow(a, b)` (`a**b`) | 큰 수일수록 비쌈 | 결과 자릿수에 비례 |
> | `pow(a, b, m)` | **O(log b)** | 모듈러 거듭제곱, 권장 |
> | `math.gcd(a, b)` | O(log(min)) | 유클리드 호제법 |
> | `is_prime(n)` 시도나눗셈 | O(sqrt n) | 제곱근까지 |
> | `sieve(n)` 에라토스테네스 | **O(n log log n)** | n 이하 모든 소수 |
> | `int(s, base)` / `to_base` | O(자릿수) | 길이에 비례 |
> | 비트 연산 `& \| ^ << >>` | O(1)* | 워드 단위 |
> | `bin(n).count("1")` | O(비트 수) | popcount |
>
> \* 파이썬 정수는 임의 정밀도(arbitrary precision)라 매우 큰 수는 자릿수에 비례한다.

> [!tip]- 💡 이해를 돕는 팁
> - **`n & (n-1)`로 2의 거듭제곱 판별**: 2의 거듭제곱은 켜진 비트가 정확히 1개다. 1을 빼면 그 비트는 0이 되고 아래가 모두 1이 되어, AND 하면 0이 된다. 면접·코테 단골 한 줄 트릭이다.
>   - 참고: [기술면접 — 비트조작(비트마스크, 비트연산)](https://soniacomp.medium.com/%EA%B8%B0%EC%88%A0%EB%A9%B4%EC%A0%91-%EB%B9%84%ED%8A%B8%EC%A1%B0%EC%9E%91-%EB%B9%84%ED%8A%B8%EB%A7%88%EC%8A%A4%ED%81%AC-%EB%B9%84%ED%8A%B8%EC%97%B0%EC%82%B0-80a42fb72147)
>   - 참고: [파이썬 코딩 도장 47.1 비트 연산자](https://dojang.io/mod/page/view.php?id=2460)
>
> - **모듈로로 나누라는 문제(`10**9 + 7`)**: 중간 계산마다 `% m`을 적용해야 오버플로(다른 언어)·속도 문제를 피한다. 파이썬은 오버플로는 없지만 거대한 수 연산은 느리므로 습관을 들이자.
>
> - **에라토스테네스의 체**: 소수를 "여러 번/범위로" 물어보면 매번 `is_prime` 대신 체를 한 번 만들어 O(1) 조회한다. 시작점을 `i*i`로 두는 최적화를 꼭 기억.
>   - 참고: [에라토스테네스의 체 (알고달레)](https://www.algodale.com/algorithms/sieve-of-eratosthenes/)
>   - 참고: [소수 구하기 - 에라토스테네스의 체 (wikidocs)](https://wikidocs.net/21638)
>
> - **GCD/LCM**: `math.gcd`는 표준 제공, `lcm = a*b // gcd`. Python 3.9+는 `math.lcm`도 있다.
>   - 참고: [최대공약수와 최소공배수 (프로그래머스 12940)](https://school.programmers.co.kr/learn/courses/30/lessons/12940)
>
> - **진법 변환은 `divmod` + reverse**: 내장 `bin/oct/hex`로 안 되는 임의 진법은 나머지를 모아 거꾸로 읽는다. 카카오 "n진수 게임"이 대표 응용 문제다.
>   - 참고: [[3차] n진수 게임 (프로그래머스 17687)](https://school.programmers.co.kr/learn/courses/30/lessons/17687)
>
> - **음수 나눗셈 주의**: 파이썬 `-7 // 2 == -4`, `-7 % 2 == 1`로 다른 언어와 다르다. 좌표·인덱스 계산에서 음수가 섞이면 결과를 꼭 검산하자.
>   - 참고: [코딩테스트를 위한 Python 정리 (choiiis)](https://choiiis.github.io/python/for-coding-test/)

> [!warning]- ⚠️ 개발자 필수 상식
> 1. **음수 floor 나눗셈**: `-7 // 2 == -4`(0방향 아님), `%` 결과 부호는 **제수**를 따른다(`-7 % 2 == 1`). C/Java와 다르므로 다른 언어 풀이를 옮길 때 특히 조심.
>
> 2. **`pow(a, b, m)`를 써라**: `(a**b) % m`은 거대한 중간값을 만든다. 3-인자 `pow`는 O(log b)에 같은 답을 준다.
>
> 3. **`(a - b) % m` 음수 보정**: 모듈러 뺄셈 결과가 음수일 수 있으니 `((a-b) % m + m) % m`로 맞춘다.
>
> 4. **소수 판별은 sqrt까지**: `for i in range(2, n)`은 O(n)이라 느리다. `while i*i <= n`으로 O(sqrt n). 1은 소수가 아니고, 2는 유일한 짝수 소수다.
>
> 5. **`int(s, base)`의 base는 2~36**: 그 밖의 진법은 직접 구현해야 한다. 반대로 `bin/oct/hex`는 접두사(`0b`,`0o`,`0x`)가 붙으니 제거하려면 `[2:]` 슬라이싱 또는 `format(x, 'b')`.
>
> 6. **`~x == -x - 1`**: 파이썬 정수는 무한 비트의 2의 보수처럼 동작해 `~5 == -6`. 비트 NOT을 "특정 폭"으로 쓰려면 마스크(`& 0xFF` 등)를 함께 적용해야 한다.
>
> 7. **시프트는 곱셈/나눗셈의 대용**: `n << k == n * 2**k`, `n >> k == n // 2**k`(양수). 가독성·정확성 문제가 없을 때만 최적화로 쓰자.
>
> 8. **`math.isqrt` vs `int(x**0.5)`**: 부동소수점 `**0.5`는 큰 수에서 오차로 1 차이가 날 수 있다. 정수 제곱근은 **`math.isqrt`**(3.8+)가 정확하다.
>
> 9. **XOR 상쇄 성질**: `a ^ a == 0`, `a ^ 0 == a`. "딱 하나만 홀수 번 등장하는 원소 찾기"를 O(n) 시간·O(1) 공간으로 푸는 핵심.
>
> 10. **`bit_count()`/`bit_length()`**: Python 3.10+는 `n.bit_count()`(popcount)를 제공한다. 하위 호환이 필요하면 `bin(n).count("1")`.

> [!example]- 예제 코드
> ```python
> import math
>
> # 나눗셈 / 모듈러
> divmod(17, 5)           # (3, 2)
> pow(7, 100, 10**9 + 7)  # 모듈러 거듭제곱 (O(log b))
>
> # GCD / LCM
> math.gcd(12, 18)        # 6
> lcm = 4 * 6 // math.gcd(4, 6)  # 12
>
> # 소수 판별 (sqrt까지)
> def is_prime(n):
>     if n < 2: return False
>     i = 2
>     while i * i <= n:
>         if n % i == 0: return False
>         i += 1
>     return True
>
> # 임의 진법 변환
> def to_base(num, base):
>     if num == 0: return "0"
>     digits = "0123456789abcdefghijklmnopqrstuvwxyz"
>     out = []
>     while num > 0:
>         num, r = divmod(num, base)
>         out.append(digits[r])
>     return "".join(reversed(out))
>
> to_base(255, 16)        # 'ff'
>
> # 비트 트릭
> n = 12
> n & (n - 1) == 0        # False (12는 2의 거듭제곱 아님)
> bin(n).count("1")       # 2 (1100 -> set bit 2개)
> ```
>
> 전체 실행 예제: [examples.py](examples.py)

> [!question]- 연습문제
> | 난이도 | 문제 | 출처 | 핵심 개념 |
> |---|---|---|---|
> | 🟢 | [Number of 1 Bits (LC 191)](https://leetcode.com/problems/number-of-1-bits/) | LeetCode Easy | 비트 연산, popcount |
> | 🟢 | [Power of Two (LC 231)](https://leetcode.com/problems/power-of-two/) | LeetCode Easy | 비트 트릭, 2의 거듭제곱 |
> | 🟡 | [이진 변환 반복하기 (70129)](https://school.programmers.co.kr/learn/courses/30/lessons/70129) | 프로그래머스 | 진법 변환, 시뮬레이션 |
> | 🟡 | [Reverse Integer (LC 7)](https://leetcode.com/problems/reverse-integer/) | LeetCode Medium | 수학, 자릿수 처리 |
> | 🔴 | [Pow(x, n) (LC 50)](https://leetcode.com/problems/powx-n/) | LeetCode Medium | 분할정복, 빠른 거듭제곱 |
> | ⚫ | [n진수 게임 (17687)](https://school.programmers.co.kr/learn/courses/30/lessons/17687) | 프로그래머스 (카카오 2018) | 진법 변환, 구현 |
>
> 전체 문제 목록 및 힌트: [problems.md](problems.md)

> [!check]- 해설
> 각 문제의 해설 및 다중 접근 방식 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-04-strings/concept|Day 04 — 문자열 다루기]]
- ➡️ 다음: [[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]
- 🧭 관련:
  - [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]] — `math.gcd`, `itertools` 등 수학 문제에서 자주 쓰는 표준 라이브러리 도구의 기반이 된다 (math·itertools)
- 🗺️ 지도: [[Phase-0 MOC]] · [[00 Algorithm MOC]]
