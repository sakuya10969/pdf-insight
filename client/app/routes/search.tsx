import { useState } from "react";
import {
  Badge,
  Button,
  Card,
  Group,
  Loader,
  Stack,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { useMutation } from "@tanstack/react-query";

import { searchQuery } from "~/lib/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");

  const searchMutation = useMutation({
    mutationFn: (q: string) => searchQuery(q, 3),
  });

  return (
    <Stack gap="lg">
      <Title order={2}>検索・チャット</Title>

      <Card withBorder radius="md">
        <Group align="end" gap="sm">
          <TextInput
            label="質問"
            placeholder="この資料で説明されている主要な要点は？"
            value={query}
            onChange={(event) => setQuery(event.currentTarget.value)}
            style={{ flex: 1 }}
          />
          <Button
            onClick={() => searchMutation.mutate(query)}
            disabled={!query.trim()}
            loading={searchMutation.isPending}
          >
            検索
          </Button>
        </Group>
      </Card>

      {searchMutation.isPending && (
        <Group>
          <Loader size="sm" />
          <Text size="sm">検索中...</Text>
        </Group>
      )}

      {searchMutation.data && (
        <Stack gap="md">
          <Card withBorder radius="md">
            <Text fw={700} mb="xs">
              LLM回答
            </Text>
            <Text>{searchMutation.data.answer}</Text>
          </Card>

          <Stack gap="sm">
            <Text fw={700}>参照ソース</Text>
            {searchMutation.data.sources.map((source) => (
              <Card key={`${source.doc_id}:${source.chunk_id}`} withBorder radius="md">
                <Group justify="space-between" mb="xs">
                  <Badge color="cyan">{source.doc_id.slice(0, 8)}</Badge>
                  <Text size="xs" c="dimmed">
                    score: {source.score.toFixed(3)}
                  </Text>
                </Group>
                <Text size="sm">{source.text}</Text>
              </Card>
            ))}
            {!searchMutation.data.sources.length && (
              <Text size="sm" c="dimmed">
                参照ソースはありません。
              </Text>
            )}
          </Stack>
        </Stack>
      )}
    </Stack>
  );
}
