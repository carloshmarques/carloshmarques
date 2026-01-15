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

const env = process.env.NODE_ENV || 'development';

let outputDir = env === 'production' ? './build/' : './dist/';
let sassStyle = env === 'production' ? 'compressed' : 'expanded';

const paths = {
    sass: 'assets/scss/**/*.scss',
    js: 'assets/js/**/*.js',
    img: 'assets/img/**/*',
    pug: 'assets/pug/**/*.pug'
};

// Compilar Sass
function css() {
    return gulp.src(paths.scss)
        .pipe(sourcemaps.init())
        .pipe(sass({ outputStyle: sassStyle }).on('error', sass.logError))
        .pipe(postcss([autoprefixer(), cssnano()]))
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(outputDir + 'css'))
        .pipe(browserSync.stream());
}

// Minificar JS
function js() {
    return gulp.src(paths.js)
        .pipe(sourcemaps.init())
        .pipe(terser())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
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

    gulp.watch(paths.sss, css);
    gulp.watch(paths.js, js);
    gulp.watch(paths.pug, html);
    gulp.watch(paths.img, images);
}

exports.css = css;
exports.js = js;
exports.html = html;
exports.images = images;
exports.serve = serve;
exports.default = gulp.series(css, js, html, images, serve);


