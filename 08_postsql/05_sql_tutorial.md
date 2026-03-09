# DVD Rental 데이터베이스 실전 SQL 튜토리얼 🎬

이 튜토리얼은 방금 복원한 `dvdrental` 데이터베이스를 활용하여 SQL의 기초부터 심화까지 완벽하게 마스터하는 과정입니다. DBeaver의 SQL 편집기를 열고, 아래 쿼리들을 직접 하나씩 복사해서 실행해보며 결과를 눈으로 확인하세요!

---

## 1. 웜업 (Warm-up): 데이터 구조 살펴보기

먼저 우리가 어떤 데이터를 가지고 있는지 가볍게 살펴봅니다.

### 1.1 `SELECT`와 `LIMIT` (모든 데이터 맛보기)
`film` (영화) 테이블과 `customer` (고객) 테이블의 데이터를 위에서부터 5개만 가져와 봅니다.
```sql
-- 어떤 영화들이 있는지 확인
SELECT * 
FROM film 
LIMIT 5;

-- 어떤 고객들이 가입되어 있는지 확인
SELECT * 
FROM customer 
LIMIT 5;
```

### 1.2 필요한 컬럼만 콕 집어 가져오기
테이블의 모든 열(`*`)을 가져오면 너무 무겁습니다. 이름과 이메일만 조회해 봅시다.
```sql
SELECT first_name, last_name, email 
FROM customer;
```

---

## 2. 데이터 필터링 (Filtering)

조건에 맞는 엑기스 데이터만 걸러내는 방법입니다.

### 2.1 `WHERE`: 특정 조건 검색
가게에 있는 영화 중, 대여료(`rental_rate`)가 딱 **0.99 달러**인 저렴한 영화들의 제목만 뽑아봅시다.
```sql
SELECT title, release_year, rental_rate 
FROM film
WHERE rental_rate = 0.99;
```

### 2.2 `AND` / `OR`: 여러 조건 섞기
대여료가 0.99 달러 **이면서(AND)**, 영화 상영 시간(`length`)이 **150분 이상**인 길고 저렴한 가성비 영화를 찾아봅니다.
```sql
SELECT title, rental_rate, length 
FROM film
WHERE rental_rate = 0.99 
  AND length >= 150;
```

### 2.3 `LIKE`: 특정 단어 포함 여부 찾기 (패턴 매칭)
고객 중에 이름(`first_name`)이 **'JOHN'**으로 시작하는 사람을 모두 찾아봅니다. (`%`는 "그 뒤에 뭐가 오든 상관없음"을 뜻합니다.)
```sql
SELECT first_name, last_name, email 
FROM customer
WHERE first_name LIKE 'John%';
```

---

## 3. 정렬과 순위 매기기 (Sorting)

### 3.1 `ORDER BY`: 오름차순/내림차순
가장 영화 상영 시간(`length`)이 **긴 영화 TOP 10**을 뽑아봅니다. `DESC`는 내림차순(큰 것부터)이라는 뜻입니다.
```sql
SELECT title, length, rating 
FROM film
ORDER BY length DESC
LIMIT 10;
```

---

## 4. 데이터 요약과 통계 (Aggregation & Grouping)

엑셀의 "피벗 테이블"과 완벽히 똑같은 역할을 하는 SQL의 꽃입니다. 실무에서 가장 많이 씁니다!

### 4.1 기본 통계 함수 (`COUNT`, `SUM`, `AVG`)
우리 DVD 대여점이 가진 **전체 영화 개수**와 **평균 영화 상영 시간**을 구해봅니다.
```sql
SELECT 
    COUNT(*) AS total_movies, 
    AVG(length) AS average_length 
FROM film;
```

### 4.2 `GROUP BY`: 카테고리별 요약
요약 기준을 잡아줍니다. 영화 등급(`rating` - 예: PG, R 등)별로 **영화가 몇 개씩 있는지** 세어봅시다.
```sql
SELECT 
    rating, 
    COUNT(*) AS movie_count
FROM film
GROUP BY rating
ORDER BY movie_count DESC;
```

### 4.3 `HAVING`: 요약된 결과 필터링
영화의 "대여 기간(`rental_duration`)" 기준으로 그룹핑했을 때, **평균 대여료(`rental_rate`)가 3달러 이상인 그룹만** 남겨봅니다. (WHERE는 그룹핑 전에, HAVING은 그룹핑 후에 필터링합니다.)
```sql
SELECT 
    rental_duration,
    AVG(rental_rate) AS avg_rate
FROM film
GROUP BY rental_duration
HAVING AVG(rental_rate) >= 3.00
ORDER BY avg_rate DESC;
```

---

## 5. 두 테이블 합치기 (JOIN) 🔥

실무에서 데이터는 절대 하나의 테이블에 예쁘게 모여있지 않습니다. 퍼즐 조각을 맞추듯 테이블을 연결해야 합니다. 결제 내역(`payment`) 테이블에는 고객의 ID(`customer_id`)만 있고 이름이 없습니다. 이름은 `customer` 테이블에 있죠. 이 둘을 합쳐봅시다.

### 5.1 `INNER JOIN`: 양쪽에 다 있는 데이터 교집합
회원들의 결제 내역 창을 "이름표"를 붙여 완성해 봅시다.
```sql
SELECT 
    c.first_name, 
    c.last_name, 
    p.amount, 
    p.payment_date
FROM payment p
JOIN customer c 
  ON p.customer_id = c.customer_id -- 두 테이블이 연결되는 연결고리(Key)
LIMIT 10;
```
> ※ `p`와 `c`는 테이블의 별칭(Alias)입니다. `payment p` 라고 쓰면 이제 쿼리 안에서 `p`라는 짧은 이름으로 부를 수 있습니다.

### 5.2 [실전 응용] JOIN + GROUP BY
**가장 많은 돈을 결제한 VIP 고객 TOP 5명**의 이름과 총 결제액을 구해봅시다. 
(이 쿼리가 완벽히 이해된다면 SQL의 절반은 마스터한 것입니다!)
```sql
SELECT 
    c.first_name, 
    c.last_name, 
    SUM(p.amount) AS total_spent
FROM customer c
JOIN payment p 
  ON c.customer_id = p.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 5;
```

---

## 6. 고급 문법 지식 (Subquery & CTE)

### 6.1 Subquery (서브쿼리 - 쿼리 안의 쿼리)
평균치보다 더 비싼 대여료를 가진 "프리미엄 영화"들을 찾고 싶습니다.
```sql
SELECT title, rental_rate 
FROM film
WHERE rental_rate > (
    -- 먼저 평균 대여료를 계산하는 내부 쿼리
    SELECT AVG(rental_rate) FROM film
);
```

### 6.2 CTE (`WITH` 절) - 쿼리를 함수처럼 깔끔하게
방금 위에서 구한 "VIP 고객 5명 명단"을 가상의 표(`vip_list`)로 미리 정의해 두고, 메인 쿼리에서 깔끔하게 꺼내 쓰는 방식입니다. 쿼리가 복잡해질수록 가독성을 높여줍니다.
```sql
WITH vip_list AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 5
)
SELECT 
    c.first_name, 
    c.last_name, 
    v.total_spent
FROM customer c
JOIN vip_list v 
  ON c.customer_id = v.customer_id;
```

---

## 7. 윈도우 함수 (Window Function) 🔥

`GROUP BY`처럼 데이터를 그룹화해서 집계하지만, **기존 데이터의 행(Row)을 하나로 뭉치지 않고 그대로 유지하면서** 계산된 결과를 각각의 행 옆에 붙여주는 아주 강력한 기능입니다. 실무 데이터 분석에서 자주 사용됩니다.

```text
💡 [한눈에 보는 비교: GROUP BY vs 윈도우 함수]

🔹 GROUP BY (행이 뭉쳐짐)
[팀 A] 100원 ──┐
[팀 A] 200원 ──┼──▶ [팀 A] 300원 (총합 1줄로 요약)
[팀 B] 150원 ──┘    [팀 B] 150원 (총합 1줄로 요약)

🔹 윈도우 함수 (행이 그대로 유지됨 + 결과 옆에 추가)
[팀 A] 100원 ──▶ [팀 A] 100원 | (A팀 총합: 300원) 
[팀 A] 200원 ──▶ [팀 A] 200원 | (A팀 총합: 300원) 
[팀 B] 150원 ──▶ [팀 B] 150원 | (B팀 총합: 150원) 
```

### 7.1 `PARTITION BY`: 그룹별 누적합 구하기
고객별(`customer_id`)로 결제한 금액(`amount`)이 시간에 따라 어떻게 누적되는지(`SUM`) 계산해 봅니다.

```text
💡 [한눈에 보는 비교: 누적합 (SUM OVER PARTITION BY)]

결제일자  |  결제액  | 누적 결제액 (시간순)
─────────┼─────────┼────────────────────
[고객 A 파티션]
5월 1일   |  5,000원 | ─▶  5,000원
5월 5일   |  8,000원 | ─▶ 13,000원 (5,000 + 8,000)
5월 12일  | 12,000원 | ─▶ 25,000원 (13,000 + 12,000)

[고객 B 파티션] (새로운 그룹이면 누적합 리셋)
5월 2일   |  7,000원 | ─▶  7,000원
5월 8일   |  3,000원 | ─▶ 10,000원 (7,000 + 3,000)
```
```sql
SELECT 
    customer_id, 
    payment_date, 
    amount,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY payment_date) AS cumulative_spent
FROM payment
LIMIT 15;
```
> ※ `PARTITION BY`로 고객마다 그룹을 나누고, 그 안에서 `ORDER BY`로 시간순으로 정렬하며 금액을 차곡차곡 더해 나갑니다.

### 7.2 `RANK()`: 그룹 내 순위 매기기
영화 등급(`rating`)별로, 대여료(`rental_rate`)가 비싼 순서대로 순위(`RANK`)를 매겨봅니다.

```text
💡 [한눈에 보는 비교: 그룹 내 순위 (RANK OVER PARTITION BY)]

영화 제목 | 등급 | 대여료 | 그룹 내 순위
──────────┼──────┼────────┼─────────────
[PG 등급 파티션]
영화 A    |  PG  |  4.99  | ─▶ 1위
영화 B    |  PG  |  2.99  | ─▶ 2위
영화 C    |  PG  |  0.99  | ─▶ 3위

[R 등급 파티션] (새로운 그룹에서 1등부터 다시 매김)
영화 X    |  R   |  4.99  | ─▶ 1위
영화 Y    |  R   |  4.99  | ─▶ 1위 (동점)
영화 Z    |  R   |  2.99  | ─▶ 3위 (2위 다음이므로 3위)
```

> ❓ **실무 꿀팁: `RANK()` vs `ROW_NUMBER()`**
> 실무에서는 동점자 처리에 따라 다른 함수를 선택합니다. 그중 결과 행수를 엄격히 맞춰야 할 때 `ROW_NUMBER()`를 가장 많이 사용합니다.
> - `ROW_NUMBER()`: **무조건 중복 없는 1, 2, 3등**을 부여합니다. (1등, 2등, 3등... 동점이라도 어떻게든 순서를 가림)
> - `RANK()`: 동점자는 같은 등수, 연속된 등수는 건너뜁니다. (1등, 1등, 3등...)
> - `DENSE_RANK()`: 동점자는 같은 등수지만, 건너뛰지 않습니다. (1등, 1등, 2등...)
>
> ```text
> 💡 [한눈에 보는 비교: 순위 함수 3총사]
> 대여료 | ROW_NUMBER | RANK | DENSE_RANK
> ──────┼────────────┼──────┼───────────
> 4.99원|     1위     |  1위 |     1위
> 4.99원|     2위     |  1위 |     1위
> 2.99원|     3위     |  3위 |     2위
> ```
```sql
SELECT 
    title, 
    rating, 
    rental_rate,
    RANK() OVER (PARTITION BY rating ORDER BY rental_rate DESC) AS rank_in_rating
FROM film
LIMIT 20;
```
> ※ 전체 데이터 통합 순위가 아니라, 각 등급(PG, R 등) 파티션 안에서 독립적으로 1등부터 순위를 매깁니다.

### 7.3 `LAG()`: 이전 데이터 가져오기 (시계열 분석)
특정 고객이 **"이전에는 얼마를 결제했는지"** 바로 옆에 붙여서 비교하고 싶을 때 사용합니다. 현재 결제액과 이전 결제액의 차이를 구하는 등의 시계열 분석(Time-series)에 필수적인 함수입니다.

```text
💡 [한눈에 보는 비교: LAG() 함수의 작동 방식]

결제일자  | 현재 결제액 | 이전 결제액 (LAG)
─────────┼────────────┼──────────────────
5월 1일   |   5,000원  |    (없음, NULL)
5월 5일   |   8,000원  | ─▶ 5,000원 (윗줄에서 가져옴)
5월 12일  |  12,000원  | ─▶ 8,000원 (윗줄에서 가져옴)
5월 20일  |   3,000원  | ─▶ 12,000원 (윗줄에서 가져옴)
```

```sql
SELECT 
    customer_id,
    payment_date,
    amount AS current_amount,
    LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY payment_date) AS previous_amount
FROM payment
WHERE customer_id = 1  -- 1번 고객의 데이터만 확인
ORDER BY payment_date
LIMIT 10;
```
> ※ `LAG(컬럼, 1)`은 1행 이전의 데이터를 가져옵니다. 반대로 다음 데이터를 가져올 때는 `LEAD()` 함수를 사용합니다.
