export class CircleDrawer {
    draw(context, particle, radius) {
        context.arc(0, 0, radius, 0, Math.PI * 2, false);
    }
    getSidesCount() {
        return 12;
    }
}
