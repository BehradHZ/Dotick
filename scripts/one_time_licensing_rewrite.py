from pathlib import Path
import re


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one match in {path}, found {count}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))


def regex_once(path: str, pattern: str, replacement: str) -> None:
    text = read(path)
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.S | re.M)
    if count != 1:
        raise RuntimeError(f"Expected exactly one regex match in {path}, found {count}: {pattern[:120]!r}")
    write(path, updated)


# ---------------------------------------------------------------------------
# Canonical System Definition
# ---------------------------------------------------------------------------
replace_once(
    "docs/requirements/system-definition.md",
    """### Hosting boundary

Current Scope does **not** include supported self-hosting for arbitrary end Users. Publishing source code or making a development environment runnable does not by itself imply providing a self-hosting package, deployment contract, operational documentation, or access to Dotick-managed secrets/configuration.

Dotick is not required to deliver Current Scope in a form that allows every User to operate a fully supported production instance on an arbitrary server. Local/development deployment belongs to the Engineering/Deployment workflow and is not a product capability.""",
    """### Open-source, hosting, support, and brand boundary

All Dotick software source code is licensed under the **GNU Affero General Public License v3.0 (`AGPL-3.0`)**. Subject to that license, individuals and organizations may use, study, modify, redistribute, and self-host the software, including for commercial and internal organizational use, without purchasing a separate software-use license from Dotick.

The open-source license applies to software code, not to Dotick's product identity. The **Dotick** name, logos, visual marks, and other brand identifiers are not licensed under AGPL-3.0. Forks and third-party services must not present themselves as the official Dotick product or imply endorsement, sponsorship, or official affiliation without separate permission. Truthful referential use, preservation of legal notices, and statements such as compatibility with or derivation from Dotick remain subject to applicable law and the project's trademark/brand policy.

Open-source rights do not create a product-level support or deployment entitlement. Current Scope does **not** include guaranteed production support, managed installation, operational assistance, SLA, or professional deployment for arbitrary self-hosted instances. Dotick may offer professional deployment, configuration, migration, customization, maintenance, managed hosting, support, training, or SLA-backed services separately, including as paid services, without restricting rights already granted by AGPL-3.0.

Dotick-managed credentials, production infrastructure, hosted-service data, domains, service accounts, and private operational configuration are not software source code and are not made public merely because the software is open source. A third-party production deployment remains that operator's responsibility unless covered by a separate services agreement.""",
)
replace_once(
    "docs/requirements/system-definition.md",
    "- supported self-hosting and production deployment for arbitrary end Users;",
    "- guaranteed production support, managed deployment, SLA, or operational assistance for arbitrary third-party self-hosted instances; self-hosting itself is permitted under AGPL-3.0;",
)
replace_once(
    "docs/requirements/system-definition.md",
    "Capabilities that are not within Current Scope are not necessarily `Future Commitments`. Capabilities such as a public social network, supported self-hosting, direct User typed-text AI input, a general-purpose public API, full UI localization, and additional TOTP/SMS 2FA are not part of the currently planned product direction and may enter Future Scope only through a new canonical decision.",
    "Capabilities that are not within Current Scope are not necessarily `Future Commitments`. Capabilities such as a public social network, a bundled free support/SLA offering for arbitrary self-hosted production instances, direct User typed-text AI input, a general-purpose public API, full UI localization, and additional TOTP/SMS 2FA are not part of the currently planned product direction and may enter Future Scope only through a new canonical decision. Permission to self-host under AGPL-3.0 is a licensing right, not a Future capability, and does not imply free operational support.",
)
replace_once(
    "docs/requirements/system-definition.md",
    "Future commercialization is likely, but the monetization model is not yet a finalized product decision. Pricing, subscriptions, licensing, billing, or payment flows must not be treated as Future commitments or architectural constraints until a separate Business/Product decision establishes them.",
    "Dotick's software-licensing model is finalized: all Dotick software code is licensed under AGPL-3.0, including for commercial and organizational use. Dotick may monetize optional services such as official managed hosting, professional deployment, configuration, migration, customization, maintenance, support, training, or SLA-backed operations. Exact pricing, packaging, subscriptions, billing/payment flows, and service levels remain separate Business/Product decisions. Dotick's name, logos, and brand identity remain outside the software license and are governed separately by the trademark/brand policy.",
)
replace_once(
    "docs/requirements/system-definition.md",
    "Full UI localization, additional TOTP/SMS 2FA, supported self-hosting, a public social network, direct User typed-text AI input, and a public developer API are not currently Planned Future Capabilities. Their absence from Current Scope must not be implicitly interpreted as a promise that they will be added in future versions.",
    "Full UI localization, additional TOTP/SMS 2FA, a bundled free support/SLA product for arbitrary self-hosted production instances, a public social network, direct User typed-text AI input, and a public developer API are not currently Planned Future Capabilities. Self-hosting permission itself is governed by AGPL-3.0 and must not be confused with a promise of free deployment or operational support.",
)


# ---------------------------------------------------------------------------
# Decision Register — close the licensing decision rather than leaving it open.
# ---------------------------------------------------------------------------
replace_once(
    "docs/decision-register.md",
    "- Current Scope does not include a supported production self-hosting product for arbitrary end users. Source availability or developer-local execution does not create that product commitment.",
    "- Self-hosting is permitted under AGPL-3.0, including commercial and organizational use. Current Scope does not include guaranteed free production support, managed deployment, SLA, or operational assistance for arbitrary self-hosted instances; those may be offered separately as professional services.",
)
replace_once(
    "docs/decision-register.md",
    "- supported self-hosting / production deployment by arbitrary end users;",
    "- guaranteed support, SLA, or professional production deployment for arbitrary self-hosted instances as a Current-Scope product entitlement; self-hosting permission itself is granted by AGPL-3.0;",
)
regex_once(
    "docs/decision-register.md",
    r"## DR-142 — Commercialization is possible but billing/subscription is not yet a product commitment\n.*?(?=\n---\n\n## DR-143)",
    """## DR-142 — Dotick software is AGPL-3.0 open source; brand identity is separately protected

**Status:** CONFIRMED

### Context and previous model

Earlier documentation deliberately kept licensing and monetization open. The project has now finalized the software-licensing principle: every Dotick software component is intended to remain fully available as open-source code, including for personal, commercial, and organizational use. At the same time, opening the software does not require giving unrestricted rights to the Dotick name, logo, visual identity, official domains, or other identifiers that distinguish the official product from forks and third-party services.

Billing, subscription, payment, managed hosting, support, deployment, and SLA behavior remain separate service/product concerns and must not be confused with permission to use the software.

### Decision

- All Dotick software source code is licensed under the **GNU Affero General Public License v3.0 (`AGPL-3.0`)**.
- Individuals and organizations may use, study, modify, redistribute, and self-host Dotick under AGPL-3.0, including for commercial and internal organizational purposes. Dotick does not require a separate commercial software-use license merely because the user is a company or because the software is used commercially.
- AGPL-3.0 obligations apply according to the license, including its source-availability and network-use provisions for covered modified versions.
- Dotick may separately charge for official managed hosting, professional deployment, configuration, migration, customization, maintenance, support, training, and SLA-backed services. Payment purchases a service commitment; it does not purchase permission to exercise software rights already granted by AGPL-3.0.
- The Dotick name, logos, visual marks, and other brand identifiers are **not** licensed under AGPL-3.0. Third parties may not use Dotick branding in a way that presents a fork or service as official, endorsed, sponsored, or operated by Dotick without separate permission.
- Truthful referential use of the Dotick name, preservation of required legal notices, and accurate statements such as "based on Dotick" or "compatible with Dotick" are not intended to be prohibited by the brand policy, subject to applicable law.
- Current architecture must not add software-license payment gates or commercial-user entitlement checks merely to distinguish business users from personal users.
- Exact hosted-service pricing, subscription packaging, billing/payment flows, support tiers, and SLA terms remain separate Business/Product decisions.

### Implications

Dotick follows a **fully open-source software + separately protected brand + optional paid services** model. Forks are permitted by the software license, but they must remain distinguishable from the official Dotick identity. Commercial-service packaging can evolve without rewriting core productivity semantics or converting software-use rights into paid entitlements.
""",
)


# ---------------------------------------------------------------------------
# SRS — formalize licensing/support boundary without adding billing behavior.
# ---------------------------------------------------------------------------
srs = read("docs/requirements/srs.md")
srs = srs.replace("**Version:** 2.9", "**Version:** 3.0", 1)
srs = srs.replace("**Baseline date:** 2026-08-26", "**Baseline date:** 2026-09-18", 1)
if "| 3.0 | 2026-09-18 | AGPL-3.0 & Brand Boundary Baseline |" not in srs:
    marker = "| 2.9 | 2026-08-26 | Traceability Reconciliation Baseline |"
    idx = srs.find(marker)
    if idx == -1:
        raise RuntimeError("SRS 2.9 history row not found")
    end = srs.find("\n", idx)
    row = "\n| 3.0 | 2026-09-18 | AGPL-3.0 & Brand Boundary Baseline | تثبیت AGPL-3.0 برای تمام کد Dotick، مجازبودن استفاده تجاری و self-hosting، تفکیک entitlement پشتیبانی از حق نرم‌افزاری، و خارج‌بودن نام/لوگو/هویت Dotick از مجوز کد. |"
    srs = srs[:end] + row + srs[end:]
srs = srs.replace(
    "| SRS-CON-004 | Current Scope نباید supported self-hosting برای arbitrary end user را به‌عنوان product capability الزام کند؛ source availability یا development/local execution به‌تنهایی self-host deployment contract ایجاد نمی‌کند. | Architecture + Deployment Inspection |",
    "| SRS-CON-004 | تمام کد نرم‌افزاری Dotick باید تحت AGPL-3.0 منتشر شود و استفاده شخصی، تجاری، سازمانی و self-hosting را طبق همان license مجاز بداند. Current Scope نباید free/guaranteed support، SLA، managed deployment یا production assistance برای arbitrary self-hosted instance را به‌عنوان entitlement محصول الزام کند. نام، لوگو و هویت برند Dotick خارج از software license هستند. | License + Architecture + Deployment Inspection |",
    1,
)
srs = srs.replace(
    "- supported self-hosting برای arbitrary end user و production deployment contract شخص ثالث.",
    "- free/guaranteed support، SLA یا professional production deployment برای arbitrary self-hosted instance به‌عنوان entitlement محصول؛ خود self-hosting طبق AGPL-3.0 مجاز است. نام، لوگو و هویت برند Dotick تحت software license قرار نمی‌گیرند.",
    1,
)
write("docs/requirements/srs.md", srs)


# ---------------------------------------------------------------------------
# Business model
# ---------------------------------------------------------------------------
replace_once(
    "docs/BUSINESS.md",
    "قیمت‌گذاری، مدل درآمد، licensing، packaging تجاری و SLA در این نسخه نهایی نشده‌اند و باید در مراحل بعدی Business Track تکمیل شوند.",
    "مدل licensing نرم‌افزار نهایی شده است: تمام کد Dotick تحت AGPL-3.0 منتشر می‌شود و استفاده شخصی، تجاری، سازمانی و self-hosting طبق این license رایگان است. نام، لوگو و هویت برند Dotick جزو license نرم‌افزار نیستند. درآمد احتمالی می‌تواند از managed hosting، deployment، configuration، migration، customization، maintenance، support، training و SLA حاصل شود. قیمت‌گذاری، packaging، subscription و جزئیات SLA همچنان تصمیم‌های جداگانه‌ی Business Track هستند.",
)
regex_once(
    "docs/BUSINESS.md",
    r"# 6\. Packaging, Pricing & Commercial Model\n.*?(?=\n---\n\n# 7\.)",
    """# 6. Packaging, Pricing & Commercial Model

## 6.1 Final software licensing model

Dotick adopts a **fully open-source software + protected official brand + optional paid services** model.

- All Dotick software source code is licensed under **GNU AGPLv3 (`AGPL-3.0`)**.
- Personal, commercial, and organizational use is permitted under AGPL-3.0 without a separate commercial-use fee.
- Users and organizations may modify, redistribute, fork, and self-host the software subject to AGPL-3.0.
- There is no closed "Enterprise code edition" in the licensing model: features that are part of Dotick's software code remain under AGPL-3.0.
- A company may operate Dotick internally without purchasing a software license from Dotick, provided it complies with AGPL-3.0.
- The Dotick name, logo, visual marks, and official product identity are not granted under the software license. Forks and third-party services must remain distinguishable from the official Dotick product and must not imply official endorsement or affiliation without permission.

## 6.2 Revenue boundary

Commercial revenue, if pursued, is based on **services rather than permission to use the code**. Possible paid offerings include:

- official managed hosting / Dotick Cloud;
- professional installation and deployment;
- environment configuration and migration;
- customization and integrations;
- maintenance and upgrades;
- support and incident assistance;
- training and onboarding;
- SLA-backed operations.

A services agreement purchases professional work, operational responsibility, convenience, or service guarantees. It does not reduce the software rights already granted by AGPL-3.0.

## 6.3 Brand and identity boundary

Open-source code does not make the official Dotick identity a free branding asset. The project retains control over the `Dotick` name, logos, visual marks, domains, and other identifiers of the official product. Third parties may accurately describe a fork as being based on or compatible with Dotick, but may not brand an independent fork/service in a manner that reasonably implies that it is the official Dotick product, an endorsed distribution, or an officially operated service without separate permission.

## 6.4 Still undecided

The following remain separate Business/Product decisions:

- pricing of an official hosted service;
- hosted Free/Pro/Teams/Enterprise packaging, if any;
- subscription mechanics and billing/payment providers;
- support tiers and SLA response targets;
- professional-services pricing;
- operational limits of the official hosted service.

None of these future decisions may convert AGPL-3.0 software-use rights into a company-only or commercial-use fee requirement for code already released under that license.
""",
)


# ---------------------------------------------------------------------------
# Deployment docs
# ---------------------------------------------------------------------------
release_path = "docs/operations/release-deployment.md"
release = read(release_path)
release = release.replace(
    "> **Primary target:** reproducible developer-local and CI execution; no supported end-user self-hosting product",
    "> **Primary target:** reproducible developer-local and CI execution; self-hosting is permitted under AGPL-3.0, while guaranteed production deployment/support is a separate professional-service boundary",
    1,
)
if "## 14. AGPL-3.0 self-hosting and professional-services boundary" not in release:
    release += """

## 14. AGPL-3.0 self-hosting and professional-services boundary

The software in this repository may be self-hosted under AGPL-3.0. That permission is distinct from an operational support commitment.

The project does not guarantee free installation assistance, production architecture review, migrations, incident response, upgrades, monitoring, backup operation, security hardening, SLA, or troubleshooting for arbitrary third-party environments. Any of those may be offered separately as paid professional services or managed hosting.

A paid services agreement changes service obligations between the parties; it does not remove or narrow software rights already granted by AGPL-3.0. The Dotick name, logos, domains, and product identity are governed separately and are not granted by the software license.
"""
write(release_path, release)


# ---------------------------------------------------------------------------
# Root README and documentation index
# ---------------------------------------------------------------------------
readme_path = "README.md"
root = read(readme_path)
if "## License and brand" not in root:
    root += """

## License and brand

Dotick software is free and open source under the [GNU Affero General Public License v3.0](LICENSE). Personal, commercial, organizational, modification, redistribution, and self-hosting use are permitted subject to AGPL-3.0.

The **Dotick** name, logos, visual marks, and official product identity are not licensed under AGPL-3.0. See [TRADEMARKS.md](TRADEMARKS.md) and [docs/licensing.md](docs/licensing.md) for the software/brand boundary.
"""
write(readme_path, root)

docs_readme_path = "docs/README.md"
docs_index = read(docs_readme_path)
if "[`licensing.md`](licensing.md)" not in docs_index:
    docs_index = docs_index.replace(
        "- [`reference/`](reference/) — اسناد مرجع مشتق‌شده یا قدیمی که منبع نهایی تصمیم نیستند\n",
        "- [`reference/`](reference/) — اسناد مرجع مشتق‌شده یا قدیمی که منبع نهایی تصمیم نیستند\n- [`licensing.md`](licensing.md) — مدل AGPL-3.0، مرز self-hosting/support و سیاست هویت/برند Dotick\n",
        1,
    )
write(docs_readme_path, docs_index)


# ---------------------------------------------------------------------------
# Dedicated licensing and trademark documents
# ---------------------------------------------------------------------------
Path("docs/licensing.md").write_text("""# Dotick Licensing and Brand Boundary

## Software license

All Dotick software source code is licensed under the **GNU Affero General Public License v3.0 (`AGPL-3.0`)**. The repository's `LICENSE` file contains the controlling license text.

Subject to AGPL-3.0, individuals and organizations may use, study, modify, redistribute, fork, and self-host Dotick, including for commercial and internal organizational use. Dotick does not require a separate commercial software-use license merely because the user is a business or because the software is used to provide a commercial service.

Users and redistributors remain responsible for complying with AGPL-3.0, including the license's source-code, notice, same-license, and network-use requirements where applicable.

## No closed code tier

Features that are part of Dotick's software code are intended to remain under AGPL-3.0. The licensing model does not define a proprietary Enterprise edition whose software-use permission depends on payment.

## Self-hosting versus support

AGPL-3.0 permits self-hosting; it does not obligate the Dotick project to provide free installation, deployment, maintenance, incident response, migration, security hardening, monitoring, backup operation, upgrades, support, or SLA for third-party environments.

Dotick may offer those services separately for a fee, as well as an official managed hosting service. Paying for a service buys professional effort, operational responsibility, convenience, or service guarantees—not permission to use rights already granted by AGPL-3.0.

## Brand and trademark boundary

The software license does **not** grant rights to the `Dotick` name, logos, visual marks, official domains, or other identifiers of the official Dotick product except as required for legally permitted reference and preservation of notices.

Third parties may make truthful referential statements such as "based on Dotick" or "compatible with Dotick". They may not use Dotick branding in a way that reasonably implies that an independent fork, distribution, hosted service, or organization is the official Dotick product or is endorsed, sponsored, or operated by Dotick without separate permission.

See the root `TRADEMARKS.md` for the project's brand-use policy.

## Operational assets

Open-source licensing of the software does not itself publish or license private credentials, hosted-service user data, service accounts, production secrets, domains, private infrastructure configuration, or other non-code operational assets.

## Precedence

For software-license rights and obligations, the text of `LICENSE` controls. This document explains project policy and the intended boundary between software, services, and brand identity; it does not replace the license text.
""", encoding="utf-8")

Path("TRADEMARKS.md").write_text("""# Dotick Trademark and Brand Policy

Dotick's software is licensed under the GNU Affero General Public License v3.0 (`AGPL-3.0`). That software license does not grant a general license to use the Dotick name, logos, visual marks, official domains, or other brand identifiers.

## Permitted referential use

You may use the Dotick name when necessary to truthfully identify the project, describe compatibility, identify the origin of a fork, comply with license/notice obligations, link to the official project, or make other legally permitted nominative or referential uses. Examples include:

- "Based on Dotick"
- "Forked from Dotick"
- "Compatible with Dotick"

Such use must not suggest sponsorship, endorsement, official status, or operation by the Dotick project when none exists.

## Uses requiring separate permission

Unless applicable law independently permits the use, separate permission is required to:

- present an independent fork or distribution under the `Dotick` product name;
- use the Dotick logo or distinctive visual identity as the primary branding of a fork, service, company, domain, or application;
- market a third-party hosted service in a way that implies it is the official Dotick service;
- imply endorsement, sponsorship, partnership, certification, or official affiliation by Dotick.

## Forks and third-party services

Forking, modifying, redistributing, selling, and hosting the software are governed by AGPL-3.0 and are not prohibited by this brand policy. A fork or third-party service should use its own primary name and visual identity while accurately acknowledging its relationship to Dotick where appropriate.

## No change to open-source rights

This policy is intended to protect the identity of the official Dotick product, not to restrict the software freedoms granted by AGPL-3.0. If a branding restriction and the software license appear to conflict with respect to software rights, the AGPL-3.0 license text governs the licensed software rights; trademark and unfair-competition law govern brand use separately.
""", encoding="utf-8")

print("Licensing documentation reconciled to AGPL-3.0 with a separate Dotick brand boundary.")
