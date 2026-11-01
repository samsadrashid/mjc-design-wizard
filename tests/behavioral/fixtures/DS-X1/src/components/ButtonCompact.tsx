// Intentional variant: compact button for dense table rows. Approved in design review, documented in docs/components.md.
type Props = { onClick?: () => void; children: string };
export function ButtonCompact({ onClick, children }: Props) {
  return <button className="btn btn-primary btn-compact" onClick={onClick}>{children}</button>;
}
