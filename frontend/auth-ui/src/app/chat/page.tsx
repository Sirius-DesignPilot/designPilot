"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  image?: string;
  timestamp: Date;
}

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Merhaba! Ben AI Çizim Asistanınızım. Size nasıl yardımcı olabilirim?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("token");
    router.push("/login");
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setUploadedImage(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const handleSendMessage = async () => {
  if (!input.trim() && !uploadedImage) return;

  const userMessage: Message = {
    id: Date.now().toString(),
    role: "user",
    content: input,
    image: uploadedImage || undefined,
    timestamp: new Date(),
  };

  setMessages((prev) => [...prev, userMessage]);
  setInput("");
  setUploadedImage(null);
  setIsLoading(true);

  try {
    const res = await fetch("http://127.0.0.1:8000/api/v1/ai/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: userMessage.content,
        language: "tr",
      }),
    });

    if (!res.ok) {
      throw new Error("Yanıt alınamadı");
    }

    const data = await res.json();

    const aiMessage: Message = {
      id: Date.now().toString(),
      role: "assistant",
      content:
        data.steps && data.steps.length > 0
          ? data.steps.join("\n")
          : "Herhangi bir çizim adımı oluşturulamadı.",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, aiMessage]);
  } catch (err) {
    const errorMessage: Message = {
      id: Date.now().toString(),
      role: "assistant",
      content: "❌ Sunucudan yanıt alınamadı. Backend çalışıyor mu?",
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, errorMessage]);
  } finally {
    setIsLoading(false);
  }
};


  return (
    // Arka plan rengi Dark Mod uyumlu yapıldı
    <div className="flex flex-col h-screen bg-[#f5f5f0] dark:bg-[#0f172a] transition-colors duration-300">
      
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-slate-700 bg-white/80 dark:bg-[#1e293b]/80 backdrop-blur-md sticky top-0 z-10 transition-colors">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-600 to-orange-600 dark:from-indigo-600 dark:to-blue-600 flex items-center justify-center text-white font-bold text-sm shadow-sm">
              AI
            </div>
            <h1 className="text-base font-medium text-gray-900 dark:text-white">Çizim Asistanı</h1>
          </div>
          <button onClick={handleLogout} className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
            Çıkış
          </button>
        </div>
      </header>

      {/* Mesaj Alanı */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
          <div className="space-y-6">
            {messages.map((message, index) => (
              // animate-fadeIn sınıfı buraya eklendi (style jsx yerine)
              <div
                key={message.id}
                className="group animate-fadeIn"
                style={{ animationDelay: `${index * 0.05}s`, animationFillMode: "backwards" }}
              >
                <div className="flex gap-4">
                  <div className="flex-shrink-0 mt-1">
                    {message.role === "assistant" ? (
                      <div className="w-7 h-7 rounded-md bg-gradient-to-br from-amber-600 to-orange-600 dark:from-indigo-600 dark:to-blue-600 flex items-center justify-center text-white text-xs shadow-sm">AI</div>
                    ) : (
                      <div className="w-7 h-7 rounded-md bg-blue-600 flex items-center justify-center text-white text-xs shadow-sm">U</div>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-baseline gap-2 mb-1">
                      <span className="text-sm font-medium text-gray-900 dark:text-white">
                        {message.role === "assistant" ? "Çizim Asistanı" : "Sen"}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {message.timestamp.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" })}
                      </span>
                    </div>
                    {message.image && (
                      <img src={message.image} alt="Uploaded" className="mb-3 rounded-lg max-w-sm border border-gray-200 dark:border-slate-700" />
                    )}
                    <div className="prose prose-sm max-w-none text-gray-800 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
                      {message.content}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex gap-4 animate-pulse">
                <div className="w-7 h-7 rounded-md bg-gray-300 dark:bg-slate-700"></div>
                <div className="space-y-2">
                  <div className="h-4 w-32 bg-gray-300 dark:bg-slate-700 rounded"></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      {/* Input Alanı */}
      <div className="border-t border-gray-200 dark:border-slate-700 bg-white dark:bg-[#1e293b] transition-colors">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 py-4">
          {uploadedImage && (
            <div className="mb-3 relative inline-block">
              <img src={uploadedImage} alt="Preview" className="max-h-32 rounded-lg border-2 border-gray-200 dark:border-slate-600 shadow-sm" />
              <button onClick={() => setUploadedImage(null)} className="absolute -top-2 -right-2 w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center">×</button>
            </div>
          )}
          <div className="relative flex items-end gap-2">
            <input ref={fileInputRef} type="file" accept="image/*" onChange={handleImageUpload} className="hidden" />
            <button onClick={() => fileInputRef.current?.click()} className="flex-shrink-0 p-2.5 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-slate-700 rounded-lg transition-colors">
              📷
            </button>
            <div className="flex-1 relative">
              <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Mesajınızı yazın..."
                className="w-full resize-none rounded-xl border border-gray-300 dark:border-slate-600 bg-transparent px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 dark:focus:ring-indigo-500 dark:text-white transition-all"
                rows={1}
              />
            </div>
            <button onClick={handleSendMessage} disabled={!input.trim() && !uploadedImage} className="flex-shrink-0 p-2.5 bg-gray-900 dark:bg-indigo-600 text-white rounded-lg hover:bg-gray-700 dark:hover:bg-indigo-500 transition-colors disabled:opacity-40">
              ➤
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}