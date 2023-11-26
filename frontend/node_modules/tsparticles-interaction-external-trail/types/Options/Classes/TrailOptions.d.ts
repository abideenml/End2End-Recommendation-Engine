import type { Options } from "tsparticles-engine";
import type { TrailMode } from "../../Types";
export declare type TrailOptions = Options & {
    interactivity: {
        modes: TrailMode;
    };
};
