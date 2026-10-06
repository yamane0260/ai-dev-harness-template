# Security Capsule

Load only when security is material.

Check the changed trust boundary, not security in the abstract:

- authenticate the actor before trusting identity;
- authorize the exact resource/action, not only the route or UI;
- validate untrusted input at the boundary and preserve safe output encoding;
- do not expose secrets, credentials, sensitive data, or privileged errors in logs/results;
- consider confused-deputy, cross-user/tenant access, replay, and privilege-escalation paths;
- prefer existing security primitives over custom mechanisms.

Add focused negative criteria where relevant, such as "another user cannot read or mutate this resource." If security behavior cannot be verified with available evidence, return an escalation rather than assuming safety.
