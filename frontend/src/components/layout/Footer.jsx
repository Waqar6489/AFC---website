import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import {
  FiFacebook,
  FiInstagram,
  FiMail,
  FiMapPin,
  FiPhone,
  FiTwitter,
} from 'react-icons/fi';
import Logo from '../common/Logo';
import Button from '@/components/ui/Button';
import { coreService } from '@/services/coreService';
import { contactService } from '@/services/contactService';
import { extractApiError } from '@/services/apiClient';

const POLICY_LINKS = [
  { to: '/privacy-policy', label: 'Privacy Policy' },
  { to: '/terms-and-conditions', label: 'Terms & Conditions' },
  { to: '/refund-policy', label: 'Refund Policy' },
  { to: '/shipping-policy', label: 'Shipping Policy' },
];

const QUICK_LINKS = [
  { to: '/shop', label: 'Shop' },
  { to: '/deals', label: 'Deals' },
  { to: '/about', label: 'About Us' },
  { to: '/contact', label: 'Contact Us' },
];

export default function Footer() {
  const [siteConfig, setSiteConfig] = useState(null);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm();

  useEffect(() => {
    coreService
      .getSiteConfig()
      .then((res) => setSiteConfig(res.data))
      .catch(() => {
        /* Footer still renders fine without live site config — the
           static quick links and policies remain fully usable. */
      });
  }, []);

  async function onSubscribe({ email }) {
    try {
      await contactService.subscribeNewsletter(email);
      toast.success("Thanks for subscribing! Watch your inbox for AFC updates.");
      reset();
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  return (
    <footer className="mt-20">
      {/* Signature ticket-edge transition */}
      <div className="ticket-edge--on-ink bg-ink-800" aria-hidden="true" />

      <div className="bg-ink-800 text-ink-100">
        <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 gap-10 md:grid-cols-2 lg:grid-cols-4">
            <div>
              <Logo  />
              <p className="mt-4 max-w-xs text-sm leading-relaxed text-ink-300">
                Freshly baked cakes, pastries and sweets, made with care and delivered to your door.
              </p>
              <div className="mt-5 flex gap-3">
                {siteConfig?.facebook_url && (
                  <SocialIcon href={siteConfig.facebook_url} label="Facebook" icon={FiFacebook} />
                )}
                {siteConfig?.instagram_url && (
                  <SocialIcon href={siteConfig.instagram_url} label="Instagram" icon={FiInstagram} />
                )}
                {siteConfig?.twitter_url && (
                  <SocialIcon href={siteConfig.twitter_url} label="Twitter" icon={FiTwitter} />
                )}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-marigold-300">Quick Links</h3>
              <ul className="mt-4 space-y-2.5">
                {QUICK_LINKS.map((link) => (
                  <li key={link.to}>
                    <Link to={link.to} className="text-sm text-ink-300 transition-colors hover:text-marigold-300">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-marigold-300">Policies</h3>
              <ul className="mt-4 space-y-2.5">
                {POLICY_LINKS.map((link) => (
                  <li key={link.to}>
                    <Link to={link.to} className="text-sm text-ink-300 transition-colors hover:text-marigold-300">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-marigold-300">Stay Updated</h3>
              <p className="mt-4 text-sm text-ink-300">Subscribe for new arrivals, deals, and seasonal specials.</p>
              <form onSubmit={handleSubmit(onSubscribe)} className="mt-3 flex flex-col gap-2" noValidate>
                <input
                  type="email"
                  placeholder="you@example.com"
                  aria-label="Email address"
                  className="h-10 rounded-[var(--radius-card)] border border-ink-600 bg-ink-700 px-3.5 text-sm text-cream
                    placeholder:text-ink-400 focus:border-marigold-400"
                  {...register('email', { required: 'Email is required' })}
                />
                {errors.email && <p className="text-xs text-marigold-300">{errors.email.message}</p>}
                <Button type="submit" variant="primary" size="sm" isLoading={isSubmitting}>
                  Subscribe
                </Button>
              </form>

              {(siteConfig?.contact_phone || siteConfig?.contact_email || siteConfig?.contact_address) && (
                <ul className="mt-5 space-y-2 text-sm text-ink-300">
                  {siteConfig?.contact_phone && (
                    <li className="flex items-center gap-2"><FiPhone className="h-4 w-4 shrink-0 text-marigold-300" /> {siteConfig.contact_phone}</li>
                  )}
                  {siteConfig?.contact_email && (
                    <li className="flex items-center gap-2"><FiMail className="h-4 w-4 shrink-0 text-marigold-300" /> {siteConfig.contact_email}</li>
                  )}
                  {siteConfig?.contact_address && (
                    <li className="flex items-start gap-2"><FiMapPin className="mt-0.5 h-4 w-4 shrink-0 text-marigold-300" /> {siteConfig.contact_address}</li>
                  )}
                </ul>
              )}
            </div>
          </div>

          <div className="mt-12 border-t border-ink-700 pt-6 text-center text-xs text-ink-400">
            &copy; {new Date().getFullYear()} AFC - Ahmad Foods. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
}

function SocialIcon({ href, label, icon: Icon }) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={label}
      className="flex h-9 w-9 items-center justify-center rounded-full bg-ink-700 text-ink-200 transition-colors hover:bg-marigold-400 hover:text-ink-900"
    >
      <Icon className="h-4 w-4" />
    </a>
  );
}
