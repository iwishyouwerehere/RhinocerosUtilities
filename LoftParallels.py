#https://discourse.mcneel.com/t/find-the-two-closest-parallel-lines-and-create-a-loft/172699
import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import logging

logging.basicConfig(filename='script_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def is_vector_parallel_to(vector1, vector2):
    try:
        return vector1.IsParallelTo(vector2, rs.UnitAngleTolerance()) != 0
    except Exception as e:
        logging.error("Error in is_vector_parallel_to: " + str(e))
        return False

def find_closest_parallel_line(lines_guid, line1_guid):
    try:
        line1 = rs.coercecurve(line1_guid)
        if not line1:
            logging.warning("Line with GUID {line1_guid} could not be coerced into a curve.")
            return None

        line1_vector = line1.TangentAtStart
        closest_line = None
        min_distance = float('inf')

        for line_guid in lines_guid:
            if line_guid == line1_guid:
                continue

            line = rs.coercecurve(line_guid)
            if not line:
                logging.warning("Line with GUID {line_guid} could not be coerced into a curve.")
                continue

            line_vector = line.TangentAtStart
            if is_vector_parallel_to(line1_vector, line_vector):
                distance = calculate_distance_between_parallel_lines(line1, line)
                if distance < min_distance:
                    min_distance = distance
                    closest_line = line_guid

        if closest_line:
            loft_and_add_surface(line1_guid, closest_line)
        else:
            logging.info("No parallel line found for line GUID " + str(line1_guid))

        return closest_line
    except Exception as e:
        logging.error("Error in find_closest_parallel_line: " + str(e))
        return None

def calculate_distance_between_parallel_lines(line1, line2):
    try:
        point_on_line1 = line1.PointAtStart
        perpendicular_plane = rg.Plane(line2.PointAtStart, line2.TangentAtStart)
        projected_point = rg.Plane.ClosestPoint(perpendicular_plane, point_on_line1)
        return point_on_line1.DistanceTo(projected_point)
    except Exception as e:
        logging.error("Error in calculate_distance_between_parallel_lines: " + str(e))
        return float('inf')

def loft_and_add_surface(line1, line2):
    try:
        if not rs.IsLine(line1) or not rs.IsLine(line2):
            logging.error("Invalid input lines for lofting.")
            return

        rhino_line1 = rs.coercecurve(line1)
        rhino_line2 = rs.coercecurve(line2)
        curves_to_loft = [rhino_line1, rhino_line2]
        lofted_surface = Rhino.Geometry.Brep.CreateFromLoft(curves_to_loft, Rhino.Geometry.Point3d.Unset, Rhino.Geometry.Point3d.Unset, Rhino.Geometry.LoftType.Normal, False)[0]
        if lofted_surface:
            if "lofted_surfaces" in sc.sticky:
                sc.sticky["lofted_surfaces"].append(lofted_surface)
            else:
                sc.sticky["lofted_surfaces"] = [lofted_surface]
            sc.doc.Objects.AddBrep(lofted_surface)
            sc.doc.Views.Redraw()
        return lofted_surface
    except Exception as e:
        logging.error("Error in loft_and_add_surface: " + str(e))
        return None

def main():
    try:
        lines_ids = rs.GetObjects("Select lines", rs.filter.curve)
        if not lines_ids:
            logging.info("No lines were selected.")
            return

        for line in lines_ids:
            find_closest_parallel_line(lines_ids, line)
    except Exception as e:
        logging.error("Error in main function: " + str(e))

if __name__ == "__main__":
    main()
