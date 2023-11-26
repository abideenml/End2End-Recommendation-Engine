'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

var createStylesServer = require('./create-styles-server.js');
var getSsrStyles = require('./get-ssr-styles.js');

const server = createStylesServer.createStylesServer();
function injectStylesIntoStaticMarkup(markup) {
  return markup.replace("<head>", `<head>${getSsrStyles.getSSRStyles(markup, server)}`);
}

exports.injectStylesIntoStaticMarkup = injectStylesIntoStaticMarkup;
//# sourceMappingURL=inject-styles-into-static-markup.js.map
