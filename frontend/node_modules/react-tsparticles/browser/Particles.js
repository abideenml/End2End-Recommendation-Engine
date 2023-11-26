import React, { Component } from "react";
import { tsParticles } from "tsparticles-engine";
import equal from "fast-deep-equal/react";
const defaultId = "tsparticles";
export default class Particles extends Component {
    constructor(props) {
        super(props);
        this.state = {
            init: false,
            library: undefined,
        };
    }
    destroy() {
        if (!this.state.library) {
            return;
        }
        this.state.library.destroy();
        this.setState({
            library: undefined,
        });
    }
    shouldComponentUpdate(nextProps) {
        return !equal(nextProps, this.props);
    }
    componentDidUpdate() {
        this.refresh();
    }
    forceUpdate() {
        this.refresh().then(() => {
            super.forceUpdate();
        });
    }
    componentDidMount() {
        (async () => {
            if (this.props.init) {
                await this.props.init(tsParticles);
            }
            this.setState({
                init: true,
            }, async () => {
                await this.loadParticles();
            });
        })();
    }
    componentWillUnmount() {
        this.destroy();
    }
    render() {
        const { width, height, className, canvasClassName, id } = this.props;
        return (React.createElement("div", { className: className, id: id },
            React.createElement("canvas", { className: canvasClassName, style: Object.assign(Object.assign({}, this.props.style), { width,
                    height }) })));
    }
    async refresh() {
        this.destroy();
        await this.loadParticles();
    }
    async loadParticles() {
        var _a, _b, _c;
        if (!this.state.init) {
            return;
        }
        const cb = async (container) => {
            if (this.props.container) {
                this.props.container.current = container;
            }
            this.setState({
                library: container,
            });
            if (this.props.loaded) {
                await this.props.loaded(container);
            }
        };
        const id = (_b = (_a = this.props.id) !== null && _a !== void 0 ? _a : Particles.defaultProps.id) !== null && _b !== void 0 ? _b : defaultId, container = this.props.url
            ? await tsParticles.loadJSON(id, this.props.url)
            : await tsParticles.load(id, (_c = this.props.params) !== null && _c !== void 0 ? _c : this.props.options);
        await cb(container);
    }
}
Particles.defaultProps = {
    width: "100%",
    height: "100%",
    options: {},
    style: {},
    url: undefined,
    id: defaultId,
};
