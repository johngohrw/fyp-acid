# fe-dev: Front-end Development Environment
[Live Prototype Website](https://johngohrw.github.io/fyp-acid/) (requires web-server running on background)

## About this environment
This folder consists of the developmental source files for FYP-ACID's (Automatic compound Image Detection) front-end client website. The website is developed using the Node.js engine and npm as the package manager and script runner. This website is coded heavily with the React.js framework, with a mixture of vanilla JavaScript. Stylesheets are manually written, but made easy with the help of CSS preprocessor engines such as SCSS. The uploading process is achieved via RESTful communication methods between the web-client and the back-end server.

The source files can be located in the `/src` folder. It contains all the individual React.js pages and components used in this website. The web-application is already deployed on github pages and can already be accessed via [this link](https://johngohrw.github.io/fyp-acid/).

## Compilation instructions
If you would like to compile the front-end client on your own and tweak around with the website's development, an installation of [node.js](https://nodejs.org/en/) is required. 

Install all neccesary dependencies:
```
npm install
```
Run the Stylesheets watcher/compiler instance:
```
npm run node-sass
```

With another terminal instance, start the hot-reloading development server
```
npm run start
```

The development server will automatically launch a browser instance with the live hot-reloading website.