import SectionTitle from './SectionTitle'

export default function Services({ services, language }) {
  return (
    <section className="section" id="services">
      <div className="container">
        <SectionTitle
          eyebrow={services.eyebrow[language]}
          title={services.title[language]}
          subtitle={services.subtitle[language]}
        />

        <div className="service-grid">
          {services.items.map((service) => (
            <article className="service-card" key={service.title.en}>
              <div className="service-number">{service.number}</div>
              <h3>{service.title[language]}</h3>
              <p>{service.description[language]}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
