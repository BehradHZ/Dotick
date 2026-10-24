# Dotick Security Operations

> **Status:** Increment 1 operational baseline; target-provider and deployment-edge evidence remains pending
> **Reconciled:** 2026-09-20

This document turns the implemented I1 security controls into deployment and incident procedures. Design invariants remain in [Security design](../design/security-design.md); variable setup is in [Development environment](../development/environment-setup.md).

## 1. Secret and public configuration handling

- Store Django/JWT signing keys, SMTP passwords, SMS-provider credentials and future provider secrets in deployment secret storage. Do not commit them, bake them into images or print them in logs.
- Treat every `EXPO_PUBLIC_*` value as public client data. `EXPO_PUBLIC_GOOGLE_CLIENT_ID` and `EXPO_PUBLIC_API_URL` may be public; no password, signing key or provider secret may use that prefix.
- Google client IDs are public identifiers. Keep `GOOGLE_OAUTH_CLIENT_ID` and `EXPO_PUBLIC_GOOGLE_CLIENT_ID` equal for the deployed web client.
- Rotate server secrets by updating secret storage, restarting/redeploying all replicas, verifying health and provider flows, and revoking the old value at its issuer. JWT signing-key rotation invalidates existing tokens under the current single-key design, so announce and schedule it accordingly.

## 2. Pre-release configuration checks

1. Run Django's production deployment check with production-like environment values.
2. Confirm SMTP delivery for registration, resend, password reset and secondary-contact verification. Verify sender identity and that credentials never appear in logs.
3. Confirm the configured SMS adapter delivers to a controlled number and leaves failed contacts pending with `contact_delivery_unavailable`.
4. Confirm Google sign-in and explicit account linking with the deployed public client ID. Confirm absence/mismatch does not affect password login.
5. Confirm WebAuthn registration and authentication in a real browser/authenticator at the final HTTPS origin. Check RP ID/name display and rejection from an unrelated origin.
6. Apply [`identity-rate-limit-policy.json`](identity-rate-limit-policy.json) at the proxy/CDN and run threshold smoke for every listed operation family.

Automated provider doubles and configuration tests are necessary implementation evidence, but none substitutes for these target-environment checks.

## 3. Edge rate-limit operation

Apply both configured limits collectively per verified client IP: the default burst threshold is 10 requests per 60 seconds and the sustained threshold is 100 requests per 3,600 seconds. Derive the key only from trusted proxy/CDN connection metadata; strip or overwrite caller-supplied forwarding headers at the trust boundary.

When either threshold is exceeded, return `429` with `Retry-After` and the same account-independent response behavior. Enforcement must be shared across replicas at the edge; do not add a process-local Django counter. Monitor rejects by policy, normalized route and trusted client-IP hash or privacy-preserving equivalent, without logging credentials, codes, assertions or request bodies.

## 4. Monitoring and incident response

Alert on sustained changes in authentication failures, verification/resend volume, provider-unavailable responses, rate-limit rejects and unexpected internal errors. Preserve request IDs, normalized routes, timestamps, deployment version and provider/edge status. Do not preserve authentication payloads or verification codes in ordinary logs.

For suspected credential or provider compromise:

1. isolate or disable the affected provider path without taking core password/manual Task access offline where possible;
2. rotate/revoke the affected secret or provider credential;
3. revoke impacted Dotick AuthSessions when account compromise is plausible;
4. validate owner isolation and audit relevant request IDs;
5. restore service with a controlled smoke test and record the incident timeline, scope and follow-up actions.

## 5. Evidence and review

Retain deployment configuration review, provider smoke results, edge threshold results, secret-rotation records and incident reports according to the hosting environment's retention policy. Review access to production secret storage and provider consoles before release and after personnel or responsibility changes. Enabled real email/SMS, Google, WebAuthn and edge-enforcement evidence is required for Increment 11 production readiness, not the closed I1 repository release.
