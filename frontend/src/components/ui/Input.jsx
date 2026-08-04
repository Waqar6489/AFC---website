import { forwardRef } from 'react';

/** Standard form input with a label and inline error message — pairs
 * naturally with react-hook-form's `register()`. */
const Input = forwardRef(function Input({ label, error, id, className = '', ...props }, ref) {
  const inputId = id || props.name;
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={inputId} className="text-sm font-medium text-ink-700">
          {label}
        </label>
      )}
      <input
        ref={ref}
        id={inputId}
        className={`h-11 rounded-[var(--radius-card)] border bg-cream px-3.5 text-sm text-ink-800
          placeholder:text-ink-300 transition-colors
          ${error ? 'border-danger' : 'border-ink-200 hover:border-ink-300 focus:border-marigold-400'}
          ${className}`}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...props}
      />
      {error && (
        <p id={`${inputId}-error`} className="text-xs text-danger">
          {error}
        </p>
      )}
    </div>
  );
});

export default Input;
