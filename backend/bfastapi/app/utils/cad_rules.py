

from typing import Dict, List, Any
import math


class CADRuleEngine:
    """
    DWG + IMAGE geometri verilerine göre hata tespit sistemi.
    DWGParser ve ImageAnalyzer ile uyumlu çalışır.
    """

    def __init__(self):
       
        self.expected_layers = {"A-WALL", "A-DOOR", "A-WINDOW", "A-GRID"}

        
        self.merge_tolerance = 5        # pixel/mm toleransı
        self.perpendicular_tolerance = 10  # derece tolerans
        self.parallel_tolerance = 5

    
    def _line_angle(self, line):
        """Bir çizginin açısını derece cinsinden döndürür."""
        x1, y1 = line["start"]
        x2, y2 = line["end"]
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        return abs(angle)

    def _distance(self, p1, p2):
        """İki nokta arası mesafe."""
        return math.dist(p1, p2)

   
    def check_closed_polygons(self, polygons: List[Dict]) -> List[str]:
        errors = []

        for poly in polygons:
            pts = poly["points"]

            if len(pts) < 3:
                errors.append("Polygon has less than 3 points (not a valid room/area).")
                continue

            
            area = 0
            for i in range(len(pts)):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % len(pts)]
                area += x1 * y2 - x2 * y1
            area = abs(area) / 2

            if area < 100:
                errors.append(f"Polygon area too small ({area:.2f}) — might be noise.")

            if area > 1_000_000:
                errors.append(f"Polygon area too large ({area:.2f}) — geometry unrealistic.")

        return errors

    def check_line_continuity(self, lines: List[Dict]) -> List[str]:
        errors = []

        for i, l1 in enumerate(lines):
            for j, l2 in enumerate(lines):
                if i >= j:
                    continue

                
                if self._distance(l1["end"], l2["start"]) < self.merge_tolerance:
                    continue

                
                angle1 = self._line_angle(l1)
                angle2 = self._line_angle(l2)

                if abs(angle1 - angle2) < self.parallel_tolerance:
                    gap = self._distance(l1["end"], l2["start"])
                    if gap > self.merge_tolerance and gap < 50:
                        errors.append(
                            f"Possible wall gap: {gap:.1f} px between lines #{i} and #{j}"
                        )

        return errors

    def check_parallel_and_perpendicular(self, lines: List[Dict]) -> List[str]:
        errors = []

        for i, l1 in enumerate(lines):
            angle1 = self._line_angle(l1)
            for j, l2 in enumerate(lines):
                if i >= j:
                    continue

                angle2 = self._line_angle(l2)
                diff = abs(angle1 - angle2)

                
                if diff < self.parallel_tolerance:
                    pass 

                
                elif abs(diff - 90) < self.perpendicular_tolerance:
                    pass  # normal

                else:
                    errors.append(
                        f"Angle mismatch ({angle1:.1f}° vs {angle2:.1f}°): walls not parallel/perpendicular."
                    )

        return errors

    def check_layer_rules(self, layers: List[str]) -> List[str]:
        """DWG dosyalarında layer standardı uygulanmış mı?"""
        errors = []

        for layer in layers:
            if layer.upper() not in self.expected_layers:
                errors.append(f"Non-standard layer detected: {layer}")

        return errors
    

    def check_duplicate_lines(self, lines: List[Dict]) -> List[str]:
        """Üst üste binen veya aynı olan çizgileri bulur."""
        errors = []

        for i, l1 in enumerate(lines):
          for j, l2 in enumerate(lines):
            if i >= j: continue
            if (l1["start"] == l2["start"] and l1["end"] == l2["end"]) or \
               (l1["start"] == l2["end"] and l1["end"] == l2["start"]):
                errors.append(f"Duplicate line detected between #{i} and #{j}")
    
        return errors



    def check_ortho_mode(self, lines: List[Dict]) -> List[str]:
        """Çizgilerin tam dikey veya tam yatay olup olmadığını denetler (Ortho Mode)."""
        errors = []
        for i, line in enumerate(lines):
          angle = self._line_angle(line) % 90
          if 0.5 < angle < 89.5: # 0.5 dereceden fazla sapma varsa
            errors.append(f"Line #{i} is slightly off-axis (Angle: {angle:.2f}°)")
        return errors
    

    
    def evaluate(self, geometry_json: Dict[str, Any]) -> List[str]:

        errors = []

        
        if "polygons" in geometry_json["entities"]:
            errors += self.check_closed_polygons(geometry_json["entities"]["polygons"])

        # LINES
        lines = geometry_json["entities"].get("lines", [])
        if lines:
            errors += self.check_line_continuity(lines)
            errors += self.check_parallel_and_perpendicular(lines)

        # DWG layer rules
        if "layers" in geometry_json:
            errors += self.check_layer_rules(geometry_json["layers"])

        return errors
