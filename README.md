# voica.ru — сайт Voica

Лендинг [Voica](https://github.com/Inhum/voica) — голосовой диктовки с пунктуацией для
**Mac и Windows**. Статический сайт на GitHub Pages, без сборочных фреймворков. Шрифты самохостятся;
аналитика — только **cookieless GoatCounter** (без кук и баннера согласия). Двуязычный:
RU (`/`) и EN (`/en/`).

## Структура

```
index.html            RU-страница (генерируется)
en/index.html         EN-страница (генерируется)
assets/
  css/tokens.css      дизайн-токены — единый источник правды (см. BRAND.md)
  css/site.css        стили компонентов (импортирует tokens.css и fonts.css)
  css/fonts.css       @font-face с локальными woff2
  fonts/*.woff2       Onest / Golos Text / JetBrains Mono (cyrillic+latin)
  img/favicon.svg     фавикон-волна
  img/og.png          карточка для соцсетей (1200×630)
src/build.py          генератор: контент (RU+EN) → index.html + en/index.html
BRAND.md              бренд-бук (характер, цвета, шрифты, компоненты, do/don't)
CNAME                 voica.ru
robots.txt sitemap.xml .nojekyll
```

## Редактирование текстов

Весь текст — в словаре `C` внутри `src/build.py` (кортежи `("RU", "EN")`). Правишь там,
затем пересобираешь:

```bash
python3 src/build.py      # перезапишет index.html и en/index.html
```

`index.html`/`en/index.html` **генерируются** — руками не править, менять только через
`build.py`. Стиль — в `assets/css/` (сначала читай BRAND.md).

## Локальный просмотр

Относительные пути к CSS работают и из файла, но надёжнее поднять локальный сервер:

```bash
python3 -m http.server 8000    # затем открыть http://localhost:8000/  и  /en/
```

## Деплой

GitHub Pages из ветки `main`, корень репозитория. Настройка (однократно):

1. Settings → Pages → Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
2. Файл `CNAME` уже указывает `voica.ru`. У регистратора домена добавить DNS:
   - **A-записи** `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - **CNAME** `www` → `inhum.github.io`
3. В Settings → Pages включить **Enforce HTTPS** (после выпуска сертификата — обычно до часа).

Кнопки «Скачать» ведут на релизы приложений: Mac → `Inhum/voica`, Windows → `Inhum/voica-win`.

## Принципы

- Ноль внешних зависимостей и трекеров (сайт честен к «нет телеметрии» приложения).
- Тема — по системе + тумблер; язык — две статические страницы + `hreflang`.
- Любые правки стиля — через `tokens.css`/`BRAND.md`, не хардкодом.
