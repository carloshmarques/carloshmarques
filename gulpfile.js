'use strict';

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
const cached = require('gulp-cached');

// Ambiente
const env = process.env.NODE_ENV || 'development';
const isDev = env === 'development';
console.log(`Running in ${env} mode`);
// Pastas de input
let inputDir = './assets/';
// Pastas de saída
let outputDir;
if (env === 'production') outputDir = './dist/';
else if (env === 'staging') outputDir = './staging/';
else if (env === 'deployment') outputDir = './build/';
else outputDir = './dev/';

// Caminhos
const paths = {
    sass: 'assets/sass/**/*.scss',
    js: 'assets/js/**/*.js',
    img: 'assets/img/**/*',
    pug: 'assets/pug/templates/pages/*.pug'
};

// Compilar Sass
function css() {
    return gulp.src(paths.sass)
        .pipe(sourcemaps.init())
        .pipe(sass({ outputStyle: isDev ? 'expanded' : 'compressed' }).on('error', sass.logError))
        .pipe(postcss(isDev ? [autoprefixer()] : [autoprefixer(), cssnano()]))
        .pipe(rename({ suffix: isDev ? '' : '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(outputDir + 'css'))
        .pipe(browserSync.stream());
}

// Bundle JS
function bundleJS() { 
    return browserify('assets/js/main.js')
        .bundle()
        .on('error', function(err) { console.error(err.message); this.emit('end'); })
        .pipe(source('main.min.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(env === 'production' ? terser() : rename({}))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(outputDir + 'js'))
        .pipe(browserSync.stream());
}

// Pug → HTML
function html() {
    return gulp.src(paths.pug)
        .pipe(cached('pug'))
        .pipe(pug({
            pretty: env !== 'production',
            locals: { env, title: 'Github Portfolio' }
        }))
        .pipe(gulp.dest(outputDir))
        .on('change', browserSync.reload);
}

// Imagens
function images() {
    return gulp.src(paths.img)
        .pipe(imagemin())
        .pipe(gulp.dest(outputDir + 'img'));
}


// wath task + server

function watchFiles() {
    gulp.watch(paths.sass, gulp.series(css, browserSync.reload));
    gulp.watch(paths.js, gulp.series(bundleJS, browserSync.reload));
    gulp.watch('assets/pug/**/*.pug', gulp.series(html, browserSync.reload));

    gulp.watch(outputDir + '*.html').on('change', browserSync.reload);
   

}
// Servidor + Watch
function serve() { 

    browserSync.init
    ({ 
        server: { baseDir: outputDir }    
    });
    watchFiles(); // <-- chama aqui }

   
}

// Default
exports.default = gulp.series(css, bundleJS, html, images, serve);

// Build
gulp.task('build', gulp.series(css, bundleJS, html, images));
