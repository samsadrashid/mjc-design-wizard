// Synthetic
type Props = { parcel: { id: string; title: string; status: 'in-transit' | 'ready' | 'collected' }; onOpen: (id: string) => void };
export function ParcelCard({ parcel, onOpen }: Props) {
  return (
    <div style={{ padding: '12px', border: '1px solid #E2E8F0', borderRadius: 8, color: '#E53E3E' }} onClick={() => onOpen(parcel.id)}>
      <h3>{parcel.title}</h3>
      <StatusBadge status={parcel.status} />
    </div>
  );
}
