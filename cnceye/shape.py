import trimesh
import numpy as np
from trimesh.graph import face_adjacency
from .arc import get_arc_info


class Shape:
    def __init__(self, stl_file_path: str):
        self.mesh = trimesh.load(stl_file_path)

    def get_unique_z_values_of_visiable_vertices(self):
        # Get the normals of the facets
        facet_normals = self.mesh.face_normals

        # Find the indices of facets facing "up" (positive z-direction)
        upward_facing_indices = np.where(facet_normals[:, 2] > 0)[0]

        # Get the unique vertices associated with upward-facing facets
        visible_vertices = np.unique(self.mesh.faces[upward_facing_indices])

        # Extract the coordinates of the visible vertices
        visible_vertex_coordinates = self.mesh.vertices[visible_vertices]

        # get unique z values
        unique_z = np.unique(visible_vertex_coordinates[:, 2])
        return unique_z

    def get_visible_facets(self):
        # Get the normals of the facets
        facet_normals = self.mesh.face_normals

        # Find the indices of facets facing "up" (positive z-direction)
        upward_facing_indices = np.where(facet_normals[:, 2] > 0)[0]

        return upward_facing_indices

    def are_coplanar(self, facet_idx0, facet_idx1, tolerance=1e-6):
        facet0 = self.mesh.vertices[self.mesh.faces[facet_idx0]]
        facet1 = self.mesh.vertices[self.mesh.faces[facet_idx1]]
        # Calculate the normal vector for each facet
        normal0 = np.cross(facet0[1] - facet0[0], facet0[2] - facet0[0])
        normal1 = np.cross(facet1[1] - facet1[0], facet1[2] - facet1[0])

        # Check if the normal vectors are parallel
        if np.all(
            np.isclose(
                normal0 / np.linalg.norm(normal0),
                normal1 / np.linalg.norm(normal1),
                atol=tolerance,
            )
        ):
            # if np.allclose(normal0, normal1):
            # Check if the facets are coplanar
            if np.all(np.abs(np.dot(facet1[0] - facet0[0], normal0)) < 1e-6):
                # The facets are coplanar
                return True
            else:
                # The facets are parallel but not coplanar
                return False
        else:
            # The facets are not coplanar
            return False

    def group_by_coplanar_facets(self, facet_indices: np.ndarray):
        """
        Group facets that are coplanar \n
        Return a list of lists of coplanar facets
        """
        coplanar_facets = [[facet_indices[0]]]
        for facet_idx in facet_indices[1:]:
            is_coplanar = False
            for i, coplanar_facet in enumerate(coplanar_facets):
                if self.are_coplanar(facet_idx, coplanar_facet[0]):
                    coplanar_facets[i].append(facet_idx)
                    is_coplanar = True
                    break
            if not is_coplanar:
                coplanar_facets.append([facet_idx])
                is_coplanar = False

        return coplanar_facets

    def get_common_point(self, prev_points, points):
        """
        Get the common point between two lists of points
        """
        if prev_points is None:
            return None
        for prev_point in prev_points:
            for point in points:
                if np.array_equal(prev_point, point):
                    return point

    def line_length_similar(self, points0, points1):
        line_length0 = np.linalg.norm(points0[0] - points0[1])
        line_length1 = np.linalg.norm(points1[0] - points1[1])
        return np.isclose(
            line_length0,
            line_length1,
            atol=1e-3,
        )

    def combine_same_arc(self, arc_group):
        """
        Combine arcs that are the same
        """
        if len(arc_group) < 2:
            return arc_group
        new_arc_group = []
        prev_points = arc_group[0]
        for i in range(1, len(arc_group)):
            arc_points = arc_group[i]
            if np.array_equal(
                prev_points[-1], arc_points[0]
            ) and self.line_length_similar(prev_points, arc_points):
                # merge prev_points and arc_points
                prev_points = np.vstack((prev_points, arc_points[1:]))
            elif np.array_equal(
                prev_points[-1], arc_points[-1]
            ) and self.line_length_similar(prev_points, arc_points):
                # reverse arc_points and merge with prev_points
                prev_points = np.vstack((prev_points, arc_points[-2::-1]))
            elif np.array_equal(
                prev_points[0], arc_points[0]
            ) and self.line_length_similar(prev_points, arc_points):
                # reverse prev_points and merge with arc_points
                prev_points = np.vstack((arc_points[-2::-1], prev_points))
            elif np.array_equal(
                prev_points[0], arc_points[-1]
            ) and self.line_length_similar(prev_points, arc_points):
                # merge prev_points and reverse arc_points
                prev_points = np.vstack((arc_points, prev_points[1:]))
            else:
                new_arc_group.append(prev_points)
                prev_points = arc_points

            if i == len(arc_group) - 1:
                new_arc_group.append(prev_points)
        return new_arc_group

    def connect_same_group(self, point_groups):
        """
        Connect point groups that are the same \n
        Check if the first and last point are the same \n
        """
        groups = []
        missing_point_groups = []
        for point_group in point_groups:
            if np.array_equal(point_group[0], point_group[-1]):
                groups.append(point_group)
            else:
                found_pair = False
                for missing_point_group in missing_point_groups:
                    if np.array_equal(missing_point_group[0], point_group[-1]):
                        combined_group = np.vstack(
                            (point_group, missing_point_group[1:])
                        )
                    elif np.array_equal(missing_point_group[-1], point_group[0]):
                        combined_group = np.vstack(
                            (missing_point_group, point_group[1:])
                        )
                    elif np.array_equal(missing_point_group[0], point_group[0]):
                        combined_group = np.vstack(
                            (point_group[::-1], missing_point_group[1:])
                        )
                    elif np.array_equal(missing_point_group[-1], point_group[-1]):
                        combined_group = np.vstack(
                            (missing_point_group[:-1], point_group[::-1])
                        )
                    else:
                        continue
                    if np.array_equal(combined_group[0], combined_group[-1]):
                        groups.append(combined_group)
                        missing_point_groups.remove(missing_point_group)
                    else:
                        # replace missing_point_group with combined_group
                        missing_point_groups.remove(missing_point_group)
                        missing_point_groups.append(combined_group)
                    found_pair = True
                    break
                if not found_pair:
                    missing_point_groups.append(point_group)

        # first and last point should be the same
        for group in groups:
            assert np.array_equal(group[0], group[-1])
        return groups

    def group_by_common_point(self, coplanar_shapes):
        """
        Group coplanar shapes by common point
        """

        def _get_point(_coplanar_shape):
            point0 = self.mesh.vertices[_coplanar_shape[0]]
            point1 = self.mesh.vertices[_coplanar_shape[1]]
            return np.array([point0, point1])

        point_groups = [_get_point(coplanar_shapes[0])]
        for i in range(1, len(coplanar_shapes)):
            point = _get_point(coplanar_shapes[i])

            duplicate = False
            for i in range(len(point_groups)):
                point_group = point_groups[i]
                first_and_last_point = np.array([point_group[0], point_group[-1]])
                common_point = self.get_common_point(first_and_last_point, point)
                if common_point is not None:
                    mask = np.any(point != common_point, axis=1)
                    new_point = point[mask]
                    if np.array_equal(point_groups[i][-1], common_point):
                        point_groups[i] = np.vstack((point_groups[i], new_point))
                    else:
                        point_groups[i] = np.vstack((new_point, point_groups[i]))
                    duplicate = True
                    break
            if not duplicate:
                point_groups.append(point)

        return self.connect_same_group(point_groups)

    def get_line_angle(self, line0: np.array, line1: np.array):
        """
        Get the angle between two lines
        """
        line0 = line0[1] - line0[0]
        line1 = line1[1] - line1[0]
        return np.arccos(
            np.dot(line0, line1) / (np.linalg.norm(line0) * np.linalg.norm(line1))
        )

    def get_line_length(self, line: np.array):
        """
        Get the length of a line
        """
        return np.linalg.norm(line[1] - line[0])

    def get_line_diff_percentage(self, line0: np.array, line1: np.array):
        """
        Get the difference in length between two lines
        """
        line_length0 = self.get_line_length(line0)
        line_length1 = self.get_line_length(line1)
        return abs(line_length0 - line_length1) / line_length0

    def get_lines_and_arcs(self, angle_threshold: float = 0.1):
        """
        Extract lines and arcs from an STL file \n
        If the line angle between two lines is close to 0 and
        the line length is close to the previous line length,
        it is considered an arc. \n
        Note: This is not a robust algorithm.

        Parameters
        ----------
        angle_threshold : int
            Angle threshold for arc

        Returns
        -------
        lines : list
            List of lines
        arcs : list
            List of arcs
        """
        shapes = self.get_shapes()
        lines = []
        arcs = []

        for coplanar_shapes in shapes:
            point_groups = self.group_by_common_point(coplanar_shapes)
            line_group = []
            arc_group = []

            for point_group in point_groups:
                arc_start_idx = None
                for i in range(len(point_group) - 2):
                    line0 = np.array([point_group[i], point_group[i + 1]])
                    line1 = np.array([point_group[i + 1], point_group[i + 2]])
                    line_angle = self.get_line_angle(line0, line1)
                    if (
                        abs(line_angle) < angle_threshold
                        and self.get_line_diff_percentage(line0, line1) < 0.01
                    ):
                        # arc
                        if arc_start_idx is None:
                            arc_start_idx = i
                        elif i == len(point_group) - 3:
                            arc_points = point_group[arc_start_idx:]
                            arc_group.append(arc_points)
                            arc_start_idx = None
                        else:
                            continue
                    else:
                        # line
                        if arc_start_idx is not None:
                            arc_points = point_group[arc_start_idx : i + 1]
                            arc_group.append(arc_points)
                            arc_start_idx = None
                        else:
                            line_group.append(line0)
                        if i == len(point_group) - 3:
                            line_group.append(line1)

            if line_group:
                lines.append(line_group)
            if arc_group:
                arcs.append(self.combine_same_arc(arc_group))

        return lines, arcs

    def get_shapes(self):
        visible_facet_indices = self.get_visible_facets()
        group_facets = self.group_by_coplanar_facets(visible_facet_indices)
        adjacency = face_adjacency(self.mesh.faces)

        shapes = []
        for coplanar_facets in group_facets:
            shapes_on_coplanar_facet = []
            for pair in adjacency:
                pair0_in_group = pair[0] in coplanar_facets
                pair1_in_group = pair[1] in coplanar_facets
                if pair0_in_group != pair1_in_group:
                    common_edge_vertices = list(
                        set(self.mesh.faces[pair[0]]) & set(self.mesh.faces[pair[1]])
                    )
                    if pair0_in_group:
                        face_id = pair[1]
                    else:
                        face_id = pair[0]
                    common_edge_vertices.append(face_id)
                    shapes_on_coplanar_facet.append(common_edge_vertices)

            # order by face index
            shapes_on_coplanar_facet.sort(key=lambda x: x[-1])
            shapes.append(shapes_on_coplanar_facet)

        return shapes

    def get_arc_info(self, arc_points: np.ndarray, decimal_places: int = 3):
        """
        Get information about arc

        Parameters
        ----------
        arc_points : list
            List of arc coordinates [(x,y,z), (x,y,z)]
        decimal_places : int
            Number of decimal places to round to

        Returns
        -------
        radius : float
            Radius of arc
        center : np.array
            Center of arc
        is_circle : bool
            True if arc is a circle
        """
        return get_arc_info(arc_points, decimal_places=decimal_places)

    def analyze(self):
        lines, arcs = self.get_lines_and_arcs()
        self.lines = lines
        self.arcs = arcs


def round_shape_values(shapes: np.ndarray, decimal_places: int = 3):
    for i in range(len(shapes)):
        shapes[i] = np.round(shapes[i], decimals=decimal_places)

    return shapes
