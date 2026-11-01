// Synthetic. Documented component: variants use tokens.
type Props = {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: string;
};
export function Button({ variant = 'primary', size = 'md', disabled, loading, onClick, children }: Props) {
  return <button className={`btn btn-${variant} btn-${size}`} disabled={disabled || loading} onClick={onClick}>{children}</button>;
}
// styles: background: var(--color-primary); padding: var(--space-2) var(--space-4); border-radius: var(--radius-md);
