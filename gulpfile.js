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

// msg de ambiente
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
        .pipe(source(env === 'production' ? 'main.min.js' : 'main.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({ loadMaps: true }))
        .pipe(env === 'production' ? terser() : rename({}))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(outputDir + 'js'))
        .pipe(browserSync.stream()); // Injecta o JS novo
}

// Pug → HTML


function html() {
    return gulp.src(paths.pug)
        .pipe(pug({
            pretty: env !== 'production', // Identação amigável em dev
            locals: { 
                env: env, 
                title: 'Github Portfolio',
                description: 'A portfolio template available on GitHub.',
                themes: ['light', 'dark', 'solarized', 'dracula', 'hydra', 'neon'] ,
                theme: '', // default theme empty for user selection
            }
        }))
        .pipe(gulp.dest(outputDir))
        .on('end', browserSync.reload);
}


// Imagens
function images() {
    return gulp.src(paths.img)
        .pipe(imagemin())
        .pipe(gulp.dest(outputDir + 'img'));
}


// wath task + server

// Função para observar ficheiros (Watch)
function watchFiles() {
    // Observa SASS: se mudar, corre a task css
    // O browserSync.stream() dentro da task css já trata do refresh do CSS sem reload total
    gulp.watch(paths.sass, css);

    // Observa JS: se mudar, corre bundleJS e depois faz reload
    gulp.watch(paths.js, bundleJS);

    // Observa PUG: Se QUALQUER ficheiro .pug na pasta assets mudar (incluindo layouts/includes), 
    // corre a task html que processa apenas as páginas principais
    gulp.watch('assets/pug/**/*.pug', html);

    // Observa Imagens
    gulp.watch(paths.img, images);

    // Opcional: Se quiseres que o browser faça reload manual quando o HTML final for gerado
    // Nota: Adicionei o pipe(browserSync.stream()) ou .on('end', browserSync.reload) nas tasks abaixo
}
// Servidor + Watch
function serve() { 

    browserSync.init({ 
        server: { 
            baseDir: outputDir }    
    });
    watchFiles(); // <-- chama aqui }

   
}

// Default Task
exports.default = gulp.series(
    gulp.parallel(css, bundleJS, html, images, 
    serve)
);

// Build
gulp.task('build', gulp.series(css, bundleJS, html, images));
