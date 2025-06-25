import { Paper, Stack, Title, Text } from "@mantine/core";

import LineChart from "./LineChart";
import { formatTimestamp } from "../../util";
import { memo, useMemo } from "react";

interface Ltr390Item {
  timestamp: string;
  light: number;
  uvs: number;
}

const ltr390Series = [
  { key: "light", name: "Light (lux)", color: "rgb(186, 85, 211)" }, // Light mode: rgb(147, 112, 219)
  { key: "uvs", name: "UVS", color: "rgb(255, 235, 59)", yAxisID: "y1" }, // Light mode: rgb(255, 193, 7)
];

const LTR390 = ({
  ltr390Data,
  isLoading,
  error,
}: {
  ltr390Data: Ltr390Item[];
  isLoading: boolean;
  error: Error | null;
}) => {
  const processedLtr390Data = useMemo(
    () =>
      ltr390Data.map((item: Ltr390Item) => ({
        date: formatTimestamp(item.timestamp),
        ...item,
      })),
    [ltr390Data]
  );

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>LTR390 - Light & UV</Title>
        {isLoading ? (
          <Text>Loading LTR390 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            labels={processedLtr390Data.map((data) => data.date)}
            data={ltr390Series.map((series) => ({
              label: series.name,
              data: processedLtr390Data.map((data) => data[series.key]),
              borderColor: series.color,
              yAxisID: series.yAxisID,
            }))}
          />
        )}
      </Stack>
    </Paper>
  );
};

export default memo(LTR390);
