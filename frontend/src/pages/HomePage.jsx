import { Helmet } from 'react-helmet-async';
import Button from '@/components/ui/Button';
import { useEffect, useState } from 'react';
import { productService } from '@/services/productService';
import CategoriesSection from '@/components/home/CategoriesSection';
import ProductsSection from '@/components/home/ProductsSection';
import DealsSection from '@/components/home/DealsSection';
import WhyChooseUsSection from '@/components/home/WhyChooseUsSection';
import TestimonialsSection from '@/components/home/TestimonialsSection';
import FAQSection from '@/components/home/FAQSection';
import ContactMapSection from '@/components/home/ContactMapSection';
import { FiZap, FiTruck, FiAward } from 'react-icons/fi';

export default function HomePage() {
  const slides = [
    {
      id: 1,
      image: '/pizza.webp', // Place in public/ folder
      
    },
    {
      id: 2,
      image: '/burger.jpg', // Place in public/ folder
      
    },
    {
      id: 3,
      image: '/cake.jpg', // Place in public/ folder

    },
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

  // Auto-scroll logic: switch image every 4 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % slides.length);
    }, 3000);

    return () => clearInterval(timer); // Clean up timer on unmount
  }, [slides.length]);

 
  return (
    <>
      <Helmet>
        <title>AFC - Ahmad Foods | Sweets & Bakers</title>
        <meta name="description" content="Order fresh cakes, pastries and sweets online from AFC - Ahmad Foods, delivered to your door." />
      </Helmet>

     <section className="relative overflow-hidden bg-ink-800 text-cream">
      <div className="mx-auto flex max-w-7xl flex-col lg:flex-row items-center justify-between gap-12 px-4 py-16 sm:px-6 sm:py-24 lg:px-8">
        
        {/* Left Side: Headline & CTA */}
        <div className="flex-1 flex flex-col items-start gap-6">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-marigold-300">
            Freshly Prepared, Daily
          </p>

          <h1 className="max-w-2xl text-4xl font-bold leading-tight text-cream sm:text-5xl">
            Handcrafted pizza, burgers &amp; cakes, delivered warm to your door.
          </h1>

           <p className="max-w-lg text-ink-300">
            AFC - Ahmad Foods brings together traditional recipes and modern flavors to create a world of tastes worth celebrating.
          </p>

          <div className="flex gap-3">

            <Button to="/shop" size="lg" className="border-ink-500 bg-cream hover:bg-ink-700">Order Now</Button>

            <Button to="/deals"  size="lg" className=" border border-marigold-300 bg-transparent text-marigold-300 hover:bg-ink-700 hover:text-ink-900">

              View Deals

            </Button>

          </div>

          {/* Feature Badges */}
          <div className="grid grid-cols-3 gap-4 pt-6 border-t border-ink-700/50 w-full max-w-lg text-xs sm:text-sm">
            <div className="flex items-center flex-col gap-1">
              <FiZap className="mx-auto text-2xl text-marigold-300" />
              < div >
              <p className="font-semibold text-cream">100% Fresh</p>
              <p className="text-ink-400">Made daily</p>
              </div>
            </div>
            <div>
              <div className="flex items-center flex-col gap-1">
              <FiTruck className="mx-auto text-2xl text-marigold-300" />
              <p className="font-semibold text-cream">Fast Delivery</p>
              <p className="text-ink-400">At your doorstep</p>
              </div>
            </div>
            <div>
              <div className="flex items-center flex-col gap-1">
              <FiAward className="mx-auto text-2xl text-marigold-300" />
              <p className="font-semibold text-cream">Premium Quality</p>
              <p className="text-ink-400">Best ingredients</p>
              </div>
            </div>
          </div>
        </div>
  

        {/* Right Side: Single Card Carousel with Controls */}
        <div className="w-full lg:w-1/2 flex flex-col items-center justify-center relative">
          
          {/* Main Display Box */}
          <div className="relative w-full max-w-lg aspect-square rounded-3xl bg-ink-900 overflow-hidden shadow-2xl transition-all duration-500 ease-in-out">
            <img
              key={slides[currentIndex].id}
              src={slides[currentIndex].image}
              alt={slides[currentIndex].title}
              className="w-full h-full object-cover transition-opacity duration-700 ease-in-out"
            />

         
            

            
           
          </div>

          {/* Indicator Dots */}
          <div className="flex gap-2 mt-6">
            {slides.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentIndex(index)}
                className={`h-2.5 rounded-full transition-all duration-300 ${
                  currentIndex === index
                    ? 'w-8 bg-marigold-400'
                    : 'w-2.5 bg-ink-600 hover:bg-ink-500'
                }`}
                aria-label={`Go to slide ${index + 1}`}
              />
            ))}
          </div>

        </div>

      </div>
    </section>

      <CategoriesSection />
      <ProductsSection eyebrow="Hot Right Now" title="Trending Products" fetcher={productService.trending} />
      <DealsSection />
      <ProductsSection eyebrow="Customer Favorites" title="Best Selling" fetcher={productService.bestSellers} />
      <ProductsSection eyebrow="Handpicked" title="Featured Products" fetcher={productService.featured} />
      <WhyChooseUsSection />
      <TestimonialsSection />
      <FAQSection />
      <ContactMapSection />
    </>
  );
}
