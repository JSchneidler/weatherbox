import { LineChart } from "@mantine/charts";
import { Paper, Stack, Title, Text } from "@mantine/core";

import { formatTimestamp } from "../../util";

interface Ltr390Item {
  timestamp: string;
  light: number;
  uvs: number;
}

const ltr390Series = [
  { name: "light", color: "blue.6" },
  { name: "uvs", color: "red.6", yAxisId: "right" },
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
  const processedLtr390Data = ltr390Data.map((item: Ltr390Item) => ({
    date: formatTimestamp(item.timestamp),
    light: item.light,
    uvs: item.uvs,
  }));

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>LTR390 - Light & UV Sensor</Title>
        <Text size="sm" c="dimmed">
          Light (lux) | UV Index
        </Text>
        {isLoading ? (
          <Text>Loading LTR390 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            h={400}
            data={processedLtr390Data}
            dataKey="date"
            series={ltr390Series}
            curveType="linear"
            withDots={false}
            withRightYAxis
            yAxisProps={{ label: "Light (lux)" }}
            xAxisProps={{ label: "Time" }}
            withLegend
          />
        )}
      </Stack>
    </Paper>
  );
};

export default LTR390;
