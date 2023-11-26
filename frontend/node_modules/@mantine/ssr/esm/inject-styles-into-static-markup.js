import { createStylesServer } from './create-styles-server.js';
import { getSSRStyles } from './get-ssr-styles.js';

const server = createStylesServer();
function injectStylesIntoStaticMarkup(markup) {
  return markup.replace("<head>", `<head>${getSSRStyles(markup, server)}`);
}

export { injectStylesIntoStaticMarkup };
//# sourceMappingURL=inject-styles-into-static-markup.js.map
