// Synthetic
type Props = { status: 'in-transit' | 'ready' | 'collected' };
export function StatusBadge({ status }: Props) {
  const color = status === 'ready' ? '#38A169' : status === 'collected' ? '#718096' : '#DD6B20';
  return <span style={{ color }}>{status}</span>;
}
