import {
  ActionIcon,
  Badge,
  Card,
  Group,
  Loader,
  Stack,
  Table,
  Text,
  Title,
  Tooltip,
} from "@mantine/core";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { deleteDocument, listDocuments } from "~/lib/api";

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

export default function DocumentsPage() {
  const queryClient = useQueryClient();
  const documentsQuery = useQuery({
    queryKey: ["documents"],
    queryFn: listDocuments,
  });

  const deleteMutation = useMutation({
    mutationFn: deleteDocument,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
  });

  return (
    <Stack gap="lg">
      <Title order={2}>ドキュメント管理</Title>

      <Card withBorder radius="md">
        {documentsQuery.isLoading ? (
          <Group>
            <Loader size="sm" />
            <Text size="sm">読み込み中...</Text>
          </Group>
        ) : (
          <Table.ScrollContainer minWidth={780}>
            <Table striped highlightOnHover>
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>ファイル名</Table.Th>
                  <Table.Th>ステータス</Table.Th>
                  <Table.Th>チャンク数</Table.Th>
                  <Table.Th>アップロード日時</Table.Th>
                  <Table.Th>操作</Table.Th>
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
                    <Table.Td>
                      <Tooltip label="削除">
                        <ActionIcon
                          color="red"
                          variant="light"
                          onClick={() => deleteMutation.mutate(doc.doc_id)}
                          loading={deleteMutation.isPending}
                          aria-label="削除"
                        >
                          ×
                        </ActionIcon>
                      </Tooltip>
                    </Table.Td>
                  </Table.Tr>
                ))}
                {!documentsQuery.data?.length && (
                  <Table.Tr>
                    <Table.Td colSpan={5}>
                      <Text size="sm" c="dimmed">
                        管理対象のドキュメントはありません。
                      </Text>
                    </Table.Td>
                  </Table.Tr>
                )}
              </Table.Tbody>
            </Table>
          </Table.ScrollContainer>
        )}
      </Card>
    </Stack>
  );
}
