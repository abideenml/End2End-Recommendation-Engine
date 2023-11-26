import { TwinkleUpdater } from "./TwinkleUpdater";
export async function loadTwinkleUpdater(engine) {
    await engine.addParticleUpdater("twinkle", () => new TwinkleUpdater());
}
