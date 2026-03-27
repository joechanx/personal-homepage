export default function TopNav({ brand, items, language, onToggleLanguage }) {
  return (
    <header className="topbar">
      <div className="container nav-row">
        <a className="brand" href="#top">
          {brand}
        </a>

        <nav className="nav-links" aria-label="Primary Navigation">
          {items.map((item) => (
            <a key={item.id} href={`#${item.id}`}>
              {item[language]}
            </a>
          ))}
        </nav>

        <button className="lang-switch" onClick={onToggleLanguage} type="button">
          {language === 'zh' ? '中文 / EN' : 'EN / 中文'}
        </button>
      </div>
    </header>
  )
}
