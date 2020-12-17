import turtle


def main():
    string = 'X'
    rule = {'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF', '+': '+', '-': '-', '[': '[', ']': ']'}
    gen = 6
    new_string = ''
    for i in range(gen):
        for s in string:
            new_string += str(rule[s])
        string = new_string
        new_string = ''
    print(len(string))
    draw(string)


def draw(string: str):
    turtle.tracer(0)

    turtle.penup()
    turtle.setpos(0, -350)
    turtle.pendown()

    turtle.left(90)
    len_line = 4
    angle_turn = 25
    stack = []

    for ch in string:
        if ch == 'F':
            turtle.forward(len_line)
        elif ch == '-':
            turtle.left(angle_turn)
        elif ch == '+':
            turtle.right(angle_turn)
        elif ch == '[':
            stack.append([turtle.pos(), turtle.heading()])
        elif ch == ']':
            turtle.penup()
            pos, angle = stack.pop()
            turtle.setpos(pos)
            turtle.setheading(angle)
            turtle.pendown()

    turtle.hideturtle()
    turtle.update()
    turtle.done()


if __name__ == '__main__':
    main()
