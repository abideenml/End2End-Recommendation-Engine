export class LineDrawer {
    draw(context, particle, radius) {
        context.moveTo(-radius / 2, 0);
        context.lineTo(radius / 2, 0);
    }
    getSidesCount() {
        return 1;
    }
}
