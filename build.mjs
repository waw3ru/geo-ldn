import esbuild from 'esbuild';
import { sassPlugin } from 'esbuild-sass-plugin';
import postcss from 'postcss';
import autoprefixer from 'autoprefixer';

const isProd = process.env.NODE_ENV === 'production';

// Generate CSS/JS Builds
const ctx = await esbuild.context({
    entryPoints: [
        { in: 'scss/style.scss', out: 'zsk/css/style' },
        { in: 'ts/index.ts', out: 'zsk/js/index' },
    ],
    outdir: 'dist',
    bundle: true,
    metafile: true,
    minify: isProd,
    target: isProd ? 'es2019' : 'esnext',
    logLevel: isProd ? 'warning' : 'debug',
    plugins: [
        sassPlugin({
            sourceMap: isProd,
            async transform(source) {
                const { css } = await postcss([autoprefixer]).process(source, {
                    from: undefined,
                    isProd,
                });
                return css;
            },
        }),
    ],
});

if (isProd) {
    await ctx.rebuild();
    console.log('🚬 Finished building...');
    ctx.dispose();
} else {
    console.log('🤖 Watching static files...');
    await ctx.watch();
}
