import { Helmet } from 'react-helmet-async';
import PageHeader from '@/components/common/PageHeader';
import LegalSection from '@/components/common/LegalSection';

export default function PrivacyPolicyPage() {
  return (
    <>
      <Helmet><title>Privacy Policy | AFC - Ahmad Foods</title></Helmet>
      <PageHeader eyebrow="Legal" title="Privacy Policy" />
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <LegalSection title="Information We Collect">
          When you create an account or place an order with AFC - Ahmad Foods, we collect information such as
          your name, email address, phone number, delivery address, and order history. When you use our
          delivery-radius feature, we also access your device’s precise location, with your permission, solely
          to confirm you’re within our delivery area.
        </LegalSection>
        <LegalSection title="How We Use Your Information">
          We use your information to process and deliver your orders, communicate order updates, respond to
          support requests, and — if you opt in — send you newsletters about new products and promotions. We do
          not sell your personal information to third parties.
        </LegalSection>
        <LegalSection title="Payment Information">
          For Cash on Delivery orders, no payment card data is collected. If card payments are enabled in the
          future, transactions will be processed by a PCI-compliant payment provider; we do not store your full
          card details on our servers.
        </LegalSection>
        <LegalSection title="Cookies & Location">
          We use essential cookies to keep you logged in and remember your cart. Location access is requested
          only when needed to validate delivery eligibility and is never used for tracking outside that purpose.
        </LegalSection>
        <LegalSection title="Your Rights">
          You may access, update, or request deletion of your account information at any time from your
          Dashboard, or by contacting us through the Contact Us page.
        </LegalSection>
        <LegalSection title="Contact">
          Questions about this policy can be sent through our Contact Us page.
        </LegalSection>
      </div>
    </>
  );
}
