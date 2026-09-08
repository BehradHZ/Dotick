# Increment 1 client review

Date: 2026-09-08. Result: usable minimal client locally verified; not an Increment 1 release.

## Delivered boundary

- Expo client targets Android, iOS and web while retaining the approved comic-inspired paper/ink/orange visual direction.
- Email/password sign-in uses revocable JWT access/refresh sessions; credentials and tokens remain in memory.
- First sign-in bootstraps the account Inbox/default Column and IANA timezone.
- Users can open Inbox/Lists, create Lists and Tasks, edit title, choose Todo/Done/Won't_Do, move a Task between Lists, refresh and sign out.
- Ordinary Task deletion uses the current version and remains recoverable through Trash/restore.
- Phone startup derives the API address from Expo's LAN host and keeps it editable for local-network correction.
- I0 `foundation_checkpoints` no longer power the product UI.

## Local verification evidence

- 8 Vitest component/time-vector tests passed, including sign-in/bootstrap, persisted Inbox rendering, draft retention after network failure, versioned status update and sign-out privacy.
- TypeScript, ESLint and Prettier checks passed.
- Expo web export and Android native bundle passed under SDK 57.
- Playwright desktop and mobile workflows passed against the real Django API and PostgreSQL: sign in, bootstrap Inbox, create, reload/reauthenticate, retrieve, complete and trash.
- Backend CORS preflight now explicitly permits the required `If-Match` Task deletion precondition; its trusted/untrusted origin behavior is tested.
- Local developer provisioning produces an active, email-verified product account without weakening the non-local workbench guard.

## Deliberate limits

- UI exposes the initial usable workflow, not every I1 backend management surface. Registration/email verification, Google, Passkey, profile/contact/session management, Folder management and custom Column management still use API boundaries only.
- Tokens are intentionally session-memory only; app restart requires sign-in. Durable secure credential storage belongs to a later security-reviewed client slice.
- Permanent deletion, 30-day purge execution, scheduling, Events/Routines, comments, audit/history, offline synchronization and collaboration retain later roadmap ownership.
- Real email, Google, WebAuthn authenticator and phone delivery require configured environment smoke evidence.
- Hosted CI, release packaging/publication and the existing Increment 0 hosted gates remain open.

The client is sufficient for initial local product use and closes the missing local account-to-Task UI evidence. Increment 1 closes only after remaining provider, hosted CI and release gates pass.
