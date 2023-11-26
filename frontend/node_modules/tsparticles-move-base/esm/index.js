import { BaseMover } from "./BaseMover";
export async function loadBaseMover(engine) {
    engine.addMover("base", () => new BaseMover());
}
