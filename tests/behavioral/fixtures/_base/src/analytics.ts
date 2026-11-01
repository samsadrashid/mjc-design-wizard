// Synthetic. Events emitted by the app today.
export function track(event: string, props?: Record<string, unknown>) { /* sends to analytics */ }
track('parcel_screen_view', { parcelId });
track('pickup_code_shown', { parcelId });
track('pickup_completed', { parcelId });
// Note: no event named alert_enabled is emitted anywhere in this codebase.
