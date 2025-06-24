import { LineChart } from "@mantine/charts";
import { Paper, Stack, Title, Text } from "@mantine/core";

import { formatTimestamp } from "../../util";

interface Ens160Item {
  timestamp: string;
  aqi: number;
  tvoc: number;
  eco2: number;
}

const ens160Series = [
  { name: "aqi", color: "blue.6", yAxisId: "right" },
  { name: "tvoc", color: "red.6" },
  { name: "eco2", color: "green.6" },
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
  const processedEns160Data = ens160Data.map((item: Ens160Item) => ({
    date: formatTimestamp(item.timestamp),
    aqi: item.aqi,
    tvoc: item.tvoc,
    eco2: item.eco2,
  }));

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>ENS160 - Air Quality Index</Title>
        <Text size="sm" c="dimmed">
          AQI | TVOC (ppb) | eCO2 (ppm)
        </Text>
        {isLoading ? (
          <Text>Loading ENS160 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            h={400}
            data={processedEns160Data}
            dataKey="date"
            series={ens160Series}
            curveType="linear"
            withDots={false}
            withRightYAxis
            yAxisProps={{ label: "TVOC (ppb) / eCO2 (ppm)" }}
            xAxisProps={{ label: "Time" }}
            withLegend
          />
        )}
      </Stack>
    </Paper>
  );
};

export default ENS160;
