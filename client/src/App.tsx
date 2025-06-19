import "./App.css";

import {
  MantineProvider,
  Grid,
  Paper,
  Title,
  Text,
  Stack,
} from "@mantine/core";
import { LineChart } from "@mantine/charts";
import { useData } from "./useData";
import { format, parseISO } from "date-fns";

import "@mantine/core/styles.css";
import "@mantine/charts/styles.css";

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
  const { data, error, isLoading } = useData();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  // Helper function to format timestamps
  const formatTimestamp = (timestamp: string) => {
    try {
      const date = parseISO(timestamp);
      return format(date, "MMM d, h:mm a");
    } catch {
      return timestamp; // fallback to original if parsing fails
    }
  };

  const sps30Data = data.sps30
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

  const as7341Data = data.as7341
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

  const ltr390Data = data.ltr390
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

  const bme688Data = data.bme688
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

  const ens160Data = data.ens160
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

  return (
    <MantineProvider defaultColorScheme="dark">
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
              <LineChart
                h={400}
                data={sps30Data}
                dataKey="date"
                series={sps30Series}
                curveType="linear"
                withDots={false}
                withRightYAxis
                yAxisProps={{ label: "PM Values (μg/m³)" }}
                xAxisProps={{ label: "Time" }}
                withLegend
              />
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
              <LineChart
                h={400}
                data={as7341Data}
                dataKey="date"
                series={as7341Series}
                curveType="linear"
                withDots={false}
                yAxisProps={{ label: "Counts" }}
                xAxisProps={{ label: "Time" }}
                withLegend
              />
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
              <LineChart
                h={400}
                data={bme688Data}
                dataKey="date"
                series={bme688Series}
                curveType="linear"
                withDots={false}
                withRightYAxis
                yAxisProps={{ label: "Temperature (°C) / Humidity (%)" }}
                xAxisProps={{ label: "Time" }}
                withLegend
              />
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
              <LineChart
                h={400}
                data={ltr390Data}
                dataKey="date"
                series={ltr390Series}
                curveType="linear"
                withDots={false}
                withRightYAxis
                yAxisProps={{ label: "Light (lux)" }}
                xAxisProps={{ label: "Time" }}
                withLegend
              />
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
              <LineChart
                h={400}
                data={ens160Data}
                dataKey="date"
                series={ens160Series}
                curveType="linear"
                withDots={false}
                withRightYAxis
                yAxisProps={{ label: "TVOC (ppb) / eCO2 (ppm)" }}
                xAxisProps={{ label: "Time" }}
                withLegend
              />
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
                  height: "100%",
                  objectFit: "cover",
                  borderRadius: "4px",
                }}
              />
            </Stack>
          </Paper>
        </Grid.Col>
      </Grid>
    </MantineProvider>
  );
}

export default App;
