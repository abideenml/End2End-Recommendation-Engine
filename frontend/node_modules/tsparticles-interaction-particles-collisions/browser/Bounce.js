import { circleBounce, circleBounceDataFromParticle } from "tsparticles-engine";
export function bounce(p1, p2) {
    circleBounce(circleBounceDataFromParticle(p1), circleBounceDataFromParticle(p2));
}
