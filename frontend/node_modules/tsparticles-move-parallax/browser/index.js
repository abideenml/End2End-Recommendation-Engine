import { ParallaxMover } from "./ParallaxMover";
export async function loadParallaxMover(engine) {
    engine.addMover("parallax", () => new ParallaxMover());
}
