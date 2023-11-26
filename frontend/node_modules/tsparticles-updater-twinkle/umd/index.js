(function (factory) {
    if (typeof module === "object" && typeof module.exports === "object") {
        var v = factory(require, exports);
        if (v !== undefined) module.exports = v;
    }
    else if (typeof define === "function" && define.amd) {
        define(["require", "exports", "./TwinkleUpdater"], factory);
    }
})(function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.loadTwinkleUpdater = void 0;
    const TwinkleUpdater_1 = require("./TwinkleUpdater");
    async function loadTwinkleUpdater(engine) {
        await engine.addParticleUpdater("twinkle", () => new TwinkleUpdater_1.TwinkleUpdater());
    }
    exports.loadTwinkleUpdater = loadTwinkleUpdater;
});
