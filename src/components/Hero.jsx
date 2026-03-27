function LinkGroup({ title, links, language }) {
  return (
    <div className="hero-link-group">
      <div className="hero-link-group-title">{title}</div>
      <div className="hero-link-row">
        {links.map((link) => (
          <a
            key={link.href}
            className={link.primary ? 'button primary' : 'button secondary'}
            href={link.href}
            target="_blank"
            rel="noreferrer"
          >
            {link.label[language]}
          </a>
        ))}
      </div>
    </div>
  )
}

export default function Hero({ profile, language }) {
  const badgeText =
    typeof profile.badge === 'object'
      ? (profile.badge?.[language] ?? '').trim()
      : (profile.badge ?? '').trim()

  return (
    <section className="hero" id="top">
      <div className="container hero-card">
        <div className="hero-copy">
          {badgeText ? <span className="badge">{badgeText}</span> : null}
          <p className="hero-name">{profile.name}</p>
          <h1>{profile.role[language]}</h1>
          <p className="hero-intro">{profile.summary[language]}</p>

          <div className="hero-points">
            {profile.points.map((point) => (
              <div key={point.en} className="hero-point-item">
                <span className="hero-point-dot" aria-hidden="true" />
                <span>{point[language]}</span>
              </div>
            ))}
          </div>

          <div className="meta-row">
            <span className="meta-pill">
              {profile.locationLabel[language]}: {profile.location}
            </span>
            <span className="meta-pill">{profile.workType[language]}</span>
          </div>

          <div className="badge-row">
            {profile.heroBadges.map((badge) => (
              <span key={badge} className="outline-badge">
                {badge}
              </span>
            ))}
          </div>

          <p className="availability">{profile.availability[language]}</p>

          <div className="hero-link-groups">
            <LinkGroup
              title={profile.profileLinksTitle[language]}
              links={profile.profileLinks}
              language={language}
            />
            <LinkGroup
              title={profile.demoLinksTitle[language]}
              links={profile.demoLinks}
              language={language}
            />
          </div>
        </div>

        <div className="hero-photo-shell">
          <div className="photo-frame">
            <img src={profile.image} alt={profile.name} className="hero-photo" />
          </div>
        </div>
      </div>
    </section>
  )
}
