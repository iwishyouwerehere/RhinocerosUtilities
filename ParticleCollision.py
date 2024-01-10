import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext as sc
import time
import random

def generate_points_in_bounding_box(bbox_corners, count, obj_id):
    bbox = rg.BoundingBox(bbox_corners)
    points = []
    while len(points) < count:
        x = random.uniform(bbox.Min.X, bbox.Max.X)
        y = random.uniform(bbox.Min.Y, bbox.Max.Y)
        z = random.uniform(bbox.Min.Z, bbox.Max.Z)
        pt = rg.Point3d(x, y, z)
        if rs.IsPointInSurface(obj_id, pt) or rs.IsPointInSolid(obj_id, pt):
            points.append(pt)
    return points

def create_point_cloud_in_object_volume(obj_id, point_count=1000):
    bbox_corners = rs.BoundingBox(obj_id)
    if bbox_corners:
        return generate_points_in_bounding_box(bbox_corners, point_count, obj_id)
    else:
        return None

def apply_physics(point, velocity, time_step):
    return point + velocity * time_step

def calculate_collision_response(vel1, vel2, pt1, pt2):
    # Simple elastic collision response for demonstration
    normal = pt1 - pt2
    normal.Unitize()
    vel1_new = vel1 - (2 * normal * (normal.Dot(vel1)))
    vel2_new = vel2 - (2 * normal * (normal.Dot(vel2)))
    return vel1_new, vel2_new

def simulate_step(cloud1, cloud2, velocities1, velocities2, time_step, collision_threshold):
    for i, pt1 in enumerate(cloud1):
        for j, pt2 in enumerate(cloud2):
            if pt1.DistanceTo(pt2) < collision_threshold:
                velocities1[i], velocities2[j] = calculate_collision_response(velocities1[i], velocities2[j], pt1, pt2)

    for i, pt in enumerate(cloud1):
        cloud1[i] = apply_physics(pt, velocities1[i], time_step)

    for i, pt in enumerate(cloud2):
        cloud2[i] = apply_physics(pt, velocities2[i], time_step)

    return cloud1, cloud2

# User selects two objects
object1_id = rs.GetObject("Select the first object")
object2_id = rs.GetObject("Select the second object")

# Convert objects to point clouds within their volume
cloud1_pts = create_point_cloud_in_object_volume(object1_id)
cloud2_pts = create_point_cloud_in_object_volume(object2_id)

# User defines movement vector
start_point = rs.GetPoint("Select the start point of the vector")
end_point = rs.GetPoint("Select the end point of the vector")
movement_vector = rg.Vector3d(end_point - start_point)

# Initial velocities
velocities1 = [movement_vector for _ in cloud1_pts]
velocities2 = [rg.Vector3d(0, 0, 0) for _ in cloud2_pts]

# Simulation parameters
time_step = 0.05  # Adjust as needed
collision_threshold = 0.1  # Adjust based on your scale
total_simulation_time = 10  # Adjust as needed
current_time = 0

while current_time < total_simulation_time:
    cloud1_pts, cloud2_pts = simulate_step(cloud1_pts, cloud2_pts, velocities1, velocities2, time_step, collision_threshold)

    if object1_id: rs.DeleteObject(object1_id)
    if object2_id: rs.DeleteObject(object2_id)
    object1_id = rs.AddPointCloud(cloud1_pts)
    object2_id = rs.AddPointCloud(cloud2_pts)

    rs.Redraw()

    time.sleep(time_step)
    current_time += time_step

print("Simulation complete")
