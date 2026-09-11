# Increment 1 Authentication Use Cases

> **Status:** Formal analysis artifact for Increment 1; this document does not assert implementation completion.
>
> **Date:** 2026-09-11
>
> **Authority:** System Definition §§3.1, 6.13, 9.1 → Decision Register → SRS §3.12 (`SRS-AUTH-001..015`) → this analysis artifact.
>
> **Design handoff:** `docs/design/authentication-design.md` and `docs/design/openapi.json` define implementation-level protocol details. If this document conflicts with a higher-authority source, the higher-authority source wins.

## 1. Scope

These use cases formalize the Increment 1 authentication boundary:

- email/password registration, verification, sign-in and recovery;
- revocable JWT sessions;
- Google authentication and explicit account linking;
- Passkey enrollment and authentication;
- independent fallback configuration for Google users;
- verified secondary email/phone contacts where they affect account identity and discovery safety.

The following are intentionally **not** separate authentication use cases here:

- `SRS-AUTH-014..015` Profile Picture behavior, which is Account identity presentation rather than authentication;
- TOTP or SMS-based second-factor enrollment, which `SRS-AUTH-011` explicitly does not require in Current Scope;
- Enterprise SSO or any external identity provider other than Google;
- authorization for shared/group resources, which belongs to Increment 7.

## 2. Actors and shared terms

| Actor | Role |
|---|---|
| Visitor | Signed-out person attempting registration, verification, recovery or authentication. |
| Authenticated User | User represented by a valid, non-revoked Dotick session. |
| Dotick Identity Service | Server-side authority for internal User identity, credential binding and session validity. |
| Email Delivery Adapter | Sends verification and recovery challenges; delivery does not decide challenge validity. |
| Google | Sole external authentication provider in Current Scope. |
| Platform Authenticator | WebAuthn authenticator used for Passkey registration/authentication. |

**Internal identity** means the stable Dotick `User.id`. Password, Google and Passkey are credential methods around that identity; none replaces it.

## 3. Global authentication invariants

These invariants apply to every use case below.

1. A credential method resolves to exactly one stable internal User identity. Provider-specific User records are not alternative Account identities.
2. Passwords are never stored or logged in plaintext and must pass through the approved secure password-hashing path.
3. Unverified/inactive email credentials cannot authenticate as a verified Account.
4. Public authentication/recovery responses must not disclose whether an Account exists when the canonical flow requires enumeration resistance.
5. Google email alone is not sufficient proof for silent account linking; the provider subject is the external identity key and linking to an existing Dotick Account requires authenticated proof.
6. Every product session is server-revocable. Revocation must affect credentials for that session rather than relying only on token expiry.
7. Authentication methods must converge on the same session/authorization boundary after successful authentication.
8. Pending secondary contacts are not active contacts and cannot be used for discovery or contact-dependent flows.
9. Secrets, verification/reset codes, bearer tokens and private credential material must not enter ordinary logs.
10. Current Scope has no mandatory TOTP/SMS second-factor use case.

---

## UC-AUTH-001 — Register with email and password

**Primary actor:** Visitor  
**Supporting actor:** Email Delivery Adapter  
**Goal:** Create a pending Dotick Account identity that can become active after email verification.  
**Trace:** `SRS-AUTH-001`, `SRS-AUTH-002`, `SRS-AUTH-008`

**Preconditions**

- The Visitor is not required to have an authenticated Dotick session.
- Submitted registration data satisfies the public input contract.

**Trigger**

- The Visitor submits email/password registration.

**Main success flow**

1. Dotick validates registration input and password policy.
2. Dotick normalizes the email according to the authentication design.
3. Dotick creates or prepares the pending Account/credential state without treating the email as verified.
4. Dotick securely hashes the password; plaintext is not persisted.
5. Dotick creates a verification challenge and requests delivery to the submitted email.
6. Dotick returns the enumeration-safe accepted response defined by the API contract.
7. The Account remains unable to complete verified email/password sign-in until UC-AUTH-002 succeeds.

**Alternate / error flows**

- A1. The email already belongs to an Account: the public response remains enumeration-safe; no duplicate internal Account is created.
- A2. Registration is rate-limited or a newer challenge supersedes the previous one: the public response follows the same disclosure-safe surface.
- A3. Delivery is unavailable: challenge/account state must not falsely become verified.
- A4. Input or password policy is invalid: return the stable validation error envelope and create no valid credential state.

**Postconditions**

- On accepted registration, there is at most one intended internal Account identity for the email.
- No verified authentication state exists until email verification succeeds.

---

## UC-AUTH-002 — Verify or resend the primary email challenge

**Primary actor:** Visitor  
**Supporting actor:** Email Delivery Adapter  
**Goal:** Prove control of the primary login email and activate email/password authentication.  
**Trace:** `SRS-AUTH-008`, `SRS-AUTH-012`, `SRS-AUTH-013`

**Preconditions**

- A pending verification challenge may exist for the submitted email.

**Trigger**

- The Visitor submits a verification code, or requests a replacement code.

**Main success flow — verification**

1. Dotick identifies the applicable pending verification challenge without exposing unrelated Account state.
2. Dotick validates that the challenge is correct, unexpired, usable and intended for email verification.
3. Dotick consumes the challenge so it cannot be replayed.
4. Dotick marks the primary email verified and activates the Account state required for password sign-in.
5. Dotick returns the success response defined by the API contract.

**Resend flow**

1. The Visitor requests another verification message.
2. Dotick applies the configured challenge lifecycle/rate controls.
3. A newer challenge invalidates any older challenge for the same purpose where required by the authentication design.
4. Dotick returns the same disclosure-safe accepted response regardless of Account enumeration-sensitive state.

**Alternate / error flows**

- A1. Incorrect, expired, consumed, superseded or locked code: return the stable verification failure; do not reveal which internal condition occurred.
- A2. Replay after successful verification: fail without changing Account state.
- A3. Delivery failure on resend: do not mark the email verified.

**Postconditions**

- Successful verification enables the primary email/password credential path.
- Failed verification leaves the Account unverified for this purpose.

---

## UC-AUTH-003 — Sign in with email and password

**Primary actor:** Visitor  
**Goal:** Authenticate to an existing verified Account and obtain a revocable Dotick session.  
**Trace:** `SRS-AUTH-001`, `SRS-AUTH-002`, `SRS-AUTH-004`, `SRS-AUTH-008`

**Preconditions**

- The Account has a verified active primary email.
- A password credential is configured.

**Trigger**

- The Visitor submits email and password credentials.

**Main success flow**

1. Dotick normalizes/locates the login identity without exposing lookup details.
2. Dotick verifies the password through the approved password-hashing framework.
3. Dotick confirms the Account is eligible to authenticate.
4. Dotick creates a new server-tracked authentication session bound to the internal User.
5. Dotick issues the JWT access/refresh pair for that session.
6. The client proceeds as the authenticated User represented by that internal User identity.

**Alternate / error flows**

- A1. Unknown email, wrong password, inactive Account or unverified Account: return the same authentication-failure surface.
- A2. Credential is valid but session issuance cannot complete atomically: do not return usable tokens for an untracked session.

**Postconditions**

- Success produces one revocable authenticated session.
- Failure produces no authenticated session.

---

## UC-AUTH-004 — Reset a forgotten password

**Primary actor:** Visitor  
**Supporting actor:** Email Delivery Adapter  
**Goal:** Replace a forgotten password after proving control of the verified primary email.  
**Trace:** `SRS-AUTH-002`, `SRS-AUTH-004`, `SRS-AUTH-008`

**Preconditions**

- The public reset-request endpoint is available.

**Trigger**

- The Visitor requests password recovery for an email address.

**Main success flow**

1. Dotick accepts the reset request using an enumeration-safe response.
2. If an eligible verified Account exists, Dotick creates a password-reset challenge and requests email delivery.
3. The Visitor submits the valid reset code and a new password.
4. Dotick validates and consumes the reset challenge.
5. Dotick validates and securely hashes the new password.
6. Dotick replaces the password credential.
7. Dotick revokes all existing sessions for the Account.
8. Dotick confirms password-reset completion.

**Alternate / error flows**

- A1. Unknown/ineligible email: reset request still uses the disclosure-safe accepted response and sends no usable challenge.
- A2. Incorrect, expired, consumed or superseded code: fail with the stable reset/verification error and retain the current password.
- A3. New password fails policy: do not consume a valid Account into a partially changed credential state.

**Postconditions**

- Success makes the new password authoritative and all previously active sessions unusable.

---

## UC-AUTH-005 — Refresh an authenticated session

**Primary actor:** Authenticated client holding a refresh credential  
**Goal:** Continue the same Dotick session without re-entering the primary credential.  
**Trace:** `SRS-AUTH-004`

**Preconditions**

- The refresh token is structurally valid and references a current server-side session.

**Trigger**

- The client requests token refresh.

**Main success flow**

1. Dotick validates token signature/claims and resolves its internal User/session binding.
2. Dotick verifies that the session is active and the refresh identity is current.
3. Dotick rotates the refresh credential according to the authentication design.
4. Dotick returns a new access/refresh pair for the same internal User/session boundary.
5. The previous refresh credential becomes unusable.

**Alternate / error flows**

- A1. Session has been revoked: reject refresh.
- A2. Refresh credential has expired, been rotated, replayed or does not match the session: reject refresh.
- A3. Token User and session User do not match: reject refresh as invalid authentication state.

**Postconditions**

- A successful refresh does not create a second Account identity.
- Old refresh credentials cannot be reused successfully.

---

## UC-AUTH-006 — Sign out or revoke sessions

**Primary actor:** Authenticated User  
**Goal:** Invalidate the current, selected, or all authentication sessions owned by the User.  
**Trace:** `SRS-AUTH-004`

**Preconditions**

- The actor is authenticated through a currently valid session.

**Trigger**

- The User chooses logout, revokes a listed session, or revokes all sessions.

**Main success flow**

1. Dotick resolves the actor from the authenticated session.
2. For selected-session revocation, Dotick scopes the target session to the current User before mutation.
3. Dotick records the applicable session(s) as revoked.
4. Existing access/refresh credentials for revoked sessions stop authorizing subsequent requests.
5. Dotick returns the API-defined success response.

**Alternate / error flows**

- A1. Requested session is not owned by the actor: expose no cross-user session data and return the owned-resource not-found/auth-safe surface.
- A2. Current credential is already revoked/invalid: the request cannot use it to revoke or inspect another User's sessions.

**Postconditions**

- Revoked sessions cannot be refreshed or used for authenticated API access.

---

## UC-AUTH-007 — Sign in or create an Account with Google

**Primary actor:** Visitor  
**Supporting actor:** Google  
**Goal:** Authenticate with Google without requiring password or Passkey enrollment first.  
**Trace:** `SRS-AUTH-003`, `SRS-AUTH-005`, `SRS-AUTH-007`, `SRS-AUTH-009`, `SRS-AUTH-010`

**Preconditions**

- Google is the only supported external authentication provider in Current Scope.
- The client has obtained a Google credential through the provider-protected flow.

**Trigger**

- The Visitor submits the Google credential to Dotick.

**Main success flow — already linked subject**

1. Dotick validates the Google credential, including provider authenticity and intended Dotick audience.
2. Dotick resolves the stable Google subject to one internal User.
3. Dotick creates a revocable Dotick session for that internal User.
4. Dotick returns authenticated session credentials and fallback recommendation state.

**Main success flow — new Account**

1. Dotick validates the Google credential and verified provider email.
2. No existing provider-subject binding exists.
3. The verified provider email is not already owned by another Dotick Account.
4. Dotick creates one new internal User and binds the Google subject to it.
5. Dotick creates a normal revocable Dotick session.
6. Dotick indicates that an independent fallback is recommended when none exists.

**Alternate / error flows**

- A1. Google credential is invalid, expired or for the wrong audience: reject authentication.
- A2. Provider subject is not linked but the verified Google email already belongs to a Dotick Account: do **not** silently merge/link; return the account-link-required/conflict flow and require UC-AUTH-008.
- A3. Google is unavailable: an existing password/Passkey fallback remains usable if previously configured; existing valid Dotick sessions remain valid.

**Postconditions**

- Successful Google authentication always resolves to one Dotick internal User and one normal revocable session.
- A Google-only Account is valid; independent fallback is recommended, not mandatory.

---

## UC-AUTH-008 — Link Google to an existing Account

**Primary actor:** Authenticated User  
**Supporting actor:** Google  
**Goal:** Bind a proven Google identity to the already-authenticated Dotick Account without account takeover or silent merge.  
**Trace:** `SRS-AUTH-003`, `SRS-AUTH-007`, `SRS-AUTH-010`

**Preconditions**

- The User has authenticated to the target Dotick Account.
- The linking operation satisfies the recent-authentication requirement defined by the authentication design.

**Trigger**

- The User asks to link a Google credential.

**Main success flow**

1. Dotick validates the Google credential and stable provider subject.
2. Dotick confirms recent proof of control of the target Dotick Account.
3. Dotick confirms the Google subject is not bound to another internal User.
4. Dotick creates the provider-identity binding to the current internal User.
5. Future valid Google authentication for that subject resolves to this same User.

**Alternate / error flows**

- A1. Recent authentication is absent/stale: reject linking.
- A2. Provider subject belongs to another User: reject linking; do not merge Accounts.
- A3. Matching email without authenticated Account proof: insufficient for linking.
- A4. Google credential is invalid: reject linking without altering current authentication methods.

**Postconditions**

- No new internal User is created when linking succeeds.

---

## UC-AUTH-009 — Enroll or remove a Passkey

**Primary actor:** Authenticated User  
**Supporting actor:** Platform Authenticator  
**Goal:** Add a Passkey as an independent credential for the same Dotick Account, or remove an owned Passkey.  
**Trace:** `SRS-AUTH-006`, `SRS-AUTH-010`

**Preconditions — enrollment**

- The User has a valid session satisfying the recent-authentication requirement.
- Dotick RP/origin configuration is valid for the current deployment.

**Trigger**

- The User starts Passkey registration.

**Main success flow — enrollment**

1. Dotick creates a short-lived registration challenge bound to the current internal User.
2. The client invokes the Platform Authenticator with Dotick's WebAuthn options.
3. The User completes authenticator verification.
4. The client submits the ceremony result.
5. Dotick verifies challenge, RP/origin, credential data and User binding.
6. Dotick stores only the credential material required for future public-key authentication; private key material never reaches Dotick.
7. The Passkey becomes an independent authentication method for the same User.

**Removal flow**

1. The authenticated User selects an owned Passkey.
2. Dotick scopes the credential lookup to the current User.
3. Dotick removes/disables that credential without changing internal User identity.

**Alternate / error flows**

- A1. Registration challenge is expired, consumed, mismatched or replayed: reject enrollment.
- A2. WebAuthn verification fails: create no Passkey credential.
- A3. Credential is not owned by the actor: do not expose or remove it.

**Postconditions**

- Successful enrollment creates another credential for the same internal User, not another Account.

---

## UC-AUTH-010 — Sign in with a Passkey

**Primary actor:** Visitor  
**Supporting actor:** Platform Authenticator  
**Goal:** Authenticate to the internal User bound to a valid Passkey.  
**Trace:** `SRS-AUTH-004`, `SRS-AUTH-006`

**Preconditions**

- The deployment supports the configured Dotick WebAuthn RP/origin.
- The Visitor has access to a registered Passkey.

**Trigger**

- The Visitor starts Passkey authentication.

**Main success flow**

1. Dotick issues a short-lived authentication challenge.
2. The client invokes the Platform Authenticator.
3. The Visitor completes authenticator verification.
4. The client submits the signed ceremony result.
5. Dotick verifies the challenge, RP/origin, credential signature/counter rules and credential-to-User binding.
6. Dotick creates a normal revocable Dotick session for the bound internal User.
7. Dotick returns authenticated session credentials.

**Alternate / error flows**

- A1. Unknown credential or invalid ceremony: return the authentication-safe failure surface.
- A2. Challenge is expired, consumed, mismatched or replayed: reject authentication.
- A3. Credential verification indicates an invalid/replayed authenticator state: reject authentication according to the WebAuthn security design.

**Postconditions**

- Success produces the same internal User/session boundary as password or Google authentication.

---

## UC-AUTH-011 — Configure or change an independent password fallback

**Primary actor:** Authenticated User  
**Goal:** Add a password fallback to an Account that does not have one, or safely change an existing password.  
**Trace:** `SRS-AUTH-001`, `SRS-AUTH-002`, `SRS-AUTH-005`, `SRS-AUTH-010`, `SRS-AUTH-011`

**Preconditions**

- The User is authenticated to the target Account.
- Adding a new password fallback satisfies the recent-authentication rule.

**Trigger**

- The User chooses to add or change a password authentication method.

**Main success flow — add fallback**

1. Dotick confirms recent control of the current Account.
2. Dotick validates the proposed password.
3. Dotick securely hashes and stores the password credential.
4. The Account remains the same internal User; only the available authentication methods change.
5. Future Google outage does not prevent new sign-in through the configured password fallback.

**Main success flow — change existing password**

1. Dotick requires and verifies the current password according to the authentication design.
2. Dotick validates and securely hashes the replacement password.
3. Dotick replaces the password credential.
4. Dotick applies the required session revocation behavior for a password change.

**Alternate / error flows**

- A1. Recent authentication/current-password proof fails: do not modify the credential.
- A2. Proposed password fails policy: reject without changing the existing credential.
- A3. User has no fallback: UI recommends adding password or Passkey but does not require TOTP/SMS enrollment.

**Postconditions**

- Adding/changing a fallback never creates a second internal User.

---

## UC-AUTH-012 — Add and verify a secondary email or phone contact

**Primary actor:** Authenticated User  
**Supporting actor:** Email/phone delivery adapter  
**Goal:** Add a secondary contact only after proving control of that contact value.  
**Trace:** `SRS-AUTH-012`, `SRS-AUTH-013`

**Preconditions**

- The actor is authenticated to the Account.
- Contact input satisfies normalization/format rules defined by the authentication design.

**Trigger**

- The User submits a new secondary email or phone contact.

**Main success flow**

1. Dotick creates pending contact state; it is not yet active/discoverable.
2. Dotick creates a verification challenge bound to that contact and Account.
3. Dotick requests delivery to the same contact value.
4. The User submits the valid verification code.
5. Dotick validates and consumes the challenge.
6. Dotick promotes the contact to verified active contact state.
7. Only now may the contact participate in discovery/contact-dependent flows allowed elsewhere by the product specification.

**Alternate / error flows**

- A1. Contact is unavailable/conflicts with another Account under the canonical uniqueness policy: reject activation without leaking unnecessary Account information.
- A2. Code is incorrect, expired, consumed or superseded: keep the contact pending/inactive.
- A3. Delivery fails: contact remains unverified.
- A4. Pending contact is queried through active-contact/discovery surfaces: it must not appear.

**Postconditions**

- A verified secondary contact remains separate from the primary login email unless a higher-authority requirement explicitly changes that role.

---

## 4. Use-case trace matrix

| Use case | Primary SRS trace | Public boundary |
|---|---|---|
| `UC-AUTH-001` Register email/password | `SRS-AUTH-001/002/008` | registration API + email adapter |
| `UC-AUTH-002` Verify/resend primary email | `SRS-AUTH-008/012/013` | verification/resend API |
| `UC-AUTH-003` Password sign-in | `SRS-AUTH-001/002/004/008` | token/sign-in API |
| `UC-AUTH-004` Password reset | `SRS-AUTH-002/004/008` | reset request/confirm API + email adapter |
| `UC-AUTH-005` Session refresh | `SRS-AUTH-004` | refresh API |
| `UC-AUTH-006` Session revocation | `SRS-AUTH-004` | logout/session APIs |
| `UC-AUTH-007` Google sign-in | `SRS-AUTH-003/005/007/009/010` | Google credential handoff API |
| `UC-AUTH-008` Google linking | `SRS-AUTH-003/007/010` | authenticated Google-link API |
| `UC-AUTH-009` Passkey enrollment/removal | `SRS-AUTH-006/010` | WebAuthn registration + credential management APIs |
| `UC-AUTH-010` Passkey sign-in | `SRS-AUTH-004/006` | WebAuthn authentication APIs |
| `UC-AUTH-011` Password fallback/change | `SRS-AUTH-001/002/005/010/011` | authenticated password-management API |
| `UC-AUTH-012` Verify secondary contact | `SRS-AUTH-012/013` | contact verification APIs |

`SRS-AUTH-014..015` remain traced to Account/profile presentation rather than these authentication use cases.

## 5. Acceptance-oriented scenario matrix

The implementation tests derived from these use cases must include at least the following scenario classes:

| Area | Required scenarios |
|---|---|
| Enumeration resistance | unknown/known/already-registered email has the required indistinguishable public response for registration/resend/reset request flows |
| Verification lifecycle | valid, invalid, expired, consumed, superseded and replayed challenge |
| Password | correct, incorrect, policy failure, reset success, reset revokes existing sessions |
| Session | issue, rotate refresh, stale refresh replay, current logout, selected revoke, revoke all, revoked access rejection |
| Google | linked subject, new verified email, existing-email link-required conflict, invalid credential, provider outage with independent fallback |
| Linking | recent-auth success, stale-auth rejection, subject already owned by another User, email-only takeover attempt |
| Passkey | registration success/failure, challenge expiry/replay, sign-in success/failure, foreign credential management attempt |
| Cross-method identity | password/Google/Passkey for the same Account resolve to the same internal User and central session model |
| Contacts | pending contact hidden, successful verification activates, failed verification remains inactive |
| Logging/security | no password, challenge code, bearer token or private credential material in ordinary logs |

## 6. Derived implementation constraints

These are analysis constraints, not new product requirements:

- Authentication adapters should depend on a shared internal identity/session service rather than duplicating Account creation/session logic per provider.
- Any endpoint that manages an existing credential or session must derive the target User from authenticated server context rather than accepting an authoritative `user_id` from the client.
- Credential linking and credential-management writes should be transactional where partial state could otherwise create takeover or lockout risk.
- Provider/delivery simulations are suitable for automated tests only at the external adapter boundary; configured Google, WebAuthn and delivery smoke remain release evidence.
- Stable public error codes and payload shapes come from the OpenAPI contract; this use-case document does not define a competing API contract.
