# Day 19 — 투 포인터 (Two Pointers) 연습문제

> 출처는 **프로그래머스**와 **LeetCode**만 사용한다.
> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 먼저 스스로 풀고, 막히면 힌트를 본 뒤 [solutions.py](solutions.py)와 비교하자.

---

## 1. Valid Palindrome 🟢
- **출처:** [LeetCode #125](https://leetcode.com/problems/valid-palindrome/)
- **요약:** 문자열 `s`에서 영숫자(alphanumeric)만 남기고 대소문자를 무시했을 때 회문(palindrome)인지 판별한다.
- **입력/출력:** `s = "A man, a plan, a canal: Panama"` → `True`, `s = "race a car"` → `False`.
- **힌트:** 양끝 포인터 `lo, hi`. 각 포인터가 영숫자가 아니면 건너뛰고(`isalnum()`), `lower()`로 비교. `lo < hi`인 동안 반복.
- **핵심:** 양끝 수렴형의 가장 기본. 문자열을 새로 만들지 않고 O(1) 공간으로 푼다.

## 2. Two Sum II - Input Array Is Sorted 🟢
- **출처:** [LeetCode #167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- **요약:** **오름차순 정렬된** 배열 `numbers`에서 합이 `target`인 두 수의 **1-indexed** 위치를 반환한다(정답은 유일하게 존재).
- **입력/출력:** `numbers = [2,7,11,15], target = 9` → `[1,2]`.
- **힌트:** `lo=0, hi=n-1`. 합이 작으면 `lo++`, 크면 `hi--`. 이미 정렬돼 있으므로 정렬 불필요.
- **핵심:** 정렬 배열 + 합 조건 → 양끝 투 포인터의 정석. 원본 인덱스가 필요한 [Two Sum I](https://leetcode.com/problems/two-sum/)과 달리 여기선 해시가 불필요.

## 3. Remove Duplicates from Sorted Array 🟢
- **출처:** [LeetCode #26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
- **요약:** 정렬된 배열에서 중복을 제거해 각 원소가 한 번씩만 남도록 in-place로 만들고, 유일 원소 개수 `k`를 반환한다.
- **입력/출력:** `nums = [0,0,1,1,1,2,2,3,3,4]` → `k = 5`, 앞 5칸 `[0,1,2,3,4]`.
- **힌트:** `slow`는 마지막으로 확정한 유일값 위치, `fast`가 새로운 값을 만날 때만 `slow++` 후 덮어쓴다.
- **핵심:** 빠름/느림(같은 방향) 포인터로 O(1) 공간 in-place 필터링. **정렬 전제**가 있어야 성립.

## 4. Squares of a Sorted Array 🟡
- **출처:** [LeetCode #977](https://leetcode.com/problems/squares-of-a-sorted-array/)
- **요약:** 오름차순 정렬된(음수 포함) 배열의 각 원소를 제곱한 결과를 **오름차순으로** 반환한다.
- **입력/출력:** `nums = [-4,-1,0,3,10]` → `[0,1,9,16,100]`.
- **힌트:** 음수의 제곱이 클 수 있으니 양 끝 절댓값을 비교해 **큰 것부터 결과 뒤에서** 채운다.
- **핵심:** 병합형 투 포인터. 다시 정렬하면 O(n log n)이지만 투 포인터로 O(n).

## 5. Container With Most Water 🟡
- **출처:** [LeetCode #11](https://leetcode.com/problems/container-with-most-water/)
- **요약:** 높이 배열 `height`에서 두 선을 골라 x축과 만드는 물통의 최대 넓이를 구한다.
- **입력/출력:** `height = [1,8,6,2,5,4,8,3,7]` → `49`.
- **힌트:** 넓이 = `min(height[lo], height[hi]) * (hi - lo)`. **더 낮은 쪽**을 안으로 옮긴다(높은 쪽을 옮기면 결코 개선 불가).
- **핵심:** 왜 낮은 쪽을 옮기는가를 설명할 수 있어야 한다(폭은 무조건 줄어드니, 높이가 커질 가능성이 있는 낮은 쪽만 이동).

## 6. 숫자의 표현 🟡
- **출처:** [프로그래머스 #12924](https://school.programmers.co.kr/learn/courses/30/lessons/12924)
- **요약:** 자연수 `n`을 **연속한 자연수의 합**으로 표현하는 경우의 수를 구한다(자기 자신 `n = n`도 1가지로 포함).
- **입력/출력:** `n = 15` → `4` (`1+2+3+4+5`, `4+5+6`, `7+8`, `15`).
- **힌트:** `1..n`에 대해 `left, right` 두 포인터로 구간 합을 유지. 합 < n이면 `right++`(합 키움), 합 > n이면 `left++`(합 줄임), 같으면 카운트 후 `right++`. 전체 O(n).
- **핵심:** 양수 수열에서 "구간 합 == 목표" 세기 → 슬라이딩 윈도우에 가까운 투 포인터. 수식 접근(약수 세기)도 있으나 투 포인터로 직관적으로 해결.

## 7. 3Sum 🟡
- **출처:** [LeetCode #15](https://leetcode.com/problems/3sum/)
- **요약:** 배열에서 합이 0이 되는 서로 다른 세 원소의 **유일한** 조합을 모두 찾는다.
- **입력/출력:** `nums = [-1,0,1,2,-1,-4]` → `[[-1,-1,2],[-1,0,1]]`.
- **힌트:** **정렬 후** 첫 원소 `i`를 고정하고, 남은 구간 `[i+1, n-1]`에서 합이 `-nums[i]`인 쌍을 양끝 투 포인터로 찾는다. `i`, `lo`, `hi` 모두에서 같은 값 건너뛰기(dedup) 필수.
- **핵심:** "정렬 → 고정 → 투 포인터" 전형. O(n²). dedup 한 줄을 빠뜨리면 중복 답이 나온다.

## 8. Trapping Rain Water 🔴
- **출처:** [LeetCode #42](https://leetcode.com/problems/trapping-rain-water/)
- **요약:** 높이 배열에서 비가 온 뒤 고이는 물의 총량을 구한다.
- **입력/출력:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]` → `6`.
- **힌트:** `lo, hi` 양끝 + `left_max, right_max` 추적. 낮은 벽 쪽을 처리: `left_max`가 작으면 왼쪽에서 `left_max - height[lo]`만큼 물이 고이고 `lo++`, 아니면 오른쪽 처리. O(n)/O(1).
- **핵심:** 각 칸에 고이는 물 = `min(왼쪽 최대, 오른쪽 최대) - 높이`. 양끝 투 포인터로 접두/접미 최댓값 배열 없이 O(1) 공간에 해결.

---

## 풀이 순서 추천
1. **회문·Two Sum II·중복 제거(1~3)** 로 세 가지 기본형(양끝/빠름·느림)을 손에 익힌다.
2. **제곱·Container(4~5)** 로 "병합형"과 "낮은 쪽 이동" 아이디어를 익힌다.
3. **숫자의 표현(6)** 으로 구간 합형(윈도우 성격)을 맛본다 → [[day-20-sliding-window/concept|Day 20]]의 다리.
4. **3Sum·빗물(7~8)** 로 "정렬+고정+투 포인터", "최댓값 추적형" 응용까지 확장한다.

전체 해설과 다중 접근·복잡도 비교: [solutions.py](solutions.py)
