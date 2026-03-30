import { useEffect, useMemo, useState } from 'react'
import { siteContent } from './data/siteContent'
import TopNav from './components/TopNav'
import Hero from './components/Hero'
import About from './components/About'
import Services from './components/Services'
import Projects from './components/Projects'
import LinksPanel from './components/LinksPanel'
import Footer from './components/Footer'

const LANGUAGE_STORAGE_KEY = 'preferred-language'
const DEFAULT_LANGUAGE = 'zh'

export default function App() {
  const [language, setLanguage] = useState(() => {
    if (typeof window === 'undefined') {
      return DEFAULT_LANGUAGE
    }

    const savedLanguage = window.localStorage.getItem(LANGUAGE_STORAGE_KEY)
    return savedLanguage === 'zh' || savedLanguage === 'en' ? savedLanguage : DEFAULT_LANGUAGE
  })

  const currentYear = useMemo(() => new Date().getFullYear(), [])
  const pageTitle = language === 'zh' ? 'Dexter Chang｜個人首頁' : 'Dexter Chang | Personal Homepage'
  const pageDescription = siteContent.seo.description[language]

  useEffect(() => {
    window.localStorage.setItem(LANGUAGE_STORAGE_KEY, language)
    document.documentElement.lang = language === 'zh' ? 'zh-Hant' : 'en'
    document.title = pageTitle

    const descriptionTag = document.querySelector('meta[name="description"]')
    if (descriptionTag) {
      descriptionTag.setAttribute('content', pageDescription)
    }
  }, [language, pageDescription, pageTitle])

  return (
    <div className="page-shell">
      <TopNav
        brand={siteContent.profile.name}
        items={siteContent.navigation}
        language={language}
        onToggleLanguage={() => setLanguage((prev) => (prev === 'zh' ? 'en' : 'zh'))}
      />

      <main>
        <Hero profile={siteContent.profile} language={language} />
        <Services services={siteContent.services} language={language} />
        <Projects projects={siteContent.projects} language={language} />
        <About about={siteContent.about} highlights={siteContent.highlights} language={language} />
        <LinksPanel contact={siteContent.contact} language={language} />
      </main>

      <Footer language={language} year={currentYear} profile={siteContent.profile} />
    </div>
  )
}
