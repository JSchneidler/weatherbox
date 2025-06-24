import {
  MantineProvider,
  Grid,
  Paper,
  Title,
  Text,
  Stack,
  Group,
  Container,
} from "@mantine/core";
import { DateTimePicker } from "@mantine/dates";
import { useState } from "react";

import { useSensorData } from "./hooks";

import SystemHealth from "./components/SystemHealth";
import { AS7341, BME688, ENS160, LTR390, SPS30 } from "./components/charts";

import "@mantine/core/styles.css";
import "@mantine/charts/styles.css";
import "@mantine/dates/styles.css";

function App() {
  const [startDate, setStartDate] = useState<string | null>(null);
  const [endDate, setEndDate] = useState<string | null>(null);

  // Single hook for all sensor data
  const { data, error, isLoading } = useSensorData({
    startDate: startDate ? new Date(startDate) : null,
    endDate: endDate ? new Date(endDate) : null,
  });

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
            <SPS30
              sps30Data={data?.sps30 || []}
              isLoading={isLoading}
              error={error}
            />
          </Grid.Col>

          {/* AS7341 - Color Sensor */}
          <Grid.Col span={6}>
            <AS7341
              as7341Data={data?.as7341 || []}
              isLoading={isLoading}
              error={error}
            />
          </Grid.Col>

          {/* BME688 - Environmental Sensor */}
          <Grid.Col span={6}>
            <BME688
              bme688Data={data?.bme688 || []}
              isLoading={isLoading}
              error={error}
            />
          </Grid.Col>

          {/* LTR390 - Light & UV Sensor */}
          <Grid.Col span={6}>
            <LTR390
              ltr390Data={data?.ltr390 || []}
              isLoading={isLoading}
              error={error}
            />
          </Grid.Col>

          {/* ENS160 - Air Quality Index */}
          <Grid.Col span={6}>
            <ENS160
              ens160Data={data?.ens160 || []}
              isLoading={isLoading}
              error={error}
            />
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

          <Grid.Col span={12}>
            <SystemHealth />
          </Grid.Col>
        </Grid>
      </Container>
    </MantineProvider>
  );
}

export default App;
