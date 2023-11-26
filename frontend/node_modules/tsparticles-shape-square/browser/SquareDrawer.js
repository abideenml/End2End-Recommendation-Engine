const fixFactor = Math.sqrt(2);
export class SquareDrawer {
    draw(context, particle, radius) {
        context.rect(-radius / fixFactor, -radius / fixFactor, (radius * 2) / fixFactor, (radius * 2) / fixFactor);
    }
    getSidesCount() {
        return 4;
    }
}
