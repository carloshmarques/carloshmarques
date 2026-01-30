'use strict';

/* ============================================================
   Starter Kit — Gulpfile (2026)
   ------------------------------------------------------------
   Simples, modular e compatível com:
   - Sass
   - Pug
   - Browserify + Babelify (ES Modules)
   - BrowserSync
============================================================ */

const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const terser = require('gulp-terser');
const pug = require('gulp-pug');
const imagemin = require('gulp-imagemin');
const sourcemaps = require('gulp-sourcemaps');
const rename = require('gulp-rename');
const browserSync = require('browser-sync').create();

const browserify = require('browserify');
const source = require('vinyl-source-stream');
const buffer = require('vinyl-buffer');


/* ============================================================
   Ambiente
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
   Caminhos
============================================================ */
const paths = {
  sass: 'assets/sass/**/*.scss',
  js:   'assets/js/**/*.js',
  img:  'assets/img/**/*',
  pug:  'assets/pug/templates/pages/*.pug'
};

/* ============================================================
   Task: CSS (Sass → CSS)
============================================================ */
function css() {
  return gulp.src(paths.sass)
    .pipe(sourcemaps.init())
    .pipe(sass({ outputStyle: isDev ? 'expanded' : 'compressed' })
      .on('error', sass.logError))
    .pipe(postcss(isDev ? [autoprefixer()] : [autoprefixer(), cssnano()]))
    .pipe(rename({ suffix: isDev ? '' : '.min' }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(outputDir + 'css'))
    .pipe(browserSync.stream());
}

/* ============================================================
   Task: JS (Browserify Bundle)
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
============================================================ */
function html() {
  return gulp.src(paths.pug)
    .pipe(pug({
      pretty: isDev,
      locals: {
        env,
        title: 'CM',
        description: 'A portfolio template available on GitHub.',

        name: '',

        themes: ['light', 'dark', 'solarized', 'dracula', 'hydra', 'neon'],
        tags: ['portfolio', 'template', 'github', 'web development'],

        theme: '',
        currentPage: 'home', // ou 'admin', etc.

        siteName: 'CM',
        pageTitle: '',
      }
    }))
    .pipe(gulp.dest(outputDir))
    .on('end', browserSync.reload);
}

/* ============================================================
   Task: Imagens
============================================================ */
function images() {
  return gulp.src(paths.img)
    .pipe(imagemin())
    .pipe(gulp.dest(outputDir + 'img'));
}

/* ============================================================
   Task: Servidor + Watch
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
   (Opcional) Task: Clean
   Apaga a pasta de output antes de um build.
   Ativar se quiseres builds 100% limpos.
============================================================ */
/*
function clean() {
  return del([outputDir + '**', '!' + outputDir]);
}
exports.clean = clean;
*/

/* ============================================================
   Tarefas públicas
============================================================ */
exports.css = css;
exports.js = bundleJS;
exports.html = html;
exports.images = images;
exports.serve = serve;

/* ============================================================
   Default (modo desenvolvimento)
============================================================ */
exports.default = gulp.series(
  gulp.parallel(css, bundleJS, html, images),
  serve
);

/* ============================================================
   Build (produção, staging, deployment)
============================================================ */
exports.build = gulp.series(
  // clean,   // ativa se quiseres limpeza automática
  gulp.parallel(css, bundleJS, html, images)
);

/* ============================================================
   COMO USAR ESTE GULPFILE
============================================================ */

/*

============================================================
MODO Global (Ambientes)
------------------------------------------------------------
Definir ambiente antes de correr o gulp:
Padrão: development
/* correr gulp em development globalmente interpretado em distros que suportam Node.js 

Node_ENV=development gulp
NODE_ENV=production gulp
NODE_ENV=staging gulp
NODE_ENV=deployment gulp

============================================================
MODO INICIANTE
------------------------------------------------------------
1. Corre simplesmente:
   gulp
   Isto inicia o servidor e compila tudo para ./dev/

2. Edita SCSS, JS ou Pug — o BrowserSync atualiza automaticamente.

============================================================
MODO INTERMÉDIO
------------------------------------------------------------
1. Para iniciar o servidor:
   gulp serve

2. Para compilar tudo sem servidor:
   gulp build

============================================================
MODO AVANÇADO (Ambientes)
------------------------------------------------------------
Definir ambiente antes de correr o gulp:
Windows (PowerShell):
   $env:NODE_ENV="development"; gulp build  

NODE_ENV=development

Windows (cmd):
   set NODE_ENV=production && gulp build

macOS/Linux:
   NODE_ENV=production gulp build

Ambientes disponíveis:
- development (padrão)
- production
- staging
- deployment

Cada ambiente compila para:
- ./dev/
- ./dist/
- ./staging/
- ./build/

============================================================
TASK CLEAN (Opcional)
------------------------------------------------------------
Ativa a task clean() no topo e no build:

1. Descomenta:
   const del = require('del');

2. Descomenta a função clean()

3. No build:
   exports.build = gulp.series(clean, gulp.parallel(...))

Isto garante builds 100% limpos.

/* ============================================================
   NOTAS TÉCNICAS (úteis para futuro Jekyll, React, TS, etc.)
============================================================ */

/*
- As tasks CSS e JS geram sourcemaps em todos os ambientes
  para facilitar debugging, inclusive quando integrados com
  Jekyll, React ou TypeScript no futuro.

- O Pug recebe:
    env: ambiente atual (dev, prod, staging, deployment)
    title: título padrão
    description: descrição padrão
    themes: lista de temas disponíveis
    theme: tema ativo (pode ser sobrescrito por página)

  Isto permite:
    • integração futura com Jekyll (via front‑matter)
    • integração com React/TS (via props ou context)
    • troca dinâmica de temas no Hydra‑Origin‑Theme

- O BrowserSync serve SEMPRE a pasta correta com base no ambiente:
    dev/        → development
    dist/       → production
    staging/    → staging
    build/      → deployment

  Isto garante compatibilidade com:
    • Jekyll (que compila para _site/)
    • React (que compila para build/)
    • HydraLife (que terá build próprio)

- A task de limpeza (clean) é opcional.
  Ativa‑a quando quiseres builds 100% limpos ou integração com CI/CD.

- A task bundleJS usa Browserify para agrupar módulos JS localmente.
  No futuro podes trocar facilmente para:
    • Rollup
    • ESBuild
    • Vite
    • Webpack
  sem alterar a estrutura do starter‑kit.

- Sobre temas:
    Se adicionares mais temas em _themes.scss,
    basta adicioná‑los ao array "themes" no Pug.
    O tema padrão pode ser definido em cada página
    ou via lógica JS (theme.js).



============================================================
FIM DO GULPFILE STARTER EDITION
============================================================
*/
