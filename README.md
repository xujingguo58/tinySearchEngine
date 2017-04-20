# search-engine

> a tiny search engine based on vue.js and use scrapy,jieba,php to accomplish it

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```
```
.
├── back_end.php
├── build
│   ├── build.js
│   ├── check-versions.js
│   ├── dev-client.js
│   ├── dev-server.js
│   ├── utils.js
│   ├── vue-loader.conf.js
│   ├── webpack.base.conf.js
│   ├── webpack.dev.conf.js
│   ├── webpack.prod.conf.js
│   └── webpack.test.conf.js
├── config
│   ├── dev.env.js
│   ├── index.js
│   ├── prod.env.js
│   └── test.env.js
├── dist
│   ├── index.html
│   └── static
│       ├── css
│       │   ├── app.bc6bcebd8dff1469ed2a180d243d1fb1.css
│       │   └── app.bc6bcebd8dff1469ed2a180d243d1fb1.css.map
│       └── js
│           ├── app.2e2f3fd3b6a1a7409115.js
│           ├── app.2e2f3fd3b6a1a7409115.js.map
│           ├── manifest.42e3257fe0dc6f03a838.js
│           ├── manifest.42e3257fe0dc6f03a838.js.map
│           ├── vendor.080f64fd4ca0f1bcf027.js
│           └── vendor.080f64fd4ca0f1bcf027.js.map
├── DomzSpider.py
├── index.html
├── node_modulels
├── package.json
├── README.md
├── src
│   ├── App.vue
│   ├── assets
│   │   └── logo.png
│   ├── components
│   │   ├── searchEngine.vue
│   │   └── searchResult.vue
│   ├── main.js
│   └── router
│       └── index.js
├── static
├── test
│   ├── e2e
│   │   ├── custom-assertions
│   │   │   └── elementCount.js
│   │   ├── nightwatch.conf.js
│   │   ├── runner.js
│   │   └── specs
│   │       └── test.js
│   └── unit
│       ├── index.js
│       ├── karma.conf.js
│       └── specs
│           └── Hello.spec.js
├── tree.txt
└── urlToKeywords.py

```

For detailed explanation on how things work, checkout the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).
