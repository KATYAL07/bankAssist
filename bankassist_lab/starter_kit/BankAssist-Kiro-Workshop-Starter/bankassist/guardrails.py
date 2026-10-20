"""BankAssist — AI Guardrails Practice Lab

Developer & Maintainer: Arnav Katyal

EDUCATIONAL & ETHICAL USE ONLY
This is a simplified practice application for training and demonstration.
It is not a production banking application or security framework.
Use synthetic data only and test only in environments you are authorized to use.
Further security, architecture, compliance, privacy, and engineering validation
is required before adapting any pattern for real-world use.
"""
import re
from .models import PolicyDecision, ToolCall
from .authorization import authorize


POLICY_VERSION = "1.0"

# Approved tools and their base risk levels
ALLOWED_TOOLS = {
    "get_public_fee": "LOW",
    "get_balance": "LOW",
    "get_transactions": "MEDIUM",
    "create_service_request": "MEDIUM",
    "send_otp": "LOW",
    "transfer_money": "HIGH",
}

# Compiled regex patterns for prompt injection & jailbreak detection
PROMPT_INJECTION_PATTERNS = [
    re.compile(r"(?i)\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b"),
    re.compile(r"(?i)\breveal\s+(?:your\s+|the\s+)?system\s+prompt\b"),
    re.compile(r"(?i)\bsystem\s+prompt\b"),
    re.compile(r"(?i)\bhidden\s+instruction\b"),
    re.compile(r"(?i)\bpretend\b"),
    re.compile(r"(?i)\bjailbreak\b"),
    re.compile(r"(?i)\bdeveloper\s+mode\b"),
    re.compile(r"(?i)\b(?:disregard|override)\s+(?:all\s+)?(?:rules|instructions|policies)\b"),
    re.compile(r"(?i)\bbypass\s+(?:policy|rules|guardrails|security)\b"),
    re.compile(r"(?i)\bi\s+am\s+(?:an?\s+)?admin\b"),
    re.compile(r"(?i)\badmin\s+access\b"),
    re.compile(r"(?i)\broleplay\s+as\b"),
    re.compile(r"(?i)\byou\s+are\s+now\b"),
    re.compile(r"(?i)\bact\s+as\b"),
    re.compile(r"(?i)\bDAN\b"),
    re.compile(r"(?i)\bunfiltered\b"),
]


# Sensitive credentials & PII patterns (OTP, PIN, Card Numbers, Passwords)
SENSITIVE_DATA_PATTERNS = [
    re.compile(r"(?i)\b(?:otp|one[- ]time[- ]password)\b.*?\b\d{4,8}\b"),
    re.compile(r"(?i)\b\d{4,8}\b.*?\b(?:otp|one[- ]time[- ]password)\b"),
    re.compile(r"(?i)\b(?:otp|pin|cvv|password)\s*[:=]?\s*\d{3,8}\b"),
    re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b"),  # 16-digit card number format
    re.compile(r"\b\d{15,19}\b"),              # Raw card-like digit sequences
]

# Output leak patterns (credentials, raw secrets, internal prompts)
OUTPUT_LEAK_PATTERNS = [
    re.compile(r"(?i)\b(?:otp|pin|cvv|password)\s*[:=]?\s*\d{3,8}\b"),
    re.compile(r"(?i)\bsystem\s+prompt\s*:", re.IGNORECASE),
    re.compile(r"(?i)never\s+share\s+this\s+internal\s+instruction"),
    re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b"),
]

def input_guardrail(text: str) -> PolicyDecision:
    """
    Validate user input before sending to agent or model.
    Detects prompt injection, secret leaks (OTP/PIN/cards), and privilege escalation.
    """
    # 1. Prompt Injection & Jailbreak check
    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern.search(text):
            return PolicyDecision(
                decision="BLOCK",
                risk="HIGH",
                policies=["PROMPT_INJECTION_PROTECTION"],
                reason="Input contains prompt injection or adversarial bypass pattern."
            )

    # 2. Sensitive Data & Secret Leakage check
    for pattern in SENSITIVE_DATA_PATTERNS:
        if pattern.search(text):
            return PolicyDecision(
                decision="BLOCK",
                risk="HIGH",
                policies=["SENSITIVE_DATA_PROTECTION"],
                reason="Input contains sensitive credentials or confidential data (e.g. OTP, PIN, Card number)."
            )

    return PolicyDecision(
        decision="ALLOW",
        risk="LOW",
        policies=["INPUT_VALIDATION_PASSED"],
        reason="Input passed all security guardrails."
    )

def tool_guardrail(user_id: str, call: ToolCall) -> PolicyDecision:
    """
    Evaluate proposed tool execution against application security policies.
    - Blocks unknown or unapproved tools
    - Enforces strict resource-level authorization
    - Escalates high-impact operations for human-in-the-loop review
    """
    # 1. Tool Allowlist Check
    if call.name not in ALLOWED_TOOLS:
        return PolicyDecision(
            decision="BLOCK",
            risk="HIGH",
            policies=["TOOL_ALLOWLIST"],
            reason=f"Tool '{call.name}' is not in the approved tool allowlist."
        )

    # 2. Resource-level Authorization Check
    args = call.arguments or {}
    requested_customer_id = args.get("requested_customer_id") or args.get("customer_id")
    is_authorized, auth_reason = authorize(user_id, requested_customer_id)
    if not is_authorized:
        return PolicyDecision(
            decision="BLOCK",
            risk="HIGH",
            policies=["RESOURCE_AUTHORIZATION"],
            reason=auth_reason
        )

    # 3. High-Impact Action Escalation (Human-in-the-loop)
    if call.name == "transfer_money":
        return PolicyDecision(
            decision="ESCALATE",
            risk="HIGH",
            policies=["HUMAN_IN_THE_LOOP", "HIGH_IMPACT_TRANSACTION"],
            reason=f"Financial transfer of funds requires human supervisor approval."
        )

    # 4. Tool call approved
    base_risk = ALLOWED_TOOLS.get(call.name, "LOW")
    return PolicyDecision(
        decision="ALLOW",
        risk=base_risk,
        policies=["APPROVED_TOOL_EXECUTION"],
        reason="Tool call is authorized and conforms to policy."
    )

def output_guardrail(output: str) -> PolicyDecision:
    """
    Validate outgoing responses before delivery to the user.
    Prevents leakage of sensitive data (OTP, internal system prompt, card numbers).
    """
    for pattern in OUTPUT_LEAK_PATTERNS:
        if pattern.search(output):
            return PolicyDecision(
                decision="BLOCK",
                risk="HIGH",
                policies=["SENSITIVE_DATA_OUTPUT_PROTECTION"],
                reason="Response contains sensitive data or internal instructions."
            )

    return PolicyDecision(
        decision="ALLOW",
        risk="LOW",
        policies=["OUTPUT_SAFETY_PASSED"],
        reason="Output passed safety checks."
    )

