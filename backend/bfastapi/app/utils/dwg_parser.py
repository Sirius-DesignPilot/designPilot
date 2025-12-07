import os
import tempfile
import ezdxf
from typing import Dict, Any,List
from fastapi import HTTPException, status, UploadFile

class DWGParser:

    def __init__(self):
        self.temp_dir=tempfile.gettempdir()


    def _save_temp_file(self,file:UploadFile)->str:
        file_ext=os.path.splitext(file.filename)[1].lower()
        if file_ext not in [".dwg",".dxf"]:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported DWG type: {file_ext}"


            )
        
        temp_path=os.path.join(self.temp_dir,file.filename)

        with open(temp_path,"wb") as buffer:
            buffer.write(file.file.read())

        file.file.seek(0)

        return temp_path
    def parse(self,file:UploadFile)->Dict[str,Any]:
        temp_path=self._save_temp_file(file)

        try:
            doc=ezdxf.readfile(temp_path)
            msp=doc.modelspace()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading DWG/DXF: {str(e)}",
            )
        lines=[]
        circles=[]
        arcs=[]
        polylines=[]
        layers=set()

        for entity in msp:
            layers.add(entity.dxf.layer)

            if entity.dsxftype()=="LINE":
                lines.append({
                    "start":[entity.dxf.start.x,entity.dxf.start.y],
                    "end":[entity.dxf.end.x,entity.dxf.end.y],
                    "layer":entity.dxf.layer
                })

            elif entity.dxftype() in ["LWPOLYLİNE","POLYLİNE"]:
                points=[[point[0],point[1]] for point in entity.get_points()]
                polylines.append({
                    "points":points,
                    "is_closed":entity.closed,
                    "layer":entity.dxf.layer
                })
            elif entity.dxftype()=="CIRCLE":
                circles.append({
                    "center":[entity.dxf.center.x,entity.dxf.center.y],
                    "radius":entity.dxf.radius,
                    "layer":entity.dxf.layer
                })
            elif entity.dxftype()=="ARC":
                arcs.append({
                    "center":[entity.dxf.center.x,entity.dxf.center.y],
                    "radius":entity.dxf.radius,
                    "start_angle":entity.dxf.start_angle,
                    "end_angle":entity.dxf.end_angle,
                    "layer":entity.dxf.layer
                })


        parsed={
            "layers":list(layers),
            "entities":{
                "lines":lines,
                "circles":circles,
                "arcs":arcs,
                "polylines":polylines
            },
            "statistics":{
                "line_count":len(lines),
                "polyline_count":len(polylines),
                "circle_count":len(circles),
                "arc_count":len(arcs)
            }
        }

        try:
            os.remove(temp_path)
        except Exception:
            pass


        return parsed

