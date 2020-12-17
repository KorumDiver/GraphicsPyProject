const config = {
    // Глобальные переменные
}


class Circle {
    constructor(pos, angle, r, rotation_speed) {
        this.pos = pos;
        this.rotation_vector = {dx: Math.cos(angle), dy: Math.sin(angle)};
        this.r = r;
        this.rotation_speed = rotation_speed;
    }

    move(new_pos) {
        this.pos = new_pos;
        this.rotation_vector = {
            dx: this.rotation_vector.dx * Math.cos(this.rotation_speed) - this.rotation_vector.dy * Math.sin(this.rotation_speed),
            dy: this.rotation_vector.dx * Math.sin(this.rotation_speed) + this.rotation_vector.dy * Math.cos(this.rotation_speed),
        }
        return {
            x: this.pos.x + this.r * this.rotation_vector.dx,
            y: this.pos.y + this.r * this.rotation_vector.dy,
        }
    }

    draw(ctx) {

        ctx.moveTo(this.pos.x, this.pos.y);
        ctx.beginPath();

        ctx.arc(this.pos.x, this.pos.y, this.r, 0, 2 * Math.PI, true);
        ctx.stroke();
    }
}

class FourierCircles {
    constructor(num_circles, first_pos, max_rad) {


        this.create_circles('', num_circles, first_pos, max_rad)

        this.points_draw = [];
    }

    move() {
        let current_pos = this.circles[0].pos;
        for (let i = 0; i < this.circles.length; i++) {
            current_pos = this.circles[i].move(current_pos);
        }
        this.points_draw.push(current_pos);
    }

    draw_line(ctx) {
        ctx.strokeStyle = '#00FF00';
        ctx.beginPath();
        ctx.moveTo(this.points_draw[0].x, this.points_draw[0].y);
        for (let i = 0; i < this.points_draw.length - 1; i++) {
            ctx.lineTo(this.points_draw[i].x, this.points_draw[i].y);
        }

        ctx.stroke();


    }

    draw_circles(ctx) {
        ctx.beginPath();
        ctx.strokeStyle = '#DC143C';
        ctx.moveTo(this.circles[0].pos.x, this.circles[0].pos.y);
        for (let i = 1; i < this.circles.length; i++) {
            ctx.lineTo(this.circles[i].pos.x, this.circles[i].pos.y);
        }
        ctx.lineTo(this.points_draw[this.points_draw.length - 1].x, this.points_draw[this.points_draw.length - 1].y);
        ctx.stroke();
        for (let i = 0; i < this.circles.length; i++) {
            this.circles[i].draw(ctx);
        }
    }

    create_circles(mode, num_circles, first_pos, max_rad) {
        switch (mode) {
            case '1':
                this.circles = [new Circle(first_pos, 0, 150, 2 * Math.PI / 90)];
                this.circles.push(new Circle(
                    {x: 0, y: 0},
                    0,
                    50,
                    2 * Math.PI /20
                ));
                break
            default:
                this.circles = [new Circle(first_pos, 0, max_rad*Math.random(), 2 * Math.PI / (Math.random() * 360))];
                for (let i = 1; i < num_circles; i++) {
                    this.circles.push(new Circle(
                        {x: 0, y: 0},
                        0,
                        Math.random()*max_rad,
                        2 * Math.PI / (Math.random() * 360)
                    ));
                }
                break
        }

    }
}

class Animation {
    constructor() {
        this.cnv = null;
        this.ctx = null;
        this.size = {w: 0, h: 0};
    }

    init() {
        // Инициализирует элементы класса
        this.createCanvas();

        this.fourierCircles = new FourierCircles(5, {x: this.size.w / 2, y: this.size.h / 2}, 100);

        // Запускает анимацию
        this.updateAnimation();
    }

    createCanvas() {
        // Создает канвас
        this.cnv = document.createElement("canvas");
        // Получает контекст из созданного канваса
        this.ctx = this.cnv.getContext('2d');
        // Вызывает метод выставляющий размер канваса в размер окна
        this.setCanvasSize();
        // Добавляет канвас на страницу
        document.body.appendChild(this.cnv);
        // Создает событие изменения размера и прикрепляет к нему функцию изменения размера окна
        window.addEventListener(`resize`, () => this.setCanvasSize());
    }

    setCanvasSize() {
        // Метод изменения размера канваса в размер окна
        this.size.w = this.cnv.width = window.innerWidth;
        this.size.h = this.cnv.height = window.innerHeight;
    }

    updateCanvas() {
        // Чистит канвас, закрашивает его в определенный цвет
        this.ctx.fillStyle = `rgb(22, 22, 25)`;
        this.ctx.fillRect(0, 0, this.size.w, this.size.h);
    }

    draw() {
        // Функция отрисовки
        // Вызывется в методе обновления анимаций
        // Вызывает остальные функций отрисовки объектов
        this.fourierCircles.move();
        this.fourierCircles.draw_line(this.ctx);
        this.fourierCircles.draw_circles(this.ctx);
    }

    updateAnimation() {
        // Вызывает метод очистки канваса
        this.updateCanvas();

        // Вызывает метод отрисовки
        this.draw();

        // Создается цикл анимаций
        window.requestAnimationFrame(() => this.updateAnimation())
    }

}

window.onload = () => {
    // Запуск скрипта
    new Animation().init();
}
