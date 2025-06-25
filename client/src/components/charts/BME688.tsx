import { Paper, Stack, Title, Text } from "@mantine/core";

import LineChart from "./LineChart";
import { formatTimestamp } from "../../util";
import { memo, useMemo } from "react";

interface Bme688Item {
  timestamp: string;
  temperature: number;
  humidity: number;
  pressure: number;
  gas: number;
}

const bme688Series = [
  { key: "temperature", name: "Temperature (°C)", color: "rgb(255, 87, 51)" }, // Light mode: rgb(255, 69, 0)
  { key: "humidity", name: "Humidity (%)", color: "rgb(30, 144, 255)" }, // Light mode: rgb(70, 130, 180)
  {
    key: "pressure",
    name: "Pressure (hPa)",
    color: "rgb(106, 90, 205)", // Light mode: rgb(123, 104, 238)
    yAxisID: "y1",
  },
  // { key: "gas", name: "Gas (Ω)", color: "rgb(255, 165, 0)", yAxisId: "right" }, // Light mode: rgb(255, 140, 0)
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
  const processedBme688Data = useMemo(
    () =>
      bme688Data.map((item: Bme688Item) => ({
        date: formatTimestamp(item.timestamp),
        ...item,
      })),
    [bme688Data]
  );

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>BME688 - Environmental Sensor</Title>
        {isLoading ? (
          <Text>Loading BME688 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            labels={processedBme688Data.map((data) => data.date)}
            data={bme688Series.map((series) => ({
              label: series.name,
              data: processedBme688Data.map((data) => data[series.key]),
              borderColor: series.color,
              yAxisID: series.yAxisID,
            }))}
          />
        )}
      </Stack>
    </Paper>
  );
};

export default memo(BME688);
