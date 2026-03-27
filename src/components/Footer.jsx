export default function Footer({ language, year, profile }) {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <span>© {year} {profile.name}</span>
        <span>
          {language === 'zh'
            ? 'React + Vite 製作，已整理為可部署到 GitHub / Railway 的版本'
            : 'Built with React + Vite and prepared for GitHub / Railway deployment'}
        </span>
      </div>
    </footer>
  )
}
