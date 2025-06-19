import {
  MantineProvider,
  Grid,
  Paper,
  Title,
  Text,
  Stack,
  Group,
  Container,
  Progress,
  Badge,
} from "@mantine/core";
import { LineChart } from "@mantine/charts";
import { DateTimePicker } from "@mantine/dates";
import { useData, useSystemStats } from "./hooks";
import { format, parseISO } from "date-fns";
import { useState } from "react";

import "@mantine/core/styles.css";
import "@mantine/charts/styles.css";
import "@mantine/dates/styles.css";

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

// Define types for the data structure
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

interface Ltr390Item {
  timestamp: string;
  light: number;
  uvs: number;
}

interface Bme688Item {
  timestamp: string;
  temperature: number;
  humidity: number;
  pressure: number;
  gas: number;
}

interface Ens160Item {
  timestamp: string;
  aqi: number;
  tvoc: number;
  eco2: number;
}

function App() {
  const [startDate, setStartDate] = useState<string | null>(null);
  const [endDate, setEndDate] = useState<string | null>(null);

  // Single hook for all sensor data
  const {
    data: allData,
    error,
    isLoading,
  } = useData({
    startDate: startDate ? new Date(startDate) : null,
    endDate: endDate ? new Date(endDate) : null,
  });

  // System stats hook
  const { data: systemStats, error: systemError } = useSystemStats();

  // Extract individual sensor data from the response
  const sps30Data = allData?.sps30 || [];
  const as7341Data = allData?.as7341 || [];
  const ltr390Data = allData?.ltr390 || [];
  const bme688Data = allData?.bme688 || [];
  const ens160Data = allData?.ens160 || [];

  // Helper function to format timestamps
  const formatTimestamp = (timestamp: string) => {
    try {
      const date = parseISO(timestamp);
      return format(date, "MMM d, h:mm a");
    } catch {
      return timestamp; // fallback to original if parsing fails
    }
  };

  // Process SPS30 data
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

  // Process AS7341 data
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

  // Process LTR390 data
  const processedLtr390Data = ltr390Data
    .slice()
    .reverse()
    .map((item: Ltr390Item) => ({
      date: formatTimestamp(item.timestamp),
      light: item.light,
      uvs: item.uvs,
    }));

  const ltr390Series = [
    { name: "light", color: "blue.6" },
    { name: "uvs", color: "red.6", yAxisId: "right" },
  ];

  // Process BME688 data
  const processedBme688Data = bme688Data
    .slice()
    .reverse()
    .map((item: Bme688Item) => ({
      date: formatTimestamp(item.timestamp),
      temperature: item.temperature,
      humidity: item.humidity,
      pressure: item.pressure,
      gas: item.gas,
    }));

  const bme688Series = [
    { name: "temperature", color: "blue.6" },
    { name: "humidity", color: "red.6" },
    { name: "pressure", color: "green.6", yAxisId: "right" },
    // { name: "gas", color: "gray.6", yAxisId: "right" },
  ];

  // Process ENS160 data
  const processedEns160Data = ens160Data
    .slice()
    .reverse()
    .map((item: Ens160Item) => ({
      date: formatTimestamp(item.timestamp),
      aqi: item.aqi,
      tvoc: item.tvoc,
      eco2: item.eco2,
    }));

  const ens160Series = [
    { name: "aqi", color: "blue.6", yAxisId: "right" },
    { name: "tvoc", color: "red.6" },
    { name: "eco2", color: "green.6" },
  ];

  // Helper function to format uptime
  const formatUptime = (bootTime: number) => {
    const now = Date.now() / 1000;
    const uptimeSeconds = now - bootTime;
    const days = Math.floor(uptimeSeconds / 86400);
    const hours = Math.floor((uptimeSeconds % 86400) / 3600);
    const minutes = Math.floor((uptimeSeconds % 3600) / 60);

    if (days > 0) {
      return `${days}d ${hours}h ${minutes}m`;
    } else if (hours > 0) {
      return `${hours}h ${minutes}m`;
    } else {
      return `${minutes}m`;
    }
  };

  return (
    <MantineProvider defaultColorScheme="dark">
      <Container size="xl" py="md">
        {/* DateTime Range Picker */}
        <Paper p="md" withBorder mb="md">
          <Stack gap="xs">
            <Title order={3}>Time Range</Title>
            <Group>
              <DateTimePicker
                label="Start DateTime"
                placeholder="Pick start date and time"
                value={startDate}
                onChange={(value) => setStartDate(value)}
                clearable
              />
              <DateTimePicker
                label="End DateTime"
                placeholder="Pick end date and time"
                value={endDate}
                onChange={(value) => setEndDate(value)}
                clearable
              />
            </Group>
          </Stack>
        </Paper>

        <Grid gutter="md">
          {/* SPS30 - Air Quality Sensor */}
          <Grid.Col span={6}>
            <Paper p="md" withBorder>
              <Stack gap="xs">
                <Title order={3}>SPS30 - Air Quality Sensor</Title>
                <Text size="sm" c="dimmed">
                  PM10, PM2.5, PM4.0, PM1.0 (μg/m³) | Particle Counts (#/cm³) |
                  Typical Particle Size (μm)
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
          </Grid.Col>

          {/* AS7341 - Color Sensor */}
          <Grid.Col span={6}>
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
          </Grid.Col>

          {/* BME688 - Environmental Sensor */}
          <Grid.Col span={6}>
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
          </Grid.Col>

          {/* LTR390 - Light & UV Sensor */}
          <Grid.Col span={6}>
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
          </Grid.Col>

          {/* ENS160 - Air Quality Index */}
          <Grid.Col span={6}>
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
          </Grid.Col>

          {/* Camera Feed */}
          <Grid.Col span={6}>
            <Paper p="md" withBorder>
              <Stack gap="xs">
                <Title order={3}>Camera Feed</Title>
                <Text size="sm" c="dimmed">
                  Live MJPEG Stream
                </Text>
                <img
                  src={`http://${window.location.hostname}:8000/mjpeg`}
                  alt="WeatherBox Camera Feed"
                  style={{
                    width: "100%",
                    height: "400px",
                    objectFit: "cover",
                  }}
                />
              </Stack>
            </Paper>
          </Grid.Col>
        </Grid>

        {/* System Stats Bar */}
        <Paper p="md" withBorder mt="md">
          <Stack gap="md">
            <Title order={4}>System Status</Title>
            {systemError ? (
              <Text c="red" size="sm">
                Error loading system stats: {systemError.message}
              </Text>
            ) : systemStats ? (
              <Grid gutter="lg">
                {/* Performance Metrics */}
                <Grid.Col span={6}>
                  <Stack gap="xs">
                    <Text size="sm" fw={500} c="dimmed">
                      Performance
                    </Text>

                    <Stack gap="xs">
                      <Group justify="space-between">
                        <Text size="sm">CPU</Text>
                        <Badge
                          variant="light"
                          color={
                            systemStats.cpu_usage > 80
                              ? "red"
                              : systemStats.cpu_usage > 60
                              ? "yellow"
                              : "green"
                          }
                        >
                          {systemStats.cpu_usage.toFixed(1)}%
                        </Badge>
                      </Group>
                      <Progress
                        value={systemStats.cpu_usage}
                        color={
                          systemStats.cpu_usage > 80
                            ? "red"
                            : systemStats.cpu_usage > 60
                            ? "yellow"
                            : "green"
                        }
                        size="xs"
                      />
                    </Stack>

                    <Stack gap="xs">
                      <Group justify="space-between">
                        <Text size="sm">Memory</Text>
                        <Badge
                          variant="light"
                          color={
                            systemStats.memory_usage > 80
                              ? "red"
                              : systemStats.memory_usage > 60
                              ? "yellow"
                              : "green"
                          }
                        >
                          {systemStats.memory_usage.toFixed(1)}%
                        </Badge>
                      </Group>
                      <Progress
                        value={systemStats.memory_usage}
                        color={
                          systemStats.memory_usage > 80
                            ? "red"
                            : systemStats.memory_usage > 60
                            ? "yellow"
                            : "green"
                        }
                        size="xs"
                      />
                    </Stack>

                    <Stack gap="xs">
                      <Group justify="space-between">
                        <Text size="sm">Disk</Text>
                        <Badge
                          variant="light"
                          color={
                            systemStats.disk_usage > 80
                              ? "red"
                              : systemStats.disk_usage > 60
                              ? "yellow"
                              : "green"
                          }
                        >
                          {systemStats.disk_usage.toFixed(1)}%
                        </Badge>
                      </Group>
                      <Progress
                        value={systemStats.disk_usage}
                        color={
                          systemStats.disk_usage > 80
                            ? "red"
                            : systemStats.disk_usage > 60
                            ? "yellow"
                            : "green"
                        }
                        size="xs"
                      />
                    </Stack>
                  </Stack>
                </Grid.Col>

                {/* System Health */}
                <Grid.Col span={6}>
                  <Stack gap="xs">
                    <Text size="sm" fw={500} c="dimmed">
                      System Health
                    </Text>

                    <Group justify="space-between">
                      <Text size="sm">CPU Temperature</Text>
                      <Badge
                        variant="light"
                        color={
                          systemStats.cpu_temperature > 80
                            ? "red"
                            : systemStats.cpu_temperature > 60
                            ? "yellow"
                            : "green"
                        }
                      >
                        {systemStats.cpu_temperature.toFixed(1)}°C
                      </Badge>
                    </Group>

                    <Group justify="space-between">
                      <Text size="sm">Fan Speed</Text>
                      <Badge variant="light" color="blue">
                        {systemStats.fan_rpm.toLocaleString()} RPM
                      </Badge>
                    </Group>

                    <Group justify="space-between">
                      <Text size="sm">Uptime</Text>
                      <Badge variant="light" color="blue">
                        {formatUptime(systemStats.uptime)}
                      </Badge>
                    </Group>
                  </Stack>
                </Grid.Col>
              </Grid>
            ) : (
              <Text size="sm" c="dimmed">
                Loading system stats...
              </Text>
            )}
          </Stack>
        </Paper>
      </Container>
    </MantineProvider>
  );
}

export default App;
