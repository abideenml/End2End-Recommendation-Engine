import type { Container } from "tsparticles-engine";
import type { ITrail } from "./Options/Interfaces/ITrail";
import type { Trail } from "./Options/Classes/Trail";
import type { TrailOptions } from "./Options/Classes/TrailOptions";
export declare type ITrailMode = {
    trail: ITrail;
};
export declare type TrailMode = {
    trail?: Trail;
};
export declare type TrailContainer = Container & {
    actualOptions: TrailOptions;
};
