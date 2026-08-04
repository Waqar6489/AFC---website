import { useEffect, useState } from 'react';
import { FiChevronDown } from 'react-icons/fi';
import { faqService } from '@/services/faqService';

export default function FAQSection() {
  const [faqs, setFaqs] = useState([]);
  const [openId, setOpenId] = useState(null);

  useEffect(() => {
    faqService.list({ ordering: 'order' }).then((data) => setFaqs(data.results ?? data));
  }, []);

  if (faqs.length === 0) return null;

  return (
    <section className="mx-auto max-w-3xl px-4 py-14 sm:px-6 lg:px-8">
      <div className="mb-8 text-center">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-marigold-600">Have Questions?</p>
        <h2 className="mt-1 text-2xl font-bold text-ink-900">Frequently Asked Questions</h2>
      </div>
      <div className="flex flex-col divide-y divide-ink-100 rounded-[var(--radius-card)] border border-ink-100 bg-white">
        {faqs.map((faq) => {
          const isOpen = openId === faq.id;
          return (
            <div key={faq.id}>
              <button
                onClick={() => setOpenId(isOpen ? null : faq.id)}
                className="flex w-full items-center justify-between px-5 py-4 text-left"
                aria-expanded={isOpen}
              >
                <span className="font-medium text-ink-800">{faq.question}</span>
                <FiChevronDown className={`h-4 w-4 shrink-0 text-ink-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
              </button>
              {isOpen && <p className="px-5 pb-4 text-sm text-ink-500">{faq.answer}</p>}
            </div>
          );
        })}
      </div>
    </section>
  );
}
