#!/usr/bin/env python3
"""Генератор сайта Voica. Контент двуязычный (единый источник ниже) → две статические
страницы: index.html (RU, корень) и en/index.html (EN). Текст вшивается в HTML (SEO),
без рантайм-i18n. Запуск: python3 src/build.py  (из корня репозитория)."""
import os, json

SITE = "https://voica.ru"

META = {
  "ru": {"title": "Voica — голосовая диктовка с пунктуацией для Mac и Windows",
         "desc": "Диктуйте голосом — получайте чистый текст с точками и запятыми. Облачный движок Groq Whisper или полностью офлайн на устройстве (GigaAM). Открытый код, свой ключ."},
  "en": {"title": "Voica — voice dictation with punctuation for Mac & Windows",
         "desc": "Dictate by voice, get clean punctuated text. Cloud engine (Groq Whisper) or fully offline on-device (GigaAM). Open source, bring your own key."},
}

C = {
 "nav.engines":("Движки","Engines"),
 "nav.privacy":("Приватность","Privacy"),
 "nav.faq":("Вопросы","FAQ"),
 "nav.docs":("Документация","Docs"),
 "nav.download":("Скачать","Download"),
 "hero.eyebrow":("Голосовая диктовка для Mac и Windows","Voice dictation for Mac & Windows"),
 "hero.h1":('Диктуйте — и получайте готовый текст <span class="accent">с пунктуацией</span>',
            'Dictate, and get clean text — <span class="accent">punctuation included</span>'),
 "hero.lede":("Voica живёт в строке меню (или в трее). Нажали клавишу, сказали — и текст с точками, запятыми и «ёлочками» появляется прямо там, где вы печатаете. В облаке через Groq Whisper или полностью офлайн, на вашем устройстве.",
              "Voica lives in your menu bar (or tray). Press a key, speak — and text with proper punctuation appears right where you're typing. In the cloud via Groq Whisper, or fully offline on your device."),
 "hero.cta1":("Скачать","Download"),
 "hero.cta2":("Как это работает","How it works"),
 "hero.note":("Mac (13+, Apple Silicon) и Windows · <b>бесплатно</b> — свой ключ Groq или локальная модель",
              "Mac (13+, Apple Silicon) and Windows · <b>free</b> — bring your own Groq key or the local model"),
 "mock.rec":("ЗАПИСЬ · ЛОКАЛЬНО","RECORDING · LOCAL"),
 "mock.res":('Поставил <span class="hl">GigaAM</span> и развернул <span class="hl">Kubernetes</span> через <span class="hl">kubectl</span>.',
             'I installed <span class="hl">GigaAM</span> and deployed <span class="hl">Kubernetes</span> via <span class="hl">kubectl</span>.'),
 "mock.hint":("удерживайте, чтобы говорить · текст уже в буфере","hold to talk · text is already on the clipboard"),
 "eng.cap":("Voica — Настройки · Основные","Voica — Settings · General"),
 "eng.h4":("Движок распознавания","Recognition engine"),
 "eng.seg1":("Облако (Groq)","Cloud (Groq)"),
 "eng.seg2":("Локально (офлайн)","Local (offline)"),
 "eng.status":("Работает: GigaAM v3 — на этом устройстве","Active: GigaAM v3 — on this device"),
 "eng.esub":("Без интернета и без ключа. Аудио не покидает устройство.","No internet, no key. Audio never leaves the device."),
 "eng.eyebrow":("Два движка, один хоткей","Two engines, one shortcut"),
 "eng.title":("Облако или полностью офлайн — на ваш выбор","Cloud or fully offline — your call"),
 "eng.sub":("Переключатель прямо в настройках. Оба движка быстрые и ставят пунктуацию; выбираете, что важнее — не занимать место на диске или не отправлять аудио в облако.",
            "A switch right in Settings. Both engines are fast and add punctuation — choose what matters more: no disk space used, or no audio sent to the cloud."),
 "eng.a.tag":("Облако","Cloud"),
 "eng.a.body":("Быстрое и точное распознавание на серверах Groq (<code>whisper-large-v3-turbo</code>). Ничего не занимает на устройстве — модель качать не нужно. Нужен свой ключ Groq (бесплатный) и интернет.",
               "Fast, accurate recognition on Groq's servers (<code>whisper-large-v3-turbo</code>). Nothing to download, zero disk footprint. Needs your own (free) Groq key and a connection."),
 "eng.a.chips":('<span class="chip">точность</span><span class="chip">без загрузки</span><span class="chip">мультиязык</span>',
                '<span class="chip">accurate</span><span class="chip">no download</span><span class="chip">multilingual</span>'),
 "eng.b.tag":("Локально · офлайн","On-device · offline"),
 "eng.b.title":("GigaAM — на вашем устройстве","GigaAM — on your device"),
 "eng.b.body":("Модель <b>GigaAM от Сбера</b> работает целиком на устройстве — быстро, без интернета и без ключа. Аудио не покидает ваш компьютер. Нативно-русское распознавание с пунктуацией из коробки. Разовая загрузка модели: ~400 МБ на Mac, ~200 МБ на Windows.",
               "<b>Sber's GigaAM</b> model runs entirely on your device — fast, no internet, no key. Audio never leaves your computer. Native Russian recognition with punctuation out of the box. One-time model download: ~400 MB on Mac, ~200 MB on Windows."),
 "eng.b.chips":('<span class="chip">офлайн</span><span class="chip">без ключа</span><span class="chip">приватно</span><span class="chip">русский</span>',
                '<span class="chip">offline</span><span class="chip">no key</span><span class="chip">private</span><span class="chip">Russian</span>'),
 "eng.b.niche":("<b>Почему это редкость:</b> нативно-русская локальная диктовка — почти пустая ниша. Западные приложения заточены под английский; GigaAM — открытая модель Сбера, сильная именно на русском.",
                "<b>Why it's rare:</b> native-Russian on-device dictation is an almost empty niche. Western apps target English; GigaAM is Sber's open model, strong on Russian."),
 "priv.h":("Приватность по умолчанию","Private by default"),
 "priv.body":('Аудио уходит только в Groq на распознавание — или <b style="color:var(--wave)">не уходит никуда</b>, если выбран локальный движок. Ключ хранится в защищённом файле на вашем устройстве. Нет бэкенда, нет телеметрии, нет аккаунтов. Код открыт под MIT — можно проверить.',
             'Audio goes only to Groq for recognition — or <b style="color:var(--wave)">nowhere at all</b> with the local engine. Your key is kept in a protected file on your device. No backend, no telemetry, no accounts. Open source under MIT — see for yourself.'),
 "how.eyebrow":("Как это работает","How it works"),
 "how.title":("Три шага — и текст на месте","Three steps to finished text"),
 "how.s1t":("Нажмите клавишу","Press the key"),
 "how.s1b":("Горячая клавиша по умолчанию — правый Option на Mac, правый Alt на Windows. Режим на выбор: удерживать во время речи или нажать один раз.",
            "The default shortcut is Right Option on Mac, Right Alt on Windows. Your choice of mode: hold while speaking, or press once."),
 "how.s2t":("Говорите","Speak"),
 "how.s2b":("Значок в строке меню (в трее) показывает запись. Говорите естественно — о знаках препинания позаботится Voica.",
            "The menu-bar (tray) icon shows it's recording. Speak naturally — Voica handles the punctuation."),
 "how.s3t":("Готово","Done"),
 "how.s3b":("Через секунду текст уже вставлен в активное поле. И всегда лежит в буфере обмена — на всякий случай.",
            "A second later the text is in your active field — and always on the clipboard, just in case."),
 "feat.eyebrow":("Что внутри","Under the hood"),
 "feat.title":("Мелочи, из которых складывается «просто работает»","The details that make it just work"),
 "feat.1t":("Пунктуация из коробки","Punctuation out of the box"),
 "feat.1b":("Точки, запятые, вопросы, «ёлочки», буква ё — без ручной правки.","Periods, commas, question marks, quotes, the letter ё — no manual cleanup."),
 "feat.2t":("Словарь терминов","Term dictionary"),
 "feat.2b":('Свои названия и жаргон + ИИ-исправление: «кубернетес» → Kubernetes.','Your names and jargon, plus AI fixing: "kubernetis" → Kubernetes.'),
 "feat.3t":("Авто-вставка","Auto-insert"),
 "feat.3b":("Текст появляется прямо в поле — или в редактируемом окне, на выбор.","Text lands right in the field — or an editable window, your choice."),
 "feat.4t":("История диктовок","Dictation history"),
 "feat.4b":("Все расшифровки под рукой: копировать, прослушать аудио, удалить.","Every transcript at hand: copy, play back the audio, delete."),
 "feat.5t":("Русский и английский","Russian & English"),
 "feat.5b":("Смешанная речь распознаётся, интерфейс — на языке системы.","Mixed speech is recognized; the UI follows your system language."),
 "feat.6t":("Открытый код","Open source"),
 "feat.6b":("MIT, никаких облачных зависимостей, кроме вашего Groq.","MIT, no cloud dependencies beyond your own Groq."),
 "cta.h":("Установите Voica за минуту","Install Voica in a minute"),
 "cta.body":("Скачайте и откройте — перетащите в «Программы» (Mac) или запустите .exe (Windows) — вставьте ключ Groq или включите локальный движок и работайте офлайн.",
             "Download and open it — drag to Applications (Mac) or run the .exe (Windows) — paste your Groq key, or switch on the local engine and work offline."),
 "cta.mac":("Скачать для Mac","Download for Mac"),
 "cta.win":("Скачать для Windows","Download for Windows"),
 "cta.note":("Mac 13+ (Apple Silicon) · Windows 10/11 · приложение пока без подписи — при первом запуске система переспросит.",
             "Mac 13+ (Apple Silicon) · Windows 10/11 · the app isn't signed yet — your system will ask once on first launch."),
 "foot.left":("© 2026 Ivan Ushakov · MIT · Открытая разработка","© 2026 Ivan Ushakov · MIT · Built in the open"),
 "foot.sber":("Сбер","Sber"),
 "faq.eyebrow":("Вопросы и ответы","Questions & answers"),
 "faq.title":("Частые вопросы","Frequently asked questions"),
 "faq.q1":("Нужен ли интернет?","Do I need an internet connection?"),
 "faq.a1":("Для облачного движка — да. Локальный движок работает полностью офлайн: без интернета, без ключа, и аудио не покидает устройство.","For the cloud engine, yes. The local engine works fully offline — no internet, no key, and audio never leaves your device."),
 "faq.q2":("Это платно?","Is it free?"),
 "faq.a2":("Voica бесплатна, код открыт под лицензией MIT. Для облачного движка нужен свой бесплатный ключ Groq; локальный движок работает вообще без ключа.","Voica is free and open source under the MIT license. The cloud engine needs your own free Groq key; the local engine needs no key at all."),
 "faq.q3":("Какие языки поддерживаются?","Which languages are supported?"),
 "faq.a3":("Русский и английский, включая смешанную речь. Локальная модель GigaAM особенно сильна на русском и ставит пунктуацию из коробки.","Russian and English, including mixed speech. The local GigaAM model is especially strong on Russian and adds punctuation out of the box."),
 "faq.q4":("Мои данные приватны?","Is my data private?"),
 "faq.a4":("Аудио уходит только в Groq на распознавание — или никуда, если выбран локальный движок. Нет бэкенда, телеметрии и аккаунтов; ключ хранится в защищённом файле на вашем устройстве.","Audio goes only to Groq for recognition — or nowhere at all with the local engine. No backend, no telemetry, no accounts; your key is kept in a protected file on your device."),
 "faq.q5":("Какие системы поддерживаются?","Which systems are supported?"),
 "faq.a5":("macOS 13 и новее (Apple Silicon) и Windows 10/11.","macOS 13 and later (Apple Silicon) and Windows 10/11."),
 "faq.q6":("Voica ставит знаки препинания?","Does Voica add punctuation?"),
 "faq.a6":("Да. Оба движка автоматически расставляют точки, запятые, вопросительные знаки и «ёлочки» — без ручной правки.","Yes. Both engines automatically add periods, commas, question marks and quotation marks — no manual cleanup."),
 "faq.q7":("Чем локальный движок отличается от облачного?","How does the local engine differ from the cloud one?"),
 "faq.a7":("Облако — быстро и точно, ничего не нужно качать, но требуется ключ и интернет. Локально — приватно и офлайн, но модель скачивается один раз (~400 МБ на Mac, ~200 МБ на Windows).","Cloud is fast and accurate with nothing to download, but needs a key and internet. Local is private and offline, but the model downloads once (~400 MB on Mac, ~200 MB on Windows)."),
 "faq.q8":("Почему при первом запуске предупреждение о безопасности?","Why the security warning on first launch?"),
 "faq.a8":("Приложение пока не подписано сертификатом разработчика, поэтому система переспрашивает один раз: на macOS — «Open Anyway» в разделе Privacy & Security, на Windows — подтверждение SmartScreen. Дальше Voica открывается обычным способом.","The app isn't signed with a developer certificate yet, so your system asks once: on macOS use “Open Anyway” in Privacy & Security, on Windows confirm the SmartScreen prompt. After that Voica opens normally."),
}

WAVE = '<span class="wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>'
def eyebrow(text): return f'<div class="eyebrow">{WAVE} <span>{text}</span></div>'

def render(lang):
    idx = 0 if lang=="ru" else 1
    t = {k:v[idx] for k,v in C.items()}
    m = META[lang]
    base = "" if lang=="ru" else "../"
    other = "en/" if lang=="ru" else "../"
    other_lang = "EN" if lang=="ru" else "RU"
    canon = SITE + ("/" if lang=="ru" else "/en/")
    # README нужного языка на GitHub (RU → README.ru.md, EN → README.md)
    readme_url = "https://github.com/Inhum/voica/blob/main/" + ("README.ru.md" if lang=="ru" else "README.md")
    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Voica",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "macOS 13+, Windows 10/11",
        "description": m["desc"],
        "url": canon,
        "inLanguage": lang,
        "softwareVersion": "0.9",
        "license": "https://opensource.org/licenses/MIT",
        "downloadUrl": "https://github.com/Inhum/voica/releases/latest",
        "author": {"@type": "Person", "name": "Ivan Ushakov"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }, ensure_ascii=False)
    mlive = "".join(f'<i style="animation-delay:{i*.1:.1f}s"></i>' for i in range(5))
    mwv = "".join(f'<i style="animation-delay:{i*.08:.2f}s"></i>' for i in range(14))
    feats = "".join(
        f'<div class="feat-i"><h3><span class="wm"><i></i><i></i><i></i></span> {t[f"feat.{n}t"]}</h3><p>{t[f"feat.{n}b"]}</p></div>'
        for n in range(1,7))
    faqs = "".join(
        f'<details><summary>{t[f"faq.q{n}"]}</summary><p>{t[f"faq.a{n}"]}</p></details>'
        for n in range(1,9))
    faq_ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": t[f"faq.q{n}"],
                        "acceptedAnswer": {"@type": "Answer", "text": t[f"faq.a{n}"]}}
                       for n in range(1, 9)],
    }, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="{lang}" prefix="og: https://ogp.me/ns#">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{m["title"]}</title>
<meta name="description" content="{m["desc"]}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="ru" href="{SITE}/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{m["title"]}">
<meta property="og:description" content="{m["desc"]}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{ld_json}</script>
<script type="application/ld+json">{faq_ld}</script>
<link rel="icon" href="{base}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{base}assets/css/site.css">
</head>
<body>
<div class="nav"><div class="wrap nav-in">
  <a class="brand" href="{base or './'}">{WAVE} Voica</a>
  <div class="nav-right">
    <a class="nav-link hide-sm" href="#engines">{t["nav.engines"]}</a>
    <a class="nav-link hide-sm" href="#privacy">{t["nav.privacy"]}</a>
    <a class="nav-link hide-sm" href="#faq">{t["nav.faq"]}</a>
    <a class="nav-link hide-sm" href="{readme_url}">{t["nav.docs"]}</a>
    <a class="nav-link" href="https://github.com/Inhum">GitHub</a>
    <a class="icon-btn" href="{other}" hreflang="{other_lang.lower()}">{other_lang}</a>
    <button class="icon-btn" id="theme" aria-label="Theme">
      <svg class="theme-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      <svg class="theme-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
    </button>
    <a class="btn btn-primary" href="#download">{t["nav.download"]}</a>
  </div>
</div></div>

<header class="hero"><div class="wrap hero-grid">
  <div>
    {eyebrow(t["hero.eyebrow"])}
    <h1>{t["hero.h1"]}</h1>
    <p class="lede">{t["hero.lede"]}</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="#download">{t["hero.cta1"]}</a>
      <a class="btn btn-ghost" href="#how">{t["hero.cta2"]}</a>
    </div>
    <p class="hero-note">{t["hero.note"]}</p>
  </div>
  <div class="mock" aria-hidden="true">
    <div class="mock-bar"><span class="mlive">{mlive}</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
      <span class="mclock">14:32</span></div>
    <div class="mock-body">
      <span class="mrec"><b></b>{t["mock.rec"]}</span>
      <div class="mwv">{mwv}</div>
      <div class="mres">{t["mock.res"]}</div>
      <div class="mhint"><span class="mkbd">⌥</span> {t["mock.hint"]}</div>
    </div>
  </div>
</div></header>

<section id="engines"><div class="wrap">
  <div class="eng-visual"><div class="epanel" aria-hidden="true">
    <div class="cap">{t["eng.cap"]}</div>
    <h4>{t["eng.h4"]}</h4>
    <div class="seg"><div>{t["eng.seg1"]}</div><div class="on">{t["eng.seg2"]}</div></div>
    <div class="estatus"><span class="dot-ok">✓</span> <span>{t["eng.status"]}</span></div>
    <p class="esub">{t["eng.esub"]}</p>
  </div></div>
  <div class="sec-head">{eyebrow(t["eng.eyebrow"])}<h2>{t["eng.title"]}</h2><p class="lede">{t["eng.sub"]}</p></div>
  <div class="engines">
    <div class="engine">
      <span class="tag tag-blue">{t["eng.a.tag"]}</span><h3>Groq Whisper</h3>
      <p>{t["eng.a.body"]}</p><div class="chips">{t["eng.a.chips"]}</div>
    </div>
    <div class="engine local">
      <span class="tag tag-ok">{t["eng.b.tag"]}</span>
      <h3><span class="wave" style="height:22px" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span> {t["eng.b.title"]}</h3>
      <p>{t["eng.b.body"]}</p><div class="chips">{t["eng.b.chips"]}</div>
      <p class="sber">{t["eng.b.niche"]}</p>
    </div>
  </div>
</div></section>

<section id="privacy"><div class="wrap"><div class="privacy">
  <span class="wave pw" style="height:56px" aria-hidden="true"><i style="width:5px"></i><i style="width:5px"></i><i style="width:5px"></i><i style="width:5px"></i><i style="width:5px"></i><i style="width:5px"></i></span>
  <div><h2>{t["priv.h"]}</h2><p>{t["priv.body"]}</p></div>
</div></div></section>

<section id="how"><div class="wrap">
  <div class="sec-head">{eyebrow(t["how.eyebrow"])}<h2>{t["how.title"]}</h2></div>
  <div class="steps">
    <div class="step"><h3>{t["how.s1t"]}</h3><p>{t["how.s1b"]}</p></div>
    <div class="step"><h3>{t["how.s2t"]}</h3><p>{t["how.s2b"]}</p></div>
    <div class="step"><h3>{t["how.s3t"]}</h3><p>{t["how.s3b"]}</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head">{eyebrow(t["feat.eyebrow"])}<h2>{t["feat.title"]}</h2></div>
  <div class="feat">{feats}</div>
</div></section>

<section id="faq"><div class="wrap">
  <div class="sec-head">{eyebrow(t["faq.eyebrow"])}<h2>{t["faq.title"]}</h2></div>
  <div class="faq">{faqs}</div>
</div></section>

<section id="download" class="cta"><div class="wrap"><div class="cta-box">
  <h2>{t["cta.h"]}</h2><p>{t["cta.body"]}</p>
  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
    <a class="btn btn-primary" href="https://github.com/Inhum/voica/releases/latest">{t["cta.mac"]}</a>
    <a class="btn btn-ghost" href="https://github.com/Inhum/voica-win/releases/latest">{t["cta.win"]}</a>
  </div>
  <p class="hero-note" style="margin-top:20px">{t["cta.note"]}</p>
</div></div></section>

<footer class="foot"><div class="wrap foot-in">
  <div>{t["foot.left"]}</div>
  <div class="foot-mono">whisper-large-v3-turbo · gigaam-v3-e2e-ctc · GigaAM © {t["foot.sber"]}</div>
</div></footer>

<script>
(function(){{var r=document.documentElement;try{{var t=localStorage.getItem("voica-theme");if(t)r.setAttribute("data-theme",t);}}catch(e){{}}
document.getElementById("theme").onclick=function(){{var c=r.getAttribute("data-theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");var n=c==="dark"?"light":"dark";r.setAttribute("data-theme",n);try{{localStorage.setItem("voica-theme",n);}}catch(e){{}}}};}})();
</script>
<!-- GoatCounter — cookieless-аналитика, без кук и баннера согласия -->
<script data-goatcounter="https://voica.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
</body>
</html>'''

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
open(os.path.join(root,"index.html"),"w").write(render("ru"))
os.makedirs(os.path.join(root,"en"),exist_ok=True)
open(os.path.join(root,"en","index.html"),"w").write(render("en"))
print("собрано: index.html (ru), en/index.html (en)")
