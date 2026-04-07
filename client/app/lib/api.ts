import axios from "axios";

export type DocumentRecord = {
  doc_id: string;
  filename: string;
  status: string;
  chunk_count: number;
  uploaded_at: string;
};

export type QuerySource = {
  doc_id: string;
  chunk_id: string;
  text: string;
  page: number | null;
  score: number;
};

export type QueryResponse = {
  answer: string;
  sources: QuerySource[];
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
});

export async function uploadPdf(file: File): Promise<DocumentRecord> {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post<{ document: DocumentRecord }>("/api/pdf/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return data.document;
}

export async function listDocuments(): Promise<DocumentRecord[]> {
  const { data } = await api.get<{ documents: DocumentRecord[] }>("/api/pdf/documents");
  return data.documents;
}

export async function deleteDocument(docId: string): Promise<void> {
  await api.delete(`/api/pdf/documents/${docId}`);
}

export async function searchQuery(query: string, topK = 3): Promise<QueryResponse> {
  const { data } = await api.post<QueryResponse>("/api/chat/query", {
    query,
    top_k: topK,
  });
  return data;
}
