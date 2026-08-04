import { Helmet } from 'react-helmet-async';
import PageHeader from '@/components/common/PageHeader';
import LegalSection from '@/components/common/LegalSection';

export default function ShippingPolicyPage() {
  return (
    <>
      <Helmet><title>Shipping Policy | AFC - Ahmad Foods</title></Helmet>
      <PageHeader eyebrow="Legal" title="Shipping & Delivery Policy" />
      <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
        <LegalSection title="Delivery Area">
          We currently deliver within a fixed radius of our restaurant. At checkout, we use your browser’s
          location (with your permission) to confirm your delivery address falls within this area before your
          order can be placed. If you’re outside the radius, checkout will be disabled and you’ll see a message
          letting you know.
        </LegalSection>
        <LegalSection title="Delivery Times">
          Estimated delivery times depend on order volume and item preparation time, and are communicated at
          checkout. You can track your order’s progress in real time from your Dashboard, from “Pending” through
          to “Delivered”.
        </LegalSection>
        <LegalSection title="Delivery Fees">
          Any applicable delivery fee is shown at checkout before you confirm your order — there are no hidden
          charges added afterward.
        </LegalSection>
        <LegalSection title="Failed Deliveries">
          Please ensure someone is available at the delivery address during the estimated delivery window. If a
          delivery attempt fails due to an incorrect address or unavailability, additional delivery charges may
          apply for a second attempt.
        </LegalSection>
      </div>
    </>
  );
}
