import { useMemo } from "react";
import {
  Badge,
  Button,
  Card,
  Group,
  Loader,
  Stack,
  Table,
  Text,
  Title,
} from "@mantine/core";
import { useDropzone } from "react-dropzone";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { listDocuments, uploadPdf } from "~/lib/api";

function statusColor(status: string): string {
  switch (status) {
    case "ready":
      return "teal";
    case "processing":
      return "blue";
    case "failed":
      return "red";
    default:
      return "gray";
  }
}

export default function UploadPage() {
  const queryClient = useQueryClient();
  const documentsQuery = useQuery({
    queryKey: ["documents"],
    queryFn: listDocuments,
  });

  const uploadMutation = useMutation({
    mutationFn: uploadPdf,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
  });

  const onDrop = useMemo(
    () => (acceptedFiles: File[]) => {
      const [first] = acceptedFiles;
      if (first) {
        uploadMutation.mutate(first);
      }
    },
    [uploadMutation]
  );

  const dropzone = useDropzone({
    onDrop,
    maxFiles: 1,
    accept: {
      "application/pdf": [".pdf"],
    },
  });

  return (
    <Stack gap="lg">
      <Title order={2}>PDFアップロード</Title>

      <Card withBorder radius="md" className="hero-card" {...dropzone.getRootProps()}>
        <input {...dropzone.getInputProps()} />
        <Stack align="center" gap="xs" py="lg">
          <Text fw={600}>PDFをドラッグ&ドロップ</Text>
          <Text size="sm" c="dimmed">
            またはクリックしてファイルを選択
          </Text>
          <Button variant="light">PDFを選択</Button>
        </Stack>
      </Card>

      {uploadMutation.isPending && (
        <Group gap="sm">
          <Loader size="sm" />
          <Text size="sm">アップロードを処理中です...</Text>
        </Group>
      )}

      {uploadMutation.isError && (
        <Text c="red" size="sm">
          アップロードに失敗しました。サーバー状態を確認してください。
        </Text>
      )}

      <Card withBorder radius="md">
        <Stack gap="sm">
          <Group justify="space-between">
            <Title order={4}>ドキュメント一覧</Title>
            <Button
              variant="subtle"
              size="xs"
              onClick={() => documentsQuery.refetch()}
              loading={documentsQuery.isFetching}
            >
              再取得
            </Button>
          </Group>

          <Table.ScrollContainer minWidth={700}>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>ファイル名</Table.Th>
                  <Table.Th>ステータス</Table.Th>
                  <Table.Th>チャンク数</Table.Th>
                  <Table.Th>アップロード日時</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {(documentsQuery.data ?? []).map((doc) => (
                  <Table.Tr key={doc.doc_id}>
                    <Table.Td>{doc.filename}</Table.Td>
                    <Table.Td>
                      <Badge color={statusColor(doc.status)}>{doc.status}</Badge>
                    </Table.Td>
                    <Table.Td>{doc.chunk_count}</Table.Td>
                    <Table.Td>{new Date(doc.uploaded_at).toLocaleString("ja-JP")}</Table.Td>
                  </Table.Tr>
                ))}
                {!documentsQuery.data?.length && (
                  <Table.Tr>
                    <Table.Td colSpan={4}>
                      <Text size="sm" c="dimmed">
                        ドキュメントはまだありません。
                      </Text>
                    </Table.Td>
                  </Table.Tr>
                )}
              </Table.Tbody>
            </Table>
          </Table.ScrollContainer>
        </Stack>
      </Card>
    </Stack>
  );
}
