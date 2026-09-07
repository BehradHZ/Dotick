# Dotick

Dotick is being implemented incrementally from its specifications and [roadmap](docs/planning/increment-roadmap.md).

The current implementation contains the verified **Increment 0 engineering foundation** and the locally complete **Increment 1 backend**: product identity (email/password, Google and Passkey), account/profile/contact preferences, Folder/List/Column organization, Inbox bootstrap and the basic Task lifecycle. Increment 1 still needs the product client integration, configured external-provider smoke tests and release gates before the whole increment can be closed.

Follow [environment setup](docs/development/environment-setup.md) to run it, and the [foundation review](docs/tracking/increment-0-foundation-review.md) for verified results and remaining gates. The prototype examples guide visual and interaction design; the specifications define behavior.

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
