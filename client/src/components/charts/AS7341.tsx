import { Paper, Stack, Title, Text } from "@mantine/core";

import LineChart from "./LineChart";
import { formatTimestamp } from "../../util";
import { memo, useMemo } from "react";

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

const as7341Series = [
  { key: "violet", name: "Violet (415nm)", color: "rgb(138, 43, 226)" }, // Light mode: rgb(148, 0, 211)
  { key: "indigo", name: "Indigo (445nm)", color: "rgb(75, 0, 130)" }, // Light mode: rgb(75, 0, 130)
  { key: "blue", name: "Blue (480nm)", color: "rgb(0, 100, 255)" }, // Light mode: rgb(30, 144, 255)
  { key: "cyan", name: "Cyan (515nm)", color: "rgb(0, 191, 255)" }, // Light mode: rgb(0, 206, 209)
  { key: "green", name: "Green (555nm)", color: "rgb(34, 139, 34)" }, // Light mode: rgb(50, 205, 50)
  { key: "yellow", name: "Yellow (590nm)", color: "rgb(255, 215, 0)" }, // Light mode: rgb(255, 165, 0)
  { key: "orange", name: "Orange (630nm)", color: "rgb(255, 140, 0)" }, // Light mode: rgb(255, 99, 71)
  { key: "red", name: "Red (680nm)", color: "rgb(220, 20, 60)" }, // Light mode: rgb(255, 69, 0)
  { key: "clear", name: "Clear", color: "rgb(128, 128, 128)", yAxisID: "y1" }, // Light mode: rgb(169, 169, 169)
  { key: "nir", name: "NIR", color: "rgb(139, 69, 19)", yAxisID: "y1" }, // Light mode: rgb(160, 82, 45)
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
  const processedAs7341Data = useMemo(
    () =>
      as7341Data.map((item: As7341Item) => ({
        date: formatTimestamp(item.timestamp),
        ...item,
      })),
    [as7341Data]
  );

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>AS7341 - Color Sensor</Title>
        {isLoading ? (
          <Text>Loading AS7341 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            labels={processedAs7341Data.map((data) => data.date)}
            data={as7341Series.map((series) => ({
              label: series.name,
              data: processedAs7341Data.map((data) => data[series.key]),
              borderColor: series.color,
              yAxisID: series.yAxisID,
            }))}
          />
        )}
      </Stack>
    </Paper>
  );
};

export default memo(AS7341);
