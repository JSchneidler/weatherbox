import { LineChart } from "@mantine/charts";
import { Paper, Stack, Title, Text } from "@mantine/core";

import { formatTimestamp } from "../../util";

interface Bme688Item {
  timestamp: string;
  temperature: number;
  humidity: number;
  pressure: number;
  gas: number;
}

const bme688Series = [
  { name: "temperature", color: "blue.6" },
  { name: "humidity", color: "red.6" },
  { name: "pressure", color: "green.6", yAxisId: "right" },
  // { name: "gas", color: "gray.6", yAxisId: "right" },
];

const BME688 = ({
  bme688Data,
  isLoading,
  error,
}: {
  bme688Data: Bme688Item[];
  isLoading: boolean;
  error: Error | null;
}) => {
  const processedBme688Data = bme688Data.map((item: Bme688Item) => ({
    date: formatTimestamp(item.timestamp),
    temperature: item.temperature,
    humidity: item.humidity,
    pressure: item.pressure,
    gas: item.gas,
  }));

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>BME688 - Environmental Sensor</Title>
        <Text size="sm" c="dimmed">
          Temperature (°C) | Humidity (%) | Pressure (hPa)
        </Text>
        {isLoading ? (
          <Text>Loading BME688 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            h={400}
            data={processedBme688Data}
            dataKey="date"
            series={bme688Series}
            curveType="linear"
            withDots={false}
            withRightYAxis
            yAxisProps={{ label: "Temperature (°C) / Humidity (%)" }}
            xAxisProps={{ label: "Time" }}
            withLegend
          />
        )}
      </Stack>
    </Paper>
  );
};

export default BME688;
