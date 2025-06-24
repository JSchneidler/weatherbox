import { LineChart } from "@mantine/charts";
import { Paper, Stack, Title, Text } from "@mantine/core";

import { formatTimestamp } from "../../util";

interface Sps30Item {
  timestamp: string;
  pm10: number;
  pm25: number;
  pm40: number;
  pm100: number;
  nc05: number;
  nc10: number;
  nc25: number;
  nc40: number;
  nc100: number;
  typical_particle_size: number;
}

const sps30Series = [
  { name: "pm10", color: "blue.6" },
  { name: "pm25", color: "red.6" },
  { name: "pm40", color: "green.6" },
  { name: "pm100", color: "yellow.6" },
  { name: "nc05", color: "purple.6" },
  { name: "nc10", color: "pink.6" },
  { name: "nc25", color: "orange.6" },
  { name: "nc40", color: "red.6" },
  { name: "nc100", color: "green.6" },
  { name: "typical_particle_size", color: "gray.6", yAxisId: "right" },
];

const SPS30 = ({
  sps30Data,
  isLoading,
  error,
}: {
  sps30Data: Sps30Item[];
  isLoading: boolean;
  error: Error | null;
}) => {
  const processedSps30Data = sps30Data
    .slice()
    .reverse()
    .map((item: Sps30Item) => ({
      date: formatTimestamp(item.timestamp),
      pm10: item.pm10,
      pm25: item.pm25,
      pm40: item.pm40,
      pm100: item.pm100,
      nc05: item.nc05,
      nc10: item.nc10,
      nc25: item.nc25,
      nc40: item.nc40,
      nc100: item.nc100,
      typical_particle_size: item.typical_particle_size,
    }));

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>SPS30 - Air Quality Sensor</Title>
        <Text size="sm" c="dimmed">
          PM10, PM2.5, PM4.0, PM1.0 (μg/m³) | Particle Counts (#/cm³) | Typical
          Particle Size (μm)
        </Text>
        {isLoading ? (
          <Text>Loading SPS30 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            h={400}
            data={processedSps30Data}
            dataKey="date"
            series={sps30Series}
            curveType="linear"
            withDots={false}
            withRightYAxis
            yAxisProps={{ label: "PM Values (μg/m³)" }}
            xAxisProps={{ label: "Time" }}
            withLegend
          />
        )}
      </Stack>
    </Paper>
  );
};

export default SPS30;
