'use strict';

/* ============================================================
   Starter Kit — Gulpfile (2026)
   ------------------------------------------------------------
   Estrutura moderna, modular e compatível com:
   - Sass
   - Pug
   - Browserify + Babelify (ES Modules)
   - BrowserSync
   - Ambientes múltiplos (dev, prod, staging, deployment)
============================================================ */

/* ------------------------------
   Dependências principais
------------------------------ */
const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const terser = require('gulp-terser');
const pug = require('gulp-pug');
const sourcemaps = require('gulp-sourcemaps');
const rename = require('gulp-rename');
const browserSync = require('browser-sync').create();


/* Browserify (JS modular) */
const browserify = require('browserify');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');

/* ============================================================
   Ambiente (dev por padrão)
============================================================ */
const env = process.env.NODE_ENV || 'development';
const isDev = env === 'development';

console.log(`Gulp is now running in ${env} mode`);

/* ============================================================
   Pastas de saída por ambiente
============================================================ */
const outputDir =
  env === 'production' ? './dist/' :
  env === 'staging'    ? './staging/' :
  env === 'deployment' ? './build/' :
                         './dev/';

/* ============================================================
   Caminhos de entrada
============================================================ */
const paths = {
  sass: 'assets/sass/**/*.scss',                 // Todos os SCSS
  js:   'assets/js/**/*.js',                     // Todos os JS
  img:  'assets/img/**/*.{jpg,jpeg,png,svg,gif,webp}', // Imagens
  pug:  'assets/pug/templates/pages/*.pug'       // Páginas Pug
};

/* ============================================================
   Task: CSS (Sass → CSS)
   - Compila SCSS
   - Gera sourcemaps
   - Autoprefixer
   - Minifica em produção
============================================================ */
function css() {
  return gulp.src(paths.sass)
    .pipe(sourcemaps.init())
    .pipe(
      sass({ outputStyle: isDev ? 'expanded' : 'compressed' })
        .on('error', sass.logError)
    )
    .pipe(postcss(isDev ? [autoprefixer()] : [autoprefixer(), cssnano()]))
    .pipe(rename({ suffix: isDev ? '' : '.min' }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(outputDir + 'css'))
    .pipe(browserSync.stream());
}

/* ============================================================
   Task: JS (Browserify + Babelify)
   - Suporta módulos ES6
   - Gera bundle único
   - Minifica em produção
============================================================ */
function bundleJS() {
  return browserify({
      entries: ['assets/js/main.js'],
      debug: true
    })
    .transform('babelify', {
      presets: ['@babel/preset-env'],
      sourceMaps: true
    })
    .bundle()
    .on('error', function (err) {
      console.error(err.message);
      this.emit('end');
    })
    .pipe(source(isDev ? 'main.js' : 'main.min.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(isDev ? rename({}) : terser())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(outputDir + 'js'))
    .pipe(browserSync.stream());
}

/* ============================================================
   Task: HTML (Pug → HTML)
   - Compila templates Pug
   - Passa variáveis globais
============================================================ */
function html() {
  return gulp.src(paths.pug)
    .pipe(pug({
      pretty: isDev,   // HTML legível em dev
      locals: {
        env,
        title: 'SK',
        description: 'A starter kit for web development projects, fwith features like Sass, Pug, Browserify, and BrowserSync, among others!',
        name: '',
        themes: ['light', 'dark', 'solarized', 'dracula', 'hydra', 'neon'],
        tags: ['starter-kit', 'template', 'html', 'web development', 'pug', 'sass', 'gulp', 'browserify', 'browser-sync '],
        theme: null,
        currentPage: 'home',
        siteName: 'SK',
        pageTitle: '',
      }
    }))
    .pipe(gulp.dest(outputDir))
    .on('end', browserSync.reload);
}

/* ============================================================
   Task: Imagens (cópia segura)
   ------------------------------------------------------------
   NOTA:
   - O imagemin foi removido porque estava a corromper JPGs.
   - Esta versão copia as imagens tal como estão.
   - No futuro podes adicionar WebP/AVIF.
============================================================ */
/* ============================================================
   Task: Imagens (cópia binária 100% segura)
   ------------------------------------------------------------
   - Evita corrupção de JPG/PNG no Windows
   - Não usa streams do Gulp (que convertem CRLF)
   - Copia byte‑a‑byte com Node.js puro
============================================================ */
const fs = require('fs');
const path = require('path');

function images(cb) {
  const srcDir = 'assets/img';
  const destDir = outputDir + 'img';

  // Garante que a pasta existe
  fs.mkdirSync(destDir, { recursive: true });

  function copyRecursive(src, dest) {
    fs.readdirSync(src, { withFileTypes: true }).forEach(entry => {
      const srcPath = path.join(src, entry.name);
      const destPath = path.join(dest, entry.name);

      if (entry.isDirectory()) {
        fs.mkdirSync(destPath, { recursive: true });
        copyRecursive(srcPath, destPath);
      } else {
        fs.copyFileSync(srcPath, destPath);
      }
    });
  }

  copyRecursive(srcDir, destDir);
  cb();
}


/* ============================================================
   Task: Servidor + Watch (BrowserSync)
============================================================ */
function serve() {
  browserSync.init({
    server: { baseDir: outputDir }
  });

  gulp.watch(paths.sass, css);
  gulp.watch(paths.js, bundleJS);
  gulp.watch('assets/pug/**/*.pug', html);
  gulp.watch(paths.img, images);
}

/* ============================================================
   Task: Clean (compatível com CJS + Node 22)
============================================================ */
const del = require('delete');

function clean(cb) {
  del([outputDir + '**'], cb);
}





/* ============================================================
   Tarefas públicas
============================================================ */
exports.css = css;
exports.js = bundleJS;
exports.html = html;
exports.images = images;
exports.serve = serve;
exports.clean = clean;
/* ============================================================
   Default (modo desenvolvimento)
============================================================ */
exports.default = gulp.series(
  clean,
  gulp.parallel(css, bundleJS, html, images),
  serve
);


/* ============================================================
   Build (produção, staging, deployment)
============================================================ */
exports.build = gulp.series(
  clean,
  gulp.parallel(css, bundleJS, html, images, serve)
);

/* ============================================================
   COMO USAR ESTE GULPFILE — Starter Kit 2026
   ------------------------------------------------------------
   Guia rápido para desenvolvimento, builds e ambientes.
============================================================ */

/*

============================================================
MODO GLOBAL (Ambientes)
------------------------------------------------------------
Define o ambiente ANTES de correr o gulp.
Se não definires nada, o ambiente padrão é: development.

Exemplos:

NODE_ENV=development gulp
NODE_ENV=production  gulp
NODE_ENV=staging     gulp
NODE_ENV=deployment  gulp

Cada ambiente compila para:
- development → ./dev/
- production  → ./dist/
- staging     → ./staging/
- deployment  → ./build/

------------------------------------------------------------
NOTA:
Em Windows PowerShell:
   $env:NODE_ENV="production"; gulp build

Em Windows CMD:
   set NODE_ENV=production && gulp build

Em macOS/Linux:
   NODE_ENV=production gulp build
============================================================



============================================================
MODO INICIANTE
------------------------------------------------------------
1. Corre simplesmente:
   gulp

Isto:
- inicia o servidor BrowserSync
- compila SCSS, JS, Pug e Imagens
- serve tudo a partir de ./dev/

2. Edita SCSS, JS ou Pug
   O BrowserSync atualiza automaticamente.
============================================================



============================================================
MODO INTERMÉDIO
------------------------------------------------------------
Para iniciar apenas o servidor:
   gulp serve

Para compilar tudo sem servidor:
   gulp build
============================================================



============================================================
MODO AVANÇADO (Ambientes)
------------------------------------------------------------
Define o ambiente e depois corre o build:

Exemplos:

• Development (padrão)
   gulp build

• Production
   NODE_ENV=production gulp build

• Staging
   NODE_ENV=staging gulp build

• Deployment
   NODE_ENV=deployment gulp build
============================================================



============================================================
TASK CLEAN (Opcional)
------------------------------------------------------------
Se quiseres builds 100% limpos:

1. Descomenta no topo:
   const del = require('del');

2. Descomenta a função clean()

3. No build:
   exports.build = gulp.series(clean, gulp.parallel(...))

Isto apaga a pasta de output antes de compilar.
============================================================



============================================================
NOTAS TÉCNICAS (úteis para futuro Jekyll, React, TS, etc.)
------------------------------------------------------------

• As tasks CSS e JS geram sourcemaps em TODOS os ambientes.
  Isto facilita debugging em:
    - Jekyll
    - React
    - TypeScript
    - Webpack/Vite no futuro

• O Pug recebe variáveis globais:
    env, title, description, themes, tags, theme, currentPage, etc.
  Isto permite:
    - integração com front‑matter (Jekyll)
    - integração com React/TS (via props)
    - troca dinâmica de temas no Hydra‑Origin‑Theme

• O BrowserSync serve SEMPRE a pasta correta:
    dev/     → development
    dist/    → production
    staging/ → staging
    build/   → deployment

• A task bundleJS usa Browserify.
  No futuro podes trocar facilmente para:
    - Rollup
    - ESBuild
    - Vite
    - Webpack
  sem alterar a arquitetura do Starter Kit.

• Sobre temas:
    Se adicionares mais temas em _themes.scss,
    adiciona-os também ao array "themes" no Pug.
    O tema padrão pode ser definido por página
    ou via lógica JS (theme.js).
============================================================



============================================================
FIM DO GULPFILE STARTER EDITION — 2026
============================================================

*/
