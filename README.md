# BankAssist - AI Agent Security and Guardrails Console

An educational banking AI agent lab demonstrating deterministic guardrail engineering, resource authorization, and safe LLM tool-calling architectures.

**Creator & Maintainer:** Arnav Katyal  
**License:** GNU General Public License v3.0 (GPLv3)

---

## 📌 Core Architectural Philosophy

> **The LLM is not the security policy.**

In secure production systems, an AI model or LLM agent can interpret language and propose actions, but a deterministic application layer must strictly evaluate whether an action is:
- **`ALLOW`**: Execute the requested tool/action within safe boundaries.
- **`BLOCK`**: Deny the request immediately (e.g., prompt injection, unauthorized cross-tenant data access, illegal tool invocations).
- **`ESCALATE`**: Require human-in-the-loop (HITL) approval before executing high-impact operations (e.g., fund transfers over threshold limits).

---

## 🛡️ Security Features & Guardrails

1. **Resource-Level Authorization (Tenant Isolation)**:
   - Enforces strict customer ownership checks (e.g., `CUST-1001` cannot read or modify records belonging to `CUST-2002`).
   - Prevents Insecure Direct Object Reference (IDOR) attacks even if the LLM is prompted to bypass them.
2. **Input Sanitization & Prompt Injection Defense**:
   - Detects jailbreak attempts, delimiter hijacking, and system prompt override patterns.
3. **Sensitive Data Protection**:
   - Redacts or rejects inputs and outputs containing sensitive credentials (OTPs, PINs, passwords, full card numbers).
4. **Tool Allowlisting & Execution Control**:
   - Explicitly checks tool names against an approved schema registry; arbitrary or hallucinated tools are blocked.
5. **Human-in-the-Loop Escalation**:
   - Sensitive financial operations (like `transfer_money`) trigger an approval token requiring explicit human confirmation.
6. **Immutable Audit Logging**:
   - Logs prompt hashes, decision classifications (`ALLOW`/`BLOCK`/`ESCALATE`), and policy rule versions for regulatory compliance.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Modern Web Browser

### 1. Launch BankAssist
```bash
# Navigate to the reference implementation or starter kit:
cd bankassist_lab/takehome_kit/BankAssist-Kiro-Guardrails_basicExamples_working

# Run the local server:
python app.py
```
Open **`http://127.0.0.1:8000`** in your browser to interact with the web interface.

### 2. Run Automated Security Test Suite
```bash
python -m unittest discover -s tests -v
```

---

## 📂 Repository Structure

- `bankassist_lab/`
  - `starter_kit/`: Hands-on skeleton for practicing security implementation and red-teaming.
  - `takehome_kit/`: Fully functional reference implementation with passing security test suite.
- `.gitignore`: Configured to exclude bytecode caches and large presentation/media binaries.
- `LICENSE`: GNU General Public License v3.0.

---

## ⚖️ Disclaimer

This project is intended strictly for educational, security research, and training purposes using synthetic sample data. It is not intended for direct production financial deployments without dedicated enterprise compliance, auditing, and infrastructure review.
