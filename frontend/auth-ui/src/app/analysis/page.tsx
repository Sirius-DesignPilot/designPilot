'use client';

import { FormEvent, useState } from 'react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

type AnalysisResponse = {
  result: string;
  confidence?: number | null;
};

export default function AnalysisPage() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/analyze/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const { detail } = await response.json();
        throw new Error(detail || 'Bir hata oluştu');
      }

      const data = (await response.json()) as AnalysisResponse;
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Beklenmeyen bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center bg-gray-100 p-6 text-gray-900">
      <div className="w-full max-w-2xl rounded-lg bg-white p-8 shadow-lg shadow-gray-400">
        <h1 className="text-2xl font-bold text-center mb-4">Metin Analizi</h1>
        <p className="text-center text-sm text-gray-600 mb-6">
          Girilen metni backend API&apos;ye iletip AI servisinden dönen sonucu gösterir.
        </p>

        <form className="space-y-4" onSubmit={onSubmit}>
          <label className="block text-sm font-medium text-gray-700">Analiz edilecek metin</label>
          <textarea
            className="w-full rounded border border-gray-300 p-3 focus:border-blue-500 focus:outline-none"
            rows={6}
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Metni buraya yazın"
            required
          />

          <button
            type="submit"
            className="w-full rounded bg-blue-600 py-2 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
            disabled={loading}
          >
            {loading ? 'Analiz ediliyor...' : 'Analizi Başlat'}
          </button>
        </form>

        {error && <p className="mt-4 rounded bg-red-100 p-3 text-red-700">{error}</p>}

        {result && (
          <div className="mt-6 rounded border border-gray-200 bg-gray-50 p-4">
            <h2 className="mb-2 text-lg font-semibold">Sonuç</h2>
            <p className="whitespace-pre-line text-gray-800">{result.result}</p>
            {typeof result.confidence === 'number' && (
              <p className="mt-2 text-sm text-gray-600">Güven skoru: {result.confidence.toFixed(2)}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
