"""EconoCausal Causal Evaluation Package.

Owned by Tanishka (Kanshika) — Causal DAG, Propensity Diagnostics,
Refutation Checks, and Uplift Evaluation.
"""

from backend.app.causal.dag import (
    CANDIDATE_COVARIATES,
    OUTCOME,
    TREATMENT,
    CausalDAG,
    build_causal_dag,
)
from backend.app.causal.propensity import (
    categorical_balance_diagnostics,
    covariate_balance_diagnostics,
    estimate_propensity_scores,
    propensity_diagnostics,
)
from backend.app.causal.refutation import (
    ALLOWED_STATUSES,
    REFUTATION_METHODS,
    format_refutation_result,
    get_refutation_plan,
    run_refutation_checks,
)
from backend.app.causal.uplift_evaluation import evaluate_uplift

__all__ = [
    "CANDIDATE_COVARIATES",
    "TREATMENT",
    "OUTCOME",
    "CausalDAG",
    "build_causal_dag",
    "estimate_propensity_scores",
    "propensity_diagnostics",
    "covariate_balance_diagnostics",
    "categorical_balance_diagnostics",
    "REFUTATION_METHODS",
    "ALLOWED_STATUSES",
    "get_refutation_plan",
    "format_refutation_result",
    "run_refutation_checks",
    "evaluate_uplift",
]
