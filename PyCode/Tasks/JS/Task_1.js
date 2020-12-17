class Template {
    constructor(ctx) {
        this.ctx = ctx;
    }

    cube(pos, size, color) {
        this.ctx.strokeStyle = color;
        this.ctx.beginPath();
        this.ctx.strokeRect(pos.x, pos.y, size.x, size.y);
        this.ctx.strokeRect(pos.x + size.x * 3 / 4,
            pos.y - size.y * 3 / 4,
            size.x,
            size.y);

        this.ctx.moveTo(pos.x, pos.y);
        this.ctx.lineTo(pos.x + size.x * 3 / 4, pos.y - size.y * 3 / 4);

        this.ctx.moveTo(pos.x + size.x, pos.y);
        this.ctx.lineTo(pos.x + size.x * 7 / 4, pos.y - size.y * 3 / 4);

        this.ctx.moveTo(pos.x, pos.y + size.y);
        this.ctx.lineTo(pos.x + size.x * 3 / 4, pos.y + size.y / 4);

        this.ctx.moveTo(pos.x + size.x, pos.y + size.y);
        this.ctx.lineTo(pos.x + size.x * 7 / 4, pos.y + size.y / 4);

        this.ctx.stroke();
    }
}

class Animation {
    constructor() {
        this.cnv = null;
        this.ctx = null;
        this.size = {w: 0, h: 0};
    }

    init() {
        this.createCanvas();

        this.template = new Template(this.ctx);

        this.updateAnimation();
    }

    createCanvas() {
        this.cnv = document.createElement("canvas");
        this.ctx = this.cnv.getContext('2d');
        this.setCanvasSize();
        document.body.appendChild(this.cnv);
        window.addEventListener(`resize`, () => this.setCanvasSize());
    }

    setCanvasSize() {
        this.size.w = this.cnv.width = window.innerWidth;
        this.size.h = this.cnv.height = window.innerHeight;
    }

    updateCanvas() {
        this.ctx.fillStyle = `rgb(22, 22, 25)`;
        this.ctx.fillRect(0, 0, this.size.w, this.size.h);
    }

    draw() {
        this.template.cube({x: Math.random() * 500, y: Math.random() * 500}, {
            x: Math.random() * 300,
            y: Math.random() * 300
        }, "#FFFFFF");


    }

    updateAnimation() {
        this.updateCanvas();
        this.draw();

        //window.requestAnimationFrame(() => this.updateAnimation())
    }

}

window.onload = () => {
    new Animation().init();
}
