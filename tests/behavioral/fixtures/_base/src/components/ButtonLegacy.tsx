// Synthetic. Older button, still used on two screens.
type Props = { type?: 'main' | 'alt'; big?: boolean; onClick?: () => void; children: string };
export function ButtonLegacy({ type = 'main', big, onClick, children }: Props) {
  return <button style={{ background: '#2B6CB0', color: '#fff', padding: big ? '14px 20px' : '10px 16px', borderRadius: 6 }} onClick={onClick}>{children}</button>;
}
