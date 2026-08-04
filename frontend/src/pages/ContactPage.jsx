import { Helmet } from 'react-helmet-async';
import { useForm } from 'react-hook-form';
import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { 
  FiPhone, 
  FiMail, 
  FiMapPin, 
  FiFacebook, 
  FiInstagram, 
  FiTwitter 
} from 'react-icons/fi';

import PageHeader from '@/components/common/PageHeader';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { contactService } from '@/services/contactService';
import { extractApiError } from '@/services/apiClient';
import { coreService } from '@/services/coreService';

export default function ContactPage() {
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm();
  const [siteConfig, setSiteConfig] = useState(null);

  async function onSubmit(values) {
    try {
      await contactService.submit(values);
      toast.success("Message sent! We'll get back to you soon.");
      reset();
    } catch (error) {
      toast.error(extractApiError(error).message);
    }
  }

  useEffect(() => {
    coreService.getSiteConfig().then((res) => setSiteConfig(res.data)).catch(() => {});
  }, []);

  const mapSrc = siteConfig?.restaurant_latitude && siteConfig?.restaurant_longitude 
    ? `https://www.google.com/maps?q=${siteConfig.restaurant_latitude},${siteConfig.restaurant_longitude}&output=embed`
    : `https://www.google.com/maps?q=31.4180,73.0800&output=embed`;

  return (
    <>
      <Helmet><title>Contact Us | AFC - Ahmad Foods</title></Helmet>
      <PageHeader eyebrow="Get in Touch" title="Contact Us" description="Questions, bulk orders, or feedback — we'd love to hear from you." />
      
      {/* Main Content Section */}
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-12 lg:gap-12 items-start">
          
          {/* Left Side: Contact Information */}
          <div className="lg:col-span-5 flex flex-col gap-6 rounded-[var(--radius-card)] border border-ink-100 bg-white p-6 sm:p-8">
            <div>
              <h3 className="text-xl font-bold text-ink-900">Contact Information</h3>
              <p className="mt-1 text-sm text-ink-600">
                Reach out to us directly or fill out the form and we will respond as soon as possible.
              </p>
            </div>

            <div className="flex flex-col gap-5 pt-2">
              {siteConfig?.contact_phone && (
                <div className="flex items-start gap-3.5">
                  <FiPhone className="mt-1 h-5 w-5 flex-shrink-0 text-marigold-400" />
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wider text-ink-500">Phone</p>
                    <a href={`tel:${siteConfig.contact_phone}`} className="text-sm font-medium text-ink-800 hover:text-marigold-400 transition-colors">
                      {siteConfig.contact_phone}
                    </a>
                  </div>
                </div>
              )}

              {siteConfig?.contact_email && (
                <div className="flex items-start gap-3.5">
                  <FiMail className="mt-1 h-5 w-5 flex-shrink-0 text-marigold-400" />
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wider text-ink-500">Email</p>
                    <a href={`mailto:${siteConfig.contact_email}`} className="text-sm font-medium text-ink-800 hover:text-marigold-400 transition-colors">
                      {siteConfig.contact_email}
                    </a>
                  </div>
                </div>
              )}

              {siteConfig?.contact_address && (
                <div className="flex items-start gap-3.5">
                  <FiMapPin className="mt-1 h-5 w-5 flex-shrink-0 text-marigold-400" />
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wider text-ink-500">Location</p>
                    <p className="text-sm font-medium text-ink-800">
                      {siteConfig.contact_address}
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Social Media Links */}
            <div className="border-t border-ink-100 pt-6 mt-2">
              <p className="text-xs font-semibold uppercase tracking-wider text-ink-500 mb-3">Follow Us</p>
              <div className="flex gap-3">
                <a 
                  href="https://facebook.com" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="flex h-10 w-10 items-center justify-center rounded-full border border-ink-200 bg-cream text-ink-700 hover:border-marigold-400 hover:text-marigold-400 transition-colors"
                >
                  <FiFacebook className="h-5 w-5" />
                </a>
                <a 
                  href="https://instagram.com" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="flex h-10 w-10 items-center justify-center rounded-full border border-ink-200 bg-cream text-ink-700 hover:border-marigold-400 hover:text-marigold-400 transition-colors"
                >
                  <FiInstagram className="h-5 w-5" />
                </a>
                <a 
                  href="https://twitter.com" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="flex h-10 w-10 items-center justify-center rounded-full border border-ink-200 bg-cream text-ink-700 hover:border-marigold-400 hover:text-marigold-400 transition-colors"
                >
                  <FiTwitter className="h-5 w-5" />
                </a>
              </div>
            </div>
          </div>

          {/* Right Side: Contact Form */}
          <div className="lg:col-span-7">
            <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 rounded-[var(--radius-card)] border border-ink-100 bg-white p-6 sm:p-8" noValidate>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <Input label="Name" error={errors.name?.message} {...register('name', { required: 'Required' })} />
                <Input label="Email" type="email" error={errors.email?.message} {...register('email', { required: 'Required' })} />
              </div>
              <Input label="Phone (optional)" type="tel" {...register('phone')} />
              <Input label="Subject" error={errors.subject?.message} {...register('subject', { required: 'Required' })} />
              <div className="flex flex-col gap-1.5">
                <label htmlFor="message" className="text-sm font-medium text-ink-700">Message</label>
                <textarea
                  id="message"
                  rows={5}
                  className="rounded-[var(--radius-card)] border border-ink-200 bg-cream px-3.5 py-2.5 text-sm focus:border-marigold-400 outline-none"
                  {...register('message', { required: 'Required' })}
                />
                {errors.message && <p className="text-xs text-danger">{errors.message.message}</p>}
              </div>
              <Button type="submit" isLoading={isSubmitting} className="w-fit">Send Message</Button>
            </form>
          </div>

        </div>
      </div>

      {/* Full Width Google Map Section */}
      <section className="mx-auto max-w-7xl pb-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full h-80 border border-ink-100 rounded-[var(--radius-card)] overflow-hidden">
          <iframe 
            title="Ahmad Foods Location"
            src={mapSrc}
            width="100%"
            height="100%"
            style={{ border: 0 }}
            allowFullScreen=""
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
          />
        </div>
      </section>
    </>
  );
}