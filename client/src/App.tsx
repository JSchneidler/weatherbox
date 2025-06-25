import {
  Grid,
  Paper,
  Title,
  Text,
  Stack,
  Group,
  Container,
  Modal,
  Button,
  AppShell,
  Image,
} from "@mantine/core";
import { DateTimePicker } from "@mantine/dates";
import { useDisclosure } from "@mantine/hooks";
import { useState } from "react";

import { useSensorData } from "./hooks";

import Gallery from "./components/Gallery";
import SystemHealth from "./components/SystemHealth";
import Settings from "./components/Settings";
import { AS7341, BME688, ENS160, LTR390, SPS30 } from "./components/charts";

function App() {
  const [startDate, setStartDate] = useState<string | null>(null);
  const [endDate, setEndDate] = useState<string | null>(null);
  const [opened, { open, close }] = useDisclosure(false);

  // Single hook for all sensor data
  const { data, error, isLoading } = useSensorData({
    startDate: startDate ? new Date(startDate) : null,
    endDate: endDate ? new Date(endDate) : null,
  });

  return (
    <AppShell header={{ height: 60 }}>
      <Modal opened={opened} onClose={close} title="Settings" size="xl">
        <Settings />
      </Modal>

      <AppShell.Header>
        <Grid gutter="xs">
          <Grid.Col span={4}>
            <Image src="/logo.png" alt="WeatherBox" w="auto" h="40px" />
          </Grid.Col>
          <Grid.Col span={4}>
            <Group justify="center">
              <DateTimePicker
                placeholder="Start"
                value={startDate}
                onChange={setStartDate}
                clearable
              />
              <Text>to</Text>
              <DateTimePicker
                placeholder="End"
                value={endDate}
                onChange={setEndDate}
                clearable
              />
            </Group>
          </Grid.Col>
          <Grid.Col
            span={4}
            style={{
              display: "flex",
              justifyContent: "flex-end",
            }}
          >
            <Button variant="outline" onClick={open}>
              Settings
            </Button>
          </Grid.Col>
        </Grid>
      </AppShell.Header>

      <AppShell.Main>
        <Container size="xxl" py="md">
          <Grid gutter="md">
            {/* ENS160 - Air Quality Index */}
            <Grid.Col span={6}>
              <ENS160
                ens160Data={data?.ens160 || []}
                isLoading={isLoading}
                error={error}
              />
            </Grid.Col>

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

            {/* LTR390 - Light & UV Sensor */}
            <Grid.Col span={6}>
              <LTR390
                ltr390Data={data?.ltr390 || []}
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
                      height: "600px",
                      objectFit: "cover",
                    }}
                  />
                </Stack>
              </Paper>
            </Grid.Col>

            <Grid.Col span={12}>
              <Paper p="md" withBorder>
                <Title order={3} mb="xs">
                  Timelapse Gallery
                </Title>
                <Gallery
                  startDate={startDate ? new Date(startDate) : undefined}
                  endDate={endDate ? new Date(endDate) : undefined}
                />
              </Paper>
            </Grid.Col>

            <Grid.Col span={12}>
              <SystemHealth />
            </Grid.Col>
          </Grid>
        </Container>
      </AppShell.Main>
    </AppShell>
  );
}

export default App;
