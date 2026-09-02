# Runbook: <operation or failure>

Use only when a human/operator may need repeatable action under maintenance or incident conditions.

## When to use
Observable trigger/symptom.

## Preconditions / safety
Access, backups, environment, and actions that must not be taken blindly.

## Diagnose
1. Evidence/source to inspect.
2. Expected healthy signal.
3. Signal that confirms the failure mode.

## Recover
1. Concrete bounded action.
2. Verification after the action.
3. Stop/escalate condition.

## Rollback / forward recovery
What is reversible, what is not, and data implications.

## Escalation
What missing knowledge/expertise requires escalation rather than guessing.

## Evidence / ownership
Relevant code/config/dashboard/log locations and last validated revision/date if useful.
