from polygon import Polygon
from vector2d import Vector2D

from pathlib import Path

class Environment:
    def __init__(self, filename):
        self.width = 800
        self.height = 600

        self.start = Vector2D(0, 0)
        self.goal = Vector2D(800, 600)

        self.obstacles = []

        lines = []

        for line in Path(filename).read_text().splitlines():
            line = line.split("#")[0].strip()

            if line:
                lines.append(line)

        data = iter(lines)

        try:
            number_of_polygons = int(next(data))

            if number_of_polygons < 0:
                raise ValueError("Invalid number of polygons.")

            for _ in range(number_of_polygons):
                number_of_vertices = int(next(data))

                if number_of_vertices < 3:
                    raise ValueError(
                        "A polygon must have at least three vertices."
                    )

                polygon = Polygon(number_of_vertices)

                for _ in range(number_of_vertices):
                    x, y = map(float, next(data).split())
                    polygon.vertices.append(Vector2D(x, y))

                self.obstacles.append(polygon)

            if next(data, None) is not None:
                raise ValueError("Unexpected extra data in the file.")

        except StopIteration as error:
            raise ValueError(
                "The environment file is incomplete."
            ) from error

    @staticmethod
    def printPath(search_name, path, output_folder):
        """Save the path using the original framework's JS format."""
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        filename = output_folder / f"{search_name}.js"

        with filename.open("w") as file:
            file.write(f"window.{search_name} = [\n")

            for point in path:
                file.write(f"    [{point.x}, {point.y}],\n")

            file.write("];\n")