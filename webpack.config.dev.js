const path = require('path');

module.exports = {
    // generate source map
    devtool: 'source-map',

    // bundling mode
    mode: 'development',

    // entry files
    entry: {
        'activities': path.resolve(__dirname, 'app', 'static', 'ts', 'activities.ts'),
        'countdown-results-service': path.resolve(__dirname, 'app', 'static', 'ts', 'countdown-results-service.ts'),
        'update-password': path.resolve(__dirname, 'app', 'static', 'ts', 'update-password.ts'),
        'register': path.resolve(__dirname, 'app', 'static', 'ts', 'register.ts'),
        'account': path.resolve(__dirname, 'app', 'static', 'ts', 'account.ts'),
        'password-reset': path.resolve(__dirname, 'app', 'static', 'ts', 'password-reset.ts'),
        'sign-in': path.resolve(__dirname, 'app', 'static', 'ts', 'sign-in.ts'),
        'contact-us': path.resolve(__dirname, 'app', 'static', 'ts', 'contact-us.ts'),
        'main': path.resolve(__dirname, 'app', 'static', 'ts', 'main.ts'),
        'models': path.resolve(__dirname, 'app', 'static', 'ts', 'models.ts'),
        'tools': path.resolve(__dirname, 'app', 'static', 'ts', 'tools.ts'),
    },

    // output bundles (location)
    output: {
        //path: './app/static/js',
        path: path.resolve(__dirname, 'app', 'static', 'js'),
        filename: '[name].js',
    },

    // file resolutions
    resolve: {
        extensions: ['.ts', '.js'],
    },

    // loaders
    module: {
        rules: [
            {
                test: /\.tsx?/,
                use: [
                    {
                        loader: "ts-loader",
                        options: {
                            transpileOnly: true
                        }
                    }
                ],
                exclude: /node_modules/,
            },
            {
                test: /\.(css)$/,
                use: ['style-loader', 'css-loader'],
            },
        ]
    }
};