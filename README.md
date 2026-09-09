# Dotick

Dotick is being implemented incrementally from its specifications and [roadmap](docs/planning/increment-roadmap.md).

The current implementation is the **Increment 0 engineering foundation**: Expo web client, Django REST/ASGI API, PostgreSQL migrations, an authenticated developer-only persistence workbench, shared time vectors, automated checks, and CI configuration. Product identity and the Folder/List/Column/Task MVP belong to Increment 1.

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
