'use strict';
/**
 * Gulp Workflow
 * 
 * Este Gulpfile compila Sass de assets/sass para dist/css.
 * Usa 'compressed' em produção e 'expanded' em desenvolvimento.
 * 
 * Para adaptar ao teu workspace, ajusta os caminhos em 'paths'.
 * Para usar outro estilo, edita 'sassStyle' conforme o ambiente.
 * 
 * Legado cerimonial por Carlos Marques.
 */

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


const env = process.env.NODE_ENV || 'development';

let outputDir;
let sassStyle;

if (env === 'production') {
    outputDir = './dist/';
    sassStyle = 'compressed';
} else if (env === 'development'){
    outputDir = './dev/';
    sassStyle = 'expanded';
} else if (env === 'deployment'){
    outputDir = './build/';
    sassStyle = 'compressed';
}else if (env === 'staging'){
    outputDir = './staging/';
    sassStyle = 'compressed';
}else if (env !== 'production' && env !== 'development' && env !== 'deployment' && env !== 'staging'){
    throw new Error("NODE_ENV must be 'production', 'development', or 'deployment'");
}

const paths = {
    sass: 'assets/sass/**/*.scss',
    js: 'assets/js/**/*.js',
    img: 'assets/img/**/*',
    pug: 'assets/pug/templates/pages/*.pug',
};


// Compilar Sass
function css() {
    return gulp.src(paths.sass)
        .pipe(sourcemaps.init())
        .pipe(sass({ outputStyle: sassStyle }).on('error', sass.logError))
        .pipe(postcss([autoprefixer(), cssnano()]))
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(outputDir + 'css'))
        .pipe(browserSync.stream());
}

// Minificar JS
function bundleJS() { 
    return browserify('assets/js/main.js') 
    .bundle() 
    .pipe(source('main.min.js')) 
    .pipe(buffer()) 
    .pipe(env === 'production' ? terser() : rename({})) 
    .pipe(gulp.dest(outputDir + 'js')) 
    .pipe(browserSync.stream()); 
}


// Pug → HTML
function html() {
    return gulp.src(paths.pug)
        .pipe(pug({ pretty: env !== 'production' }))
        .pipe(gulp.dest(outputDir))
        .pipe(browserSync.stream());
}

// Imagens
function images() {
    return gulp.src(paths.img)
        .pipe(imagemin())
        .pipe(gulp.dest(outputDir + 'img'));
}

// Servidor + Watch
function serve() {
    browserSync.init({
        server: { baseDir: outputDir }
    });

    gulp.watch(paths.sass, css);
    gulp.watch(paths.js, bundleJS);
    gulp.watch(paths.pug, html);
    gulp.watch(paths.img, images);
}

exports.css = css;
exports.bundleJS = bundleJS;
exports.html = html;
exports.images = images;
exports.serve = serve;
// Default (modo recomendado)
exports.default = gulp.series(css, bundleJS, html, images, serve);


// Task para construir tudo sem servidor (útil para CI/CD ou iniciantes)
gulp.task('build', gulp.series(css, bundleJS, html, images));

// Task para desenvolvimento com servidor (igual ao default)
gulp.task('start', gulp.series(css,bundleJS, html, images, serve));

/**
 * COMO USAR AS TASKS DO GULP (iniciantes)
 * ------------------------------------------------------------
 * Basta correr:
 *     gulp
 * 
 * O Gulp compila tudo, inicia o servidor e observa alterações.
 * 
 * Alternativas:
 *     gulp start   → igual ao default
 *     gulp build   → compila tudo sem servidor
 *
 * ============================================================
 * COMO USAR AS TASKS DO GULP PARA O SEU PROJECTO (avançado)
 * ------------------------------------------------------------
 * ➤ Executar todas as tasks + servidor (modo padrão)
 *     gulp
 *   - Compila Sass
 *   - Minifica JS
 *   - Converte Pug → HTML
 *   - Optimiza imagens
 *   - Inicia BrowserSync
 *   - Observa alterações em tempo real
 * 
 * ------------------------------------------------------------
 * ➤ Executar tasks individuais
 * 
 *   gulp css
 *     - Compila Sass → CSS
 *     - Aplica Autoprefixer + CSSNano
 *     - Gera sourcemaps
 *     - Cria ficheiro .min.css
 * 
 *   gulp js
 *     - Minifica JavaScript (apenas em produção)
 *     - Gera sourcemaps
 *     - Cria ficheiro .min.js
 * 
 *   gulp html
 *     - Converte ficheiros Pug → HTML
 *     - Em produção: HTML comprimido
 *     - Em desenvolvimento: HTML legível
 * 
 *   gulp images
 *     - Optimiza imagens (PNG, JPG, SVG, etc.)
 * 
 *   gulp serve
 *     - Inicia servidor local com BrowserSync
 *     - Observa alterações e recarrega automaticamente
 * 
 * ------------------------------------------------------------
 * ➤ Usar ambientes (NODE_ENV)
 * 
 *   Desenvolvimento (padrão):
 *       NODE_ENV=development gulp
 *       - Output: ./dev/
 *       - Sass expandido
 *       - HTML bonito
 * 
 *   Produção:
 *       NODE_ENV=production gulp
 *       - Output: ./dist/
 *       - Sass comprimido
 *       - JS minificado
 *       - HTML comprimido
 * 
 *   Deployment:
 *       NODE_ENV=deployment gulp
 *       - Output: ./build/
 *       - Igual a produção, mas para deploy manual
 * 
 *   Staging:
 *       NODE_ENV=staging gulp
 *       - Output: ./staging/
 *       - Ambiente intermédio para testes finais
 * 
 * ============================================================
 * O QUE É "STAGING"?
 * ------------------------------------------------------------
 *   É um ambiente intermédio entre desenvolvimento e produção.
 *   Serve para testar tudo como se fosse produção, mas sem
 *   publicar ainda para o público.
 * 
 *   Exemplos:
 *     - Testar o site num servidor privado
 *     - Validar performance antes do deploy
 *     - Verificar se tudo funciona com minificação ativa
 * 
 *   Não precisas disto agora — mas já deixei preparado para
 *   quando o teu workflow crescer.
 * 
 * ============================================================
 * Legado cerimonial por Carlos Marques.
 * ============================================================
 /*======================================================*/