#https://discourse.mcneel.com/t/similar-objects/169361/11
def compare_breps(brep1, brep2):
    def get_largest_face(brep):
        
        largest_face = max(brep.Faces, key=lambda face: rg.AreaMassProperties.Compute(face).Area)
        return largest_face

    def get_distances_to_centroid(face):
        
        centroid = rg.AreaMassProperties.Compute(face).Centroid
        
        distances = [round(trim.Edge.EdgeCurve.PointAtStart.DistanceTo(centroid))
                     for loop in face.Loops for trim in loop.Trims]
        distances += [round(trim.Edge.EdgeCurve.PointAtEnd.DistanceTo(centroid))
                      for loop in face.Loops for trim in loop.Trims]
        return sorted(distances)


    return get_distances_to_centroid(get_largest_face(brep1)) == get_distances_to_centroid(get_largest_face(brep2))
