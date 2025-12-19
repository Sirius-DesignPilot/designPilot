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
    

    def parse(self, file: UploadFile) -> Dict[str, Any]:
        temp_path = self._save_temp_file(file)

        try:
            doc = ezdxf.readfile(temp_path)
            msp = doc.modelspace()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error reading DWG/DXF: {str(e)}",
            )
            
        lines, circles, arcs, polylines = [], [], [], []
        layers = set()
        blocks, texts = [], []

        for entity in msp:
            layers.add(entity.dxf.layer)

            # Çizgi Analizi
            if entity.dxftype() == "LINE":
                lines.append({
                    "start": [entity.dxf.start.x, entity.dxf.start.y],
                    "end": [entity.dxf.end.x, entity.dxf.end.y],
                    "layer": entity.dxf.layer
                })

            # Poligon Analizi
            elif entity.dxftype() in ["LWPOLYLINE", "POLYLINE"]:
                points = [[point[0], point[1]] for point in entity.get_points()]
                polylines.append({
                    "points": points,
                    "is_closed": entity.closed,
                    "layer": entity.dxf.layer
                })

            # Blok Analizi (Kapı, Pencere vb.)
            elif entity.dxftype() == "INSERT":
                blocks.append({
                    "name": entity.dxf.name,
                    "insert": [entity.dxf.insert.x, entity.dxf.insert.y],
                    "layer": entity.dxf.layer,
                    "rotation": entity.dxf.rotation
                })

            # Metin Analizi (Oda isimleri vb.)
            elif entity.dxftype() in ["TEXT", "MTEXT"]:
                texts.append({ # BURASI DÜZELTİLDİ: parse.append yerine texts.append
                    "content": entity.plain_text() if hasattr(entity, 'plain_text') else entity.dxf.text,
                    "insert": [entity.dxf.insert.x, entity.dxf.insert.y],
                    "layer": entity.dxf.layer
                })
        
        # Sonuç Sözlüğünü Oluşturma
        parsed_result = { # BURASI DÜZELTİLDİ: Fonksiyon ismiyle çakışmaması için parsed_result kullanıldı
            "layers": list(layers),
            "entities": {
                "lines": lines,
                "circles": circles,
                "arcs": arcs,
                "polylines": polylines,
                "blocks": blocks,
                "texts": texts
            },
            "statistics": {
                "line_count": len(lines),
                "block_count": len(blocks),
                "text_count": len(texts)
            }
        }

        if os.path.exists(temp_path):
            os.remove(temp_path)

        return parsed_result
    


    