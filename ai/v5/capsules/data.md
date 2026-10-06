# Data Capsule

Load for persistence, schema, migration, or state-transition changes.

Check:

- invalid input cannot leave partial mutation;
- retries/duplicates are safe where operations may repeat;
- concurrency cannot silently overwrite or corrupt state;
- old and new representations remain compatible through rollout where needed;
- destructive operations have an explicit scope and recovery story;
- defaults/nullability/backfill behavior is defined for existing data;
- invariants live at an appropriate layer and are testable.

Never infer that a migration is harmless only because it applies cleanly to an empty/local database.
