import { useEffect, useState } from 'react';
import { FiMail, FiMapPin, FiPhone } from 'react-icons/fi';
import { coreService } from '@/services/coreService';

export default function ContactMapSection() {
  const [siteConfig, setSiteConfig] = useState(null);

  useEffect(() => {
    coreService.getSiteConfig().then((res) => setSiteConfig(res.data)).catch(() => {});
  }, []);

  if (!siteConfig) return null;

  const mapSrc = `https://www.google.com/maps?q=${siteConfig.restaurant_latitude},${siteConfig.restaurant_longitude}&output=embed`;

  return (
    <section className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 gap-8 overflow-hidden rounded-[var(--radius-card)] border border-ink-100 bg-white lg:grid-cols-2">
        <div className="p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-marigold-600">Visit Us</p>
          <h2 className="mt-1 text-2xl font-bold text-ink-900">Find Our Restaurant</h2>
          <ul className="mt-5 flex flex-col gap-3 text-sm text-ink-600">
            {siteConfig.contact_address && (
              <li className="flex items-start gap-2.5"><FiMapPin className="mt-0.5 h-4 w-4 shrink-0 text-marigold-500" /> {siteConfig.contact_address}</li>
            )}
            {siteConfig.contact_phone && (
              <li className="flex items-center gap-2.5"><FiPhone className="h-4 w-4 shrink-0 text-marigold-500" /> {siteConfig.contact_phone}</li>
            )}
            {siteConfig.contact_email && (
              <li className="flex items-center gap-2.5"><FiMail className="h-4 w-4 shrink-0 text-marigold-500" /> {siteConfig.contact_email}</li>
            )}
            {siteConfig.working_hours && (
              <li className="text-ink-500">{siteConfig.working_hours}</li>
            )}
          </ul>
          <p className="mt-4 text-xs text-ink-400">
            We currently deliver within {siteConfig.delivery_radius_km} KM of this location.
          </p>
        </div>
        <iframe
          title="AFC - Ahmad Foods location"
          src={mapSrc}
          className="h-64 w-full border-0 lg:h-full"
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
        />
      </div>
    </section>
  );
}
