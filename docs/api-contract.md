# EconoCausal — Shared Causal Evaluation API Contract

**Authors:** Tanishka (Causal Evaluation) in coordination with Harsh (API & Backend) and Khushi (Frontend)  
**Date:** November 2026 (Week 4 Final)  
**Status:** Agreed & Verified  

---

## 1. Overview & Purpose

This contract defines the shared data schemas, endpoint specifications, status flags, and user-facing warning standards for the causal evaluation components in EconoCausal.

It connects:
* **Tanishka's Causal Engine** (`backend/app/causal/`)
* **Harsh's FastAPI Service & Optimizer** (`backend/app/api/`, `optimization/`)
* **Khushi's React Dashboard** (`frontend/src/components/CausalAnalysisPanel.jsx`)

---

## 2. API Endpoints & Data Contracts

### 2.1 Causal DAG Endpoint
* **Route:** `GET /api/causal/dag`
* **Response Status:** `200 OK`

```json
{
  "treatment": "discount_offered",
  "outcome": "purchased",
  "n_nodes": 33,
  "n_edges": 63,
  "is_acyclic": true,
  "candidate_covariates": [
    "age",
    "income_bracket",
    "historical_spend",
    "recency_days",
    "cart_abandonment_rate"
  ],
  "edges": [
    ["discount_offered", "purchased"],
    ["historical_spend", "discount_offered"],
    ["historical_spend", "purchased"]
  ],
  "caveat": "The DAG represents provisional domain assumptions, not empirical proof of zero unobserved confounding."
}
```

---

### 2.2 Propensity & Overlap Diagnostics Endpoint
* **Route:** `POST /api/causal/diagnostics/propensity`
* **Request Body:**
  ```json
  {
    "treatment_col": "discount_offered",
    "covariates": null
  }
  ```
* **Response Status:** `200 OK`
* **Response Body:**
  ```json
  {
    "status": "completed",
    "n_observations": 20000,
    "n_treatment_groups": 4,
    "treatment_levels": [0, 5, 10, 20],
    "probabilities_sum_to_one": true,
    "min_propensity": 0.000578,
    "max_propensity": 0.934422,
    "near_zero_probability_count": 308,
    "overlap_warning": true,
    "warning_message": "308 observations have estimated treatment probability below 0.01, indicating thin overlap in tail customer segments."
  }
  ```

---

### 2.3 Covariate Balance Endpoint
* **Route:** `POST /api/causal/diagnostics/balance`
* **Response Status:** `200 OK`
* **Response Body:**
  ```json
  {
    "numeric_balance": {
      "total_comparisons": 126,
      "imbalanced_comparisons_at_0_1": 24,
      "max_smd": 0.9485,
      "max_smd_covariate": "recency_days",
      "treatment_pair": [0, 20]
    },
    "categorical_balance": {
      "total_comparisons": 60,
      "comparisons_above_0_1": 0,
      "max_proportion_diff": 0.0226
    },
    "interpretation": "Descriptive balance diagnostics indicate mild-to-moderate imbalance in recency_days between 0% and 20% discount tiers."
  }
  ```

---

### 2.4 Refutation Robustness Endpoint
* **Route:** `GET /api/causal/refutation/plan`
* **Response Status:** `200 OK`
* **Response Body:**
  ```json
  {
    "status": "ready_or_unsupported",
    "dependency_available": false,
    "methods": [
      "random_common_cause",
      "placebo_treatment_refuter",
      "data_subset_refuter"
    ],
    "checks": [
      {
        "check_name": "random_common_cause",
        "configuration": {"method_name": "random_common_cause"},
        "status": "unsupported",
        "error": "Missing optional dependency: dowhy",
        "interpretation": "Check was not executed because DoWhy is unavailable in this environment."
      }
    ],
    "causal_claim_proven": false
  }
  ```

---

### 2.5 Uplift & Qini Curve Endpoint
* **Route:** `POST /api/causal/uplift/evaluate`
* **Request Body:**
  ```json
  {
    "treatment_level": 20,
    "control_level": 0,
    "id_col": "customer_id"
  }
  ```
* **Response Status:** `200 OK`
* **Response Body:**
  ```json
  {
    "treatment_level": 20,
    "control_level": 0,
    "n_evaluated": 10000,
    "max_uplift_gain": 102.0,
    "final_uplift_gain": 95.0,
    "ranking": [
      {
        "rank": 1,
        "customer_id": "CUST_00142",
        "score": 0.4852,
        "treatment": 20,
        "outcome": 1,
        "cumulative_treated": 1,
        "cumulative_control": 0,
        "uplift_gain": 1.0
      }
    ]
  }
  ```

---

## 3. UI Display & Warning Standards for Dashboard (Khushi)

| Diagnostic | Safe Display Label | UI Status / Badge | Required User Caveat |
|---|---|:---:|---|
| Propensity Overlap ($P < 0.01$) | **Segment Overlap Warning** | `Amber / Warning` | *"Some customer subsets rarely receive discounts; estimates in this region carry higher uncertainty."* |
| Standardized Mean Difference ($\text{SMD} \ge 0.1$) | **Covariate Imbalance** | `Blue / Info` | *"Descriptive imbalance observed. The DML model adjusts for these features, but unmeasured bias may remain."* |
| DoWhy Refutation | **Model Sensitivity Check** | `Neutral / Unsupported` | *"Refutation tests probe stability against simulated perturbations; passing does not prove causality."* |
| Qini Cumulative Gain | **Targeting Efficiency** | `Green / Metric` | *"Ranks customers by predicted sensitivity. Realized gain depends on stable customer response behavior."* |

---

## 4. Scientific Integrity Rule

To prevent misleading claims to stakeholders:
1. Every evaluation payload returning refutation or diagnostic data must include `"causal_claim_proven": false`.
2. Estimates must be labelled as **"Estimated Incremental Effects"**, never as "Proven Effects" or "Guaranteed Uplift".

