from manim import *
import numpy as np

class MolecularCloudCollapse(Scene):
    def construct(self):
        # 1. Introduction: The Molecular Cloud Core
        title = Text("Core supported by thermal pressure", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Create a "cloud" of particles
        num_particles = 1000
        particles = VGroup(*[
            Dot(
                point=[np.random.uniform(-3, 3), np.random.uniform(-3, 3), 0],
                radius=0.03,
                color=BLUE_E,
                fill_opacity=0.6
            ) for _ in range(num_particles)
        ])

        self.play(FadeIn(particles, lag_ratio=0.1))
        self.wait(1)

        # 2. Gravity Initiation: Slow Infall
        subtitle = Text("Gravitational Collapse", font_size=24, color=GRAY).next_to(title, DOWN)
        self.play(Write(subtitle))

        # We define a function to move particles toward the center while slightly rotating
        # This simulates the initial net angular momentum of the core.
        def collapse_and_rotate(obj, alpha):
            # Move toward center (collapse)
            current_pos = obj.get_center()
            dist = np.linalg.norm(current_pos)
            
            # Rotation factor increases as distance decreases (Conservation of L)
            rotation_speed = 0.05 / np.sqrt(dist + 0.1) 
            angle = rotation_speed * alpha
            
            # Apply rotation and radial shrink
            new_pos = current_pos * (1 - 0.7 * alpha)
            matrix = [[np.cos(angle), -np.sin(angle), 0],
                      [np.sin(angle),  np.cos(angle), 0],
                      [0, 0, 1]]
            obj.move_to(np.dot(matrix, new_pos))

        self.play(
            UpdateFromAlphaFunc(particles, collapse_and_rotate),
            run_time=2,
            rate_func=linear
        )
        self.play(FadeOut(subtitle))

        # 3. Flattening into a Disk
        # As it collapses, it flattens due to rotation
        disk_subtitle = Text("Angular Momentum convervation results in a rotationally supported disk", font_size=24, color=BLUE_B).next_to(title, DOWN)
        self.play(Write(disk_subtitle))

        # Transform particles into a structured disk
        disk_particles = VGroup()
        for i in range(num_particles):
            angle = np.random.uniform(0, TAU)
            # Denser toward the center (1/r distribution)
            radius = np.random.power(2) * 2.5 
            disk_particles.add(
                Dot(
                    point=[radius * np.cos(angle), radius * np.sin(angle), 0],
                    radius=0.02,
                    color=interpolate_color(ORANGE, YELLOW, radius/2.5)
                )
            )

        self.play(Transform(particles, disk_particles), run_time=3)
        
        # 4. Protoplanetary Disk Rotation
        # Add a central Protostar
        protostar = Dot(radius=0.15, color=WHITE).set_glow_factor(1)
        protostar.add(Circle(radius=0.15, color=YELLOW).set_stroke(width=8))
        
        self.play(FadeIn(protostar))

        # Final Rotation loop
        def rotate_disk(obj, dt):
            obj.rotate(0.5 * dt)

        particles.add_updater(rotate_disk)
        self.wait(10)
        
        # Cleanup
        particles.remove_updater(rotate_disk)
        self.play(FadeOut(particles), FadeOut(protostar), FadeOut(title), FadeOut(disk_subtitle))
