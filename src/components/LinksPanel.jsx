import SectionTitle from './SectionTitle'

export default function LinksPanel({ contact, language }) {
  return (
    <section className="section" id="links">
      <div className="container">
        <div className="panel contact-panel">
          <SectionTitle
            eyebrow={contact.title[language]}
            title={contact.heading[language]}
            subtitle={contact.description[language]}
          />

          <div className="contact-grid">
            <div className="future-list">
              {contact.groups.map((group) => (
                <div key={group.key} className="link-group-card">
                  <h3>{group.title[language]}</h3>
                  <div className="quick-link-list">
                    {group.items.map((item) => (
                      <a key={item.href} href={item.href} target="_blank" rel="noreferrer" className="quick-link-card">
                        <span>{item.label[language]}</span>
                        <strong>{item.description[language]}</strong>
                        <small>{item.href.replace('https://', '')}</small>
                      </a>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="future-list notes-list">
              {contact.notes.map((item) => (
                <div className="future-item" key={item.en}>
                  {item[language]}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
