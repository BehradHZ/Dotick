# Increment 0 dependency review

Date: 2026-09-06. Scope: locked API and Expo web foundation dependencies.

`pip-audit` reports no known vulnerabilities in the resolved Python environment. `npm audit` reports ten moderate package entries, all originating from one advisory: [GHSA-w5hq-g745-h8pq](https://github.com/advisories/GHSA-w5hq-g745-h8pq) in `uuid@7.0.3`, through `xcode@3.0.1` and Expo's native project tooling. There are no high/critical entries in the inspected lockfile.

The vulnerable operations described by the advisory are v3/v5/v6 calls with caller-supplied buffers. The installed `xcode/lib/pbxProject.js` uses `uuid.v4()` without a supplied buffer, to generate Xcode project identifiers. The current client build targets web only and has no Xcode/native generation flow. This inspection does not establish that the dependency itself is fixed.

Keep the accepted Expo 57 baseline and report the advisory in CI. The dependency gate fails on high/critical entries; moderate entries remain visible. Revisit when Expo/xcode provides an upstream fix and before native generation becomes an active build target. Do not downgrade the app to the unrelated old Expo major suggested by `npm audit --force`. No audit entries are suppressed, and the Python scan remains strict.
