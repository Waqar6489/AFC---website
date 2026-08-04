/**
 * Placeholder wordmark lockup — the spec calls for the client's real
 * uploaded logo, which was not provided. This renders a clean text-based
 * lockup in the brand palette so the layout is fully functional today;
 * swap it for an <img> pointing at the real logo asset in
 * src/assets/logo.svg the moment it's available, and this component's
 * call sites (Navbar, Footer) won't need to change.
 */

export function footerLogo() {
 
  return (
    <div className='inline-flex items-center gap-2.5'>
      <img src="/footer-logo.png" alt="AFC - Ahamed Food center" 
      
      className="h-25 w-full"/>
     
      
    </div>
  );
}

export default function Logo() {
 
  return (
    <div className='inline-flex items-center gap-2.5'>
      <img src="/logos_afc.png" alt="AFC - Ahamed Food center" 
      
      className="h-22 w-full"/>
     
      
    </div>
  );
}