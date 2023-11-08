from json import JSONEncoder

class DetectionJSONEncoder(JSONEncoder):
    def default(self, obj):
        ret = {}
        ret["label_id"] = obj.label_id[0]
        ret["score"] = obj.score[0]
        
        location_object = {}
        location_object["format"] = obj.location_data.format
        location_object["relative_bounding_box"] = {
            "xmin":obj.location_data.relative_bounding_box.xmin,
            "ymin":obj.location_data.relative_bounding_box.ymin,
            "width":obj.location_data.relative_bounding_box.width,
            "height":obj.location_data.relative_bounding_box.height,
        }
        
        temp = []
        for keypoint in obj.location_data.relative_keypoints:
            temp.append({"x":keypoint.x,"y":keypoint.y})
        location_object["relative_keypoints"] = temp
        
        ret["location_data"] = location_object
        return ret

