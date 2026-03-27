import SectionTitle from './SectionTitle'

function ProjectCard({ project, language }) {
  return (
    <article className="project-card">
      <span className="project-tag">{project.tag[language]}</span>
      <h3>{project.title[language]}</h3>
      <p>{project.description[language]}</p>

      <div className="stack-row">
        {project.stack.map((item) => (
          <span key={item} className="mini-badge">
            {item}
          </span>
        ))}
      </div>

      <div className="link-row">
        {project.links.map((link) => (
          <a key={link.href} href={link.href} target="_blank" rel="noreferrer" className="text-link">
            {link.label[language]}
          </a>
        ))}
      </div>
    </article>
  )
}

export default function Projects({ projects, language }) {
  return (
    <section className="section" id="projects">
      <div className="container">
        <SectionTitle
          eyebrow={language === 'zh' ? '作品集' : 'Portfolio'}
          title={language === 'zh' ? '精選展示專案' : 'Featured Demo Projects'}
          subtitle={
            language === 'zh'
              ? '以可交付、可解釋、可擴充為導向的展示內容'
              : 'Demo projects designed to be explainable, deliverable, and ready for future expansion'
          }
        />

        <div className="project-grid">
          {projects.map((project) => (
            <ProjectCard key={project.title.en} project={project} language={language} />
          ))}
        </div>
      </div>
    </section>
  )
}
