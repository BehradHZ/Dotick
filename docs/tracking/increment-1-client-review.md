# Increment 1 client review

Date: 2026-09-08. Result: usable minimal client locally verified; not an Increment 1 release.

## Delivered boundary

- Expo client targets Android, iOS and web while retaining the approved comic-inspired paper/ink/orange visual direction.
- Email/password sign-in uses revocable JWT access/refresh sessions; credentials and tokens remain in memory.
- Account registration, six-digit email verification/resend and password reset/confirmation are available from the signed-out client.
- Configured web builds can hand a Google ID credential to the backend and perform a browser WebAuthn Passkey ceremony. Provider-specific native builds remain a release input.
- First sign-in bootstraps the account Inbox/default Column and IANA timezone.
- Users can open Inbox/Lists, create Lists and Tasks, edit title, choose Todo/Done/Won't_Do, move a Task between Lists, refresh and sign out.
- Ordinary Task deletion uses the current version and remains recoverable through Trash/restore.
- Phone startup derives the API address from Expo's LAN host and keeps it editable for local-network correction.
- I0 `foundation_checkpoints` no longer power the product UI.

## Local verification evidence recorded on 2026-09-08

- 11 Vitest auth/component/time-vector tests passed, including registration/verification, password recovery, safe validation errors, sign-in/bootstrap, persisted Inbox rendering, draft retention after network failure, versioned status update and sign-out privacy.
- TypeScript, ESLint and Prettier checks passed.
- Expo web export and Android native bundle passed under SDK 57.
- Playwright desktop and mobile workflows passed against the real Django API and PostgreSQL: sign in, bootstrap Inbox, create, reload/reauthenticate, retrieve, complete and trash.
- Backend CORS preflight explicitly permits the required `If-Match` Task deletion precondition while denying untrusted origins and cross-origin credentials.
- Local developer provisioning produces an active, email-verified product account without weakening the non-local workbench guard.

## Deliberate limits

- UI exposes complete signed-out email identity flows plus configured web Google/Passkey sign-in. Passkey enrollment, Google linking, profile/contact/session management, Folder management and custom Column management remain API-first boundaries rather than complete product UI surfaces.
- Tokens are intentionally session-memory only; app restart requires sign-in. Durable secure credential storage belongs to a later security-reviewed client slice.
- Permanent deletion, 30-day purge execution, scheduling, Events/Routines, comments, audit/history, offline synchronization and collaboration retain later roadmap ownership.
- Real email, Google, WebAuthn authenticator and phone delivery require configured environment smoke evidence.

## Post-review reconciliation — 2026-09-16

Later commits and hosted evidence change the release-status wording, not the deliberate product limits above:

- Hosted CI is now green for the current I1 product slice. Run `35057831342` succeeded against audited implementation HEAD `7302ca3b18a79af35058828102bb62e845a56645` before this documentation reconciliation.
- The same hosted workflow covers frontend component/network/time tests, web export, desktop/mobile Playwright E2E and container persistence smoke alongside backend/security/migration gates.
- Increment 0 is already formally closed; its hosted gates are no longer an I1 dependency.
- The backend contract now exactly matches the published I1 route set and rejects malformed/oversized/non-JSON writes with stable error envelopes.
- Production CORS/host/origin/HTTPS settings have been hardened without changing the local Expo-Go development path.

Formal Increment 1 closure still requires configured real email/Google/WebAuthn/phone smoke, deployment-edge rate-limit enforcement for the declared identity ceremonies, and the formal Increment 1 release record/publication. No public GitHub Release or production deployment is claimed.

For the complete 148-commit reconciliation, see [development-commit-audit.md](development-commit-audit.md).
