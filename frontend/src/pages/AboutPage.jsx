import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { teamService } from '@/services/teamService';
import PageHeader from '@/components/common/PageHeader';
import WhyChooseUsSection from '@/components/home/WhyChooseUsSection';
import TestimonialsSection from '@/components/home/TestimonialsSection';

export default function AboutPage() {
  const [team, setTeam] = useState([]);

  useEffect(() => {
    teamService.list({ ordering: 'order' }).then((data) => setTeam(data.results ?? data));
  }, []);

  return (
    <>
      <Helmet><title>About Us | AFC - Ahmad Foods</title></Helmet>
      {/* <PageHeader eyebrow="Our Story" title="About AFC - Ahmad Foods" description="Mission, vision, history, and the team behind every bake." /> */}

      {/* Main About Container */}
      <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8 space-y-16">

        {/* 1. Hero / Our Story Section (Left: Text, Right: Image) */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
  
  {/* Left Side: Content aligned to start */}
  <div className="lg:col-span-6 flex flex-col items-start justify-start">
    <p className="text-xs font-semibold uppercase tracking-[0.16em] text-marigold-600 mb-2">Since Day One</p>
    <h2 className="text-2xl sm:text-3xl font-bold text-ink-900 mb-4">Our Story</h2>
    <p className="leading-relaxed text-ink-600 text-justify">
      AFC - Ahmad Foods started with a simple passion: creating exceptional food that brings people together.
      What began as a cherished local spot has evolved into a complete dining experience — bringing together
      sizzling fast food favorites like burgers and pizzas alongside our signature handcrafted sweets and
      freshly baked treats. Whether you are grabbing a quick bite on the go or celebrating a sweet moment with family,
      our commitment to authentic recipes, fresh ingredients, and warm hospitality remains at the heart of everything we serve.
    </p>
  </div>

  {/* Right Side: Full Width & Full Height Image Container */}
  <div className="w-full h-full lg:col-span-6 flex items-center justify-center">
    <div className="w-110 h-110 overflow-hidden rounded-[var(--radius-card)]">
      <img
        src="/afc.png"
        alt="AFC Ahmad Foods Bakery Story"
        className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
      />
    </div>
  </div>

</section>

        {/* 2. Mission & Vision Section (Styled Cards) */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <section className="relative rounded-[var(--radius-card)] border border-ink-100 bg-white p-6 sm:p-8 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-10 h-1 bg-marigold-400 rounded-full mb-4" />
            <h2 className="text-lg font-semibold text-ink-900">Our Mission</h2>
            <p className="mt-2 leading-relaxed text-ink-600">
              To bake fresh, quality desserts every single day and deliver them quickly to our community, at a
              price that makes celebrating life&rsquo;s moments easy.
            </p>
          </section>

          <section className="relative rounded-[var(--radius-card)] border border-ink-100 bg-white p-6 sm:p-8 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-10 h-1 bg-marigold-400 rounded-full mb-4" />
            <h2 className="text-lg font-semibold text-ink-900">Our Vision</h2>
            <p className="mt-2 leading-relaxed text-ink-600">
              To be the most trusted name in fresh sweets and baked goods, known for consistency, quality, and
              genuine care for every customer.
            </p>
          </section>
        </div>

      </div>

      {/* Why Choose Us */}
      <WhyChooseUsSection />

      <TestimonialsSection />

      {/* 3. Team Member Section (Unique Cards + Increased Image Size) */}
      {team.length > 0 && (
        <section className="bg-ink-50 py-16">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mb-12 text-center">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-marigold-600">Meet the Team</p>
              <h2 className="mt-1 text-2xl font-bold text-ink-900">The People Behind AFC</h2>
            </div>

            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {team.map((member) => (
                <div
                  key={member.id}
                  className="group rounded-[var(--radius-card)] border border-ink-100 bg-white overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col"
                >
                  {/* Image Container with larger aspect ratio */}
                  <div className="relative w-full aspect-square bg-ink-100 overflow-hidden">
                    <img
                      src={member.image || member.photo || '/placeholder-avatar.png'}
                      alt={member.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </div>

                  {/* Member Details */}
                  <div className="p-5 flex flex-col flex-1 justify-between bg-white border-t border-ink-100/60">
                    <div>
                      <h3 className="text-lg font-semibold text-ink-900 group-hover:text-marigold-600 transition-colors">
                        {member.name}
                      </h3>
                      {member.position && (
                        <p className="mt-1 text-xs font-medium uppercase tracking-wider text-marigold-600">
                          {member.position}
                        </p>
                      )}
                      
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </>
  );
}