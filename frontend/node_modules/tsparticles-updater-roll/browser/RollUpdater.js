import { getRandom, getRangeValue, rangeColorToHsl } from "tsparticles-engine";
import { Roll } from "./Options/Classes/Roll";
function updateRoll(particle, delta) {
    const roll = particle.options.roll;
    if (!particle.roll || !(roll === null || roll === void 0 ? void 0 : roll.enable)) {
        return;
    }
    const speed = particle.roll.speed * delta.factor, max = 2 * Math.PI;
    particle.roll.angle += speed;
    if (particle.roll.angle > max) {
        particle.roll.angle -= max;
    }
}
export class RollUpdater {
    getTransformValues(particle) {
        var _a;
        const roll = ((_a = particle.roll) === null || _a === void 0 ? void 0 : _a.enable) && particle.roll, rollHorizontal = roll && roll.horizontal, rollVertical = roll && roll.vertical;
        return {
            a: rollHorizontal ? Math.cos(roll.angle) : undefined,
            d: rollVertical ? Math.sin(roll.angle) : undefined,
        };
    }
    init(particle) {
        const rollOpt = particle.options.roll;
        if (rollOpt === null || rollOpt === void 0 ? void 0 : rollOpt.enable) {
            particle.roll = {
                enable: rollOpt.enable,
                horizontal: rollOpt.mode === "horizontal" || rollOpt.mode === "both",
                vertical: rollOpt.mode === "vertical" || rollOpt.mode === "both",
                angle: getRandom() * Math.PI * 2,
                speed: getRangeValue(rollOpt.speed) / 360,
            };
            if (rollOpt.backColor) {
                particle.backColor = rangeColorToHsl(rollOpt.backColor);
            }
            else if (rollOpt.darken.enable && rollOpt.enlighten.enable) {
                const alterType = getRandom() >= 0.5 ? "darken" : "enlighten";
                particle.roll.alter = {
                    type: alterType,
                    value: getRangeValue(alterType === "darken" ? rollOpt.darken.value : rollOpt.enlighten.value),
                };
            }
            else if (rollOpt.darken.enable) {
                particle.roll.alter = {
                    type: "darken",
                    value: getRangeValue(rollOpt.darken.value),
                };
            }
            else if (rollOpt.enlighten.enable) {
                particle.roll.alter = {
                    type: "enlighten",
                    value: getRangeValue(rollOpt.enlighten.value),
                };
            }
        }
        else {
            particle.roll = {
                enable: false,
                horizontal: false,
                vertical: false,
                angle: 0,
                speed: 0,
            };
        }
    }
    isEnabled(particle) {
        const roll = particle.options.roll;
        return !particle.destroyed && !particle.spawning && !!(roll === null || roll === void 0 ? void 0 : roll.enable);
    }
    loadOptions(options, ...sources) {
        if (!options.roll) {
            options.roll = new Roll();
        }
        for (const source of sources) {
            options.roll.load(source === null || source === void 0 ? void 0 : source.roll);
        }
    }
    update(particle, delta) {
        if (!this.isEnabled(particle)) {
            return;
        }
        updateRoll(particle, delta);
    }
}
