---
name: browser-form-automation
description: Patterns for filling and submitting complex modern web forms (Shopify, React, Vue) using browser_console and synthetic events.
category: computer-use
---

# Browser Form Automation

When automating complex or modern web forms (like those built with React, Vue, or Shopify's Formbuilder), simply setting `.value` on input elements via `browser_console` is often insufficient. The underlying JavaScript frameworks rely on DOM events to update their internal state and trigger validation or dependent fields.

## Core Pattern: Value + Event Dispatch

Always dispatch an `input` or `change` event immediately after setting a value.

```javascript
// For standard text inputs
let input = document.getElementById("field-id");
if (input) {
  input.value = "Test Value";
  input.dispatchEvent(new Event('input', { bubbles: true }));
}

// For select dropdowns or checkboxes
let select = document.getElementById("select-id");
if (select) {
  select.value = "Option 1";
  select.dispatchEvent(new Event('change', { bubbles: true }));
}
```

## Pitfalls & Workarounds

1. **Dependent Fields (e.g., State/Province unlocks after Country is chosen)**
   After dispatching a `change` event on the parent field, the framework may need a moment to render the dependent field or fetch data. Use `await new Promise(r => setTimeout(r, 200))` before trying to interact with the dependent field in an async script.

2. **React 16+ Overrides**
   In some strict React apps, setting `.value` is intercepted. If `dispatchEvent` still doesn't update the UI, you may need to bypass the React setter:
   ```javascript
   let input = document.querySelector('input');
   let nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
   nativeInputValueSetter.call(input, 'New Value');
   input.dispatchEvent(new Event('input', { bubbles: true }));
   ```

3. **Submitting Forms**
   If calling `.submit()` on the form element bypasses JS validation, click the submit button directly instead:
   ```javascript
   document.querySelector("button[type='submit']").click();
   ```
