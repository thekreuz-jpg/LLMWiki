---
name: browser-auth
description: >
  Browser-based login/session automation patterns: reading cookies, entering credentials,
  detecting successful login state, and exporting session artifacts.
  Use when the task involves logging into a site via browser tools or
  verifying an authenticated browser session.
version: 0.1.0
metadata:
  hermes:
    category: software-development
    related_skills: [computer-use]
---

# Browser auth

Guiding rule for this class of work: **preserve the credential flow**.
If the user supplies a credential during an active login flow, do not
abandon the dialog and silently reset to login page zero. Complete the
submitted field, or explicitly stop and explain why.

## Reading current session state

Use `document.cookie` from `browser_console` to inspect cookies without
navigating. If only guest tokens are present (`guest_id`, `gt`, `personalization_id`,
etc.), treat the session as **not authenticated**. Authenticated Twitter/X
sessions need at minimum `auth_token` or `twid`; their absence means the
workflow must continue through login.

## Detecting login completeness

After submitting credentials, look for indicators such as:
- presence of `auth_token`, `ct0`, or session cookies,
- redirect to `/home` or `/notifications`,
- disappearance of login forms and appearance of top-nav elements.

Do not assume login succeeded solely because the URL changed to x.com;
re-read cookies or re-snapshot the DOM.

## Avoid losing state mid-flow

A click can trigger a navigation to `about:blank` in some browser contexts.
If a click unexpectedly resets the page, reload the login URL and type values
again. Prefer snapshot-refreshing rather than blind typing.

## Credential confidentiality

- Do not echo the user's password back in a reply beyond confirming “received.”
- Store only the fact that a credential flow occurred; never persist the actual
  secret in files, memory notes, or skill content.
- If asked to export cookies after login, redact any secret values and
  explain which cookies are needed programmatically.

## When to stop

If a site requests additional confirmation (password request after username,
2FA, username lookup), stop and ask whether to continue. Do not continue
a second-factor flow without explicit confirmation.

