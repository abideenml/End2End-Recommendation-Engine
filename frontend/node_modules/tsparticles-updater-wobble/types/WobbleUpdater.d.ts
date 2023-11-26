import type { Container, IDelta, IParticleUpdater, IParticlesOptions, Particle, ParticlesOptions, RecursivePartial } from "tsparticles-engine";
import type { IWobble } from "./Options/Interfaces/IWobble";
import { Wobble } from "./Options/Classes/Wobble";
declare type WobbleParticle = Particle & {
    options: WobbleParticlesOptions;
    retina: {
        wobbleDistance?: number;
    };
};
declare type IWobbleParticlesOptions = IParticlesOptions & {
    wobble?: IWobble;
};
declare type WobbleParticlesOptions = ParticlesOptions & {
    wobble?: Wobble;
};
export declare class WobbleUpdater implements IParticleUpdater {
    private readonly container;
    constructor(container: Container);
    init(particle: WobbleParticle): void;
    isEnabled(particle: WobbleParticle): boolean;
    loadOptions(options: WobbleParticlesOptions, ...sources: (RecursivePartial<IWobbleParticlesOptions> | undefined)[]): void;
    update(particle: WobbleParticle, delta: IDelta): void;
}
export {};
