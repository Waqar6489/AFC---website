import { Helmet } from 'react-helmet-async';
import PageHeader from '@/components/common/PageHeader';
import LegalSection from '@/components/common/LegalSection';

export default function RefundPolicyPage() {
  return (
    <>
      <Helmet><title>Refund Policy | AFC - Ahmad Foods</title></Helmet>
      <PageHeader eyebrow="Legal" title="Refund Policy" />
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <LegalSection title="Order Cancellations">
          Orders can be cancelled free of charge before they enter preparation. Once an order status moves to
          “Preparing” or beyond, cancellation may not be possible as ingredients are already committed.
        </LegalSection>
        <LegalSection title="Quality Issues">
          If your order arrives damaged, incorrect, or not as described, please contact us within 24 hours of
          delivery with photos where possible. We will offer a replacement or a refund at our discretion.
        </LegalSection>
        <LegalSection title="Refund Method">
          For Cash on Delivery orders, approved refunds are issued via bank transfer or store credit. Refunds are
          typically processed within 5–7 business days of approval.
        </LegalSection>
        <LegalSection title="Non-Refundable Situations">
          We’re unable to offer refunds for change-of-mind after an order has been prepared, or for delivery
          delays caused by incorrect address information provided at checkout.
        </LegalSection>
        <LegalSection title="How to Request a Refund">
          Reach out via the Contact Us page with your order number and a description of the issue, and our team
          will respond as quickly as possible.
        </LegalSection>
      </div>
    </>
  );
}
