import { LineChart } from "@mantine/charts";
import { Paper, Stack, Title, Text } from "@mantine/core";

import { formatTimestamp } from "../../util";

interface As7341Item {
  timestamp: string;
  violet: number;
  indigo: number;
  blue: number;
  cyan: number;
  green: number;
  yellow: number;
  orange: number;
  red: number;
  clear: number;
  nir: number;
}

// Process AS7341 data

const as7341Series = [
  { name: "violet", color: "violet.6" },
  { name: "indigo", color: "indigo.6" },
  { name: "blue", color: "blue.6" },
  { name: "cyan", color: "cyan.6" },
  { name: "green", color: "green.6" },
  { name: "yellow", color: "yellow.6" },
  { name: "orange", color: "orange.6" },
  { name: "red", color: "red.6" },
  { name: "clear", color: "gray.6" },
  { name: "nir", color: "gray.6" },
];

const AS7341 = ({
  as7341Data,
  isLoading,
  error,
}: {
  as7341Data: As7341Item[];
  isLoading: boolean;
  error: Error | null;
}) => {
  const processedAs7341Data = as7341Data
    .slice()
    .reverse()
    .map((item: As7341Item) => ({
      date: formatTimestamp(item.timestamp),
      violet: item.violet,
      indigo: item.indigo,
      blue: item.blue,
      cyan: item.cyan,
      green: item.green,
      yellow: item.yellow,
      orange: item.orange,
      red: item.red,
      clear: item.clear,
      nir: item.nir,
    }));

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>AS7341 - Color Sensor</Title>
        <Text size="sm" c="dimmed">
          Spectral channels (counts)
        </Text>
        {isLoading ? (
          <Text>Loading AS7341 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            h={400}
            data={processedAs7341Data}
            dataKey="date"
            series={as7341Series}
            curveType="linear"
            withDots={false}
            yAxisProps={{ label: "Counts" }}
            xAxisProps={{ label: "Time" }}
            withLegend
          />
        )}
      </Stack>
    </Paper>
  );
};

export default AS7341;
