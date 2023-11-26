import type { IOptionLoader, IParticlesOptions, RecursivePartial } from "tsparticles-engine";
import type { ITrail } from "../Interfaces/ITrail";
export declare class Trail implements ITrail, IOptionLoader<ITrail> {
    delay: number;
    particles?: RecursivePartial<IParticlesOptions>;
    pauseOnStop: boolean;
    quantity: number;
    constructor();
    load(data?: RecursivePartial<ITrail>): void;
}
