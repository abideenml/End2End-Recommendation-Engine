'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

var createEmotionServer = require('@emotion/server/create-instance');
var styles = require('@mantine/styles');

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e['default'] : e; }

var createEmotionServer__default = /*#__PURE__*/_interopDefaultLegacy(createEmotionServer);

function createStylesServer(options) {
  return createEmotionServer__default(styles.getCache(options));
}

exports.createStylesServer = createStylesServer;
//# sourceMappingURL=create-styles-server.js.map
