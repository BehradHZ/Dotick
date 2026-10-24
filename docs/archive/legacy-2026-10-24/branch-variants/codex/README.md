# Dotick

Dotick is being implemented incrementally from its specifications and [roadmap](docs/planning/increment-roadmap.md).

The current implementation contains the verified **Increment 0 engineering foundation**, locally complete **Increment 1 backend**, and a usable minimal **Increment 1 Expo client**. The client signs in, opens Inbox/Lists, creates and edits Tasks, changes status and placement, and uses Trash/restore on web and Expo-native bundles. Increment 1 still needs configured external-provider smoke tests, hosted CI and release gates before the whole increment can be closed.

Follow [environment setup](docs/development/environment-setup.md) to run it, and the [Increment 1 client review](docs/tracking/increment-1-client-review.md) for verified results and remaining gates. The prototype examples guide visual and interaction design; the specifications define behavior.

## Source of truth

Start at [docs/README.md](docs/README.md). Behavioral authority is:

1. [System Definition](docs/requirements/system-definition.md)
2. [Decision Register](docs/decision-register.md)
3. [Formal SRS](docs/requirements/srs.md)
4. [Domain Model](docs/design/domain-model.md) and design documents
5. [Roadmap](docs/planning/increment-roadmap.md) and derived references

The roadmap owns implementation order. It does not change product semantics. The archived previous implementation is not an active source of truth.

## Repository

- `apps/api`: Django API, custom UUID user model, migrations and tests.
- `apps/client`: TypeScript + Expo/React Native for Web client and component tests.
- `e2e`: desktop/mobile client-to-PostgreSQL verification.
- `docs`: requirements, design, roadmap, setup and verification evidence.
- `scripts`: traceability checker and local exported-web server.

Each increment adds only its own implementation scope, updates traceability, and runs the applicable tests and build gates.
