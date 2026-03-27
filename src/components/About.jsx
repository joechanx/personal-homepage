import SectionTitle from './SectionTitle'

export default function About({ about, highlights, language }) {
  return (
    <section className="section" id="about">
      <div className="container two-column-grid">
        <div className="panel">
          <SectionTitle
            eyebrow={about.sectionLabel[language]}
            title={about.title[language]}
            subtitle={about.subtitle[language]}
          />

          <div className="text-stack">
            {about.paragraphs.map((paragraph) => (
              <p key={paragraph.en}>{paragraph[language]}</p>
            ))}
          </div>
        </div>

        <div className="panel">
          <SectionTitle
            eyebrow={language === 'zh' ? '核心方向' : 'Core Focus'}
            title={language === 'zh' ? '我能提供的內容' : 'What I Can Offer'}
          />

          <div className="feature-list">
            {highlights.map((item) => (
              <article className="feature-card" key={item.title.en}>
                <h3>{item.title[language]}</h3>
                <p>{item.description[language]}</p>
              </article>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
