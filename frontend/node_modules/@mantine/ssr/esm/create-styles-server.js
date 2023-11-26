import createEmotionServer from '@emotion/server/create-instance';
import { getCache } from '@mantine/styles';

function createStylesServer(options) {
  return createEmotionServer(getCache(options));
}

export { createStylesServer };
//# sourceMappingURL=create-styles-server.js.map
