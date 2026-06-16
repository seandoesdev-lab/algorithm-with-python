# Day 5 연습문제 — 수학·진법·비트 기초

> 난이도 표기: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(대기업)
> 출처: 프로그래머스(programmers.co.kr), LeetCode(leetcode.com)
> 해설·여러 접근 비교는 `solutions.py` 참고.

---

## 🟢 문제 1. Number of 1 Bits (켜진 비트 수)
- 출처: LeetCode #191 — https://leetcode.com/problems/number-of-1-bits/
- 카테고리: 비트 연산 (Bit Manipulation)
- 요약: 정수 `n`의 이진 표현에서 1인 비트(set bit)의 개수를 반환한다(popcount).
- 💭 힌트: `n & (n - 1)`은 가장 낮은 켜진 비트 1개를 지운다. 0이 될 때까지 반복하면 반복 횟수가
  곧 1의 개수다. (또는 `bin(n).count("1")`.)

## 🟢 문제 2. Power of Two (2의 거듭제곱 판별)
- 출처: LeetCode #231 — https://leetcode.com/problems/power-of-two/
- 카테고리: 비트 연산 / 수학
- 요약: 정수 `n`이 2의 거듭제곱이면 `True`를 반환한다.
- 💭 힌트: 2의 거듭제곱은 켜진 비트가 정확히 1개다. `n > 0 and (n & (n - 1)) == 0` 한 줄로 끝난다.

## 🟡 문제 3. 이진 변환 반복하기
- 출처: 프로그래머스 #70129 — https://school.programmers.co.kr/learn/courses/30/lessons/70129
- 카테고리: 진법 변환 / 시뮬레이션
- 요약: "0 제거 -> 남은 길이를 이진수로 변환"을 "1"이 될 때까지 반복하며,
  변환 횟수와 제거된 0의 총개수를 반환한다.
- 💭 힌트: 0의 개수 = `s.count("0")`, 남은 1의 개수 `c1`을 `bin(c1)[2:]`로 변환해 다음 `s`로 삼는다.

## 🟡 문제 4. Reverse Integer (정수 뒤집기)
- 출처: LeetCode #7 — https://leetcode.com/problems/reverse-integer/
- 카테고리: 수학 / 자릿수 처리
- 요약: 32비트 부호 정수 `x`의 자릿수를 뒤집어 반환한다. 32비트 범위를 벗어나면 0을 반환.
- 💭 힌트: `divmod`로 끝자리를 떼어 누적(`res = res * 10 + digit`)한다. 부호를 분리하고
  마지막에 `[-2**31, 2**31 - 1]` 범위를 검사한다. (파이썬은 오버플로가 없으므로 범위는 직접 확인.)

## 🔴 문제 5. Pow(x, n) (빠른 거듭제곱)
- 출처: LeetCode #50 — https://leetcode.com/problems/powx-n/
- 카테고리: 수학 / 분할정복 (Divide & Conquer)
- 요약: `x**n`을 계산한다(`n`은 음수 가능).
- 💭 힌트: 단순 반복은 O(n)이라 큰 `n`에서 느리다. **빠른 거듭제곱(분할정복)**으로
  `x**n = (x**(n//2))**2`를 이용하면 O(log n). `n`이 음수면 `1 / x**(-n)`.

## ⚫ 문제 6. [3차] n진수 게임 (기출 - 카카오 2018)
- 출처: 프로그래머스 #17687 — https://school.programmers.co.kr/learn/courses/30/lessons/17687
- 카테고리: 진법 변환 / 구현 (2018 KAKAO BLIND 3차)
- 요약: 0부터 차례로 `n`진수로 적은 긴 문자열에서, 튜브(본인)가 말하는 `m`명 게임의
  `p`번째 순서 숫자들을 `t`개 모아 대문자 문자열로 반환한다.
- 💭 힌트: `0,1,2,...`를 `n`진법 문자열로 바꿔(직접 구현 `to_base`) 길게 이어 붙인 뒤,
  인덱스 `p-1`부터 `m` 간격으로 `t`개를 골라낸다. 10~15는 'A'~'F'로 표기.
