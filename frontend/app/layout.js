import "./globals.css";
export const metadata = {
  title: "RAG + Teophilo | Cucando TI",
  description: "Laboratório didático de recuperação e geração",
};
export default function Layout({ children }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
