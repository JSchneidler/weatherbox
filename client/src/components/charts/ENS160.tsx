import { Paper, Stack, Title, Text } from "@mantine/core";

import LineChart from "./LineChart";
import { formatTimestamp } from "../../util";
import { memo, useMemo } from "react";

interface Ens160Item {
  timestamp: string;
  aqi: number;
  tvoc: number;
  eco2: number;
}

const ens160Series = [
  { key: "aqi", name: "AQI", color: "rgb(255, 193, 7)", yAxisID: "y1" }, // Light mode: rgb(255, 152, 0)
  { key: "tvoc", name: "TVOC (ppb)", color: "rgb(156, 39, 176)" }, // Light mode: rgb(142, 36, 170)
  { key: "eco2", name: "eCO2 (ppm)", color: "rgb(76, 175, 80)" }, // Light mode: rgb(56, 142, 60)
];

const ENS160 = ({
  ens160Data,
  isLoading,
  error,
}: {
  ens160Data: Ens160Item[];
  isLoading: boolean;
  error: Error | null;
}) => {
  const processedEns160Data = useMemo(
    () =>
      ens160Data.map((item: Ens160Item) => ({
        date: formatTimestamp(item.timestamp),
        ...item,
      })),
    [ens160Data]
  );

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>ENS160 - Air Quality</Title>
        {isLoading ? (
          <Text>Loading ENS160 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            labels={processedEns160Data.map((data) => data.date)}
            data={ens160Series.map((series) => ({
              label: series.name,
              data: processedEns160Data.map((data) => data[series.key]),
              borderColor: series.color,
              yAxisID: series.yAxisID,
            }))}
          />
        )}
      </Stack>
    </Paper>
  );
};

export default memo(ENS160);
