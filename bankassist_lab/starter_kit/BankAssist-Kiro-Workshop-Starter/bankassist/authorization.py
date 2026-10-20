"""BankAssist — AI Guardrails Practice Lab

Developer & Maintainer: Arnav Katyal

EDUCATIONAL & ETHICAL USE ONLY
This is a simplified practice application for training and demonstration.
It is not a production banking application or security framework.
Use synthetic data only and test only in environments you are authorized to use.
Further security, architecture, compliance, privacy, and engineering validation
is required before adapting any pattern for real-world use.
"""

def authorize(user_id: str, requested_customer_id: str | None) -> tuple[bool, str]:
    """
    Enforce resource-level authorization.
    A customer can access only their own customer data.
    Access control is enforced deterministically by the application,
    independent of LLM outputs or system prompts.
    """
    if not requested_customer_id or requested_customer_id == user_id:
        return True, "Access authorized."

    return False, f"Access denied: User '{user_id}' is not authorized to access data for customer '{requested_customer_id}'."

