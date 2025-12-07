# utils/image_analyzer.py

import cv2
import numpy as np
from typing import Dict, Any, List
from fastapi import UploadFile, HTTPException, status
import tempfile
import os


class ImageAnalyzer:
    """
    Görsel CAD çizimlerinden (PNG/JPG/HEIC/WebP)
    çizgi, kontur ve basit geometri çıkaran modül.
    DWG parser ile aynı formatta JSON üretir.
    """

    def __init__(self):
        self.temp_dir = tempfile.gettempdir()

    def _save_temp_image(self, file: UploadFile) -> str:
        """Gelen görüntüyü geçici klasöre kaydeder."""
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in [".png", ".jpg", ".jpeg", ".webp", ".heic"]:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported image format"
            )

        tmp_path = os.path.join(self.temp_dir, file.filename)

        with open(tmp_path, "wb") as buffer:
            buffer.write(file.file.read())

        file.file.seek(0)

        return tmp_path

    def analyze(self, file: UploadFile) -> Dict[str, Any]:
        """Ana image analiz fonksiyonu."""
        img_path = self._save_temp_image(file)

        # 1) Görseli yükle
        img = cv2.imread(img_path)
        if img is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to read image"
            )

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 2) Kenar bulma (Canny)
        edges = cv2.Canny(gray, threshold1=80, threshold2=150)

        # 3) Çizgi tespiti (HoughLinesP)
        raw_lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=60,
            minLineLength=40,
            maxLineGap=10
        )

        lines = []
        if raw_lines is not None:
            for line in raw_lines:
                x1, y1, x2, y2 = line[0]
                lines.append({
                    "start": [int(x1), int(y1)],
                    "end": [int(x2), int(y2)]
                })

        # 4) Kontur bulma → alan/oda tespiti
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        polygons = []
        for cnt in contours:
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) >= 3:  # en az üçgen
                poly_points = [[int(p[0][0]), int(p[0][1])] for p in approx]
                polygons.append({
                    "points": poly_points,
                    "is_closed": True
                })

        # 5) Basit daire tespiti (HoughCircles)
        circles = []
        try:
            detected = cv2.HoughCircles(
                gray,
                cv2.HOUGH_GRADIENT,
                dp=1.2,
                minDist=30,
                param1=80,
                param2=35,
                minRadius=10,
                maxRadius=300
            )
            if detected is not None:
                detected = np.round(detected[0, :]).astype("int")
                for (x, y, r) in detected:
                    circles.append({
                        "center": [int(x), int(y)],
                        "radius": int(r)
                    })
        except:
            pass

        # 6) JSON çıktısı
        result = {
            "source_type": "image",
            "entities": {
                "lines": lines,
                "polygons": polygons,
                "circles": circles,
            },
            "statistics": {
                "line_count": len(lines),
                "polygon_count": len(polygons),
                "circle_count": len(circles),
                "image_width": img.shape[1],
                "image_height": img.shape[0],
            },
            "scale_estimated": False  # Görsellerde ölçek bilinmez
        }

        # geçici dosya sil
        try:
            os.remove(img_path)
        except:
            pass

        return result
