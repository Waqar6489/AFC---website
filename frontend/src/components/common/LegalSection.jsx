export default function LegalSection({ title, children }) {
  return (
    <section className="mb-8">
      <h2 className="mb-2 text-lg font-semibold text-ink-900">{title}</h2>
      <p className="leading-relaxed text-ink-600">{children}</p>
    </section>
  );
}
