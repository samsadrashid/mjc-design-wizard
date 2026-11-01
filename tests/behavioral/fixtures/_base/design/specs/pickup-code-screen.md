# Spec: pickup code screen (synthetic)
Status: approved by Product (approver name not recorded). Version: v3.

- Title text: "Your pickup code", body font token --font-size-body.
- Card padding: 16px (token --space-4). Card radius: 8px (--radius-md).
- Code text: 32px (token --font-size-code), bold, color token --color-primary (#1E4FD8).
- Primary action: button labeled "Copy code", secondary variant, minimum tap target 44px.
- States: default; copied (toast text "Code copied"); expired (message "This code has expired" and a "Get a new code" button).
- Responsive: single column below 600px.
- Not specified: QR image size, QR position, animation.
