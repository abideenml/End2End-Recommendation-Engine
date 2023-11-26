import { getRandom, getRangeValue } from "tsparticles-engine";
import { Wobble } from "./Options/Classes/Wobble";
function updateWobble(particle, delta) {
    var _a;
    const wobble = particle.options.wobble;
    if (!(wobble === null || wobble === void 0 ? void 0 : wobble.enable) || !particle.wobble) {
        return;
    }
    const angleSpeed = particle.wobble.angleSpeed * delta.factor, moveSpeed = particle.wobble.moveSpeed * delta.factor, distance = (moveSpeed * (((_a = particle.retina.wobbleDistance) !== null && _a !== void 0 ? _a : 0) * delta.factor)) / (1000 / 60), max = 2 * Math.PI;
    particle.wobble.angle += angleSpeed;
    if (particle.wobble.angle > max) {
        particle.wobble.angle -= max;
    }
    particle.position.x += distance * Math.cos(particle.wobble.angle);
    particle.position.y += distance * Math.abs(Math.sin(particle.wobble.angle));
}
export class WobbleUpdater {
    constructor(container) {
        this.container = container;
    }
    init(particle) {
        var _a;
        const wobbleOpt = particle.options.wobble;
        if (wobbleOpt === null || wobbleOpt === void 0 ? void 0 : wobbleOpt.enable) {
            particle.wobble = {
                angle: getRandom() * Math.PI * 2,
                angleSpeed: getRangeValue(wobbleOpt.speed.angle) / 360,
                moveSpeed: getRangeValue(wobbleOpt.speed.move) / 10,
            };
        }
        else {
            particle.wobble = {
                angle: 0,
                angleSpeed: 0,
                moveSpeed: 0,
            };
        }
        particle.retina.wobbleDistance = getRangeValue((_a = wobbleOpt === null || wobbleOpt === void 0 ? void 0 : wobbleOpt.distance) !== null && _a !== void 0 ? _a : 0) * this.container.retina.pixelRatio;
    }
    isEnabled(particle) {
        var _a;
        return !particle.destroyed && !particle.spawning && !!((_a = particle.options.wobble) === null || _a === void 0 ? void 0 : _a.enable);
    }
    loadOptions(options, ...sources) {
        if (!options.wobble) {
            options.wobble = new Wobble();
        }
        for (const source of sources) {
            options.wobble.load(source === null || source === void 0 ? void 0 : source.wobble);
        }
    }
    update(particle, delta) {
        if (!this.isEnabled(particle)) {
            return;
        }
        updateWobble(particle, delta);
    }
}
