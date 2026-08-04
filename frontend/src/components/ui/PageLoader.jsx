/** Full-viewport loading state — shown while auth/session state or a
 * lazy-loaded route chunk is resolving. */
export default function PageLoader() {
  return (
    <div className="flex min-h-[50vh] w-full items-center justify-center">
      <div
        className="h-9 w-9 animate-spin rounded-full border-[3px] border-ink-200 border-t-marigold-400"
        role="status"
        aria-label="Loading"
      />
    </div>
  );
}
