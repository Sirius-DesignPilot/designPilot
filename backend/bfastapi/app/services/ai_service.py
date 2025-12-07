import httpx  # dış API çağrısı için
from typing import Any

class AIService:
    #Eğitilmiş AI modelini çağırmak için servis.
    MODEL_API_URL = "" #AI modelinin API URL'si

    async def get_prediction(self, input_data: dict) -> Any:
        """Eğitilmiş modelden tahmin sonucu alır."""

        async with httpx.AsyncClient() as client:
            response = await client.post(self.MODEL_API_URL, json=input_data)

        if response.status_code != 200:
            return {"error": "Model service error",
                     "status": response.status_code}

        return response.json()



    

