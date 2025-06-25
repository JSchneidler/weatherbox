import { Paper, Stack, Title, Text } from "@mantine/core";

import LineChart from "./LineChart";
import { formatTimestamp } from "../../util";
import { memo, useMemo } from "react";

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
  { key: "pm10", name: "PM10 (μg/m³)", color: "rgb(76, 175, 80)" }, // Light mode: rgb(129, 199, 132)
  { key: "pm25", name: "PM2.5 (μg/m³)", color: "rgb(255, 235, 59)" }, // Light mode: rgb(255, 241, 118)
  { key: "pm40", name: "PM4.0 (μg/m³)", color: "rgb(255, 152, 0)" }, // Light mode: rgb(255, 183, 77)
  { key: "pm100", name: "PM1.0 (μg/m³)", color: "rgb(244, 67, 54)" }, // Light mode: rgb(239, 83, 80)
  { key: "nc05", name: "NC0.5 (#/cm³)", color: "rgb(224, 247, 250)" }, // Light mode: rgb(178, 235, 242)
  { key: "nc10", name: "NC1.0 (#/cm³)", color: "rgb(129, 212, 250)" }, // Light mode: rgb(100, 181, 246)
  { key: "nc25", name: "NC2.5 (#/cm³)", color: "rgb(33, 150, 243)" }, // Light mode: rgb(66, 165, 245)
  { key: "nc40", name: "NC4.0 (#/cm³)", color: "rgb(13, 71, 161)" }, // Light mode: rgb(30, 136, 229)
  { key: "nc100", name: "NC1.0 (#/cm³)", color: "rgb(26, 35, 126)" }, // Light mode: rgb(57, 73, 171)
  {
    key: "typical_particle_size",
    name: "Typical Particle Size (μm)",
    color: "rgb(96, 125, 139)", // Light mode: rrgb(120, 144, 156)
    yAxisID: "y1",
  },
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
  const processedSps30Data = useMemo(
    () =>
      sps30Data.map((item: Sps30Item) => ({
        date: formatTimestamp(item.timestamp),
        ...item,
      })),
    [sps30Data]
  );

  return (
    <Paper p="md" withBorder>
      <Stack gap="xs">
        <Title order={3}>SPS30 - Air Quality</Title>
        {isLoading ? (
          <Text>Loading SPS30 data...</Text>
        ) : error ? (
          <Text c="red">Error loading data: {error.message}</Text>
        ) : (
          <LineChart
            labels={processedSps30Data.map((data) => data.date)}
            data={sps30Series.map((series) => ({
              label: series.name,
              data: processedSps30Data.map((data) => data[series.key]),
              borderColor: series.color,
              yAxisID: series.yAxisID,
            }))}
          />
        )}
      </Stack>
    </Paper>
  );
};

export default memo(SPS30);
