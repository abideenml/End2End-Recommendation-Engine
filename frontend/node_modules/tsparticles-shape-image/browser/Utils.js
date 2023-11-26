import { getStyleFromHsl } from "tsparticles-engine";
const currentColorRegex = /(#(?:[0-9a-f]{2}){2,4}|(#[0-9a-f]{3})|(rgb|hsl)a?\((-?\d+%?[,\s]+){2,3}\s*[\d.]+%?\))|currentcolor/gi;
function replaceColorSvg(imageShape, color, opacity) {
    const { svgData } = imageShape;
    if (!svgData) {
        return "";
    }
    const colorStyle = getStyleFromHsl(color, opacity);
    if (svgData.includes("fill")) {
        return svgData.replace(currentColorRegex, () => colorStyle);
    }
    const preFillIndex = svgData.indexOf(">");
    return `${svgData.substring(0, preFillIndex)} fill="${colorStyle}"${svgData.substring(preFillIndex)}`;
}
export async function loadImage(image) {
    return new Promise((resolve) => {
        image.loading = true;
        const img = new Image();
        image.element = img;
        img.addEventListener("load", () => {
            image.loading = false;
            resolve();
        });
        img.addEventListener("error", () => {
            image.element = undefined;
            image.error = true;
            image.loading = false;
            console.error(`Error tsParticles - loading image: ${image.source}`);
            resolve();
        });
        img.src = image.source;
    });
}
export async function downloadSvgImage(image) {
    if (image.type !== "svg") {
        await loadImage(image);
        return;
    }
    image.loading = true;
    const response = await fetch(image.source);
    if (!response.ok) {
        console.error("Error tsParticles - Image not found");
        image.error = true;
    }
    if (!image.error) {
        image.svgData = await response.text();
    }
    image.loading = false;
}
export function replaceImageColor(image, imageData, color, particle) {
    var _a, _b, _c;
    const svgColoredData = replaceColorSvg(image, color, (_b = (_a = particle.opacity) === null || _a === void 0 ? void 0 : _a.value) !== null && _b !== void 0 ? _b : 1), imageRes = {
        color,
        data: Object.assign(Object.assign({}, image), { svgData: svgColoredData }),
        loaded: false,
        ratio: imageData.width / imageData.height,
        replaceColor: (_c = imageData.replaceColor) !== null && _c !== void 0 ? _c : imageData.replace_color,
        source: imageData.src,
    };
    return new Promise((resolve) => {
        const svg = new Blob([svgColoredData], { type: "image/svg+xml" }), domUrl = URL || window.URL || window.webkitURL || window, url = domUrl.createObjectURL(svg), img = new Image();
        img.addEventListener("load", () => {
            imageRes.loaded = true;
            imageRes.element = img;
            resolve(imageRes);
            domUrl.revokeObjectURL(url);
        });
        img.addEventListener("error", async () => {
            domUrl.revokeObjectURL(url);
            const img2 = Object.assign(Object.assign({}, image), { error: false, loading: true });
            await loadImage(img2);
            imageRes.loaded = true;
            imageRes.element = img2.element;
            resolve(imageRes);
        });
        img.src = url;
    });
}
