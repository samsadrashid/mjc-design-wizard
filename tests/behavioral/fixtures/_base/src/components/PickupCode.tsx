// Synthetic
type Props = { code: string; expiresAt?: string; onCopy: () => void };
export function PickupCode({ code, expiresAt, onCopy }: Props) {
  return (
    <section>
      <h2>Your pickup code</h2>
      <p style={{ fontSize: 28, color: '#2B6CB0' }}>{code}</p>
      <div onClick={onCopy}>Copy</div>
      <img src="/qr.png" width="120" />
      {expiresAt ? <p>Expires {expiresAt}</p> : null}
    </section>
  );
}
