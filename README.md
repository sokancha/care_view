# 🥗 CareView - 개인 맞춤형 식단·운동 추천 서비스

사용자의 **신체 정보, 건강 목표, 알레르기, 보유 식재료**를 기반으로
개인에게 적합한 식단과 운동을 추천하는 헬스케어 서비스입니다.

사용자별 건강 및 알레르기 정보를 관계형 데이터로 관리하고, 이를 기반으로 **알레르기 안전 식단 추천, 보유 식재료 기반 레시피 조회, BMI·연령대 기반 운동 추천, 4주 체중 변화 산출** 기능을 제공하도록 개발했습니다.

---

## 📌 프로젝트 개요

* **프로젝트명**: CareView
* **개발 기간**: 2025.09 ~ 2025.11
* **팀 구성**: 4인
* **프로젝트 유형**: 팀 프로젝트

### 주요 기술

* **Backend**: Python, FastAPI
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Migration**: Alembic
* **Authentication**: JWT
* **API**: RESTful API

---

## 🎯 프로젝트 목표

사용자의 건강 정보와 알레르기 조건을 서비스 데이터와 연결하여 다음 기능을 제공하는 것을 목표로 했습니다.

* 알레르기 정보를 반영한 식단 추천
* 보유 식재료 기반 레시피 추천
* 알레르기 유발 식재료 차단
* 연령대 및 BMI 등급 기반 운동 추천
* 운동 데이터를 기반으로 한 4주 체중 변화 산출

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy

### Database

* PostgreSQL

### Authentication

* JWT
* Password Hashing

### Database Migration

* Alembic

### Development

* Git
* GitHub

---

## 👨‍💻 담당 역할

### Backend 개발 총괄 & Database 설계

백엔드 구조와 데이터베이스 설계를 주도하고, 사용자 인증 및 개인 맞춤형 식단·운동 추천 기능을 API로 구현했습니다.

* 사용자, 알레르기, 레시피, 식재료, 운동 데이터의 관계형 DB 구조 설계
* N:M 관계를 고려한 Association Table 설계
* FastAPI 기반 REST API 설계 및 구현
* JWT 기반 회원가입 / 로그인 / 인증 구현
* 비밀번호 Hashing 및 Access Token 발급·검증
* 사용자 신체 정보 및 건강 목표를 저장하는 Onboarding API 구현
* 사용자 알레르기 정보 저장 및 조회 API 구현
* 사용자 알레르기 기반 식단 필터링 로직 구현
* 보유 식재료 기반 Meal Item 조회 로직 구현
* 알레르기 유발 식재료를 포함한 Meal Item 제외 로직 구현
* 연령대 및 BMI 등급 기반 운동 추천 로직 구현
* 운동 중복 추천 방지 로직 구현
* 운동 칼로리 소모량을 기반으로 한 4주 체중 변화 산출 로직 구현

---

## 🏗️ System Architecture

```text
┌─────────────────────────┐
│         Client          │
└────────────┬────────────┘
             │ HTTP / REST API
             ▼
┌─────────────────────────┐
│        FastAPI          │
│                         │
│  ┌───────────────────┐  │
│  │ Authentication     │  │
│  │ JWT / Security     │  │
│  └───────────────────┘  │
│                         │
│  ┌───────────────────┐  │
│  │ Service Layer      │  │
│  │                    │  │
│  │ Meal Recommendation│  │
│  │ Exercise           │  │
│  │ Expected Effect    │  │
│  └───────────────────┘  │
└────────────┬────────────┘
             │ SQLAlchemy
             ▼
┌─────────────────────────┐
│       PostgreSQL        │
│                         │
│ User / Allergy          │
│ Recipe / MealItem       │
│ Ingredient              │
│ Exercise                │
│ HealthMetric            │
│ CookingStep             │
└─────────────────────────┘
```

---

## 🗄️ Database Design

사용자와 식단 데이터를 하나의 테이블에 저장하지 않고, **데이터의 역할과 관계를 분리하여 관계형 데이터베이스 구조를 설계**했습니다.

특히 레시피와 식재료, 사용자와 알레르기처럼 하나의 데이터가 여러 데이터와 연결되는 관계를 Association Table로 분리했습니다.

### 주요 데이터 관계

```text
User
 │
 ├── User ↔ Allergy
 │       └── N:M
 │
 └── Onboarding
         ├── 신체 정보
         └── 건강 목표


Recipe
 │
 ├── RecipeComposition
 │       ↓
 │    MealItem
 │       │
 │       └── ItemIngredient
 │               ↓
 │           Ingredient
 │
 └── RecipeAllergen
         ↓
      Allergy


Ingredient
 │
 └── IngredientAllergen
         ↓
      Allergy


MealItem
 │
 └── CookingStep
```

### 주요 관계

* **User ↔ Allergy** : N:M
* **Recipe ↔ Allergy** : N:M
* **Ingredient ↔ Allergy** : N:M
* **Recipe ↔ MealItem** : `RecipeComposition`을 통한 관계
* **MealItem ↔ Ingredient** : `ItemIngredient`을 통한 N:M 관계
* **MealItem → CookingStep** : 1:N

이러한 구조를 통해 레시피 구성 재료와 알레르기 정보를 분리하여 관리하고, 식재료 단위의 알레르기 검증 및 보유 재료 기반 추천이 가능하도록 설계했습니다.

---

# 🍽️ 주요 기능

## 1. 알레르기 기반 식단 추천

사용자가 등록한 알레르기 정보를 기반으로 알레르기 유발 레시피를 제외하고 **아침·점심·저녁 식단을 각각 추천**합니다.

사용자의 알레르기 ID를 조회한 뒤 `RecipeAllergen` 관계 테이블에서 해당 알레르기를 포함하는 Recipe ID를 서브쿼리로 조회하고, 메인 Recipe 조회에서 `NOT IN` 조건으로 제외했습니다.

```text
사용자 알레르기
      ↓
RecipeAllergen
      ↓
알레르기 포함 Recipe ID 조회
      ↓
Subquery
      ↓
NOT IN
      ↓
알레르기 레시피 제외
      ↓
식사 유형별 Recipe 조회
      ↓
아침 / 점심 / 저녁 추천
```

실제 SQLAlchemy 구현에서는 다음과 같은 방식으로 알레르기 포함 레시피를 제외합니다.

```python
~Recipe.recipe_id.in_(
    allergy_filter_subquery.scalar_subquery()
)
```

각 식사 유형에서는 `func.random()`과 `limit(1)`을 사용하여 조건을 만족하는 레시피 중 하나를 선택합니다.

---

## 2. 보유 식재료 기반 레시피 추천

사용자가 보유하고 있는 식재료를 입력하면 해당 재료를 **모두 포함하는 Meal Item**을 조회합니다.

```text
사용자 입력 식재료
        ↓
Ingredient ID 조회
        ↓
ItemIngredient
        ↓
입력 재료를 모두 포함하는 MealItem 선별
        ↓
Recipe / CookingStep 관계 조회
        ↓
추천 결과 제공
```

입력받은 식재료의 개수를 기준으로 `GROUP BY`와 `HAVING`을 사용하여 필요한 재료를 모두 포함하는 Meal Item을 선별했습니다.

---

## 3. 알레르기 유발 식재료 차단

보유 식재료 기반 추천에서는 사용자의 알레르기와 식재료의 관계를 `IngredientAllergen`을 통해 확인합니다.

알레르기를 유발하는 Ingredient가 포함된 Meal Item ID를 서브쿼리로 먼저 조회한 후, `notin_()`을 사용하여 해당 Meal Item을 추천 대상에서 제외했습니다.

```text
사용자 알레르기
      ↓
IngredientAllergen
      ↓
알레르기 유발 Ingredient ID
      ↓
ItemIngredient
      ↓
해당 Ingredient를 포함하는 MealItem ID
      ↓
Subquery
      ↓
NOT IN
      ↓
알레르기 MealItem 제외
```

실제 구현에서는 다음과 같이 SQLAlchemy의 `notin_()`을 사용했습니다.

```python
ItemIngredient.item_id.notin_(
    allergy_containing_item_ids
)
```

이를 통해 단순한 문자열 비교가 아니라 **관계형 데이터베이스의 관계와 서브쿼리를 활용하여 알레르기 유발 항목을 제외**하도록 구현했습니다.

---

## 4. 연령대 및 BMI 기반 운동 추천

사용자의 생년월일과 신체 정보를 기반으로 연령대와 BMI 등급을 계산하고, 이에 대응하는 운동 데이터를 조회합니다.

### 연령대 계산

```text
생년월일
   ↓
현재 나이 계산
   ↓
10대 / 20대 / 30대 / 40대 /
50대 / 60대 이상
```

### BMI 등급 계산

```text
키 + 체중
   ↓
BMI 계산
   ↓
BMI 등급 분류
   ↓
저체중 / 정상 / 비만전단계 /
1단계 / 2단계 / 3단계
```

연령대와 BMI 등급을 조합하여 데이터베이스의 사용자 그룹을 조회하고, 해당 그룹에 연결된 운동 데이터를 기반으로 운동 세트를 구성합니다.

각 운동 세트는 다음 세 단계로 구성됩니다.

```text
준비운동
   ↓
본운동
   ↓
마무리운동
```

또한 이미 선택된 운동 ID를 `notin_()` 조건으로 제외하여 아침·점심·저녁 운동 간 동일한 운동이 중복 추천되지 않도록 구현했습니다.

---

## 5. 4주 체중 및 BMI 변화 산출

추천 운동의 일일 예상 칼로리 소모량을 기반으로 **4주간의 예상 체중과 BMI 변화를 계산**합니다.

현재 체중과 운동으로 인한 일일 예상 칼로리 소모량을 이용하여 주당 예상 체중 감소량을 계산하고, 1~4주차의 예상 체중과 BMI를 산출합니다.

```text
현재 체중
     +
일일 예상 칼로리 소모량
     ↓
주당 예상 체중 감소량
     ↓
┌──────────────┐
│ 1주차        │
│ 예상 체중/BMI│
├──────────────┤
│ 2주차        │
│ 예상 체중/BMI│
├──────────────┤
│ 3주차        │
│ 예상 체중/BMI│
├──────────────┤
│ 4주차        │
│ 예상 체중/BMI│
└──────────────┘
```

체중 변화는 **1kg 감량에 7,700 kcal의 에너지 적자가 필요하다는 가정**을 기반으로 산출합니다.

따라서 이 기능은 머신러닝 기반 예측 모델이 아니라 **운동 칼로리 소모량을 기반으로 한 규칙 기반 산출 로직**입니다.

---

# 🔥 Trouble Shooting

## 1. N:M 관계에서 알레르기 필터링

### 문제

사용자의 알레르기 정보와 레시피 및 식재료의 관계가 N:M으로 구성되어 있어, 사용자의 알레르기 조건을 만족하지 않는 식단을 추천 대상에서 제외해야 했습니다.

특히 보유 식재료 기반 추천에서는 사용자의 알레르기 정보가 식재료와 연결되어 있기 때문에, 알레르기 유발 식재료를 포함하는 Meal Item을 별도로 찾아 제외할 필요가 있었습니다.

### 해결

추천 경로에 따라 서로 다른 관계를 활용하여 필터링했습니다.

#### 메인 식단 추천

```text
User Allergy
     ↓
RecipeAllergen
     ↓
알레르기 포함 Recipe ID
     ↓
Subquery
     ↓
NOT IN
     ↓
Recipe 제외
```

`RecipeAllergen`에서 사용자의 알레르기에 해당하는 Recipe ID를 서브쿼리로 조회한 후, 메인 Recipe 조회에서 `NOT IN` 조건을 적용했습니다.

#### 보유 식재료 기반 추천

```text
User Allergy
     ↓
IngredientAllergen
     ↓
알레르기 유발 Ingredient
     ↓
ItemIngredient
     ↓
알레르기 포함 MealItem
     ↓
Subquery
     ↓
NOT IN
     ↓
MealItem 제외
```

알레르기 유발 Ingredient를 포함하는 Meal Item ID를 서브쿼리로 조회한 후 `notin_()` 조건을 적용했습니다.

이를 통해 알레르기 정보를 단순 문자열 비교가 아닌 **관계형 데이터베이스의 관계와 서브쿼리를 활용한 필터링 로직**으로 처리했습니다.

---

## 2. 레시피 / 식재료 데이터 구조 복잡성

### 문제

하나의 Recipe가 여러 Meal Item으로 구성되고, 하나의 Meal Item 역시 여러 Ingredient를 포함할 수 있었습니다.

또한 각 Meal Item에 조리 과정이 연결되어 있어 모든 정보를 하나의 테이블에서 관리할 경우 데이터 중복과 관계 관리의 복잡성이 증가할 수 있었습니다.

### 해결

각 데이터의 역할을 분리하고 관계 테이블을 활용하여 데이터 구조를 정규화했습니다.

```text
Recipe
  │
  └── RecipeComposition
          │
          ▼
       MealItem
          │
          └── ItemIngredient
                  │
                  ▼
              Ingredient

MealItem
  │
  └── CookingStep
```

또한 레시피와 알레르기, 식재료와 알레르기의 관계 역시 각각 별도의 Association Table로 분리했습니다.

```text
Recipe
  │
  └── RecipeAllergen
          │
          ▼
       Allergy

Ingredient
  │
  └── IngredientAllergen
          │
          ▼
       Allergy
```

이를 통해 식단 구성, 식재료, 알레르기, 조리 과정을 각각 독립적으로 관리하면서 필요한 시점에 관계를 통해 조회할 수 있도록 설계했습니다.

---

# 🔐 Authentication

사용자 인증에는 **JWT 기반 Stateless Authentication**을 적용했습니다.

### 인증 흐름

```text
회원가입
   ↓
비밀번호 Hashing
   ↓
사용자 정보 저장
   ↓
로그인
   ↓
Access Token 발급
   ↓
API 요청
   ↓
JWT 검증
   ↓
사용자별 데이터 접근
```

비밀번호는 Hashing하여 저장하고, 인증이 필요한 API에서는 JWT Access Token을 검증하여 사용자별 데이터에 접근하도록 구현했습니다.

---

# 📊 핵심 구현 정리

| 영역             | 구현 내용                         |
| -------------- | ----------------------------- |
| Backend        | FastAPI 기반 REST API           |
| Database       | PostgreSQL 관계형 DB             |
| ORM            | SQLAlchemy                    |
| Migration      | Alembic                       |
| Authentication | JWT / Password Hashing        |
| 식단 추천          | 알레르기 기반 Recipe 필터링            |
| 레시피 추천         | 보유 식재료 기반 Meal Item 조회        |
| 안전성            | 알레르기 유발 Recipe / Meal Item 제외 |
| 운동 추천          | 연령대 + BMI 등급 기반 운동 추천         |
| 중복 방지          | `NOT IN`을 활용한 운동 중복 제외        |
| 체중 변화          | 운동 칼로리 기반 4주 체중 변화 산출         |
| 데이터 모델링        | N:M 관계 및 Association Table 설계 |

---

# 📂 Project Structure

```text
CareView/
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── endpoints/
│   │       ├── exercise.py
│   │       ├── expected_effect.py
│   │       ├── main_page.py
│   │       ├── meals.py
│   │       ├── onboarding.py
│   │       ├── record.py
│   │       └── user.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── allergy.py
│   │   ├── convenience_item.py
│   │   ├── cooking_step.py
│   │   ├── exercise.py
│   │   ├── ingredient_allergy.py
│   │   ├── main_health_metric.py
│   │   ├── meal.py
│   │   ├── onboarding.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── exercise.py
│   │   ├── expected_effect.py
│   │   ├── main_page.py
│   │   ├── meal.py
│   │   ├── onboarding.py
│   │   ├── record.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── exercise_crud.py
│   │   ├── expected_effect_crud.py
│   │   ├── meal_service.py
│   │   └── meals_items_crud.py
│   │
│   ├── initial_data.py
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── Dockerfile
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# 💡 프로젝트를 통해 얻은 경험

이 프로젝트를 통해 단순히 API를 구현하는 것에서 나아가, **서비스 요구사항을 관계형 데이터 구조로 설계하고 이를 실제 API의 조회 로직으로 연결하는 과정**을 경험했습니다.

특히 알레르기 기반 식단 추천 기능을 구현하면서 `RecipeAllergen`, `IngredientAllergen`, `ItemIngredient` 등 여러 관계를 연결하고, 서브쿼리와 `NOT IN`을 활용하여 추천 대상에서 제외해야 하는 데이터를 효율적으로 필터링하는 방법을 경험했습니다.

또한 레시피·식재료·알레르기·조리 과정 간의 관계를 Association Table로 분리하면서 **N:M 관계를 고려한 데이터 모델링과 정규화의 필요성**을 학습했습니다.

운동 추천에서는 사용자의 연령대와 BMI 등급을 데이터베이스의 운동 그룹과 연결하고, 운동 중복을 방지하는 조회 로직까지 구현하면서 **사용자 입력 → 데이터 변환 → DB 조회 → 추천 결과 생성**으로 이어지는 데이터 흐름을 직접 설계했습니다.

마지막으로 운동 칼로리 소모량을 활용한 4주 체중 변화 산출 기능을 구현하면서, 추천 시스템의 결과를 사용자가 이해할 수 있는 지표로 변환하는 과정도 경험했습니다.

---


