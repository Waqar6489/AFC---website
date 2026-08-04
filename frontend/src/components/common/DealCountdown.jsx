import { useEffect, useState } from 'react';

function formatRemaining(totalSeconds) {
  const days = Math.floor(totalSeconds / 86400);
  const hours = Math.floor((totalSeconds % 86400) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = Math.floor(totalSeconds % 60);
  return { days, hours, minutes, seconds };
}

/** Live countdown timer for a deal's remaining time — ticks client-side
 * from the seconds_remaining value the backend computed at fetch time. */
export default function DealCountdown({ secondsRemaining }) {
  const [remaining, setRemaining] = useState(secondsRemaining);

  useEffect(() => {
    setRemaining(secondsRemaining);
    const interval = setInterval(() => {
      setRemaining((prev) => Math.max(prev - 1, 0));
    }, 1000);
    return () => clearInterval(interval);
  }, [secondsRemaining]);

  if (remaining <= 0) {
    return <span className="text-xs font-semibold text-danger">Deal ended</span>;
  }

  const { days, hours, minutes, seconds } = formatRemaining(remaining);

  return (
    <div className="flex items-center gap-1.5 font-price text-xs font-semibold text-ink-900">
      {days > 0 && <TimeBox value={days} label="d" />}
      <TimeBox value={hours} label="h" />
      <TimeBox value={minutes} label="m" />
      <TimeBox value={seconds} label="s" />
    </div>
  );
}

function TimeBox({ value, label }) {
  return (
    <span className="rounded bg-ink-800 px-1.5 py-1 text-cream">
      {String(value).padStart(2, '0')}{label}
    </span>
  );
}
