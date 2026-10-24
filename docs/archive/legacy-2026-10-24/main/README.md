# Dotick

Dotick is being implemented incrementally from its specifications and [roadmap](docs/planning/increment-roadmap.md).

The current repository contains the **Increment 1 implementation slice**: verified identity and revocable sessions, Folder/List/Column organization, the Basic Task lifecycle, an Expo web/Android product client, PostgreSQL-backed APIs, executable OpenAPI contracts and desktop/mobile browser acceptance coverage.

Increment 1 is released as `v0.2.0`. Closure evidence is recorded in [Increment 1 readiness](docs/tracking/increment-1-readiness.md) and the [formal review](docs/tracking/increment-1-review.md). External email/SMS delivery is optional and unconfigured by default; live provider, authenticator, edge and production-device validation belongs to Increment 11 deployment hardening.

Follow [environment setup](docs/development/environment-setup.md) to run it. The prototype examples guide visual and interaction design; the specifications define behavior.

## Source of truth

Start at [docs/README.md](docs/README.md). Behavioral authority is:

1. [System Definition](docs/requirements/system-definition.md)
2. [Decision Register](docs/decision-register.md)
3. [Formal SRS](docs/requirements/srs.md)
4. [Domain Model](docs/design/domain-model.md) and design documents
5. [Roadmap](docs/planning/increment-roadmap.md) and derived references

The roadmap owns implementation order. It does not change product semantics. The archived previous implementation is not an active source of truth.

## Repository

- `apps/api`: Django API, identity/organization/Task modules, migrations and tests.
- `apps/client`: TypeScript + Expo web/Android product client and component tests.
- `e2e`: desktop/mobile client-to-PostgreSQL verification.
- `docs`: requirements, design, roadmap, setup and verification evidence.
- `scripts`: traceability checker and local exported-web server.

Each increment adds only its own implementation scope, updates traceability, and runs the applicable tests and build gates.

## License and brand

Dotick software is free and open source under the [GNU Affero General Public License v3.0](LICENSE). Personal, commercial, organizational, modification, redistribution, and self-hosting use are permitted subject to AGPL-3.0.

The **Dotick** name, logos, visual marks, and official product identity are not licensed under AGPL-3.0. See [TRADEMARKS.md](TRADEMARKS.md) and [docs/licensing.md](docs/licensing.md) for the software/brand boundary.
