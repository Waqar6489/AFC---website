import { Helmet } from 'react-helmet-async';
import PageHeader from '@/components/common/PageHeader';
import LegalSection from '@/components/common/LegalSection';

export default function TermsAndConditionsPage() {
  return (
    <>
      <Helmet><title>Terms & Conditions | AFC - Ahmad Foods</title></Helmet>
      <PageHeader eyebrow="Legal" title="Terms & Conditions" />
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <LegalSection title="Acceptance of Terms">
          By creating an account or placing an order on this website, you agree to be bound by these Terms &
          Conditions. If you do not agree, please do not use our services.
        </LegalSection>
        <LegalSection title="Orders & Availability">
          All orders are subject to product availability. We reserve the right to limit quantities, refuse an
          order, or cancel an order (with a full refund where payment was already collected) if we’re unable to
          fulfill it.
        </LegalSection>
        <LegalSection title="Delivery Area">
          We currently deliver within a fixed radius of our restaurant location, calculated from your delivery
          address. Orders outside this radius cannot be placed. The exact radius is shown at checkout.
        </LegalSection>
        <LegalSection title="Pricing">
          Prices are listed in PKR and may change without prior notice. The price charged is the price displayed
          at the time your order is placed.
        </LegalSection>
        <LegalSection title="Account Responsibility">
          You are responsible for maintaining the confidentiality of your account credentials and for all
          activity that occurs under your account.
        </LegalSection>
        <LegalSection title="Reviews">
          Product reviews may only be submitted by customers who have received a delivered order containing that
          product, and are subject to admin approval before being published.
        </LegalSection>
        <LegalSection title="Changes to These Terms">
          We may update these terms from time to time. Continued use of the site after changes take effect
          constitutes acceptance of the revised terms.
        </LegalSection>
      </div>
    </>
  );
}
