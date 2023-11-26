import { ExternalInteractorBase } from "tsparticles-engine";
import type { IDelta, IModes, Modes, Particle, RecursivePartial } from "tsparticles-engine";
import type { ITrailMode, TrailContainer, TrailMode } from "./Types";
export declare class TrailMaker extends ExternalInteractorBase<TrailContainer> {
    private _delay;
    private _lastPosition?;
    constructor(container: TrailContainer);
    clear(): void;
    init(): void;
    interact(delta: IDelta): Promise<void>;
    isEnabled(particle?: Particle): boolean;
    loadModeOptions(options: Modes & TrailMode, ...sources: RecursivePartial<(IModes & ITrailMode) | undefined>[]): void;
    reset(): void;
}
