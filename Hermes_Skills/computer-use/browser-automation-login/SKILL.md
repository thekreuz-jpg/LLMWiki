---
name: browser-automation-login
description: >
  Principles and safe fallbacks for performing web logins using a browser
  automation tool. Covers isolated-session limits, platform-specific oddities
  like X/Twitter confirmation flows, and submit strategies that avoid blank-page
  nav traps. Use when the goal is “log into site X and read cookies/tokens.”
---

# Browser automation login

## First principle: isolation

Automated browsers **do not share** cookies or login state with the user’s
personal browser. If the user says “I’m logged in,” that state is only in
their actual browser, not in the controlled automation session. Do not try to
read hidden cookies from another context.

## Default flow

1. Open the canonical login URL for the site (not a generic home page).
2. Identify the visible form fields from the accessibility snapshot.
3. Insert known credential fields carefully; do **not** continue blindly after
   sensitive entry unless the user explicitly says to submit.
4. Watch the next state before retrying.

## X / Twitter specific

X frequently splits login into stages even after email entry:

- Email → “Confirm your account” / “Enter the information associated with your account.”
- Then it asks for **Username**, with an option “Use password.”
- Only after username does it show the password form in some sessions.

If you land on a **Confirm your account / Username** screen, do **not** loop
back to the email screen or try to submit from the wrong fields. Enter the
username and continue through the intended buttons.

## Submit pitfalls

- `browser_press(key='Enter')` on some confirmation dialogs Causes navigation
  to `about:blank`, losing the form entirely.
- Clicking a generic container (`<div>`) can have the same effect.

If Enter fails with a blank-page nav error:

1. Reload the login page.
2. Re-enter the fields.
3. Prefer clicking an explicit submit button from the snapshot rather than
   pressing Enter.
4. If no explicit submit button is visible, inspect the page visually and
   locate the button; do not submit blind.

## Preferred fallback: cookie transfer

If the user is already logged in on their normal browser, or if the automation
login flow blanks/regresses repeatedly, **stop retrying the form**. Switch to a
cookie-export/import workflow:

1. Ask the user to export `x.com` / target-site cookies from their personal browser
   using a browser extension like **EditThisCookie** or **Cookie-Editor**, or via
   the browser DevTools Console with a small script that reads `document.cookie`.
2. Accept only the JSON array shape with cookie objects/names+values.
3. **Do not submit credentials** through the automation browser if the user has
   already shared cookies over a side channel.
4. Inject the cookies into the automation session by setting `document.cookie`
   for each entry with `domain`, `path=/`, and `secure` as appropriate.
5. Reload the site and verify authenticated cookies are present
   (`auth_token`, `ct0`, etc.). Guest cookies alone mean the session is still
   unauthenticated.

**Why this beats retrying:** automation browsers are isolated from the user's
personal browser login state, and some login flows blank the page or trip
bot-prevention checks after credential entry. Cookie transfer is often faster,
more reliable, and avoids password handling in automation altogether.

## Verification

After submit, read the snapshot again. Success indicators:

- Home/feed elements appear instead of the login form.
- Authenticated cookies appear, e.g. `auth_token`, `ct0`, `twid`.

If only guest tokens like `guest_id`, `gt`, `__cuid`, `personalization_id`
remain, the session is still guest/unauthenticated.

## Safety

- Never submit credentials unless the user explicitly approves.
- After submission, only report the outcome; never echo full sensitive cookie
  values. Cookie names and a sanitized profile is enough.