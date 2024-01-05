#https://discourse.mcneel.com/t/need-help-to-recreate-move-command-with-custom-direction/172543
import rhinoscriptsyntax as rs
def custom_move():
    obj_id = rs.GetObject("Select object to move")
    if not obj_id:
        return
    start_point = rs.GetPoint("Pick the start point of the vector")
    if not start_point:
        return
    end_point = rs.GetPoint("Pick the end point of the vector")
    if not end_point:
        return
    direction_vector = rs.VectorCreate(end_point, start_point)
    distance = rs.GetReal("Enter distance to move")
    move_vector = rs.VectorScale(rs.VectorUnitize(direction_vector), distance)
    rs.MoveObject(obj_id, move_vector)
custom_move()

