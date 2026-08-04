import { FiFacebook, FiInstagram, FiLinkedin, FiTwitter } from 'react-icons/fi';

export default function TeamMemberCard({ member }) {
  const socials = [
    { url: member.facebook_url, icon: FiFacebook },
    { url: member.instagram_url, icon: FiInstagram },
    { url: member.twitter_url, icon: FiTwitter },
    { url: member.linkedin_url, icon: FiLinkedin },
  ].filter((s) => s.url);

  return (
    <div className="flex flex-col items-center rounded-[var(--radius-card)] border border-ink-100 bg-white p-6 text-center">
      <div className="h-24 w-24 overflow-hidden rounded-full bg-ink-50">
        {member.image && <img src={member.image} alt={member.name} className="h-full w-full object-cover" />}
      </div>
      <h3 className="mt-4 font-semibold text-ink-900">{member.name}</h3>
      <p className="text-xs font-medium uppercase tracking-wide text-marigold-600">{member.display_title}</p>
      {socials.length > 0 && (
        <div className="mt-3 flex gap-2.5">
          {socials.map(({ url, icon: Icon }, index) => (
            <a
              key={index}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex h-8 w-8 items-center justify-center rounded-full bg-ink-50 text-ink-500 hover:bg-marigold-100 hover:text-marigold-700"
            >
              <Icon className="h-3.5 w-3.5" />
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
