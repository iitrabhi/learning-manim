from manim import *
import scipy.integrate as spi


class SinusArea(Scene):
    def construct(self):

        ax = Axes(
            x_range=(-10, 10, 1),
            y_range=(-3, 3, 1),
            x_length=13,
            y_length=5,
            tips=False,
        )

        Nombre = MathTex(r"A \cdot \sin(\omega \cdot t - \kappa \cdot x)").to_edge(
            UP, buff=0.5
        )

        Nombre[0][0].set_color(PURPLE)
        Nombre[0][6].set_color(ORANGE)
        Nombre[0][8].set_color(BLUE)
        Nombre[0][10].set_color(GOLD)
        Numeritos1 = NumberLine(
            x_range=[-10, 10, 1],
            length=13,
            include_numbers=True,
            label_direction=DOWN,
            include_tip=False,
            include_ticks=False,
            font_size=17,
            numbers_to_exclude=[0],
        )
        Numeritos2 = NumberLine(
            x_range=[-3, 3, 1],
            length=5,
            include_numbers=True,
            label_direction=LEFT,
            include_tip=False,
            include_ticks=False,
            font_size=17,
            numbers_to_exclude=[0],
            rotation=PI / 2,
        )

        t = ValueTracker(0)
        t_number = DecimalNumber(
            t.get_value(),
            num_decimal_places=2,
            show_ellipsis=True,
            font_size=30,
            color=BLUE,
        ).shift(2.77 * UP + 5.7 * LEFT)
        t_number.add_updater(lambda mobject: mobject.set_value(t.get_value()))
        
        def clock(mobject, dt):
            mobject.increment_value(dt)

        t.add_updater(clock)
        seno = ax.plot(lambda x: 2 * np.sin(1 * t.get_value() - 0.7 * x), color=RED)
        seno.add_updater(
            lambda mobject: mobject.become(
                ax.plot(lambda x: 2 * np.sin(1 * t.get_value() - 0.7 * x), color=RED)
            )
        )

        area = ax.get_area(seno, (0, 4.5), color=(RED_A, RED_D), opacity=0.5)
        area.add_updater(
            lambda mobject: mobject.become(
                ax.get_area(seno, (0, 4.5), color=(RED_A, RED_D), opacity=0.5)
            )
        )

        area_value = ValueTracker(0)
        area_value.add_updater(
            lambda mobject: mobject.set_value(
                spi.quad(lambda x: 2 * np.sin(1 * t.get_value() - 0.7 * x), 0, 4.5)[0]
            )
        )

        area_number = DecimalNumber(
            area_value.get_value(),
            num_decimal_places=3,
            show_ellipsis=True,
            font_size=30,
            color=RED_A,
        ).shift(1.5 * RIGHT + 1 * UP)

        area_number.add_updater(
            lambda mobject: mobject.set_value(area_value.get_value())
        )
        Area_Nombre = MathTex(r"Area =", font_size=30).next_to(
            area_number, UP, buff=0.3
        )

        Conjunto = VGroup(ax, Numeritos1, Numeritos2, seno, area).shift(1 * DOWN)
        Constantes = (
            VGroup(
                MathTex(r"A = 2", font_size=30, color=PURPLE),
                MathTex(r"\omega = 1", font_size=30, color=ORANGE),
                MathTex(r"t =", font_size=30, color=BLUE),
                MathTex(r"\kappa = 0.7", font_size=30, color=GOLD),
            )
            .arrange(DOWN)
            .to_edge(UL, buff=0.2)
        )

        self.add(Numeritos1, Numeritos2, ax)
        self.play(
            Write(Nombre), Write(Constantes), Write(t_number), Create(seno, run_time=2)
        )
        self.play(Create(area))
        self.play(Write(Area_Nombre), Write(area_number))
        self.play(
            t.animate.set_value(0), area_value.animate.set_value(0), rate_func=linear
        )
        self.wait(10)
