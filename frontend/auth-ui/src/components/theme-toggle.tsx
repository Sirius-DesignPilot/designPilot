"use client";

import { useState, useEffect } from "react";
import { useTheme } from "next-themes";

export default function ThemeToggle() {
  const [mounted, setMounted] = useState(false);
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  const toggle = () => setTheme(theme === "light" ? "dark" : "light");

  return (
    <button
      onClick={toggle}
      className="fixed top-4 right-4 px-4 py-2 rounded bg-gray-200 text-black dark:bg-darkblue-button dark:text-white"
    >
      {theme === "light" ? "Koyu Tema" : "Açık Tema"}
    </button>
  );
}
